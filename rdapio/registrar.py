import pkg_resources

def by_id(regid):
    fname = pkg_resources \
        .resource_filename(__name__, 'static/doc/registrar-ids.txt')
    if not isinstance(regid, int):
        try:
            regid = int(regid)
        except ValueError:
            return

    with open(fname) as f:
        for line in f:
            try:
                sp = line.split()
                if (sp and sp[-1] == 'Accredited' and int(sp[0]) == regid):
                    return ' '.join(sp[1:-1])
            except ValueError:
                pass
