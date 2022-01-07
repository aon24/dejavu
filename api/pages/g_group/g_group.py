# -*- coding: utf-8 -*- 
'''
Created on 2020.

@author: aon
'''
from tools.DC import well, toWell
from api.formTools import style, _div, _field, labField, _table, docTitle, label, _tab, _mainPage
from api.classPage import Page
from api.toolbars import toolbar

# *** *** ***

class g_group(Page):
    def __init__(self, form):
        self.title = 'Группа'
        self.jsCssUrl = ['jsv?api/pages/g_group/g_group.js']
        self.dbAlias = 'groups'
        super().__init__(form)

    
    def page(self, dcUK):
        fields = [
            labField('Название группы', 'groupName'),
        ]

        if dcUK.mode == 'preview':
            cn = 'pagePreview' 
        elif dcUK.mode != 'admin':
            cn = 'page'
        else:
            cn = ''
        
        _docTitle = docTitle(
            'Группа',
            WLR='25%',
            left=_field('created_FD', 'fd', **style(font='normal 12px Arial')),
            right=_field('modified_FD', 'fd', **style(font='normal 12px Arial')),
        )

        tracks = _field('tracks', 'lbmd', dropList=[]) #well('tracks') or 
        # mailings = _field('mailings', 'tx', readOnly=1)
        mailings = _field('mailings', 'table', btn=[4, '55mm'], ttaStyle={'padding': 0, 'background': '#fff'}),

        # ***

        # h = '100%' if dcUK.mode == '' else '100%'

        return _div(className='q',
            **style(backgroundImage='url(/image?24x24LB.png)', overflow='hidden', height='calc(100vh - 50px)'),
            focus='groupName', children=[
                toolbar.o(dcUK.mode),
                _div(**style(width=800, margin='auto'), className=cn, children=[
                    _docTitle,
                    
                    _div(wl=200, className='cellbg-green', **style(borderSpacing=1), children=_table(*fields)),
                    _div(wl=200, className='cellbg-green',
                        children=_table(labField('Комментарий', 'NOTES'),)
                    ),
                    _tab('cellbg-green', 140, [
                            ['Курсы', tracks],
                            ['Рассылки', mailings],
                    ]),
                ])
        ])
    
    def queryOpen(self, dcUK):
        dcUK.doc.created_FD = dcUK.doc.DT('created')
        dcUK.doc.modified_FD = dcUK.doc.DT('modified')
        dcUK.doc.mailings = '''1
2
3
4
45'''
    
# *** *** ***

    def afterSave(self, dcUK):
        toWell(None, f'viewloaded-{dcUK.dbAlias}-VIEWGROUPS') # viewPeople = view-field-name
        return True

# *** *** ***
