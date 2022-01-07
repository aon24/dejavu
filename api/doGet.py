# -*- coding: utf-8 -*- 
"""
AON 2020
"""
try:
    from dejavu.imidjan import HttpResponse
except:
    from django.http import HttpResponse

from tools.checkRights import isEditor, isReader
from tools.first import err, BASE_DIR
from tools.common import liform, notFound, jsonNotFound, well, urlKeys
from tools.DC import DC
from api.classPage import getPageObj
from api.pages.colors import boxToHtml

import tools.dbToolkit.Book as Book

import json
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
    
    dcUK.dbAlias = dcUK.dbAlias
    # checkRight(dba, mode, userName) - return accessDenied(userName)
    if dcUK.mode == 'new':
        dcUK.doc = DC()
    else:
        if Book.docFromDB(dcUK):
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
    url: opendoc?mode=new&form=a_design&dbAlias=draft
    открывает страницу
    user_id = request.session.get('_auth_user_id', '')
    user_id - str
    '''
    dcUK = urlKeys(request, 'openPage')
    if 'HttpResponse' in str(type(dcUK)):
        return dcUK

    if dcUK.mode == 'html':
        Book.docFromDB(dcUK)
        html = boxToHtml(dcUK.doc.root)
        title = f'html {dcUK.docNo}'
        page = liform('open', 'html') % (title, html)
        return HttpResponse(page)

    return notFound(f'openPage mode={dcUK.mode}', un=dcUK.userName)

# *** *** ***

def returnPageOrDoc(dcUK):
    opg = getPageObj(dcUK)
    if not opg:
        return notFound(f'form "{dcUK.page or dcUK.form or dcUK.doc.form or "-?-"}', dcUK.userName)
    dcUK.dbAlias = dcUK.dbAlias or opg.dbAlias
    
    jsDoc = opg.getJsDoc(dcUK)
    html = liform('index', 'html')
    html = html.replace('<title></title>', f'<title>{opg.title}</title>')
    html = html.replace('</head>', f'<script>window.jsDoc={jsDoc};</script>\n</head>', 1)

    return HttpResponse(html)

# *** *** ***

def _loadForm(dcUK): # при перезагрузкe форма может исчезнуть
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
        return jsonNotFound(dcUK)
    return opg.getJsDoc(dcUK), 'application/json'

# *** *** ***

def _new(request):
    '''
    url: /new?form=myform&dbAlias=dba
    '''
    dcUK = urlKeys(request, 'new')
    dcUK.mode = 'new'
    dcUK.doc = DC({'form': dcUK.form})
    return returnPageOrDoc(dcUK)

# *** *** ***

def jsv(request):
    query = unquote(request.META['QUERY_STRING'])
    fn = f'{BASE_DIR}{query}'.partition('::')[0].replace('..', '')
    
    try:
        with open(fn, 'rb') as f:
            mimeType = f'{guess_type(fn, False)[0]}; charset=utf-8'
            return HttpResponse(f.read(), mimeType)
    except:
        err(f'jsv: {fn}', cat='doGet.py')
        return notFound(fn)

# *** *** ***

def image(request):
    query = unquote(request.META['QUERY_STRING'])
    fn = f'{BASE_DIR}api/react/images/{query}'.replace('..', '')
    try:
        with open(fn, 'rb') as f:
            mimeType = f'{guess_type(fn, False)[0]}'
            return HttpResponse(f.read(), mimeType)
    except:
        return notFound(fn)

# *** *** ***
def _loadDropList(dcUK):
    listName = dcUK.p0.partition('::')[0]
    ls = well('dropList', *listName.split('|')[:2])
    if type(ls) is dict:
        ls = list(ls.keys())

    return json.dumps(ls or [], ensure_ascii=False), 'application/json'

# *** *** ***

def _loadSubCats(dcUK):
    if dcUK.form:
        viewOrPage = getPageObj(dcUK)
    else:
        viewOrPage = well('viewObjects', f'{dcUK.view}')
    if viewOrPage:
        return json.dumps(viewOrPage.subCats.get(dcUK.cat, []), ensure_ascii=False), 'application/json'
    else:
        return '[]', 'application/json'
    
# *** *** ***

def _paging(dcUK):
    if isEditor(dcUK.dbAlias, dcUK.userName):
        dcUK.mode = 'edit'
    elif isReader(dcUK.dbAlias, dcUK.userName):
        dcUK.mode = 'read'
    else:
        return [f'accessDenied for {dcUK.userName}'], 'application/json'

    key = f'{dcUK.fieldName}-{dcUK.dbAlias}'
    rw = well('viewObjects', key)
    if rw:
        ds = rw.paging(dcUK)
    else:
        err(key, cat='view object not found')
        ds = [f'paging: view object "{key}" not found']
    return json.dumps(ds, ensure_ascii=False), 'application/json'

# *** *** ***

def _loadDoc(dcUK):
    '''
    вызывется из xhr для показа в pageFrame
    '''
    if Book.docFromDB(dcUK):
        opg = getPageObj(dcUK)
        if opg:
            return opg.getJsDoc(dcUK), 'application/json'
    # dbg(f'dc not loaded\n{dcUK}\n\n{dcUK}\n oldPage {not not oldPage}', cat='_loadDoc')
    return '{}', 'application/json'

# *** *** ***

def _getData(dcUK):
    '''
    вызывется из xhr для загрузки каких-либо данных
    '''
    opg = getPageObj(dcUK)
    if opg:
        return opg.getData(dcUK)

    s = f'form "{dcUK.form}" not found'
    err(s, cat='_getData')
    return s,

# *** *** ***

_apiGetList = {
    'loadForm': (None, _loadForm),
    'newForm': (None, _newForm),
    'loadDropList': (None, _loadDropList),
    'paging': (None, _paging),
    'loadDoc': (None, _loadDoc),
    'loadSubCats': (None, _loadSubCats),
    'getData': (None, _getData),
}

# *** *** ***