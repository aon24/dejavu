# -*- coding: utf-8 -*- 
"""
AON 2020

"""
try:
    from imidjan import HttpResponse
except:
    from django.http import HttpResponse


from common.checkRights import notReader, isEditor
from common.first import err
from common.common import liform, notFound, jsonNotFound, well, urlKeys
from common.dbToolkit.DC import DC
from common.dbToolkit.Book import docFromDB
from common.api.classPage import getPageObj

import json
import os
from mimetypes import guess_type
from urllib.parse import unquote

# *** *** ***

def apiDoGet(request):
    dcUK = urlKeys(request, 'apiDoGet')
    if 'HttpResponse' in str(type(dcUK)):
        return dcUK

    right, handler = _apiGetList.get(dcUK.path, (None, jsonNotFound))
    return HttpResponse(*handler(dcUK))

# *** *** ***

def openDoc(request):
    '''
    открывает или создает новый док нужной формы
    параметры: dbAlias+, form+, dbaGr, unidGr, smartPhone... etc
    '''
    dcUK = urlKeys(request, 'openDoc')
    if 'HttpResponse' in str(type(dcUK)):
        return dcUK
    
    dcUK.dbAlias = dcUK.dbAlias or dcUK.p0
    # checkRight(dba, mode, userName) - return accessDenied(userName)
    if dcUK.mode == 'new':
        dcUK.doc = DC()
    else:
        if docFromDB(dcUK):
            if dcUK.mode == 'info':
                dcUK.form = 'info'
                if True or isEditor(dcUK.dbAlias, dcUK.userName):
                    dcUK.mode = 'edit'
                else:
                    dcUK.mode = 'read'
                
            else:
                dcUK.mode = dcUK.mode or 'read'
        else:
            s = f'Документ не найден ({dcUK.path}?{dcUK.QUERY})'
            err(s, cat='openDoc')
            dcUK.mode = 'read'
            dcUK.doc = DC({'FORM':'info', 'ERROR': s})
    return returnPageOrDoc(dcUK)
    
# *** *** ***

def openPage(request):
    '''
    открывает страницу
    user_id = request.session.get('_auth_user_id', '')
    user_id - str
    '''
    dcUK = urlKeys(request, 'openPage')
    if 'HttpResponse' in str(type(dcUK)):
        return dcUK

    dcUK.mode = dcUK.mode or 'read'

    dcUK.doc = DC()
    if dcUK.dbAlias:
        dcUK.doc.dbAlias = dcUK.dbAlias
    if dcUK.unid:
        dcUK.doc.unid = dcUK.unid
    return returnPageOrDoc(dcUK)

# *** *** ***

def returnPageOrDoc(dcUK):
    opg = getPageObj(dcUK)
    if not opg:
        return notFound(dcUK.page or dcUK.form or dcUK.doc.form or '-?-', dcUK.userName)
    jsDoc = opg.getJsDoc(dcUK)
    html = liform('index', 'html')
    html = html.replace('<title></title>', f'<title>{opg.title}</title>')
    html = html.replace('</head>', f'<script>window.jsDoc={jsDoc};</script>\n</head>', 1)

    return HttpResponse(html)

# *** *** ***

def _loadForm(dcUK): # при перезагрузки форма может исчезнуть
    # dbg(f"{dcUK}\n{well('form-json', dcUK.p0)}", cat='_loadForm')
    return well('form-json', dcUK.p0) or '"{}"', 'application/json'

# *** *** ***

def _newForm(dcUK):
    '''
    url: /api.get/newForm?form=myform & dbAlias=draft & unid=94ec-2580-...
    '''
    dcUK.doc = DC({'dbAlias': dcUK.dbAlias, 'unid': dcUK.unid, 'form': dcUK.form})
    opg = getPageObj(dcUK)
    if not opg:
        return jsonNotFound(f'''newForm not found '{dcUK.form or dcUK.p0}' ''')
    return opg.getJsDoc(dcUK), 'application/json'

# *** *** ***

def jsv(request):
    query = unquote(request.META['QUERY_STRING'])
    fn = f'{os.getcwd()}/{query}'.partition('::')[0].replace('..', '')
    try:
        with open(fn, 'rb') as f:
            mimeType = f'{guess_type(fn, False)[0]}; charset=utf-8'
            return HttpResponse(f.read(), mimeType)
    except:
        err(f'jsv: {fn}', cat='doGet.py')
        return notFound(fn)

# *** *** ***

def _loadDropList(dcUK):
    listName = dcUK.p0.partition('::')[0]
    ls = well('dropList', *listName.split('|')[:2])
    if type(ls) is dict:
        ls = list(ls.keys())

    return json.dumps(ls or [], ensure_ascii=False), 'application/json'

# *** *** ***

def _paging(dcUK):
    rw = well('reviewClass', f'{dcUK.reviewClass}-{dcUK.fieldName}-{dcUK.dbAlias}')
    if rw:
        ds = rw.paging(dcUK)
    else:
        err(str(dcUK), cat='review not found')
        ds = {}
    return json.dumps(ds, ensure_ascii=False), 'application/json'

# *** *** ***

def _loadDoc(dcUK):
    '''
    вызывется из xhr для показа в pageFrame
    '''
    if docFromDB(dcUK):
        opg = getPageObj(dcUK)
        if opg:
            return opg.getJsDoc(dcUK), 'application/json'
    # dbg(f'dc not loaded\n{dcUK}\n\n{dcUK}\n oldPage {not not oldPage}', cat='_loadDoc')
    return '{}', 'application/json'

# *** *** ***

_apiGetList = {
    'loadForm': (None, _loadForm),
    'newForm': (None, _newForm),
    'loadDropList': (None, _loadDropList),
    'paging': (None, _paging),
    'loadDoc': (None, _loadDoc),
}

# *** *** ***