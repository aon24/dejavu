# -*- coding: utf-8 -*- 
'''
Created on 2022.

@author: aon
'''
from tools.DC import toWell
from api.formTools import style, _div, _field, labField, _table, docTitle, label, _tab, _mainPage
from api.classPage import Page
from api.toolbars import toolbar

# *** *** ***

class lk(Page):
    def __init__(self, form):
        self.title = 'Студент'
        self.jsCssUrl = ['jsv?api/pages/lk/lk.js']
        self.dbAlias = 'people'
        super().__init__(form)

    
    def page(self, dcUK):
        fields = [
            labField('Фамилия Имя Отчество', 'fullName'),
            labField('e-mail', 'email', **style('ttaStyle', font='normal 16px Courier')),
            labField('телефон', 'phone'),
            [   label('город'),
                _div(children=_table(
                    [   {'rowStyle': {'margin': 0}},
                        _field('city'),
                        label('пол', 50), _field('gender', 'lbsd', ['женский', 'мужской', 'паркет', 'ламинат', 'еще не решил(а)'], placeholder='Список'),
                        label('день рождения', 140), _field('birthday', 'dt', **style(width=128))
                    ],)
                )
            ],
            [_div(children=[
             _field('status', 'chb3', ['\xa0 студент\xa0|студент', 'сотрудник'], noEmpty=1, **style(letterSpacing=1))]) 
            ],
            # labField('входит в группы', 'groups'),
            labField('Приветствие, обращение', 'greeting'),
            [   label('логин'),
                _div(children=_table(
                    [   {'rowStyle': {'margin': 0}},
                        _field('Login'),
                        label('пароль', 100), _field('Password')
                    ],)
                )
            ],
            labField('схема доступа', 'acrScheme'),
        ]

        cn = 'pagePreview' if dcUK.mode == 'preview' else 'page'

        return _mainPage(
            **style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden', height='100vh'),
            focus='fullName', children=[
                toolbar.o(dcUK.mode),
                _div(**style(width=800, margin='auto'), className=cn, children=[
                    
                    docTitle(
                            'Студент',
                            WLR='25%',
                            left=_field('created_FD', 'fd', **style(font='normal 12px Arial')),
                            right=_field('modified_FD', 'fd', **style(font='normal 12px Arial')),
                    ),
                    
                    _div(wl=200, className='cellbg-green', **style(borderSpacing=1), children=_table(*fields)),
                    _div(wl=200, className='cellbg-green',
                        children=_table(labField('Комментарий', 'NOTES'),)
                    ),
                    _tab('cellbg-green', 140, [
                            ['Курсы', _div('b1 Курсы')],
                            ['Консультации', _div('b1 Консультации')],
                            ['Общение', _div('b1 Общение')],
                            ['Рассылки', _div('b1 Рассылки')],
                            ['Платежи', _div('b1 Платежи')],
                    ]),
                ])
        ])
    
    def queryOpen(self, dcUK):
        dcUK.doc.created_FD = dcUK.doc.DT('created')
        dcUK.doc.modified_FD = dcUK.doc.DT('modified')
    
# *** *** ***

    def afterSave(self, dcUK):
        toWell(None, f'viewloaded-{dcUK.dbAlias}-VIEWPEOPLE') # viewPeople = view-field-name
        return True

# *** *** ***
