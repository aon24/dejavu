# -*- coding: utf-8 -*- 
'''
Created on 2021

@author: aon

'''
import common.first as log
from common.dbToolkit.DC import DC, config
from common.sovaWS import startWebSocketServer
from common.common import toWell, setVersionJS
from common.username import loadUsers

import json
import socket
import os
from hashlib import md5

# *** *** ***

def appConfig():
    name = 'appDesign' # путь к файлам приложения
    BASE_DIR = os.getcwd()
    for s in ['index']:
        try:
            path = os.path.join(BASE_DIR, 'common', f'{s}.html')
            with open(path, 'r', encoding='utf-8') as f:
                html = setVersionJS(f.read(), BASE_DIR)[0]
                _fo = DC({'html': html})
                toWell(_fo, 'groundForms', s)
        except:
            log.err(f'file "{path}" not loaded', cat=name)
        
    log.initLog(mainProcess=True, prpr=True, logFile=f'log{os.sep}sova', logLevel='INFO')
    path = os.path.join(BASE_DIR, 'DB', f'{name}.ini')
    loadIniFile(path)
    
    path = os.path.join(BASE_DIR, 'DB', 'passwords')
    loadUsers(path)
    
    startWebSocketServer()
    return config

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
    
    log.sovaLogger.logLevel = new_config.logLevel or 'INFO' # or DEBUG
    log.sovaLogger.prpr = not new_config.disableLogPrint
    
    # ***
    
    hostName = socket.gethostname()
    port = new_config.httpPort
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

    ls = [x+'\n' for x in [' ', google_ip, local_ip, hostName] if x]
    new_config.hostAddress = 'http://'.join(ls)
    
    for k in config._KV_:
        config._KV_[k] = ''
        
    for k in new_config._KV_:
        config.S(k, new_config.F(k))
        log.snd(f'config set: {k}={config.F(k)}', cat='config')

# *** *** ***






