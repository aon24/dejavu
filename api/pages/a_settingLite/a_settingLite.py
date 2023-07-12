# -*- coding: utf-8 -*-
'''
Created on 2020.

@author: aon
'''
from api.formTools import style, _div, _field, label, _btnD, _table, _span, labField, _br, _tab, labell, _teg
from api.classPage import Page

# *** *** ***


class a_settingLite(Page):

    def __init__(self, form):
        self.title = 'Setting'
        self.jsCssUrl = ['jsv?api/pages/a_settingLite/a_settingLite.js']

        self.dbAlias = 'db_pages_l'
        super().__init__(form)

    def page(self, dcUK):
        return _div('qq', className='setting-page', children=[
            _div(name='setArrow', children=self.setArrow()),
        ])

# *** *** ***

    def setArrow(self):

        def tx_1_2(lcr):
            return [
                _div(className='tx-1'),
                _div(className=f'tx-2-{lcr}'),
                _div(className='tx-1'),
                _div(className=f'tx-2-{lcr}'),
                _div(className='tx-1'),
            ]

        return [
            _div(className='setting-line'),

            _field('textAlign', 'band', [
                _div(**style(width=30, height=30, margin='auto'), children=tx_1_2('l')),
                _div(**style(width=30, height=30, margin='auto'), children=tx_1_2('c')),
                _div(**style(width=30, height=30, margin='auto'), children=tx_1_2('q')),
                _div(**style(width=30, height=30, margin='auto'), children=tx_1_2('r')),
                ], **style(width='80%', margin='auto', borderSpacing='5px')),
        ]

