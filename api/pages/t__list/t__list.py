# -*- coding: utf-8 -*- 
'''
Created on 2020.

@author: aon
'''
from tools.DC import DC
from api.formTools import style, _div, pyramid, pyramidInit, _mainPage
from api.classPage import Page

# *** *** ***

class t__list(Page):
    def __init__(self, dcUK):
        self.noCaching = True
        self.jsCssUrl = [
            'jsv?api/react/_pyramid.js',
            'jsv?api/pages/t__list/t__list.js',
            'jsv?api/pages/t_lesson/t_lesson.js',
            'jsv?api/react/view.css']

        self.cats = {
            'Курсы': DC(condition='True', sort='docNo', reverse=True,
                fixedSubCats=[
                    DC(subCat='По\xa0названию', condition='True', sort='trackName'),
                ]
            ),
            'По\xa0категории': DC(condition='True', sort='trackName', subCat="d.cat or '-'"),
            'По\xa0кураторам': DC(condition='True', sort='trackName', subCat="d.curator or '-'"),
        }

        super().__init__(dcUK)
    
    def page(self, dcUK):
        self.title = f"Курс {dcUK.dbAlias.rpartition('_')[2]}"
        
        dcVP = dict(
            cats=self.cats, 
            forChildStyle = dict(height='calc(100vh - 50px)', background='#fff'),

            viewStyle=dict(width=200), # стиль вида
            form = 'g_group',
            dbAlias = dcUK.dbAlias,
        )

        view = self.getViewObject('ViewGroups', dcVP)
        
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

    
