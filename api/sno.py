# -*- coding: utf-8 -*-
'''
Created 2021

@author: aon

'''

from tools.dbToolkit.Book import setDocNo
from tools.first import snd, err

# *** *** ***


def snoDB(dcUK, cmd):
    dbAlias = dcUK.dbAlias

    if cmd == 'inc':
        n = setDocNo(dbAlias) or ''
        if n:
            snd(f'{dcUK.userName}: зарегистрирован номер {n} в {dbAlias}', cat='Регистрация')
        else:
            err(f'{dcUK.userName}: номер не сохранен в {dbAlias} из-за ошибки', cat='Регистрация')
    return n

# *** *** ***
