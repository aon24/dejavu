# -*- coding: utf-8 -*-
'''
Created on 2022.

@author: aon
'''
from tools.DC import toWell
from tools.common import rToL
from tools.dbToolkit.Book import filines, docFromDB, createDB
from api.formTools import style, _div, _field, docTitle, _tab, _mainPage, _img
from api.classPage import Page
from api.toolbars import toolbar
from api.sno import snoDB

from .profile import profile
from .training import training

import json

# *** *** ***


class lk(Page):

    def __init__(self, form):
        self.title = 'ЛК'
        self.jsCssUrl = ['jsv?api/pages/lk/lk.js']
        self.dbAlias = 'people'
        super().__init__(form)

    # *** *** ***

    def page(self, dcUK):
        cn = 'pagePreview' if dcUK.mode == 'preview' else 'page'
        # , height='100vh'
        return _mainPage(
            **style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden'),
            focus='fullName', children=[
                toolbar.o(dcUK.mode),
                _div(**style(maxWidth=750, margin='auto', height='calc(100vh - 110px)'), className=cn, children=[

                    docTitle(
                            _field('fio_FD', 'fd'),
                            WLR='25%',
                            left=_field('created_FD', 'fd', **style(font='normal 12px Arial')),
                            right=_field('modified_FD', 'fd', **style(font='normal 12px Arial')),
                    ),

                    _tab(140, [
                            ['Профиль', profile(dcUK)],
                            ['Курсы', training(dcUK)],
                            ['Мои ответы', _div('b1 Рассылки')],
                            ['Консультации', _div('b1 Консультации')],
                            ['Оплата', _div('b1 Платежи')],
                    ]),
                ])
        ])

    # *** *** ***

    def queryOpen(self, dcUK):
        d = dcUK.doc
        d.created_FD = d.DT('created')
        d.modified_FD = d.DT('modified')
        d.fio_FD = d.FULLNAME or 'Студент'
        d._tabHeader = 0

        arr = filines(d, 'FILES1_')
        if arr:
            arr = [a for a in arr if 'image' in a[3]]  # a[3] - mimetype, a[5] - датаЗаписиВбазу_датаФайла
            if arr:
                a = sorted(arr, key=lambda x: x[5], reverse=True)[0]  # берем последний записанный в базу
                src = '&'.join([
                        f'download/{a[0]}?dbAlias={dcUK.dbAlias}',
                        f'unid={dcUK.unid}',
                        f"idbl={a[6].split('_')[1]}",  # название поля FILES1_idbl
                        f'f_store={a[0]}',
                        f'fzip={a[1]}',
                        f'mimetype={a[3]}',
                        f'length={a[4]}'
                    ])
                d.avatar_FD = json.dumps(_img(src, width='100%', height='100%'))

    # *** *** ***

    def querySave(self, dcUK):
        d = dcUK.doc
        if not d.docNo:
            d.docNo = snoDB(dcUK, 'inc')

        d.fio = f'{d.lastName} {d.firstName} {d.MiddleName}'.strip()
        if not d.dbAlias:
            f = rToL(d.lastName or d.firstName) or 'z'
            i = rToL(f'{d.firstName}')[:1]
            o = rToL(f'{d.MiddleName}')[:1]
            d.dbAlias = f'STUDENTS/{f[0]}.{f}_{i}_{o}_{d.docNo}'
            createDB(d.dbAlias)
        return True

    # *** *** ***

    def afterSave(self, dcUK):
        toWell(None, f'viewloaded-{dcUK.dbAlias}-VIEWPEOPLE')  # viewPeople = view-field-name
        return True

    # *** *** ***

    def getData(self, dcUK):
        if not docFromDB(dcUK):
            return '["1"]', 'application/json'

        return '["urok1", "urok1", ]', 'application/json'

# *** *** ***

