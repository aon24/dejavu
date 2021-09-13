# -*- coding: utf-8 -*- 
"""
AON 2020

"""
try:
    from imidjan import HttpResponse
except:
    from django.http import HttpResponse

from common.first import err, dbg, snd
from common.common import accessDenied, urlKeys, DC, emailValidator
from common.checkRights import isReader, notEditor, isRole, isEditor
from common.htmlToPy import htmlToPy
from common.colors import htmlToJsReact, jsToHtml, pyToHtml, htmlToPython
from common.dbToolkit.Book import docFromDB
from common.api.classPage import getPageObj


import re
import json
import uuid

# *** *** ***

def doPost(request):
#     time.sleep(2)
    """
    query - параметры, разделенные '&'
    В конце строки справа от :: дата-время версии ИЛИ контр. сумма ИЛИ нет.
    Пример url: 'loadForm?form=outlet.gru::804597279', 'user/SOVA'
    """
    
    dcUK = urlKeys(request, 'doPost')
    if 'HttpResponse' in str(type(dcUK)):
        return dcUK

    
    right, handler = _keysApiPost.get(dcUK.path, (isReader, badPostReq))
    ln = int(request.META.get('CONTENT_LENGTH', -1))
    buf = request.META['wsgi.input'].read(ln).decode()

    if not right or right(dcUK.dbAlias, dcUK.userName): # проверка прав доступа
        ls = handler(dcUK, buf)
        return HttpResponse(*ls)
    else:
        return accessDenied(dcUK.userName)
    
# *** *** ***

def badPostReq(dcUK, buf=None):
    dbg(f'param: {dcUK}', cat='badReq')
    return f'Access denied for {dcUK.userName}', None, 403

# *** *** ***

def apiSaveDoc(dcUK, buf):
    # print('apiSaveDoc---apiSaveDoc---apiSaveDoc---apiSaveDoc---\n', dcUK)
    
#     if notEditor(dcUK.dbAlias, dcUK.userName):
#         return f'Access denied for {dcUK.userName}', None, 403

    # TODO: придумать что-нибудь получше
#     if isRole(dcUK.dbAlias, dcUK.userName, 'restrict'):
#         return f'Access denied for {dcUK.userName}', None, 403
    
    cat = 'doPost.py.saveDoc'
    try:
        jsonO = json.loads(buf)
    except Exception as ex:
        s = f'Except by save: json.loads(): \n{ex}\n{buf[:100]}'
        err(s, cat=cat)
        return s, None, 400

    oldF, newF = {}, {}
    for k in jsonO:
        oldF[k], newF[k] = jsonO[k]

    dcUK.unid = newF['UNID'] = newF.get('UNID', uuid.uuid4().hex)

    if not (('EMAIL' not in newF) or emailValidator(newF['EMAIL']) or dcUK.force):
        return f"В поле E_MAIL недействительный эл. адрес:\n\n{newF['EMAIL']}", None, 449

    oldPage = docFromDB(dcUK) or '' # возвращает запись(модель типа Page для dcUK.dbAlias == 'draft') 
    if oldPage:
        oldFields = dcUK.doc._KV_
        if not dcUK.force:
            mdf = oldFields.get('MODIFIER')
            for k in oldF:
                if k not in ['ROOT', 'MODIFIED', 'MODIFIER']:
                    of = oldFields.get(k, '')
                    if oldF[k] != of and newF.get(k, '') != of:
                        s = f'''ИМЯ ПОЛЯ: {k}
НОВОЕ ЗНАЧЕНИЕ: "{newF.get(k, '')}"
СТАРОЕ ЗНАЧЕНИЕ: "{oldF[k]}"
КОНФЛИКТНОЕ ЗНАЧЕНИЕ: "{of}"
ИЗМЕНЕНО: {oldFields.get('MODIFIED', '- ? -')}
РЕДАКТОР: {mdf or '- ? -'}'''
                        err(s, cat=cat)
                        return s, None, 409

            if mdf and mdf != dcUK.userName and oldF.get('ROOT', '') != oldFields.get('ROOT', ''):
                s = f'''ИМЯ ПОЛЯ: 'ROOT'
НОВОЕ ЗНАЧЕНИЕ (размер): {len(newF.get('ROOT', ''))}
СТАРОЕ ЗНАЧЕНИЕ (размер): {len(oldF.get('ROOT', ''))}
КОНФЛИКТНОЕ ЗНАЧЕНИЕ (размер): {len(oldFields.get('ROOT', ''))}
ИЗМЕНЕНО: {oldFields.get('MODIFIED', '- ? -')}
РЕДАКТОР: {mdf}'''
                err(s, cat=cat)
                return s, None, 409


        for k, v in oldFields.items(): # в newF только изменения, добавляем в него неизмененные поля
            if k not in newF and v: # пустые поля нафиг
                newF[k] = v
        
    dcUK.doc = DC(newF)
    opg = getPageObj(dcUK)

    if opg:
        if not opg.querySave(dcUK):
            return 'BeforeSave error', None, 400

    if dcUK.doc.noSave:
        return 'OK',

    if not dcUK.save(): # Page для dcUK.dbAlias == 'draft'
        return 'DocSave error', None, 400
    
    if opg and not opg.afterSave(dcUK):
        return 'AfterSave error', None, 400
    return 'OK',

