import json

import requests
from flask import Flask, render_template, request, redirect, Response

from whois import find_best

app = Flask(__name__, static_folder='doc')

@app.route("/")
def slash():
    return redirect("https://github.com/kalou/rdap.io", 302)

@app.route("/domain/<domain>")
def domain(domain):
    js = json.dumps(find_best(domain.lower()))
    return Response(js, status=200, mimetype='application/json')

@app.route('/doc/<fname>')
def regdoc(fname):
    return app.send_static_file('{}/index.html'.format(fname))

@app.errorhandler(404)
def notfound(uri):
    return app.send_static_file('0/index.html')

# Allow everyone to use us from anywhere.
@app.after_request
def append_CORS(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Methods', 'GET')
  return response


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False, host='0.0.0.0')
