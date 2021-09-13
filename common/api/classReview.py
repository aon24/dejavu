# -*- coding: utf-8 -*- 
'''
Created on 7 apr 2018

@author: aon
'''
from common.common import well, toWell
from common.first import err
from .formTools import _div
from .toolbars import reviewToolbar

import importlib

# *** *** ***

def viewDiv(fieldName, reviewClass, style={}, toolbar=None, newDoc='', **par):
    fieldName = fieldName.upper()
    fi = {'field': (fieldName, 'view'), 'attributes': {}, 'fieldProps': {'reviewClass': reviewClass}}
    
    divStyle = {'overflow': 'hidden auto', 'display': 'block'}
    divStyle.update(style)
    
    for k, v in par.items():
        if k in ['name', 'id', 'className']:
            fi['attributes'][k] = v
        else:
            fi['fieldProps'][k] = v # стиль вида задается параметром viewStyle={'background': '#fff'...} или **style('viewStyle', background='#fff')

    dbAlias = fi['fieldProps'].get('dbAlias')
    if not dbAlias:
        s = f'dbAlias не указан для вида "{reviewClass}"'
        err(s, cat='viewTools.py.viewDiv')
        return _div(f'viewTools.py.viewDiv: {s}')

    s = f'{reviewClass}-{fieldName}-{dbAlias}'
    view = well('reviewClass', s)
    if not view:
        view = makeReviewClass(fieldName, reviewClass, dbAlias, fi['fieldProps'].get('viewAlias'))
    if not view:
        s = f'not review for reviewClass "{reviewClass}"'
        err(s, cat='classReview.py.viewDiv')
        return _div(f'viewTools.py.viewDiv: {s}')

    ls = []
    if toolbar:
        ls.append(reviewToolbar(toolbar, dbAlias=dbAlias, newDoc=newDoc))
    if hasattr(view, 'header'):
        ls.append(view.header())
        
    ls.append(_div( style=divStyle, children=[fi] ))
    return _div(children=ls)

# *** *** ***

def makeReviewClass(fieldName, reviewClass, dbAlias, viewAlias):
    path = {'va': 'appDesign'}.get(reviewClass.partition('_')[0], 'common')
    path = f"{path}.reviews.{reviewClass}.{reviewClass}"
    try:
        module = importlib.reload(importlib.import_module(path))
        view = getattr(module, reviewClass)(fieldName, reviewClass, dbAlias, viewAlias)
        toWell(view, 'reviewClass', reviewClass + '-' + fieldName + '-' + dbAlias)
        return view
    except Exception as ex:
        err(f'reviewClass "{path}"\n{ex}', cat='makeReviewClass')

# *** *** ***
# *** *** ***

class Review(object):
    def __init__(self, fieldName, reviewClass, dbAlias, reviewAlias=None):
        self.reviewClass = reviewClass
        self.fieldName = fieldName
        self.dbAlias = dbAlias

    # ***

    def paging(self, dcUK):
        return {'mainDocs': []}

    
# *** *** ***

