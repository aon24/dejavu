# -*- coding: utf-8 -*-
'''
Created on 2022

@author: aon
'''
from api.formTools import _btnD, _field, label, style, _div, _table, _img

# *** *** ***


def docNoPreview(docNo, dbAlias, d, width=140, br=1):
    title = f'{docNo} _ '.split()[0]
    param = f"dbAlias={dbAlias}&unid={d.unid}&title=_{title}_&form={d.form or 'info'}&mode=preview"
    return _btnD(docNo, 'previewNew', param, title='быстрый просмотр', s2=1,
            className='mCell docNo', br=br,
            style={'width': width, 'letterSpacing': 1, 'font': 'normal 14px Arial'})

# *** *** ***


def navigator(dcVP, maxHeight=500):
    if dcVP.userAgent == 'mobile':
        width = 85
    else:
        width = 170

    if dcVP.fieldName:
        key = f'view={dcVP.fieldName}-{dcVP.dbAlias}-{dcVP.viewKey}'  # api.get/loadSubCats?... передается в classReview
    else:
        key = f'form={dcVP.form}'  # api.get/loadSubCats?... передается в classPage

    if dcVP.repository:
        repository = [
            label('repository'),
            _field('repository', 'tx', readOnly=1, **style(font='normal 11px/1.4 Verdana')),
            label()
        ]
    else:
        repository = []

    cat = _field('cat', 'list', list(dcVP.cats.keys()), alias=1, className='navBtn', listItemClassName='rsvTop')

    # при вызове doc.changeDropList('subCat') в url подставится значение поля "CAT" вместо {FIELD}
    # при вызове doc.changeDropList('subCat', 'qq') в url подставится строка "qq" вместо {FIELD}
    subCat = _field('subCat', 'list', f'CAT|||api.get/loadSubCats?{key}&cat={{FIELD}}',
        **style(maxHeight=maxHeight, overflow='hidden auto', width='90%', margin='auto', display='block'),
        saveAlias=1, evenColor='#f4f8ff', default=-1)

    if dcVP.dubl:
        return _div(**style(width=width * 2, display='table-cell'), children=[
            _div(**style(display='table', width='100%'), children=[
                _div(**style(display='table-cell', width='50%', position='relative'), children=[
                    *repository,
                    cat,
                    dcVP.downButtons,
                ]),
                _div(**style(display='table-cell', width='50%'), children=[
                    subCat
                ])
            ])
        ])
    else:
        return _div(**style(width=width, display='table-cell', position='relative'), children=[
            *repository,
            cat,
            subCat,
            dcVP.downButtons,
        ])

# *** *** ***


def btn3cix(dbAlias, unid, title):  # три кнопки в каждой строке в виде: скопировать, показать поля, удалить
    dba = f'dbAlias={dbAlias}&unid={unid}'
    return _div(className='mCell', **style(width=110, verticalAlign='middle', textAlign='right'),
            children=[
                _btnD('C', 'xcopy', dba, title='скопировать документ', className='forView fvc'),
                _btnD('i', 'previewNew', f'{dba}&form=info&title={title}&mode=preview', title='поля документа', className='forView fvi'),
                _btnD('\xd7', 'toArchive', dba, title='убрать в архив', className='forView fva'),
            ])

# *** *** ***


def viewToolbar(form, dbAlias, checkBox=None, button=None):

    return _div(**style(padding=3, background='#dfe', border='0 solid #eee', borderBottomWidth=2),
        children=_table([style('rowStyle', width='100%', borderSpacing='5px 0'),
            _div(**style(width=30), children=
            [
                _btnD('', 'xopen', f'new?form={form}&dbAlias={dbAlias}', className=' ',
                      children=[_img(title='создать новый документ', **style(width=25), src='image?new.png')]
                )
            ]),
            checkBox,
            label('поиск', **style(width=50)),
            _div(**style(verticalAlign='middle'), children=
                [_field('search_FD', **style(margin='auto', letterSpacing=1))]),
            _btnD('', 'search', f'api.get/search?dbAlias={dbAlias}', className='search',
                title='искать', children=
                [_img(**style(width=20), src='image?search.png')]),
            button,
        ])
    )

# *** *** ***
