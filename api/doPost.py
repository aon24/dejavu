# -*- coding: utf-8 -*-
"""
AON 2020

"""
from tools.httpMisc import HttpResponse, urlKeys, accessDenied
from tools.DC import DC
from tools.first import err, dbg, snd
from tools.common import emailValidator
from tools.checkRights import isReader, notEditor, isRole, isEditor
from api.pages.htmlToPy import htmlToPy
from api.pages.colors import htmlToJsReact, jsToHtml, pyToHtml, htmlToPython
from api.classPage import getPageObj

import tools.dbToolkit.Book as Book

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

    if not right or right(dcUK.dbAlias, dcUK.userName):  # проверка прав доступа
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
    for k, v in jsonO.items():
        oldF[k], newF[k] = v

    dcUK.unid = newF['UNID'] = newF.get('UNID', uuid.uuid4().hex)

    if not (('EMAIL' not in newF) or emailValidator(newF['EMAIL']) or dcUK.force):
        return f"В поле E_MAIL недействительный эл. адрес:\n\n{newF['EMAIL']}", None, 449

    oldPage = Book.docFromDB(dcUK) or ''  # возвращает запись(модель типа Page для dcUK.dbAlias == 'draft')
    if oldPage:
        if not dcUK.force:
            mdf = dcUK.doc.MODIFIER

            if 'FROMHIST' in newF:  # FROMHIST - всегда даст конфликт
                del newF['FROMHIST']
            else:
                for k in oldF:
                    if k not in ['ROOT', 'MODIFIED', 'MODIFIER']:
                        of = dcUK.doc[k]
                        if oldF[k] != of and newF.get(k, '') != of:
                            s = f'''ИМЯ ПОЛЯ: {k}
    НОВОЕ ЗНАЧЕНИЕ: "{newF.get(k, '')}"
    СТАРОЕ ЗНАЧЕНИЕ: "{oldF[k]}"
    КОНФЛИКТНОЕ ЗНАЧЕНИЕ: "{of}"
    ИЗМЕНЕНО: {dcUK.doc.MODIFIED or '- ? -'}
    РЕДАКТОР: {mdf or '- ? -'}'''
                            err(s, cat=cat)
                            return s, None, 409

            if mdf and mdf != dcUK.userName and oldF.get('ROOT', '') != dcUK.doc.ROOT:
                s = f'''ИМЯ ПОЛЯ: 'ROOT'
НОВОЕ ЗНАЧЕНИЕ (размер): {len(newF.get('ROOT', ''))}
СТАРОЕ ЗНАЧЕНИЕ (размер): {len(oldF.get('ROOT', ''))}
КОНФЛИКТНОЕ ЗНАЧЕНИЕ (размер): {len(dcUK.doc.ROOT)}
ИЗМЕНЕНО: {dcUK.doc.MODIFIED or '- ? -'}
РЕДАКТОР: {mdf}'''
                err(s, cat=cat)
                return s, None, 409

        for k, v in dcUK.doc.items():
            if k not in newF:  # в newF только изменения, добавляем в него неизмененные поля
                newF[k] = v

    # v = json.loads(newF['ROOT'])
    # for i in range(10):
        # v = v.get('boxes')
        # if not v:
            # break
        # if not len(v):
            # break
        # v = v[0]
        # t = v.get('tuning')
        # if t.get('wall'):
            # for k, vv in t.items():
                # print('tuning:', k, vv)
            # t = v.get('rect')
            # for k, vv in t.items():
                # print('rect', k, vv)
            # break
    # return

    dcUK.doc = DC(newF)
    opg = getPageObj(dcUK)

    if opg:
        if not opg.querySave(dcUK):
            return 'BeforeSave error', None, 400

    if dcUK.doc.noSave:
        return 'OK',

    if not dcUK.save():  # Page для dcUK.dbAlias == 'draft'
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
            try: s = buf.decode()
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
            try: s = buf.decode()
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


reColor = re.compile(r'(#\w{8})(#\w{8})')  # '#f59090ff#5cffc6ff' -> '#f59090ff', '#5cffc6ff'


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
            s = v.replace('\n', '')  # чтобы <br> не вставлял
            r = htmlToPython(f"<div>{s}</div>")  # <div> добавляется автоматом, если нет обертки
            js[k] = r[0]['children']  # убираем добавленный <div>

        return json.dumps(js, ensure_ascii=False), 'application/json'
    except Exception as ex:
        err(str(ex), cat='apiRtfToReact')
        return f'"ERR": "{ex}"', 'application/json'

# *** *** ***


def toArchive(dcUK, buf):
    cat = 'toArchive'
    if not Book.docFromDB(dcUK):
        err(f'Документ уже удален: "{dcUK.dbAlias}:{dcUK.unid}"', cat=cat)
        return 'Документ уже удален', None, 410

    dcUK.doc.key_ = dcUK.doc.key;
    dcUK.doc.key = 'Archive'
    if dcUK.save():
        return 'OK',
    else:
        err(f'Ошибка записи в базу: "{dcUK.dbAlias}:{dcUK.unid}"', cat=cat)
        return 'Ошибка записи в базу', None, 411

# *** *** ***


def duplicate(dcUK, buf):
    cat = 'duplicate'
    if not Book.docFromDB(dcUK):
        err(f'Документ был удален: "{dcUK.dbAlias}:{dcUK.unid}"', cat=cat)
        return 'Документ был удален', None, 410

    # dcUK.doc.dir = 'A'
    dcNew = DC(dcUK)
    dcNew.doc = dcUK.doc
    dcNew.unid = dcNew.doc.unid = uuid.uuid4().hex
    n1, _, n2 = dcNew.doc.docNo.partition('.')
    n2 = int(n2 or '0', base=10) + 1
    dcNew.doc.docNo = f'{n1}.{n2:02}'
    if dcNew.save():
        return 'OK',
    else:
        err(f'Ошибка записи в базу: "{dcUK.dbAlias}:{dcUK.unid}"', cat=cat)
        return 'Ошибка записи в базу', None, 411

# *** *** ***


def apiSetFieldFromView(dcUK, buf):
    # in Sova-17 used for setting the field 'publich'
    p = Book.docFromDB(dcUK)
    if not p:
        err(f'Документ удален: "{dcUK.dbAlias}:{dcUK.unid}', cat='apiSetFieldFromView')
        return 'Документ удален', None, 410

    dcUK.doc[dcUK.field] = dcUK.value
    if dcUK.save(p):
        return 'OK',

    err(f'Ошибка записи в базу: "{dcUK.dbAlias}:{dcUK.unid}', cat='apiSetFieldFromView')
    return 'Ошибка записи в базу', None, 411

# *** *** ***


_keysApiPost = {
    'duplicate': (None, duplicate),
    'toArchive': (None, toArchive),
    'saveDoc': (None, apiSaveDoc),
    'setFieldFromView': (None, apiSetFieldFromView),

    'jsToHtml': (None, apiJsToHtml),
    'pyToHtml': (None, apiPyToHtml),
    'showFile': (None, apiShowFile),
    'showPy': (None, apiShowPy),
    'htmlToReact': (None, apiHtmlToReact),
    'showReact': (None, apiShowReact),
    'rtfToReact': (None, apiRtfToReact),
}

# *** *** ***

