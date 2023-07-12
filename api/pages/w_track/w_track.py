# -*- coding: utf-8 -*-
'''
Created on 2022.

@author: aon
'''
from tools.first import err
from tools.DC import toWell
from tools.common import now
from tools.dbToolkit.Book import hasDB, createDB
from api.formTools import style, _div, _field, labField, _table, docTitle, label, _tab, _mainPage, _btnD
from api.classPage import Page
from api.toolbars import toolbar
from api.sno import snoDB

# *** *** ***


class w_track(Page):

    def __init__(self, form):
        self.title = 'Курс'
        self.jsCssUrl = ['jsv?api/pages/w_track/w_track.js']
        self.dbAlias = 'well'
        super().__init__(form)

    def page(self, dcUK):
        fields1 = [
            labField('Название', 'trackTitle'),
            labField('Категория', 'cat', 'lbme', dropList=[]),
            labField('Статус', 'status', 'lbsd', dropList=['Подготовка', 'Ожидание', 'Обучение', 'Завершен']),
            [   label('Начало'),
                _div(children=_table(
                    [   {'rowStyle': {'margin': 0}},
                        _field('trackStart', 'dt'),
                        label('окончание', 'auto'),
                        _field('trackEnd', 'dt'),
                    ],)
                )
            ]
        ]

        fields2 = [
            [   label('Содержание'),
                _div(children=_table(
                    [
                        _btnD('открыть таблицу', 'xopen', f'new?form=t__list&dbAlias={dcUK.doc.dbAlias}',
                            className='toolbar-button', **style(width=200)),
                        label('', 20),
                        _field('dbAlias', 'fd', **style(font='normal 16px Courier', color='#555'))
                    ],)
                )
            ],
        ]

        fields3 = [
            labField('Куратор', 'curator', 'lbsd', dropList=[]),
            labField('E-mail', 'email', readOnly=1, **style(font='normal 16px Courier')),
            labField('Телефон', 'phone', readOnly=1),
        ]

        cn = 'pagePreview' if dcUK.mode == 'preview' else 'page'

        return _mainPage(
            **style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden', height='100vh'),
            focus='trackTitle', children=[
                toolbar.o(dcUK.mode),
                _div(**style(width=800, margin='auto'), className=cn, children=[

                    docTitle(
                            _field('docNo_fd', 'fd'),
                            WLR='25%',
                            left='',
                            right=_field('created_FD', 'fd', **style(font='normal 12px Arial')),
                    ),

                    _div(wl=200, className='cellbg-green',
                         **style(borderSpacing=1), children=_table(*fields1)),
                    _div(wl=200, className='cellbg-green', name='dbAlias',
                         **style(borderSpacing=1), children=_table(*fields2)),
                    _div(wl=200, className='cellbg-green',
                         **style(borderSpacing=1), children=_table(*fields3)),
                    _div(wl=200, className='cellbg-green',
                        children=_table(labField('Комментарий', 'NOTES'),)
                    ),
                    _tab(140, [
                            ['Группы', _div('b1 Курсы')],
                    ]),
                ])
        ])

    # *** *** ***

    def queryOpen(self, dcUK):
        dcUK.doc.docNo_FD = f'Курс {dcUK.doc.docNo}'
        dcUK.doc.created_FD = f"{dcUK.doc.DT('created')}"

    # *** *** ***

    def querySave(self, dcUK):
        d = dcUK.doc
        d.docNo = d.docNo or snoDB(dcUK, 'inc')
        d.dir = d.dir or 'T'

        if not d.dbAlias:
            d.dbAlias = f'COURSES/track_{d.docNo}'
            if hasDB(d.dbAlias):
                err(f'Table {d.dbAlias} already exists', cat='w_track-querySave')
                return
            createDB(d.dbAlias)
        return True

    # *** *** ***

    def afterSave(self, dcUK):
        toWell(None, f'viewloaded-{dcUK.dbAlias}-VIEWTRACKS')  # VIEWTRACKS = view-field-name
        return True
# *** *** ***

