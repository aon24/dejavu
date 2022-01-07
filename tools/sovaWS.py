# -*- coding: utf-8 -*- 
'''
Created on 2021

@author: aon
'''
# *** *** ***

from tools.DC import config, DC
from tools.first import err, snd


import threading
import websockets
import asyncio
import time
from urllib.parse import unquote

# *** *** ***

catErr = 'Web Socket Server Error'
_pageEditors = {} # { key: {websocket: websocket, userName: userName, unid: unid} }
_forDisplay = {}
_pages = {}
_clipboard = {}

# *** *** ***

async def hello(websocket, path):
    '''
    websocket для каждой сессии запускает hello в новом триде.
    Hello ждет от клиента сообщений с помощью "async for message in websocket:"
    '''
    try:
        dataType, unid, userName = unquote(path).split('&')
        key = websocket.request_headers['sec-websocket-key']
    except Exception as ex:
        err(f'path: {path}\n{ex}', cat='websocket-hello')
        return
    
    global _pageEditors, _forDisplay, _pages

    if dataType == '/html-editor': # 'Hello Websocket, accept the changes'
        snd(f'{path} {websocket.remote_address[0]}', cat='WS-page-creator-list')
        _pageEditors[key] = dict(websocket=websocket, userName=userName, unid=unid)

        try:
            async for message in websocket: # message (data) by creator
                if '¤' in message: # exchange
                    _pages[unid] = message
                    if unid in _forDisplay:
                        for disp in _forDisplay[unid]:
                            if not disp.closed:
                                await disp.send(message)
                else: # clipboard (copy item)
                    for k, page in _pageEditors.items():
                        if k != key and page['userName'] == userName and not page['websocket'].closed:
                            await page['websocket'].send(message)


        except Exception as ex:
            err(f'Exception(html-editor): {websocket.remote_address[0]}:\n {ex}', cat=catErr)
                
    
    elif dataType == '/html-viewer': # 'Hello Websocket, add me to the show list'
        _forDisplay[unid] = _forDisplay.get(unid, [])
        _forDisplay[unid].append(websocket)
        snd(f'{userName} ({websocket.remote_address[0]})   {unid}', cat='WS-show-list')
        try:
            if unid in _pages:
                await websocket.send(_pages[unid])
            async for message in websocket: # держим открытое соединение для вьювера
                pass
        except:
            pass

    else:
        snd(f'{path} {websocket.remote_address[0]}', cat='WS-unknown-action')

# *** *** ***

def cleaning():
    global _pageEditors, _forDisplay

    while True:
        time.sleep(3) #3600) # 60 minutes

    # Cleaning creators of pages
        for key in list(_pageEditors):
            sock = _pageEditors[key]['websocket']
            if sock.closed:
                snd(f'Cleaning-editors ({key}): {sock.remote_address[0]}', cat='WebSocket closed')
                del _pageEditors[key]

    # Cleaning viewers of page
        for unid, dispArr in _forDisplay.items():
            forDel = []
            for disp in dispArr:
                if disp.closed:
                    forDel.append(disp)
            for k in forDel:
                snd(f'Cleaning-viewers: {k.remote_address[0]}', cat='WebSocket closed')
                _forDisplay[unid].remove(k)

        for unid in list(_forDisplay):
            if not _forDisplay[unid]:
                del _forDisplay[unid]
            
# *** *** ***

def wsServer(port):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        start_server = websockets.serve(hello, port=port)
        loop.run_until_complete(start_server)
        loop.run_forever()
    except Exception as ex:
        err(f'Run_forever exception\n{ex}', cat=catErr)
        
# *** *** ***
def startWebSocketServer():
    '''
    Start ws in self thread
    '''
    try:
        if config.ws_server and config.ws_port:
            port = int(config.ws_port)
            threading.Thread(target=wsServer, args=(port,)).start()
            threading.Thread(target=cleaning).start()
            s =  f'{config.ws_server}:{config.ws_port}'
            config.webSocketServer = s
            snd(s, cat='Start WebSocket Server')
    except Exception as ex:
        err(f'Start exception\n{ex}', cat=catErr)

# *** *** ***

def splitMsg(message):
    head, _, body = message.partition('¤') 
    dc = DC()
    for p in head.split('&'):
        l, _, r = p.partition('=')
        if l and r:
            dc.S(l.strip(), r.strip())
    return dc, body











