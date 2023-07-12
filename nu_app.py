# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/root/nu/')

import api.doGet as doGet
import api.doPost as doPost
import tools.first as log
from tools.DC import DC, DCC, toWell, config
from tools.common import setVersionJS
from tools.appConfig import loadAll
from tools.sovaWS import startWebSocketServer
from tools.dbToolkit.upload import uploadFile
from tools.dbToolkit.download import downloadFile

import os
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
    soft, hard = resource.getrlimit(resource.RLIMIT_NOFILE)
    soft = 100000
    resource.setrlimit(resource.RLIMIT_NOFILE, (soft, hard))
except:
    pass

# *** *** ***

urlForGet = {
    'opendoc': doGet.openDoc,
    'pages': doGet.openDoc,
    'new': doGet._new,
    'openpage': doGet.openPage,
    'image': doGet.image,
    'jsv': doGet.jsv,
    'js': doGet.jsv,
    'api.getc': doGet.apiDoGet,
    'api.get': doGet.apiDoGet,
    'download': downloadFile,
    '': doGet.openDoc,  # /opendoc?mode=new&form=a_main
}
urlForPost = {
    'api.post': doPost.doPost,
    'upload': uploadFile,
}

# *** *** ***

httpStatus = { v._value_: v.phrase for v in HTTPStatus }

# *** *** ***


def application(environ, start_response):

    def do_Get():
        handler = urlForGet.get(path.partition('/')[0], showStaticPage)
        return handler(request)

    # *** *** ***

    def do_Post():  # upload, save, action, getView
        handler = urlForPost.get(path.partition('/')[0])
        if handler:
            return handler(request)

        return 501, None, 'Invalid request'

    # *** *** ***

    def http_err(ex):
        s = f'500. Server error. Method: {method}, path: {path}, query: {query}'
        s += f'\n*** {ex}\n\n{traceback.format_exc()}'
        log.err(s, cat='err-app-Exception')
        return 500, None, s.replace('\n', '<br>')

    # *** *** ***

    def makeResponse(status, contentType=None, body=b''):
        header = []
        contentType = contentType or 'text/html; charset=UTF-8'

        if len(body) > 100 and any(c in contentType for c in ['/json', '/html', '/javascript', '/css']):
            try:
                body = gzip.compress(body.encode() if type(body) is str else body)
                header.append(('Content-Encoding', 'gzip'))
            except Exception as ex:
                log.err(f'{contentType}, {status}, {ex}', cat='makeResponse')
                return

        if not type(status) is int:
            body = f"Internal Server Error({method}). Path:{path}, query:{query}, status:{status or '?'})"
            status = 500

        if method == 'GET' and path in ['image', 'jsv', 'list', 'api.getc']:
            days = 15 if path == 'list' else 30

            maxAge = 60 * 60 * 24 * days
            header.append(('Expires', email.utils.formatdate(time.time() + maxAge, usegmt=True)))
            header.append(('Cache-Control', f'max-age={maxAge}'))

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
            header.append(('Content-Range', f'bytes 0-{lbody-1}/{lbody}'))

        header.append(('content-type', contentType))
        header.append(('Content-length', str(lbody)))

        return status, header, body

    # *** *** ***
    # *** *** ***
    # *** *** ***

    method = environ.get('REQUEST_METHOD', '')
    path = environ.get('PATH_INFO', '')[1:100]
    query = urllib.parse.unquote(environ.get('QUERY_STRING', '')[:10000])

    request = DCC({'META': environ})

    if '..' in path or '..' in query:
        status, header, body = makeResponse(200)
    else:
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
    if request.META['REQUEST_METHOD'] != 'GET':
        return 400,

    try:
        p = os.path.join(log.BASE_DIR, 'static', request.META['PATH_INFO'][1:])
        with open(p.replace('..', '').replace('//', ''), 'rb') as f:
            return 200, guess_type(p)[0], f.read()
    except:
        return 200, None, f'<h3>404<br>Static page "{p}" not found</h3>'

# *** *** ***


def appConfig():
    name = 'appDesign'  # путь к файлам приложения

    for s in ['index', 'open']:
        try:
            path = os.path.join(log.BASE_DIR, 'api', 'react', f'{s}.html')
            with open(path, 'r', encoding='utf-8') as f:
                html = setVersionJS(f.read(), log.BASE_DIR)[0]
                _fo = DC({'html': html})
                toWell(_fo, 'groundForms', s)
        except:
            log.err(f'file "{path}" not loaded', cat=name)

    log.initLog(mainProcess=True, prpr=True, logLevel='INFO')
    loadAll(os.path.join(log.BASE_DIR, f'DB/{name}.ini'))

    startWebSocketServer()
    return config

# *** *** ***


config = appConfig()

# *** *** ***

