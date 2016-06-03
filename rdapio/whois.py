import pkg_resources
import re
import socket
import urllib
import random
import json

import dnsknife
import requests

_svc_template = {
    'nameservers': 'http://rdap.io/doc/{}',
    'record': 'http://rdap.io/doc/{}',
    'website': 'http://rdap.io/doc/{}',
    'email': 'http://rdap.io/doc/{}',
    'dnssec': 'http://rdap.io/doc/{}',
    'cdscheck': 'http://rdap.io/doc/{}'
}

def service(domain, conf):
    fname = pkg_resources.resource_filename(__name__, conf)
    for line in open(fname).readlines():
        try:
            rxp, server = line.split()
            obj = re.compile(rxp)
            if obj.search(domain):
                return server
        except:
            pass

def from_bootstrap(domain):
    fname = pkg_resources.resource_filename(__name__, 'bootstrap.json')

    def candidates(domain):
        data = json.loads(open(fname).read())
        for tld_list, uri_list in data.get('services', []):
            for tld in tld_list:
                if domain.endswith('.{}'.format(tld)):
                    yield tld, uri_list

    def preferred(uri_list):
        https = [x for x in uri_list if x.startswith('https')]
        if https:
            return random.sample(https, 1)[0]
        return random.sample(uri_list, 1)[0]

    matches = list(candidates(domain))
    matches.sort(lambda x, y: cmp(len(x[0]), len(y[0])))
    if matches and matches[-1][1]:
        return preferred(matches[-1][1]) + '/domain/{}'

def rdap_registrar(domain):
    url = from_bootstrap(domain) or service(domain, 'rdap.conf')
    if not url:
        return

    url = url.format(domain)
    print('Using rdap {}'.format(url))

    rdap = requests.get(url, verify=False)
    if rdap.status_code != 200:
        print 'rdap %s' % rdap.status_code
        return

    rdap = rdap.json()

    def reg_id(entity):
        #XXX STD ?
        ids = [x['identifier'] for x in entity.get('publicIds', []) if
               x.get('type') == 'IANA Registrar ID']
        if len(ids):
            return ids[0]
        return 0

    for entity in rdap.get('entities', []):
        if entity.get('role') == 'registrar' or entity.get('roles') \
           and 'registrar' in entity['roles']:
            rdap['registrar'] = entity['handle']
            rdap['registrar_id'] = reg_id(entity)

    return rdap


def whois_registrar(domain, single=''):
    svc = service(domain, 'whois.conf')
    if not svc:
        print('No whois server for {}'.format(domain))
        return

    print('Using whois {}'.format(svc))

    try:
        sd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        sd.connect((svc, 43))
        sd.sendall('{}{}\n\n'.format(single, domain))
    except:
        print('Unable to connect to {}'.format(svc))

    rep = ''
    buf = sd.recv(4096)
    while buf:
        rep += buf
        buf = sd.recv(4096)

    obj = {}
    for line in rep.split('\n'):
        line = line.rstrip('\r\n')
        if 'single out one' in line and not single:
            return whois_registrar(domain, '=')
        if 'Registrar: ' in line:
            obj['registrar'] = line.split(': ')[1]
        if 'Registrar IANA ID: ' in line:
            obj['registrar_id'] = line.split(': ')[1]

    if not obj.get('registrar') or not obj.get('registrar_id'):
        print('Whois output badly parsed: %s' % rep)

    return obj

def fake_endpoints(rdap):
    if not rdap.get('registrar'):
        rdap['registrar'] = 'unknown'
        rdap['registrar_id'] = 0

    rdap['registrar'] = urllib.quote(rdap['registrar'])

    if 'tpda_endpoints' not in rdap:
        rdap['tpda_endpoints'] = dict((url, svc.format(rdap['registrar_id'])) for
                                       url, svc in _svc_template.items())

def operator_endpoints(domain, rdap):
    checker = dnsknife.Checker(domain, nameservers=dnsknife.resolver
                               .system_resolver.nameservers)
    for svc in ('record', 'email', 'website'):
        uri = checker.tpda_endpoint(svc)
        if uri:
            rdap['tpda_endpoints'][svc] = uri

def find_best(domain):
    obj = rdap_registrar(domain) or whois_registrar(domain) or {}
    fake_endpoints(obj)
    operator_endpoints(domain, obj)
    return obj
