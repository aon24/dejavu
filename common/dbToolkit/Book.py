# -*- coding: utf-8 -*-

from common.common import now, toWell
from common.first import err, snd
from common.dbToolkit.DC import DC

# from appSchedule.models import Hours

import json
import zlib, base64
from datetime import datetime
import os
import sqlite3 as sqldb
from random import random
import time
from contextlib import suppress

# *** *** ***

def sqlite_collation_casei(x, y):
    _x = x.lower()
    _y = y.lower()
    return 0 if _x == _y else -1 if _x < _y else 1

def sqlite_function_sqLike(s, patt):
    # TODO: process wildcards
    # return fnmatch.fnmatch(s, patt.replace('%', '*').replace('_', '?'))
    
    _patt = patt.lower().replace('%', '')
    _s = s.lower()
    if patt[0] == '%' and patt[-1] == '%':
        return _patt in _s
    elif patt[0] == '%':
        return _s.endswith(_patt)
    elif patt[-1] == '%':
        return _s.startswith(_patt)
    else:
        return _s == _patt
    
# *** *** ***

def connectToSrv(dbAlias):
    if dbAlias not in ['draft', 'docno']:
        err(f'''Invalid dbAlias: "{dbAlias or '-empty-'}"''', cat='connectToSrv')
        return
    
    # if not dbWait(self.alias):
        # return er('Database is locked')

    dbFile = f'{os.getcwd()}/DB/{dbAlias}.rsf'

    if os.path.isfile(dbFile) and os.stat(dbFile).st_size:
        con = sqldb.connect(database=dbFile, timeout=10.0)
        con.create_collation("casei", sqlite_collation_casei)
        con.create_function("sqLike", 2, sqlite_function_sqLike)
        return con
    else:
        err(f'SQLITE: DB "{dbFile}" not found', cat='error_connect')

# *** *** ***

def docFromDB(dcUK):
    """
    возвращает документ по unid. unid - текстовый hex
    """
    con = connectToSrv(dcUK.dbAlias)
    if not con:
        return
    
    table = 'appDesign_page'
    unid = dcUK.unid.replace('-', '')
    sql = f"SELECT xfields FROM {table} WHERE (unid='{unid}') AND (xmdf IS NULL);" 
        
    cur = cursorExecute(dcUK.dbAlias, con, sql)

    if not cur:
        con.close()
        return
    
    xfields = None
    for row in cur:
        xfields = row[0] or '{}'

    cur.close()
    con.close()

    if not xfields:
        return
    
    try:
        fields = json.loads(xfields)
        if 'ROOT' in fields:
            fields['ROOT'] = zlib.decompress(base64.b64decode(fields['ROOT'])).decode()
        dcUK.doc = DC(fields)
        return True

    except Exception as ex:
        err(f'dbAlias={dcUK.dbAlias}&unid={unid}, invalid document structure\n{ex}', cat='Book.py.docFromDB')
   
        
# *** *** ***

def docSave(dcUK):
    try:
        xfi = json.dumps(dcUK.doc._KV_, ensure_ascii=False)
        if dcUK.dbAlias == 'draft':
            p = DC({'unid': dcUK.unid, 'xfields': xfi})
        elif dcUK.dbAlias == 'draft':
            p = DC({'unid': dcUK.unid, 'xfields': xfi})
        else:
            err(f'Неизвестный dbAlias: "{dcUK.doc.dbAlias}"', cat='docSave')
            return
        
        p.save(using=dcUK.dbAlias)
        return p
    
    except Exception as ex:
        err(f'dbAlias: "{dcUK.doc.dbAlias}"\n{ex}\n', cat='docSave')

# *** *** ***

def docSaveDB(dcUK):
    '''
    dcUK.doc - документ, который нужно записать
    oldDoc - запись в базе с существующим документом, котрую нужно перевести в истоию.
    '''
    table = 'appDesign_page'
    old = DC({'dbAlias': dcUK.dbAlias, 'unid': dcUK.unid})
    oldDoc = docFromDB(old)
    unid = dcUK.unid.replace('-', '')
    con = connectToSrv(dcUK.dbAlias)
    if not con:
        return
    
    if oldDoc: # есть такой, - переводим в историю
        dcUK.doc.MODIFIED = now('-')
        dcUK.doc.MODIFIER = dcUK.userName
        sql = [f"UPDATE {table} SET xmdf='{datetime.now()}' WHERE (unid='{unid}') AND (xmdf IS NULL);"]
    else:
        sql = []
        dcUK.doc.CREATED = now('-')
        dcUK.doc.CREATOR = dcUK.userName

    # сохраняем новый док(или новую версию)
    if dcUK.doc.root:
        lenRoot = len(dcUK.doc.root)
        c = zlib.compress(dcUK.doc.root.encode(), 9)
        root = str(base64.b64encode(c), 'ascii')
        dcUK.doc.root = root

        s = f'size:{lenRoot} zip:{len(c)} b64:{len(root)}'
        dcUK.doc.pageSize = s
        snd(f'{s} (№ {dcUK.doc.docNo})', cat='ROOT-size')
    
    xfi = json.dumps(dcUK.doc._KV_, ensure_ascii=False)
    sql.append(f"INSERT INTO {table} (unid, xfields, xmdf) VALUES ('{unid}', '{xfi}', NULL);")
    
    cur = con.cursor()
    for s in sql:
        try:
            cur.execute(s)
        except Exception as ex:
            err(f'can not execute SQL statement. Exception: {ex}, SQL: {s}', cat='docSaveDB')
            with suppress(Exception):
                cur and cur.close()
                con.rollback()
                con.close()
            return

    try:
        cur.close()
        con.commit()
        con.close()
        return True
    except Exception as ex:
        err(f'ex', cat='docSaveDB-commit')

        
