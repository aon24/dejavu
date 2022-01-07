# -*- coding: utf-8 -*- 
'''
Created on 2020.

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

class v_track(Page):
    def __init__(self, form):
        self.title = 'Курс'
        self.jsCssUrl = ['jsv?api/pages/v_track/v_track.js']
        self.dbAlias = 'tracks'
        super().__init__(form)

    
    def page(self, dcUK):
        fields1 = [
            labField('Название', 'trackTitle'),
            labField('Категория', 'cat', 'lbme', dropList=[]),
            labField('Статус', 'status', 'lbsd', dropList=['Подготовка', 'Ожидание', 'Обучение', 'Завершен']),
            [   label('Начало'),
                _div(children=_table(
                    [   {'rowStyle': {'margin': 0}},
                        _field('trackStart', 'dt', **style(width=95)),
                        label('окончание'), _field('trackEnd', 'dt', **style(width=95)),
                    ],)
                )
            ]
        ]
        
        fields2 = [
            [   label('Содержание'),
                _div(children=_table(
                    [   _btnD('создать таблицу', 'createTrack', name='btnCrt',
                            className='armBtn armBtnRed', **style(width=200)),
                        _btnD('открыть таблицу', 'xopen', f'new?form=t__list&dbAlias=courses.track_{dcUK.doc.docNo}', name='btnOpen',
                            className='toolbar-button', **style(width=200)),
                        label('', 20),
                        _field('trackContent', 'fd', **style(font='bold 16px Courier'))
                    ],)
                )
            ],
        ]
        
        fields3 = [
            labField('Куратор', 'curator', 'lbsd', dropList=[]),
            labField('E-mail', 'email', readOnly=1, **style('ttaStyle', font='normal 16px Courier')),
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
                    _div(wl=200, className='cellbg-green', name='buttons',
                         **style(borderSpacing=1), children=_table(*fields2)),
                    _div(wl=200, className='cellbg-green',
                         **style(borderSpacing=1), children=_table(*fields3)),
                    _div(wl=200, className='cellbg-green',
                        children=_table(labField('Комментарий', 'NOTES'),)
                    ),
                    _tab('cellbg-green', 140, [
                            ['Группы', _div('b1 Курсы')],
                    ]),
                ])
        ])
    
    def queryOpen(self, dcUK):
        dcUK.doc.trackContent = f"track_{dcUK.doc.docNo or '?'}"
        dcUK.doc.docNo_FD = f'Курс {dcUK.doc.docNo}'
        dcUK.doc.created_FD = f"{dcUK.doc.DT('created')}"

# *** *** ***

    def querySave(self, dcUK):
        if not dcUK.doc.docNo:
            dcUK.doc.docNo = snoDB(dcUK, 'inc')
            
        if dcUK.doc.createTrack:
            dbaTrack = f'COURSES/TRACK_{dcUK.doc.docNo}'
            try:
                del dcUK.doc._KV_['CREATETRACK']
                if not hasDB(dbaTrack):
                    createDB(dbaTrack)
                    dcUK.doc.trackCreated = now()
            except Exception as ex:
                err(f'{dbaTrack}\n{ex}', cat='createTrack')
        return True

# *** *** ***

    def afterSave(self, dcUK):
        toWell(None, f'viewloaded-{dcUK.dbAlias}-VIEWTRACKS') # VIEWTRACKS = view-field-name
        return True

# *** *** ***
