# -*- coding: utf-8 -*- 
'''
Created on 2022.

@author: aon
'''

# *** *** ***

from api.formTools import _span, style, _div, _field, label, _lf, _btnD

# *** *** ***

def training(dcUK):
    courses = ['Марафон "Быстрый старт"', 'Просто старт']
    key = 'form=lk&subcats=lessons&dbAlias=&unid='
    
    width = 85 if dcUK.userAgent == 'mobile' else 170
    maxHeight = 'calc(100vh - 180px)'
    
    cat = _field('cat_FD', 'list', courses, alias=1, className='navBtn', listItemClassName='rsvTop')

    subCat = _field('subCat_FD', 'list', f'CAT_FD|||api.get/getData?{key}&cat={{FIELD}}',
        **style(maxHeight=maxHeight, overflow='hidden auto', width='90%', margin='auto', display='block'),
        saveAlias=1, evenColor='#f4f8ff', default=-1)
    
    return _div(children=[
                    cat, subCat,
                ])
# *** *** ***