# *** *** ***

def apiJsToHtml(dcUK, buf):
    return jsToHtml(f'<source lang="javascript">{buf}</source>'),

# *** *** ***

def apiPyToHtml(dcUK, buf):
    return pyToHtml(f'<source lang="python">{buf}</source>'),

# *** *** ***

def apiShowReact(dcUK, buf):
    '''
    на входе html-страница
    возвращает json-строку, для прорисовки компонент    
    '''
    return json.dumps(htmlToPy(buf), ensure_ascii=False), 'application/json'

# *** *** ***

def apiShowPy(dcUK, b):
    s = './static/' + dcUK.file.replace('..', '')
    dbg(s, cat='apiShowPy')
    try:
        with open(s, 'rb') as f:
            buf = f.read()
            try:    s = buf.decode()
            except: s = buf.decode('cp1251')
    except Exception as ex:
        s = f'file not read: "{s}"\n{ex}'
        err(s, cat='apiShowPy')
    s = f'<source lang="python">\n{s}\n</source>'
    return json.dumps(htmlToPy(pyToHtml(s)), ensure_ascii=False), 'application/json'

# *** *** ***

def apiShowFile(dcUK, b):
    s = './static/' + dcUK.file.replace('..', '')
    dbg(s, cat='apiShowFile')
    try:
        with open(s, 'rb') as f:
            buf = f.read()
            try:    s = buf.decode()
            except: s = buf.decode('cp1251')
    except Exception as ex:
        s = f'file not read: "{s}"\n{ex}'
        err(s, cat='apiShowFile')
    return s,

# *** *** ***

def apiHtmlToReact(dcUK, buf):
    '''
    на входе html-страница
    возвращает html-строку, для показа js-реакт-кода
    '''
    return htmlToJsReact(buf),
    
# *** *** ***

reColor = re.compile(r'(#\w{8})(#\w{8})') # '#f59090ff#5cffc6ff' -> '#f59090ff', '#5cffc6ff'

def apiRtfToReact(dcUK, buf):
    '''
    на входе html-страница
    возвращает json-строку(массив элементов для boxing)
    '''
    try:
        s = buf
        for r in re.finditer(reColor, s):
            s = s.replace(r.group(0), f'{r.group(1)}; background-color: {r.group(2)}')

        js = {}
        rtf = json.loads(s)
        for k, v in rtf.items():
            s = v.replace('\n', '') # чтобы <br> не вставлял
            r = htmlToPython(f"<div>{s}</div>") # <div> добавляется автоматом, если нет обертки
            js[k] = r[0]['children'] # убираем добавленный <div>
        
        return json.dumps(js, ensure_ascii=False), 'application/json'
    except Exception as ex:
        print(4, ex)
        return f'"ERR": "{ex}"', 'application/json'
    
# *** *** ***

def apiSetFieldFromView(dcUK, buf):
    p = docFromDB(dcUK)
    if not p:
        err(f'Документ удален: "{dcUK.dbAlias}:{dcUK.unid}', cat='apiSetFieldFromView')
        return 'Документ удален', None, 410

    dcUK.doc.S(dcUK.field, dcUK.value)
    if dcUK.save(p, toHist=dcUK.toHist):
        return 'OK',
        
    err(f'Ошибка записи в базу: "{dcUK.dbAlias}:{dcUK.unid}', cat='apiSetFieldFromView')
    return 'Ошибка записи в базу', None, 411

# *** *** ***

_keysApiPost = {
    'saveDoc': (None, apiSaveDoc),
    'setFieldFromView': (None, apiSetFieldFromView),
    
    'jsToHtml': (None, apiJsToHtml),
    'pyToHtml': (None, apiPyToHtml),
    'showFile': (None, apiShowFile),
    'showPy': (None, apiShowPy),
    'htmlToReact': (None, apiHtmlToReact),
    'showReact': (None, apiShowReact),
    'rtfToReact':  (None, apiRtfToReact),
}

# *** *** ***
        

