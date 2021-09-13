# -*- coding: utf-8 -*-
'''
Created 2021

@author: aon

'''

from common.dbToolkit.Book import setDocNo
from .first import snd, err

import time
import threading

# *** *** ***
lockSno = {}

def snoDB(dcUK, cmd):
    dbAlias = dcUK.dbAlias
    
    if dbAlias not in lockSno:
        lockSno[dbAlias] = threading.Lock()

    if cmd == 'inc':
        for n in range(50):
            if lockSno[dbAlias].acquire(False):
                n = setDocNo(dcUK)
                lockSno[dbAlias].release()
                if n:
                    snd(f'{dcUK.userName}: зарегистрирован номер {n} в {dbAlias}', cat='Регистрация')
                else:
                    err(f'{dcUK.userName}: номер не сохранен в {dbAlias} из-за ошибки', cat='Регистрация')
                return n
            time.sleep(0.05)
        lockSno[dbAlias].release() # разблокировать полюбому
    return ''