# *** *** ***

def viewReload(dbAlias, table):
    con = connectToSrv(dbAlias)
    if not con:
        return

    sql = f"SELECT xfields FROM {table} WHERE xmdf IS NULL;"
        
    cur = cursorExecute(dbAlias, con, sql)

    cats = {'': []}
    if cur:
        for row in cur:
            d = DC(json.loads(row[0] or '{}'))
            if d.dir == '0':
                cats[''].append(d)
                if d.cat:
                    for cat in d.cat.split('\n'):
                        if cat not in cats:
                            cats[cat] = [d]
                        else:
                            cats[cat].append(d)

    with suppress(Exception):
        cur and cur.close()
        con.close()
                    
    for c in cats:
        cats[c] = sorted(cats[c], key=lambda d: d.docNo.rjust(6), reverse=True)
    toWell(cats, dbAlias)
    
# *** *** ***

def cursorExecute(dbAlias, con, sql):
    def exx(con):
        tryNum = 0
        cat = 'deadlock'
        try:
            cur = con.cursor()
        except:
            return
        while True:
            try:
                r = cur.execute(sql)
                if tryNum:
                    snd(f'OK. TryNum={tryNum}', cat=cat)
                return r
            except Exception as ex:
                err(f'{sql}\n{ex}', cat='cur.execute')
                s = str(ex).lower()
                dbIsLocked = ('database is locked' in s or 'deadlock' in s)
                if dbIsLocked and tryNum < 5:
                    time.sleep(0.1 + 0.1 * random())
                    tryNum += 1
                    snd(f'tryNum={tryNum}\n{ex}', cat=cat)
                else:
                    return

    c = exx(con)
    if not c:
        con = recon(dbAlias, con)
        if not con:
            err(f'Can not reconnect to {dbAlias}', cat='cursorExecute')
            return
        
        c = exx(con)
        if not c:
            err(f'con: {dbAlias} exx: {sql}', cat='cursorExecute')

    return c

# *** *** ***

def recon(dbAlias, con):
    with suppress(Exception):
        con.commit()
    with suppress(Exception): con.close()
    try:
        return connectToSrv(dbAlias)
    except Exception as ex:
        err(f'Database.recon() exception: {ex}', cat='db-recon')

# *** *** ***
def setDocNo(dcUK):
    dbAlias = dcUK.dbAlias
    table = 'appAll_docno'
    con = connectToSrv('docno')
    if not con:
        return
    
    sql = f"SELECT docno FROM {table} WHERE dbalias='{dbAlias}';"
    cur = cursorExecute('docno', con, sql)
    if cur:
        n = 0
        for row in cur:
            n = row[0]
        cur.close()
    else:
        return ''
    
    if n:
        sql = f"UPDATE {table} SET docno={n+1} WHERE dbalias='{dbAlias}';"
    else:
        sql = f"INSERT INTO {table} (dbalias, docno) VALUES ('{dbAlias}', {n+1});"
    
    cur = cursorExecute('docno', con, sql)
    
    try:
        cur and cur.close()
        con.commit()
        con.close()
        return str(n+1)
    except Exception as ex:
        return ''

# *** *** ***

'''
dbLocks = {} # { dbAlias: [threading.Lock(), threading.get_ident()] }



def dbWait(dba):
    iniTime = time()
    while dba in dbLocks and dbLocks[dba][1] and dbLocks[dba][1] != threading.get_ident():
        sleep(0.1 + 0.05 * random())
#         print('dbWait %r, thread_id = %r, time = %r' % (dba, dbLocks[dba][1], time() - iniTime))
        if time() - iniTime > 60:
            return False
    return True



def dbIsLocked(dba):
    return dbLocks.get(dba, [0, 0])[1]

'''


