def application(env, start_response):
    start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
    return ['<!DOCTYPE html><html><meta charset="utf-8"><title>It works',
            "</title><b>It seems to work!</b><br /><br />This is the server's ",
            'default wsgi.py.']
