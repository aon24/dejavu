# -*- coding: utf-8 -*-
'''
Created on 2020.

@author: aon
'''
from tools.DC import toWell
from api.formTools import style, _div, _field, labField, _table, docTitle, label, _tab, _mainPage
from api.classPage import Page
from api.toolbars import toolbar

# *** *** ***


class w_list(Page):

    def __init__(self, form):
        self.title = 'Справочник'
        self.jsCssUrl = ['jsv?api/pages/w_list/w_list.js']
        self.dbAlias = 'well'
        super().__init__(form)

    def page(self, dcUK):
        fields1 = [
            labField('Название', 'listName'),
            labField('для курсов', 'tracks'),
        ]
        fields2 = [
            labField('Список', 'list'),
            labField('Формула', 'formula', **style(fontFamily='Courier')),
        ]

        cn = 'pagePreview' if dcUK.mode == 'preview' else 'page'

        return _mainPage(
            **style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden', height='100vh'),
            focus='fullName', children=[
                toolbar.o(dcUK.mode),
                _div(**style(width=800, margin='auto'), className=cn, children=[

                    docTitle(
                            'Общий справочник',
                            WLR='25%',
                            left=_field('created_FD', 'fd', **style(font='normal 12px Arial')),
                            right=_field('modified_FD', 'fd', **style(font='normal 12px Arial')),
                    ),

                    _div(wl=200, className='cellbg-green', **style(borderSpacing=1), children=_table(*fields1)),
                    _div(wl=200, className='cellbg-green', **style(borderSpacing=1), children=_table(*fields2)),
                    _div(wl=200, className='cellbg-green',
                        children=_table(labField('Комментарий', 'NOTES'),)
                    ),
                    _div(wl=200, className='cellbg-green', children=
                        labField('тип', 'system', 'chb', ['SYSTEM'], className='label')
                    ),
                ])
        ])

    # *** *** ***

    def queryOpen(self, dcUK):
        dcUK.doc.created_FD = dcUK.doc.DT('created')
        dcUK.doc.modified_FD = dcUK.doc.DT('modified')

    # *** *** ***

    def querySave(self, dcUK):
        dcUK.doc.dir = dcUK.doc.dir or 'L'
        return True

    # *** *** ***

    def afterSave(self, dcUK):
        toWell(None, f'viewloaded-{dcUK.dbAlias}-VIEWWELL')  # view = view-field-name
        return True

# *** *** ***
