# -*- coding: utf-8 -*- 
'''
Created on 7 apr 2018

@author: aon
'''
from tools.dbToolkit.Book import allFromDB
from tools.DC import DC, well, toWell
from api.formTools import _div, style, navigator, viewToolbar

# *** *** ***

class Review(object):
    def __init__(self, dcVP):
        self.cats = dcVP.get('cats', {})
        self.dcVP = dcVP
        
        self.sortBy = getattr(self, 'sortBy', '')
        self.dir_ = getattr(self, 'dir_', '')
        self.reverse = getattr(self, 'reverse', False)
        
        self.DBC = {} # documents by category
        self.subCats = {}

    # ***
    
    def make(self):
        v = self.dcVP
        fi = {'field': (v['fieldName'], 'view'), 'attributes': {}, 'fieldProps': {}}
        
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
        
        fi['fieldProps']['dbAlias'] = v['dbAlias']
        fi['fieldProps']['form'] = v.get('form', '')
        fi['fieldProps']['addClassName'] = v.get('addClassName', 'mRowPM')
        fi['fieldProps']['limit'] = v.get('limit', 0)
        fi['fieldProps']['refs'] = v.get('refs')
        
        isNav = v.get('isNav', True)
        isTlb = v.get('isTlb', True)
        chb = v.get('checkBox')
        btn = v.get('button')

        if 'forChildStyle' in v:
            fi['attributes']['style'].update({'display':'table-cell'})
            v['forChildStyle'].update({'display':'table-cell'})
            viewArea = _div(**style(width='100%', display='table', tableLayout='fixed'), children=[
                            fi,
                            _div(id='forChild', style=v['forChildStyle']),
                        ])
        else:
            viewArea = fi
        return [
            isNav and navigator(DC(v)),
            _div( style=divStyle, children=[
                isTlb and viewToolbar(v['form'], v['dbAlias'], chb, btn),
                viewArea
            ] ),
        ]
    
    # ***
    
    def paging(self, dcUK):
        return {'mainDocs': []}

    # ***

    def viewReload(self, dcUK):
        c_s = f'{dcUK.cat}|{dcUK.subCat}'
        keyWell = f"viewloaded-{dcUK.dbAlias}-{self.dcVP['fieldName']}"
        if well(keyWell):
            return self.DBC.get(c_s, [])

        ls = allFromDB(dcUK.dbAlias, dcUK.dir_ or self.dir_) or []
        
        self.loadCats(ls)

        for c in self.DBC:
            cat = c.partition('|')[0]
            dcCat = self.cats.get(cat)
            if dcCat and dcCat.sort:
                if dcCat.sort == 'docNo':
                    self.DBC[c] = sorted(self.DBC[c], key=lambda d: d.F(dcCat.sort).rjust(9), reverse=dcCat.reverse)
                else:
                    self.DBC[c] = sorted(self.DBC[c], key=lambda d: d.F(dcCat.sort), reverse=dcCat.reverse or False)
        
        toWell(True, keyWell)

        return self.DBC.get(c_s, [])
        
        # ***
        
    def loadCats(self, ls):
        self.DBC = {}
        self.subCats = {}
        

        for cat, dc in self.cats.items():
            self.subCats[cat] = []
            if dc.fixedSubCats: # в dc.fixedSubCats словарь фиксированных подкатегорий
                for sc in dc.fixedSubCats:
                    self.subCats[cat].append(sc.subCat)
        for d in ls:
            for cat, dc in self.cats.items():
                if dc.fixedSubCats:
                    if eval(dc.condition):
                        key = f'{cat}|'
                        self.DBC[key] = self.DBC.get(key, [])
                        self.DBC[key].append(d)
                        for fix in dc.fixedSubCats:
                            if eval(fix.condition):
                                key = f'{cat}|{fix.subCat}'
                                self.DBC[key] = self.DBC.get(key, [])
                                self.DBC[key].append(d)
                elif eval(dc.condition):
                    key = f'{cat}|'
                    self.DBC[key] = self.DBC.get(key, [])
                    self.DBC[key].append(d)
                    if eval(dc.condition):
                        subCat = eval(dc.subCat)
                        if subCat not in self.subCats[cat]: 
                            self.subCats[cat].append(subCat)
                        key = f'{cat}|{subCat}'
                        self.DBC[key] = self.DBC.get(key, [])
                        self.DBC[key].append(d)
        
        # for c in self.subCats:
            # print('------self.subCats--------------', c)

    # ***
        
    def loadCatsOld(self, ls):
        self.DBC = {'Все|': []}
        self.subCats = {}
        for d in ls:
            self.DBC['Все|'].append(d)
            for cat, fName in self.cats.items():
                if fName and type(fName) == str:
                    if fName[0] == '=': # formula
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

