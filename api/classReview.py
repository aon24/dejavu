# -*- coding: utf-8 -*-
'''
Created on 7 apr 2018

@author: aon
'''
from tools.dbToolkit.Book import allFromDB
from tools.DC import DCC, well, toWell
from api.formTools import _div, style
from api.viewTools import navigator, viewToolbar

# *** *** ***


class Review(object):

    def __init__(self, dcVP):
        self.cats = dcVP.cats or {}
        self.dcVP = dcVP

        self.sortBy = getattr(self, 'sortBy', '')
        self.dir_ = getattr(self, 'dir_', '')
        self.reverse = getattr(self, 'reverse', False)

        self.DBC = {}  # documents by category: {'По помещениям|': [<tools.DC.DC object at 0x03215B30>, ...]}
        self.subCats = {}

    # ***

    def make(self):
        v = self.dcVP
        fi = {'field': (v.fieldName, 'view'), 'attributes': {}, 'fieldProps': {}}

        divStyle = dict(overflow='hidden', display='table-cell', background='#fff')
        viewStyle = dict(height='calc(100vh - 50px)', background='#eff')

        for k, val in v.items():
            if k == 'divStyle':
                divStyle.update(val)
            elif k == 'viewStyle':
                viewStyle.update(val)
            elif k in ['name', 'id', 'className']:
                fi['attributes'][k] = val

        fi['attributes']['style'] = viewStyle
        fi['fieldProps']['dbAlias'] = v.dbAlias
        fi['fieldProps']['addClassName'] = v.addClassName or 'mRowPM'
        fi['fieldProps']['limit'] = v.limit or 0
        fi['fieldProps']['refs'] = v.refs
        fi['fieldProps']['viewKey'] = v.viewKey
        fi['fieldProps']['catDir'] = v.catDir

        isNav = v.isNav or True
        isTlb = v.isTlb or True
        chb = v.checkBox
        btn = v.button

        if v.forChildStyle:
            fi['attributes']['style'].update({'display':'table-cell'})
            v.forChildStyle.update({'display':'table-cell'})
            viewArea = _div(**style(width='100%', display='table', tableLayout='fixed'), children=[
                            fi,
                            _div(id='forChild', style=v.forChildStyle),
                        ])
        else:
            viewArea = fi

        form = v.form or ''
        if v.newFormKey:  # задать параметр в навигаторе для кнопки new
            form += f'&key={v.newFormKey}'

        for cat, dc in self.cats.items():
            self.subCats[cat] = []
            if dc.fixedSubCats:  # в dc.fixedSubCats словарь фиксированных подкатегорий
                for sc in dc.fixedSubCats:
                    self.subCats[cat].append(sc.subCat)

        return [
            isNav and navigator(v),
            _div(style=divStyle, children=[
                isTlb and viewToolbar(form, v.dbAlias or '', chb, btn),
                viewArea
            ]),
        ]

    # ***

    def paging(self, dcUK):
        return {'mainDocs': []}

    # ***

    def viewReload(self, dcUK):
        c_s = f'{dcUK.cat}|{dcUK.subCat}'
        keyWell = f"viewloaded-{dcUK.dbAlias}-{self.dcVP.fieldName}"
        if well(0 and keyWell):
            return self.DBC.get(c_s, [])

        ls = allFromDB(dcUK.dbAlias, dcUK.dir_ or self.dir_) or []
        self.loadCats(ls)

        def sortByNum(num):  # вместо d[dcCat.sort].rjust(9)
            try:
                return float(num or 0)
            except:
                return 0
        for c in self.DBC:
            cat = c.partition('|')[0]
            dcCat = self.cats.get(cat)

            if dcCat and dcCat.sort:
                if dcCat.sort == 'docNo':
                    self.DBC[c] = sorted(self.DBC[c], key=lambda d: sortByNum(d[dcCat.sort]), reverse=not not dcCat.reverse)
                else:
                    self.DBC[c] = sorted(self.DBC[c], key=lambda d: d[dcCat.sort], reverse=not not dcCat.reverse)

        toWell(True, keyWell)

        return self.DBC.get(c_s, [])

        # ***

    def loadCats(self, ls):
        self.DBC = {}
        self.subCats = {}

        for cat, dc in self.cats.items():
            self.subCats[cat] = []
            if dc.fixedSubCats:  # в dc.fixedSubCats словарь фиксированных подкатегорий
                for sc in dc.fixedSubCats:
                    self.subCats[cat].append(sc.subCat)
        for d in ls:
            for cat, dc in self.cats.items():
                if not eval(dc.condition or True):  # условие вида, т.е. условие отбора для всех верхних кнопок
                    continue

                key = f'{cat}|'
                self.DBC[key] = self.DBC.get(key, [])
                self.DBC[key].append(d)

                if dc.fixedSubCats:
                    for fix in dc.fixedSubCats:
                        if eval(fix.condition):
                            key = f'{cat}|{fix.subCat}'
                            self.DBC[key] = self.DBC.get(key, [])
                            self.DBC[key].append(d)

                if dc.byFieldSubCats:
                    dynamoCat = eval(dc.byFieldSubCats) or 'не задано'
                    if dynamoCat not in self.subCats[cat]:  # subCats нужны, чтобы вытащить в
                        self.subCats[cat].append(dynamoCat)  # навигатор список с помощью loadSubCats
                    key = f'{cat}|{dynamoCat}'
                    self.DBC[key] = self.DBC.get(key, [])
                    self.DBC[key].append(d)

    # ***

    def loadCatsOld(self, ls):
        self.DBC = {'Все|': []}
        self.subCats = {}
        for d in ls:
            self.DBC['Все|'].append(d)
            for cat, fName in self.cats.items():
                if fName and type(fName) == str:
                    if fName[0] == '=':  # formula
                        fi = eval(fName[1:])
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

    # *** *** ***

# *** *** ***

