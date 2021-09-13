# -*- coding: utf-8 -*-

'''
Created on 17 авг. 2018 г.

@author: aon24
'''
from .first import snd, err
from .dbToolkit.DC import DC, config

import re, time, threading
from hashlib import md5

sessionID = {} # {sid: {'tm': time.time(), 'un': userName} }
usersByLogin = {}

reRealm = re.compile(r'realm="(.+?)"')
reUsername = re.compile(r'username="(.+?)"')
reNonce = re.compile(r'nonce="(.+?)"')
reCnonce = re.compile(r'cnonce="(.+?)"')
reUri = re.compile(r'uri="(.+?)"')
reOpaque = re.compile(r'opaque="(.+?)"')
reNc = re.compile(r'nc=(.+?),')
reResponse = re.compile(r'response="(.+?)"')

# *** *** ***

def getUserName(env, logoff=None):
    if config.noAut:
        return 'Sova Designer/SV' if len(config.noAut) == 1 else f'{config.noAut}/SV'

    aut = env.get('HTTP_AUTHORIZATION')
    # aut='Digest username="RS Designer", realm="Result-Systems", nonce="cf5fc7ea191b46dfbb0da553f373eecf", uri="/arm", response="dd11817971226695fb5fdabfa781fada", opaque="61972fa1adefe6d756c9482bab050b3b", qop=auth, nc=00000002, cnonce="200a2285d4ee2c89"'
    if aut:
        sid = env.get('HTTP_COOKIE', '').partition('sovasid=')[2][:32]
        if sid in sessionID:
            uname = checkPassword(aut, env.get('REQUEST_METHOD', ''))
            if uname:
                if logoff:
                    addSessionID(sid, newSid=None)
                else:
                    sessionID[sid]['tm'] = time.time()
                    if 'un' not in sessionID[sid]:
                        sessionID[sid]['un'] = uname
                        snd(f"{uname}({env.get('REMOTE_ADDR', 'local')})", cat='login')
                    return uname

# *** *** ***

def checkPassword(aut, method):
    
    m = reUsername.search(aut)
    if not m:
        return
    
    user = usersByLogin.get(m.group(1))
    if not user:
        return

    m = reNonce.search(aut)
    nonce = m.group(1) if m else ''
    
    m = reCnonce.search(aut)
    cnonce = m.group(1) if m else ''

    m = reUri.search(aut)
    uri = m.group(1) if m else ''
    
    m = reNc.search(aut)
    nc = m.group(1) if m else ''
    
    m = reResponse.search(aut)
    response = m.group(1) if m else ''


    a2 = md5(f'{method}:{uri}'.encode()).hexdigest()
    s = f"{user['pw']}:{nonce}:{nc}:{cnonce}:auth:"

    if md5( (s+a2).encode() ).hexdigest() == response:
        return user['userName']

    a2 = md5((method + ':' + uri.replace('\\\\', '\\')).encode()).hexdigest() # sucking chrome
    if md5( (s+a2).encode() ).hexdigest() == response:
        return user['userName']

# *** *** ***

lockSessID = threading.Lock()

# *** *** ***

def addSessionID(sid, newSid=None):
    for i in range(1, 100):
        if lockSessID.acquire(False):
            if newSid and sid not in sessionID:
                sessionID[sid] = newSid # login
                
            for k in list(sessionID):
                if k == sid:
                    if not newSid:
                        del sessionID[k] # logoff
                else:
                    if 'un' in sessionID[k]:
                        if time.time() - sessionID[k]['tm'] > 3600*24:  # clearSession
                            del sessionID[k]
                    else:
                        if time.time() - sessionID[k]['tm'] > 300:
                            del sessionID[k]
            lockSessID.release()
            return
        else:
            time.sleep(0.05)

# *** *** ***

def loadUsers(path):
    try:
        with open(path, 'rb') as f:
            buf = f.read()
            try: buf = buf.decode()
            except: buf = buf.decode('cp1251')
    except:
        err('Error', cat='AUTHORIZATION')
        return
                        
    usersByUserName = {}
    ls = buf.replace('\ufeff', '').replace('\r', '').split('\n')       # deleting BOM

    for s in ls:
        p = s.partition('#')[0] + ':'*10
        ls = [x.strip() for x in p.split(':')]
        if ls[0] and ls[1] and ls[2]: # fullName : login : password : e-mail : dName
            un = f"{ls[0]}/{[4] or 'SV'}"
            pw = md5(f'{ls[1]}:sova.online:{ls[2]}'.encode()).hexdigest()
            usersByLogin[ls[1]] = dict(pw=pw, userName=un)

            usersByUserName[un] = DC(dict(fullName=ls[0], email=ls[3], dNmae=ls[4])) # fullName : e-mail : dName

    from .common import toWell
    toWell(usersByUserName, 'usersByUserName')
        













