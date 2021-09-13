# -*- coding: utf-8 -*-

import common.api.doGet as doGet
import common.api.doPost as doPost
from common.first import err
from common.dbToolkit.DC import DC

from http import HTTPStatus
import email.utils
import urllib.parse

import traceback
import time
import gzip
from mimetypes import guess_type

# *** *** ***

try:
    import importlib
    resource = importlib.import_module('resource')
    resource.setrlimit(resource.RLIMIT_NOFILE, (100000, 100000))
except:
    resource = None

# *** *** ***

urlForGet = {
    'opendoc': doGet.openDoc,
    'jsv': doGet.jsv,
    'js': doGet.jsv,
    'api.getc': doGet.apiDoGet,
    'api.get': doGet.apiDoGet,
    '': doGet.openDoc,               # /opendoc?mode=new&form=a_main
}
urlForPost = {
    'api.post': doPost.doPost,
}

# *** *** ***

httpStatus = { v._value_: v.phrase for v in HTTPStatus }

# *** *** ***

def application(environ, start_response):
    
    method = environ.get('REQUEST_METHOD', '')
    path = environ.get('PATH_INFO', '')[1:100]
    query = urllib.parse.unquote(environ.get('QUERY_STRING', '')[:10000])
    
    request = DC({'META': environ})
    
    def do_Get():
        handler = urlForGet.get(path.partition('/')[0], showStaticPage)
        return handler(request)

    # *** *** ***

    def do_Post():      # upload, save, action, getView
        handler = urlForPost.get(path.partition('/')[0])
        if handler:
            return handler(request)
        
        return 501, None, 'Invalid request'

    # *** *** ***

    def http_err(ex):
        s = f'500. Server error. Method: {method}, path: {path}, query: {query}'
        s += f'\n*** {ex}\n\n{traceback.format_exc()}'
        err(s, cat='err-app-Exception')
        return 500, None, s.replace('\n', '<br>')

    # *** *** ***

    def makeResponse(status, contentType=None, body=b''):
        header = []
        contentType = contentType or 'text/html; charset=UTF-8'

        if len(body) > 100 and any(c in contentType for c in ['/json', '/html', '/javascript', '/css']):
            try:
                body = gzip.compress( body.encode() if type(body) is str else body )
                header.append( ('Content-Encoding', 'gzip') )
            except Exception as ex:
                err(f'{contentType}, {status}, {ex}', cat='makeResponse')
                return

        if not type(status) is int:
            body = f"Internal Server Error({method}). Path:{path}, query:{query}, status:{status or '?'})"
            status = 500
            
        if method == 'GET' and path in ['image', 'jsv', 'list', 'api.getc']:
            days = 15 if path == 'list' else 30

            maxAge = 60*60*24*days
            header.append( ('Expires', email.utils.formatdate( time.time() + maxAge, usegmt=True ) ))
            header.append( ('Cache-Control', f'max-age={maxAge}') )

        if type(body) is str:
            try:
                body = body.encode()
            except:
                status = 500
                contentType = 'text/html; charset=UTF-8'
                body = b'rs_app.py.makeResponse: encode-error'

        lbody = len(body)
        if environ.get('HTTP_RANGE') and status == 200:
            status = 206
            header.append( ('Content-Range', f'bytes 0-{lbody-1}/{lbody}'))

        header.append( ('content-type', contentType) )
        header.append( ('Content-length', str(lbody)) )
        
        return status, header, body

    # *** *** ***
    # *** *** ***
    # *** *** ***

    try:
        if method == 'GET':
            status, header, body = makeResponse(*do_Get())
        elif method == 'POST':
            status, header, body = makeResponse(*do_Post())
        else:
            status, header, body = makeResponse(405, None, b'Allow: GET, POST')
    except Exception as ex:
        status, header, body = makeResponse(*http_err(ex))
    
    phrase = httpStatus.get(status, 'OK')
    start_response(f'{status} {phrase}', header)
    
    return body,

# *** *** ***

def showStaticPage(request):
    p = request.META['PATH_INFO']
    if p == '/':
        p = '/index.html'
    if request.META['REQUEST_METHOD'] == 'GET':
        try:
            with open(f'./static{p or "/index.html"}'.replace('..', ''), 'rb') as f:
                return 200, guess_type(p)[0], f.read()
        except:
            return 404, None, f'<h3>404<br>Static page "{p}" not found</h3>'

    return 400

# *** *** ***

