# -*- coding: utf-8 -*- 
'''
Created on 2020.

@author: aon
'''
from tools.DC import DC
from api.formTools import style, _div, _mainPage
from api.classPage import Page

# *** *** ***

class g__groups(Page):
    def __init__(self, dcUK):
        self.title = 'Группы'
        self.jsCssUrl = [
            'jsv?api/pages/g__groups/g__groups.js',
            'jsv?api/react/view.css',
        ]
        self.subCats = {}
        self.DBC = {}
        self.noCaching = False
        self.dbAlias = 'groups'
        self.cats = {
            'Группы': DC(condition='True', sort='groupName', reverse=False,
                fixedSubCats=[
                    DC(subCat='Общие', condition='not d.tracks'),
                    DC(subCat='Служебные', condition='d.system'),
                ]
            ),
            'По\xa0номеру': DC(condition='True', sort='docNo', reverse=True,
                fixedSubCats=[
                    DC(subCat='Общие', condition='not d.tracks'),
                    DC(subCat='Служебные', condition='d.system'),
                ]
            ),
            'По\xa0курсам': DC(condition='d.tracks', sort='groupName', subCat='d.tracks'),
        }
        
        super().__init__(dcUK)
    
    def page(self, dcUK):
        '''
            cats=self.cats, - кнопки навигатора 
            isNav = False, # показать навигатор (default True)
            isTlb = False, # показать тулбар (default True)
            divStyle=dict(background='#fff'), # стиль div, в котором будет вид, включая тулбар
            forChildStyle = dict(height='calc(100vh - 50px)', background='#fff'), - div для preview документа 
            
            form = 'g_group', - кнопка создать с формой
            dbAlias = dcUK.dbAlias,

            viewStyle=dict(width=200), # стиль вида
            limit = 10, - порция документов при пайджинге (50 по умолчанию)
            addClassName = 'mRowPM', # подсвечивает строку, у которых unid+ (например, опубликованные)
            refs = 1 - вид со столбцом Expand
        '''
        dcVP = dict(
            cats=self.cats, 
            forChildStyle = dict(height='calc(100vh - 50px)', background='#fff'),

            viewStyle=dict(width=200), # стиль вида
            form = 'g_group',
            dbAlias = dcUK.dbAlias,
        )

        view = self.getViewObject('ViewGroups', dcVP)
        
        return _mainPage(className='page51', children=[
            _div(**style(maxWidth=1000, margin='auto'), className='cellbg-green', children=
                view.make() # вид с кнопками слева  и тулбаром
            )
        ])

    # *** *** ***
    
    def queryOpen(self, dcUK):
        dcUK.doc._page_ = 1
    
    # *** *** ***

    
# *** *** ***
