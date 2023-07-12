# -*- coding: utf-8 -*-
"""
AON 2023

"""

from tools.first import err, dbg, snd
from tools.username import getUserName, addSessionID
from tools.DC import DC

import traceback, uuid, time
from urllib.parse import unquote
from hashlib import md5

from user_agents import parse

# *** *** ***

def badReq(par, userName='-?-'):
    dbg('param: %s' % par, cat='badReq')
    return accessDenied(userName)

def notFound(s, un=''):
    err(f'404 (userName={un})\n{s}', cat='page not found')
    return HttpResponse(f'''<h3>404 {s}</h3> not found (un={un or 'userName'})''', None, 200)

def jsonNotFound(dcUK):
    err(f'404. UserName={dcUK.un} Path={dcUK.path}', cat='json-object not found')
    return f'''404 "{dcUK.path or 'block not found'} ({dcUK.un or 'userName'})"''', 'application/json', 200

def accessDenied(userName):
    snd(userName, cat='accessDenied')
    return HttpResponse(f'Access denied for {userName}', status=403)

# *** *** ***

def HttpResponse(bo, ty=None, status=200):
    return (status, ty, bo)

# *** *** ***
def stackEx():
    return traceback.format_exc()

# *** *** ***

def httpError(ret=None):
    """
    Декоратор, пищуий в журнал ошибки.
    """

    def _wrapper1(func):

        def _wrapper2(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                err(str(ex), cat=func.__name__)
                err(stackEx())
                if ret:
                    return ret, 'text/html; charset=UTF-8', f'{func.__name__},\n{ex}'

        return _wrapper2

    return _wrapper1

# *** *** ***

def status_401():
    sid = uuid.uuid4().hex.upper()
    addSessionID(sid, newSid={'tm': time.time()})
    rsOpaque = md5(b'sova.online').hexdigest()
    s = f'Digest realm="sova.online", qop="auth", nonce="{uuid.uuid4().hex}", opaque="{rsOpaque}"'
    body = '''<h2 align="center">Введите логин и пароль для доступа к системе <input type="button" value="Войти" onclick="window.location.href='/'"/></h2> '''.encode()
    headers = {}
    headers['WWW-Authenticate'] = s
    headers['content-type'] = 'text/html; charset=UTF-8'
    headers['Set-Cookie'] = f'sovasid={sid}; Max-Age={3600*24}; HttpOnly'
    headers['Content-length'] = str(len(body))
    return HttpResponse(body, status=401, charset='utf-8', headers=headers)

# *** *** ***

def urlKeys(request, cat):
    userName = getUserName(request.META)
    if not userName:
        return status_401()

    path = request.META.get('PATH_INFO', '').rpartition('/')[2]
    query = unquote(request.META['QUERY_STRING'])

    snd(f'path: "{path}" query: "{query}", userName: {userName}', cat=cat)

    if not query:
        if path == 'pages':
            query = 'form=a__pages & mode=new'
        elif not path:
            query = 'form=irm & mode=new'

    ua = parse(request.META['HTTP_USER_AGENT'])
    dcUK = DC(
        userAgent=(ua.is_mobile and 'mobile') or (ua.is_pc and 'pc') or (ua.is_tablet and 'tablet') or 'unknown',
#                 ua_os=ua.os.family, ua_browser=ua.browser.family,
        path=path,
        query=query,
        userName=userName,
        length=request.META.get('CONTENT_LENGTH', -1),
        remote_addr=request.META.get('REMOTE_ADDR', 'hide')
    )
    dcUK._KV_['INPUT'] = request.META.get('wsgi.input')

    i = 0
    for p in query.split('&'):
        if '=' in p:
            l, _, r = p.partition('=')
            dcUK[l.strip()] = r.strip()
        else:
            dcUK[f'P{i}'] = p.strip()
            i += 1
    return dcUK

# *** *** ***
