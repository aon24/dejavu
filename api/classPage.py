# -*- coding: utf-8 -*-
'''
Created on 24 apr 2020

@author: aon
'''

# *** *** ***

from tools.common import setVersionFiles
from tools.first import err, dbg, BASE_DIR, versionString
from tools.DC import DC, config, well, toWell

import json
import importlib
import uuid
import traceback
from copy import deepcopy
from binascii import crc32

# *** *** ***


def getPageObj(dcUK):  # dcUK = urlKeys
    '''
    у документа из БД форма, у страницы page
    '''
    page = dcUK.form or (dcUK.doc and dcUK.doc.form) or dcUK.page
    if (not page):
        page = {'draft': 'a_design'}.get(dcUK.dbAlias, '')

    if page:
        opg = well('forms', page)
        if opg:
            return opg

        path = f'api.pages.{page}.{page}'

        dbg(path, cat='getPageObj')

        try:
            module = importlib.import_module(path)
            opg = getattr(module, page)(dcUK)
            toWell(opg, 'forms', page)
            return opg
        except Exception as ex:
            return err(f'Page not found: "{path}"\n {ex} \n*** *** *** {traceback.format_exc()}', cat='getPageObj')

# *** *** ***


class Page(object):
    '''
    urlForms - словарь в форме, хранит url для форм. КЛЮЧ: form+mode, возвращает "apigetc?loadForm&outlet.gru::2113546371"
    form-json - в глобальном словаре готовый json. КЛЮЧ: 'form::CRC-СУММА'
    '''

    def __init__(self, dcUK):
        self.form = self.__class__.__name__
        self.styles = ''
        self.dbAlias = dcUK.dbAlias or getattr(self, 'dbAlias', '')

        self.urlForms = {}  # key = '-'.join([dbAlias, key, mode, multiPage, smartPhone])

        for a in ['jsCssUrl', 'jsCssUrlRead', 'jsCssUrlEdit', 'dbAlias', 'noCaching']:
            not getattr(self, a, None) and setattr(self, a, '')

        self.title = getattr(self, 'title', 'sova.online')

        if self.jsCssUrl:
            self.jsCssUrlRead = self.jsCssUrlEdit = setVersionFiles(self.jsCssUrl, BASE_DIR)
        else:
            self.jsCssUrlRead = setVersionFiles(self.jsCssUrlRead, BASE_DIR)
            self.jsCssUrlEdit = setVersionFiles(self.jsCssUrlEdit, BASE_DIR)

    # *** *** ***

    def getJsDoc(self, dcUK):
        '''
        вормирует словарь для отправки клиенту
        '''
        if not dcUK.doc:
            dcUK.doc = DC()
        dcUK.doc.form = dcUK.doc.form or self.form
        if dcUK.mode in ['edit', 'admin']:  # чтобы можно было установить новое значение в queryOpen
            do = {k: dcUK.doc[k] for k in dcUK.doc.keys()}  # save oldValues in 'do'

        dcUK.unid = dcUK.unid or dcUK.doc.unid or uuid.uuid4().hex
        self.queryOpen(dcUK)

        fv = {}  # fieldValues- KV для отправки клиенту
        for k, v in dcUK.doc.items():  # dcUK.doc - DC-object
            if 'PASSW' not in k:
                if type(v) == str:
                    fv[k] = v.replace('\u2028', ' ').replace('\u2029', ' ')
                else:
                    fv[k] = v
        ds = dict(
                fieldValues=fv,
                rsMode=dcUK.mode,
                dbAlias=dcUK.dbAlias or self.dbAlias,
                userName=dcUK.userName,
                unid=dcUK.unid,
                urlForm=self.getUrl(dcUK),
                cssJsUrl=self.getJsCssUrl(dcUK.mode),
                version=f'{versionString}',
            )
        if  dcUK.mode == 'new':
            ds['oldValues'] = {k: '' for k in fv}
        elif dcUK.mode in ['edit', 'admin']:  # чтобы можно было установить новое значение в queryOpen
            ds['oldValues'] = {k: do.get(k, '') for k in fv if do.get(k, '') != fv[k]}

        return json.dumps(ds, ensure_ascii=False).replace('</script', '<\/script')

    def queryOpen(self, dcUK): pass

    def querySave(self, dcUK): return True

    def afterSave(self, dcUK): return True

    def getData(self, dcUK): return '',  # вызывется из xhr для загрузки каких-либо данных

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
        key = '-'.join([dcUK.dbAlias or self.dbAlias, dcUK.key, dcUK.mode, dcUK.multiPage, dcUK.userAgent])

        if (not self.noCaching) and (key in self.urlForms):
            return self.urlForms[key]

        jsCss = str(self.getJsCssUrl(dcUK.mode))  # чтобы изменение js-css сбрасывали кэш
        if config.debug:
            pg = deepcopy(self.page(dcUK))
            pg = self.parseCell(pg)
            jsPage = json.dumps(pg, ensure_ascii=False, sort_keys=True)
            crc = crc32((jsPage + jsCss).encode(), 0)
        else:
            try:
                pg = deepcopy(self.page(dcUK))
                pg = self.parseCell(pg)
                jsPage = json.dumps(pg, ensure_ascii=False, sort_keys=True)
                crc = crc32((jsPage + jsCss).encode(), 0)
            except Exception as ex:
                err(f'{self.form}\n{ex}', cat='classPage.getUrl')
                return f'error-{self.form}-classPage.getUrl'

        if self.noCaching:
            urlForm = f'api.get/loadForm?{self.form}::{crc}'
        else:
            urlForm = f'api.getc/loadForm?{self.form}::{crc}'
        self.urlForms[key] = urlForm
        toWell(jsPage, 'form-json', f'{self.form}::{crc}')

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
            td = [*cell['field']]  # в td массив: название, тип[, справочник[, формула]]
            td[0] = td[0].upper()
            cell['field'] = td  # замена tuple to list

            if (td[1].startswith('lb') or td[1] == 'list') and type(td[2]) is not list and '|||' not in td[2]:  # поле со сложным списком с url
                url = td[2]
                if len(td) > 3:  # formula
                    if td[2]:  # если == '', значит строка url в td[3]
                        url += '|'
#                     mode = self.mode
#                     dbProfile = profile(self.dbAlias)
#                     dName = dbProfile.dName if dbProfile else ''
#                     url += eval(td[3])
                    del td[3]

                if td[2]:
                    ver = well('lsVersions', url) or well('lsVersions', url.replace('|', '¤'))
                    if ver:
                        url = f'api.getc/loadDropList?{url}::{ver}'  # api.getc - кэшируемый
                    else:
                        url = f'api.get/loadDropList?{url}'  # api.get - некэшируемый

                td[2] = url

        return cell

    # *** *** ***

    def getViewObject(self, className, dcVP, file='reviews'):
        key = f'{className.upper()}-{dcVP.dbAlias}-{dcVP.viewKey}'  # className - это не html, это pythonClass
        view = well('viewObjects', key)

        if not view or dcVP.noCaching:
            path = f'api.reviews.{file}'
            module = importlib.import_module(path)
            v = getattr(module, className, None)
            if v:
                dcVP.fieldName = className.upper()
                view = v(dcVP)
                toWell(view, 'viewObjects', key)
        return view

    # *** *** ***

