# -*- coding: utf-8 -*-

from tools.common import now, sndErr
from tools.first import err, snd, BASE_DIR
from tools.DC import DC, well, toWell #, profiles

# from appSchedule.models import Hours

import json
import zlib, base64
from datetime import datetime
import os
import sqlite3 as sqldb
import time
from contextlib import suppress
import threading

# *** *** ***

@sndErr
def createDB(dba):
    cat='createDB'
    dbAlias = tableName(dba)
    # if dbAlias not in profiles:
        # err(f'''Invalid dbAlias: "{dbAlias or '-empty-'}"''', cat=cat)
        # return
    
    dbFile = os.path.join(BASE_DIR, 'DB' f'{dbAlias}.rsf')

    con = sqldb.connect(database=dbFile, timeout=10.0)
    con.create_collation("casei", sqlite_collation_casei)
    con.create_function("sqLike", 2, sqlite_function_sqLike)

    sql = """CREATE TABLE "LIFE" (
"id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
"unid" char(32) NOT NULL,
"xfld" text NOT NULL,
"xmdf" timestamp NULL);

CREATE INDEX "LIFE_unid" ON "LIFE" ("unid");
CREATE INDEX "LIFE_xmdf" ON "LIFE" ("xmdf");
"""
    cur = con.cursor()
    
    for s in sql.split(';\n'):
        s and cur.execute(s)
    
    with suppress(Exception):
        cur.close()
        con.commit()
        con.close()

    snd(f'Created database "{dbFile}"', cat=cat)
    return True

# *** *** ***

def tableName(dbAlias):
    return dbAlias.replace('.', '/').upper()

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

def hasDB(dbAlias):
    dbFile = os.path.join(BASE_DIR, 'DB', f'{tableName(dbAlias).upper()}.rsf')
    return os.path.isfile(dbFile) and os.stat(dbFile).st_size

# *** *** ***

def connectToSrv(dba):
    dbAlias = tableName(dba)
    # if dbAlias not in profiles:
        # err(f'''Invalid dbAlias: "{dbAlias or '-empty-'}"''', cat='connectToSrv')
        # return

    dbFile = os.path.join(BASE_DIR, 'DB', f'{dbAlias}.rsf')

    if os.path.isfile(dbFile) and os.stat(dbFile).st_size:
        if lockupConnect(dbAlias):
            con = sqldb.connect(database=dbFile, timeout=10.0)
            con.create_collation("casei", sqlite_collation_casei)
            con.create_function("sqLike", 2, sqlite_function_sqLike)
            return con
        else:
            err(f'SQLITE: DB "{dbFile}" is locked', cat='connectToSrv')
            return
    else:
        err(f'SQLITE: DB "{dbFile}" not found', cat='connectToSrv')

# *** *** ***

lockedCon = {}

def lockupConnect(dbAlias):
    if dbAlias not in lockedCon:
        lockedCon[dbAlias] = threading.Lock()
        lockedCon[dbAlias].acquire()
        return True

    for n in range(100):
        if lockedCon[dbAlias].acquire(False):
            return True
        time.sleep(0.1)

def unlockCon(con, dbAlias):
    with suppress(Exception):
        con.close()
        lockedCon[tableName(dbAlias)].release()
        del lockedCon[tableName(dbAlias)]

def unlockAll():
    global lockedCon
    for l in lockedCon.items():
        l.release()
    lockedCon = {}

# *** *** ***

def docFromDB(dcUK):
    """
    возвращает документ по unid. unid - текстовый hex
    """
    try:
        con = connectToSrv(dcUK.dbAlias)
        if not con:
            return
        
        unid = dcUK.unid.replace('-', '')
        sql = f"SELECT xfld FROM LIFE WHERE (unid='{unid}') AND (xmdf IS NULL);" 
    
        cur = con.cursor()
        cursor = cur.execute(sql)
        if not cursor:
            cur and cur.close()
            unlockCon(con, dcUK.dbAlias)
            return
        
        xfld = None
        for row in cursor:
            xfld = row[0] or '{}'
    
        cur.close()
        unlockCon(con, dcUK.dbAlias)
    
        if not xfld:
            return
    
        fields = json.loads(xfld)
        if 'ROOT' in fields:
            fields['ROOT'] = zlib.decompress(base64.b64decode(fields['ROOT'])).decode()
        dcUK.doc = DC(fields)
        return True

    except Exception as ex:
        err(f'dbAlias={dcUK.dbAlias}&unid={unid}\n{ex}', cat='Book.py.docFromDB')
        
# *** *** ***

