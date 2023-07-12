# -*- coding: utf-8 -*- 
'''
Created on 2021

@author: aon

'''
import tools.first as log
from tools.DC import DC, toWell, config, usersByLogin
from tools.dbToolkit.Book import hasDB, createDB, allFromDB

import socket
from hashlib import md5

# *** *** ***

def loadAll(iniFile):
    try:
        for dbAlias in ['people', 'courses', 'mailing', 'groups', 'payments', 'well']:
            if not hasDB(dbAlias): createDB(dbAlias)
    except:
        log.err(f'createDB "{dbAlias}"', cat='loadPeople')
        return

    loadIniFile(iniFile)
    
    # ***
    
    log.sovaLogger.logLevel = config.logLevel or 'INFO'
    log.sovaLogger.prpr = not config.disableLogPrint
    
    # ***
    
    loadPeople()
    loadWell()
    
# *** *** ***

def loadIniFile(iniFile):
    new_config = DC()
    try:
        log.snd(f'--- file ---: {iniFile}', cat='config')
        with open(iniFile, 'rb') as f:
            buf = f.read()
            try:
                buf = buf.decode()
            except:
                buf = buf.decode('cp1251')
    except Exception as ex:
        log.err(f'"{iniFile}" error:\n{ex}', cat='LoadIniFile')
        return
                        
    ls = buf.replace('\ufeff', '').replace('\r', '').split('\n')       # deleting BOM
    for s in ls:
        p = s.partition('#')[0]
        l, _, r = p.partition('=')
        l, r = l.strip(), r.strip()
        if r:
            new_config.S(l, r)
        elif r:
            log.err(f'file: {iniFile}, string: "{s}"', cat='config')
    
    # ***
    
    hostName = socket.gethostname()
    port = new_config.httpPort or '80'
    local_ip = socket.gethostbyname(hostName)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        google_ip = s.getsockname()[0]
        if google_ip == local_ip:
            local_ip = None
    except:
        google_ip = None

    new_config.ws_server = google_ip or local_ip
    new_config.ws_port = new_config.webSocketServerPort
    
    if port != '80':
        hostName += f':{port}'
        if local_ip: local_ip += f':{port}'
        if google_ip: google_ip += f':{port}'

    ls = [x+'/pages\n' for x in [google_ip, local_ip, hostName] if x]
    new_config.hostAddress = 'http://'.join(ls)
    
    config._KV_.clear()

    for k in new_config._KV_:
        config.S(k, new_config.F(k))
        log.snd(f'config set: {k}={config.F(k)}', cat='config')

# *** *** ***

def loadPeople():
    usersByUserName = {}
    usersByLogin.clear()

    ls = allFromDB('people') or []
    for d in ls:
        if d.fullName:
            un = f"{d.fullName}/{d.dName or 'SV'}"
            usersByUserName[un] = d
            if d.login and d.password:
                pw = md5(f'{d.login}:sova.online:{d.password}'.encode()).hexdigest()
                usersByLogin[d.login] = DC(dict(pw=pw, userName=un))

    toWell(usersByUserName, 'who')

# *** *** ***

def loadWell():
    ls = allFromDB('well') or []
    for d in ls:
        if d.formula:
            try:
                o = eval(d.formula)
            except Exception as ex:
                log.err(f'Eval-error for {d.listName}: {d.formula}\n{ex}', cat='loadWell')
                return
        else:
            o = d.A('list')

        if d.system:
            toWell(o, 'system', d.listName)
        elif d.tracks:
            for tr in d.A('tracks'):
                toWell(o, 'tracks', tr, d.listName)
        else:
            toWell(o, 'list', d.listName)







