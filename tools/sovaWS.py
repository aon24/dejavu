# -*- coding: utf-8 -*-
'''
Created on 2021

@author: aon
'''
# *** *** ***

from tools.DC import config, DC
from tools.first import err, snd
from api.pages.a_react.a_react import rootToJson

import threading
import websockets
import asyncio
import time
from urllib.parse import unquote
import traceback

# *** *** ***

catErr = 'Web Socket Server Error'
_pageEditors = {}  # { key: {websocket: websocket, userName: userName, unid: unid} }
_forDisplay = {}  # { unid1: [websocket1, websocket2], unid2: [..] }

# *** *** ***


async def hello(websocket, path):
    '''
    websocket-server для каждой сессии запускает hello в новом триде.
    Hello ждет от клиента сообщений с помощью "async for message in websocket:"
    '''
    try:
        dataType, unid, userName = unquote(path).split('&')
        key = websocket.request_headers['sec-websocket-key']
    except Exception as ex:
        err(f'path: {path}\n{ex}', cat='websocket-hello')
        return

    global _pageEditors, _forDisplay

    if dataType == '/html-editor':  # 'Hello Websocket, accept the changes'
        snd(f'{path} {websocket.remote_address[0]}', cat='WS-page-creator-list')
        _pageEditors[key] = dict(websocket=websocket, userName=userName, unid=unid)

        try:
            async for message in websocket:  # message (data) by creator
                ls = message.split('_¤_')
                if len(ls) == 3:  # exchange
                    param, root, styles = ls
                    dc = {}
                    for p in param.split('&'):
                        l, _, r = p.partition('=')
                        dc[l] = r
                    try:
                        react_fd = rootToJson(root, styles, int(dc.get('screen', 1000)))
                    except Exception as ex:
                        err(ex, cat='rootToJson (hello, websocket)')
                        err(traceback.format_exc(), cat='rootToJson (hello, websocket)')

                    if unid in _forDisplay:
                        for disp in _forDisplay[unid]:
                            if not disp.closed:
                                await disp.send(react_fd)
                elif len(ls) == 2:  # clipboard (copy item): clipBoard_¤_colorStyleMap
                    # with open('tt.css', 'wt') as f:
                    #     f.write(message)
                    #     print('copy item', len(message))

                    for k, page in _pageEditors.items():
                        if k != key and page['userName'] == userName and not page['websocket'].closed:
                            await page['websocket'].send(message)

        except Exception as ex:
            err(f'Hello(html-editor)\n{ex}', cat=catErr)

    elif dataType == '/html-viewer':  # 'Hello Websocket, add me to the show list'
        _forDisplay[unid] = _forDisplay.get(unid, [])
        _forDisplay[unid].append(websocket)
        snd(f'{userName} ({websocket.remote_address[0]})   {unid}', cat='WS-show-list')
        try:
            async for message in websocket:  # держим открытое соединение для вьювера
                pass
        except Exception as ex:
            err(f'Hello(html-viewer)\n{ex}', cat=catErr)

    else:
        return snd(f'{path} {websocket.remote_address[0]}', cat='WS-unknown-action')

    # цикл "async for message in websocket:" тихо завершается при закрытии вкладки
    cleaningOne()

# *** *** ***


def cleaning():
    while True:
        time.sleep(3600)  # 60 minutes
        cleaningOne(True)


def cleaningOne(prpr=None):
    global _pageEditors, _forDisplay

    # Cleaning creators of pages
    for key in list(_pageEditors):
        sock = _pageEditors[key]['websocket']
        if sock.closed:
            prpr and snd(f'Cleaning-editors: {sock.remote_address[0]}', cat='WebSocket closed')
            del _pageEditors[key]

    # Cleaning viewers of page
    for unid, dispArr in _forDisplay.items():
        forDel = []
        for disp in dispArr:
            if disp.closed:
                forDel.append(disp)
        for k in forDel:
            prpr and snd(f'Cleaning-viewers: {k.remote_address[0]}', cat='WebSocket closed')
            _forDisplay[unid].remove(k)

    for unid in list(_forDisplay):
        if not _forDisplay[unid]:
            del _forDisplay[unid]

# *** *** ***


def wsServer(server, port):
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(hello, host=server, port=port)
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
            threading.Thread(target=wsServer, args=(config.ws_server, port,)).start()
            threading.Thread(target=cleaning).start()
            snd(f'{config.ws_server}:{config.ws_port}', cat='Start WebSocket Server')
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