def docSaveDB(dcUK):
    '''
    dcUK.doc - документ, который нужно записать
    oldDoc - запись в базе с существующим документом, котрую нужно перевести в истоию.
    '''
    old = DC({'dbAlias': dcUK.dbAlias, 'unid': dcUK.unid})
    oldDoc = docFromDB(old)
    unid = dcUK.unid.replace('-', '')
    con = connectToSrv(dcUK.dbAlias)
    if not con:
        return
    
    if oldDoc: # есть такой, - переводим в историю
        dcUK.doc.MODIFIED = now('-')
        dcUK.doc.MODIFIER = dcUK.userName
        sql = [f"UPDATE LIFE SET xmdf='{datetime.now()}' WHERE (unid='{unid}') AND (xmdf IS NULL);"]
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
    sql.append(f"INSERT INTO LIFE (unid, xfld, xmdf) VALUES ('{unid}', '{xfi}', NULL);")
    
    cur = con.cursor()

    for s in sql:
        try:
            cur.execute(s)
        except Exception as ex:
            err(f'can not execute SQL statement. Exception: {ex}, SQL: {s}', cat='docSaveDB')
            with suppress(Exception):
                cur and cur.close()
                con.rollback()
                unlockCon(con, dcUK.dbAlias)
            return

    try:
        cur.close()
        con.commit()
        unlockCon(con, dcUK.dbAlias)
        return True
    except Exception as ex:
        err(f'ex', cat='docSaveDB-commit')

        
# *** *** ***

@sndErr
def allFromDB(dbAlias, dir_=None):
    """
    возвращает все документы из таблицы
    """

    con = connectToSrv(dbAlias)
    if not con:
        return []
    
    sql = 'SELECT xfld FROM LIFE WHERE (xmdf IS NULL);'

    cur = con.cursor()
    cursor = cur.execute(sql) or []

    docs = []
    for row in cursor:
        fields = json.loads(row[0])
        if dir_ and fields.get('DIR') != dir_:
            continue
        if 'ROOT' in fields:
            fields['ROOT'] = zlib.decompress(base64.b64decode(fields['ROOT'])).decode()
        docs.append( DC(fields) )

    cur.close()
    unlockCon(con, dbAlias)

    return docs
        
# *** *** ***

def setDocNo(dcUK):
    dbAlias = dcUK.dbAlias
    table = 'appAll_docno'
    con = connectToSrv('docno')
    if not con:
        return
    
    sql = f"SELECT docno FROM {table} WHERE dbalias='{dbAlias}';"
    cur = con.cursor()
    cursor = cur.execute(sql)
    n = 0
    if cursor:
        for row in cursor:
            n = row[0]
    else:
        return ''
    
    if n:
        sql = f"UPDATE {table} SET docno={n+1} WHERE dbalias='{dbAlias}';"
    else:
        sql = f"INSERT INTO {table} (dbalias, docno) VALUES ('{dbAlias}', 1);"
    
    cur.execute(sql)
    
    try:
        cur.close()
        con.commit()
        unlockCon(con, dbAlias)
        return str(n+1)
    except:
        unlockCon(con, dbAlias)
        return ''

# *** *** ***
"""
def docsByCats(key, dcUK, param):
    '''
    param - dict
    cat: {},
    
    '''
    docs = well('docsByCats', key) or {}
    if docs:
        return docs

    ls = allFromDB(dcUK.dbAlias, dcUK.dir_) or []


    self.subCats = {}
    for d in ls:
        self.DBC['Все|'].append(d)
        for cat, fName in self.dcVP.cats.items():
            if fName and type(fName) == str:
                if fName[0] == '=': # formula
                    fi = eval(fName[1:])
                    print('*******', fi)
                else:
                    fi = d.F(fName)
                if fi:
                    if fi == True:
                        fi = ''
                    k = f'{cat}|{fi}'
                    if k in self.DBC:
                        self.DBC[k].append(d)
                    else:
                        self.DBC[k] = [d]
                    if cat not in self.subCats:
                        self.subCats[cat] = []
                    if fi and fi not in self.subCats[cat]:
                        self.subCats[cat].append(fi)

    for c in self.DBC:
        if sort == 'docNo':
            self.DBC[c] = sorted(self.DBC[c], key=lambda d: d.F(sort).rjust(6), reverse=reverse)
        else:
            self.DBC[c] = sorted(self.DBC[c], key=lambda d: d.F(sort), reverse=reverse)
    toWell(True, keyWell)

    return self.DBC.get(c_s, [])

"""



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

if __name__ == '__main__':
    createDB('rf.qq/ogg')


