import os
import pkg_resources
import json


from flask import Flask, redirect, Response, render_template


import registrar
from whois import find_best


static = os.path.abspath(pkg_resources.resource_filename(__name__, 'static'))
app = Flask(__name__, static_url_path='/s', static_folder=static)


@app.route("/")
def slash():
    return render_template('index.html')


@app.route("/about")
def about():
    return redirect("https://github.com/kalou/rdap.io", 302)


@app.route("/domain/<domain>")
def domain(domain):
    js = json.dumps(find_best(domain.lower()))
    return Response(js, status=200, mimetype='application/json')


@app.route('/doc/<regid>')
@app.route('/doc/<regid>/<svcname>')
def regdoc(regid, svcname=None):
    names=['doc/{}/{}.html'.format(regid, svcname),
           'doc/{}/index.html'.format(regid)]

    for name in names:
        if os.path.exists('{}/{}'.format(static, name)):
            return app.send_static_file(name)
    return render_template('noreg.html', registrar=registrar.by_id(regid))


# Allow everyone to use us from anywhere.
@app.after_request
def append_CORS(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    return response


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host='0.0.0.0')
