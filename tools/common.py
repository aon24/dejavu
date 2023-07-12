# -*- coding: utf-8 -*- 
"""
AON 2020
"""

from _ast import Or
try:
    from dejavu.imidjan import HttpResponse
except:
    from django.http import HttpResponse

from .first import snd, err, dbg
from .DC import DC, well
from .username import getUserName, addSessionID

import re, os, shutil, traceback, time, uuid
from binascii import hexlify
from datetime import datetime
from urllib.parse import unquote
from hashlib import md5

from user_agents import parse

# *** *** ***

sovaOnline = 'sova.online'

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

def now(dlm='.'):
    if dlm == '.':
        return datetime.now().strftime('%d.%m.%Y %H:%M:%S')
    else:
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # if dlm == '.':
        # return datetime.now(tz=get_current_timezone()).strftime('%d.%m.%Y %H:%M:%S')
    # else:
        # return datetime.now(tz=get_current_timezone()).strftime('%Y-%m-%d %H:%M:%S')

# *** *** ***

def today(dlm='.'):
    if dlm == '.':
        return datetime.today().strftime('%d.%m.%Y')
    else:
        return datetime.today().strftime('%Y-%m-%d')

# *** *** ***
def stackEx():
    return traceback.format_exc()

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

def sndErr(func):
    """
    Декоратор. Вызывает функцию func и ловит Exception.
    Если поймал:
        - выводит имя функции и сообщение об ошибке;
        - возвращает None.
    """
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as ex:
            err(str(ex), cat=func.__name__)

    return wrapper

# *** *** ***

def files(fn, key):
    fn = fn.lower()
    ff = (well('files') or {}).get(fn)

    return   ff.get(key, '')     if ff \
        else well('scripts', fn) if key == 'buf' \
        else well('verJS', fn)   if key == 'ver' \
        else ''
        
# *** *** ***

def liform(f, k):
    fo = (well('groundForms') or {}).get(f.lower())
    return fo.F(k) if fo else ''

# *** *** ***

def chModOwn (f, mode=0o777):
    try:
        os.chmod( f, mode )
        shutil.chown( f, 'nobody', 'nogroup' )
    except:
        pass

# *** *** ***

def tryDecode(s):
    for x in ['utf-8', 'cp1251', 'cp437']:
        try:
            return s.decode(x), x
        except:
            pass
                
    return None, None

# *** *** ***

def xunid(s):
    return str(hexlify(s), 'ascii')

reHex = re.compile('(?:[0-9a-fA-F][0-9a-fA-F])+$')
def isHex(s):
    try:
        return not not reHex.match(s)
    except:
        return False

# *** *** ***

js_search = re.compile(r'((<script[\s]+src[\s]*)|(<link[\s]+rel[\s]*))=[\s]*[\'"][\s\S]+?(\.css"|\.js")', re.IGNORECASE | re.M | re.U)

def setVersionJS(bf, path):
    """
bf = 
...
<script src="jsv?lb.js"></script>
<link rel="stylesheet" href="jsv?std3d.css"/>

returned:
...
[
<script src="jsv?lb.js::2013-09-02 09:57:24"></script>
<link rel="stylesheet" href="jsv?std3d.css::2013-08-29 13:16:28"/>
, ver
]
    """
    itr = js_search.finditer(bf)
    l0 = 0
    bf2 = ''
    ver = ''
    for match in itr:
        s = match.group()
        if 'jsv?' in s:
            s = s[:-1]
            fn = os.path.join(path, s.partition('jsv?')[2])
            try:
                stat = os.stat(fn)
                v = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y-%H:%M:%S')
                s += '::' + v
                ver = max(ver, v)
            except:
                s = s.replace('jsv?', 'js?')
                err(f'{fn} not found', cat='setVersionJS')
        else:
            s = s.replace('jsv?', 'js?')

        s += '"'

        l1,l2 = match.span()
        bf2 += bf[l0:l1] + s
        l0 = l2
        
    return bf2 + bf[l0:], ver

# *** *** ***

def setVersionFiles(ls, path):
    ols = []
    if ls:
        if type(ls) is str:
            ls = [ls]
        for s in ls:
            if 'jsv?' not in s:
                ols.append(s)
            else:
                fn = os.path.join(path, s.partition('jsv?')[2])
                try:
                    stat = os.stat(fn)
                    v = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y-%H:%M:%S')
                    ols.append(s + '::' + v)
                except:
                    err(f'"{fn}" not found', cat='setVersionFiles')
    return ols
    
# *** *** ***

def setLevel(inh, d):
    def incAA(s): # увеличивает заданный в s o_level
        if len(s) < 3 or not('.aa' <= s < '.zz'):
            return '.aa'
        
        if ord(s[2]) < ord('z'):
            return '.' + s[1] + chr(ord(s[2]) + 1)
        else:
            return '.' + chr(ord(s[1]) + 1) + 'a'
    
    # *** *** ***
    
    dic = {}
    first = d.form[0].lower()

    for r in d.db.getResponses(d.ref):
        if r.form.split('.')[0] == d.form and r.o_level and r.dir != 'd':
            dic[r.o_level] = r

    if not dic:
        return first + '.aa'

    sk = sorted(dic.keys())
    
    if not (inh.ref and inh.o_level):
        return first + incAA(sk[-1][1:])
    
    io_level = inh.o_level
    lol = len(io_level)
    
    for i in range(len(sk)):
        if io_level == dic[sk[i]].o_level[:lol]: # ищем свою ветку
            
            while i < len(sk):
                if io_level != dic[sk[i]].o_level[:lol]: # своя ветка кончилась ?
                    if io_level == dic[sk[i-1]].F('o_level'):
                        return io_level + '.aa'
                    return io_level + incAA(sk[i-1][lol:])
                
                i += 1
                
            if io_level == dic[sk[i-1]].o_level:
                return io_level + '.aa'
            return io_level + incAA(sk[i-1][lol:])

    return first + incAA(sk[-1][1:])

# *** *** ***

user_regex = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*\Z"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-\011\013\014\016-\177])*"\Z)',  # quoted-string
    re.IGNORECASE)
domain_regex = re.compile(
    r'((?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+)(?:[A-Z0-9-]{2,63}(?<!-))\Z',
    re.IGNORECASE)

def emailValidator(value):
    user_part, _, domain_part = value.partition('@')
    return user_regex.match(user_part) and domain_regex.match(domain_part)

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
    dcUK = DC( dict(
                userAgent=(ua.is_mobile and 'mobile') or (ua.is_pc and 'pc') or (ua.is_tablet and 'tablet') or 'unknown',
#                 ua_os=ua.os.family, ua_browser=ua.browser.family,
                path=path,
                query=query,
                userName=userName,
                remote_addr=request.META.get('REMOTE_ADDR', 'hide')) )
    
    i = 0
    for p in query.split('&'):
        l, _, r = p.partition('=')
        if l and r:
            dcUK.S(l.strip(), r.strip())
        elif l:
            dcUK.S(f'P{i}', l.strip())
            i += 1
   
    return dcUK

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







