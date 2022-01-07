# -*- coding: utf-8 -*- 
'''
Created on 2021.

@author: aon

Classifiers

'''
from tools.DC import DC
from api.formTools import style, _div, pyramid, pyramidInit, _mainPage
from api.classPage import Page

# *** *** ***

class w__wells(Page):
    def __init__(self, dcUK):
        self.title = 'Справочник'
        self.jsCssUrl = [
            'jsv?api/react/_pyramid.js',
            'jsv?api/pages/w__wells/w__wells.js',
            'jsv?api/pages/w_list/w_list.js',
            'jsv?api/react/view.css']
        self.dbAlias = 'well'

        self.cats = {
            'Справочники': DC(condition='True', sort='d.listName', reverse=True,
                fixedSubCats=[
                    DC(subCat='Общие', condition='not (d.tracks or d.system)'),
                    DC(subCat='Для\xa0курсов', condition='d.tracks'),
                    DC(subCat='Настройки', condition='d.system'),
                ]
            ),
        }

        super().__init__(dcUK)

    # *** *** ***
    
    def page(self, dcUK):
        dcVP = dict(cats=self.cats, form='w_list', dbAlias=dcUK.dbAlias)
        view = self.getViewObject('ViewWell', dcVP)

        return _mainPage(className='page51', children=[
            pyramid(),
            
            _div(**style(maxWidth=1000, margin='auto'), className='cellbg-green', children=
                view.make() # вид с кнопками слева  и тулбаром
            ) 
        ])
    
    def queryOpen(self, dcUK):
        dcUK.doc._page_ = '1'
        pyramidInit(dcUK)

# *** *** ***

    
