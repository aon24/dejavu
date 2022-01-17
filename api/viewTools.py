# -*- coding: utf-8 -*- 
'''
Created on 2022

@author: aon
'''
from api.formTools import _btnD

# *** *** ***
def docNoPreview(docNo, dbAlias, d, width=140):
    title = docNo.split()[0]
    param = f"{dbAlias}&{d.unid}&_{title}_&{d.form or 'info'}"
    return _btnD(docNo, 'previewNew', param, title='быстрый просмотр', s2=1,
            className='mCell docNo', br='p',
            style={'width': width, 'letterSpacing': 1, 'font': 'normal 14px Arial'})
