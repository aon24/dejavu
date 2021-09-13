# -*- coding: utf-8 -*- 
'''
Created on 24 apr 2020

@author: aon
'''
from common.common import well, toWell, setVersionFiles
from common.dbToolkit.DC import DC, config
from common.first import err, dbg

import json
import importlib
import uuid
from copy import deepcopy
from binascii import crc32
from platform import python_version

# *** *** ***

def getPageObj(dcUK):     # dcUK = urlKeys
    '''
    у документа из БД форма, у страницы page
    '''
    page = dcUK.form or (dcUK.doc and dcUK.doc.form) or dcUK.page
    page = page.lower()

    if page:
        opg = well('forms', page)
        if opg:
            return opg

        pref = page.partition('_')[0]
        if pref == f'a':
            path = f'appDesign.pages.{page}.{page}'
        elif pref == 'sch':
            path = f'appSchedule.pages.{page}.{page}'
        else:
            path = 'common.pages.info.info'
            page = 'info'

        dbg(path, cat='getPageObj')
        # module = importlib.import_module(path)
        try:
            module = importlib.import_module(path)
        except Exception as ex:
            return err(f'Page not found: "{path}"\n {ex}', cat='getPageObj')
            
        opg = getattr(module, page)(page)
        toWell(opg, 'forms', page)
        return opg

# *** *** ***


class Page(object):
    '''
    urlForms - словарь в форме, хранит url для форм. КЛЮЧ: form+mode, возвращает "apigetc?loadForm&outlet.gru::2113546371"
    form-json - в глобальном словаре готовый json. КЛЮЧ: 'form::CRC-СУММА'
    '''

    def __init__(self, form):
        self.form = form
        self.title = self.title or 'React-py.ru'

        self.urlForms = {} # key = '-'.join([dbAlias, mode, multiPage, smartPhone])
        self.caching = True
        path = f'./'

        not getattr(self, 'title', None) and setattr(self, 'title', 'React-py')
        for a in ['title', 'jsCssUrl', 'jsCssUrlRead', 'jsCssUrlEdit']:
            not getattr(self, a, None) and setattr(self, a, '')

        if self.jsCssUrl:
            self.jsCssUrlRead = self.jsCssUrlEdit = setVersionFiles(self.jsCssUrl, path)
        else:
            self.jsCssUrlRead = setVersionFiles(self.jsCssUrlRead, path)
            self.jsCssUrlEdit = setVersionFiles(self.jsCssUrlEdit, path)

    # *** *** ***
    
    def getJsDoc(self, dcUK):
        '''
        вормирует словарь для отправки клиенту
        '''
        if not dcUK.doc:
            dcUK.doc = DC()
        dcUK.doc.form = dcUK.doc.form or self.form

        if dcUK.mode == 'edit': # чтобы можно было установить новое значение в queryOpen
            do = {k: dcUK.doc.F(k) for k in dcUK.doc._KV_} # save oldValues in 'do'
        
        dcUK.unid = dcUK.unid or dcUK.doc.unid or uuid.uuid4().hex
        self.queryOpen(dcUK)

        fv = {} # fieldValues- KV для отправки клиенту
        for k, v in dcUK.doc._KV_.items():      # dcUK.doc - DC-object
            if 'PASSW' not in k:
                fv[k] = v.replace('\u2028', ' ').replace('\u2029', ' ')
                    
        ds = dict(
                fieldValues = fv,
                rsMode = dcUK.mode,
                dbAlias = dcUK.dbAlias,
                userName = dcUK.userName,
                unid = dcUK.unid,
                urlForm = self.getUrl(dcUK),
                cssJsUrl = self.getJsCssUrl(dcUK.mode),
                version = f'Python {python_version()}',
            )
        if  dcUK.mode == 'new':
            ds['oldValues'] = {k: '' for k in fv}
        elif dcUK.mode == 'edit': # чтобы можно было установить новое значение в queryOpen
            ds['oldValues'] = {k: do.get(k, '') for k in fv if do.get(k, '') != fv[k]}

        return json.dumps(ds, ensure_ascii=False).replace('</script','<\/script')
    
    def queryOpen(self, dcUK): pass
    def querySave(self, dcUK): return True
    def afterSave(self, dcUK): return True
    
    def getJsCssUrl(self, mode):
        if mode in ['read', 'preview']:
            return self.jsCssUrlRead
        else:
            return self.jsCssUrlEdit
    
    # *** *** ***

    def getUrl(self, dcUK):
        '''
        возвращает url для загрузки формы формы
        сама форма хранится в глоб. словаре 'form-json', в url ключ для этого словаря
        '''
        key = '-'.join([dcUK.dbAlias, dcUK.mode, dcUK.multiPage, dcUK.userAgent])

        if self.caching and key in self.urlForms:
            return self.urlForms[key]
    
        try:
            pg = deepcopy(self.page(dcUK))
            pg = self.parseCell(pg)
            jsPage = json.dumps(pg, ensure_ascii=False, sort_keys=True)
            crc = crc32(jsPage.encode(), 0)
        except Exception as ex:
            err(f'{self.form}\n{ex}', cat='classPage.getUrl')
            return f'error-{self.form}-classPage.getUrl'
        
        if self.caching:
            urlForm = f'api.getc/loadForm?{self.form}::{crc}'
        else:
            urlForm = f'api.get/loadForm?{self.form}::{crc}'
        self.urlForms[key] = urlForm
        toWell( jsPage, 'form-json', f'{self.form}::{crc}' )

        return urlForm

    # *** *** ***

    def parseCell(self, cell):
        if type(cell) is str:
            return cell
        if not (type(cell) is dict and not cell.get('skip')):
            return None
        
        row = cell.get('children')
        if row:
            ls = []
            for it in row:
                c = self.parseCell(it)
                if c:
                    ls.append(c)
            cell['children'] = ls

        if cell.get('field'):
            td = [*cell['field']] # в td массив: название, тип[, справочник[, формула]]
            td[0] = td[0].upper()
            cell['field'] = td # замена tuple to list
            
            if (td[1].startswith('lb') or td[1] == 'list') and type(td[2]) is not list and '|||' not in td[2]: # поле со сложным списком с url
                url = td[2]
                if len(td) > 3: # formula
                    if td[2]: # если == '', значит строка url в td[3]
                        url += '|'
#                     mode = self.mode
#                     dbProfile = profile(self.dbAlias)
#                     dName = dbProfile.dName if dbProfile else ''
#                     url += eval(td[3])
                    del td[3]
        
                if td[2]:
                    ver = well('lsVersions', url) or well('lsVersions', url.replace('|', '¤'))
                    if ver:
                        url = f'api.getc/loadDropList?{url}::{ver}' # api.getc - кэшируемый
                    else:
                        url = f'api.get/loadDropList?{url}' # api.get - некэшируемый

                td[2] = url
    
        return cell
    
    # *** *** ***
