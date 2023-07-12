# -*- coding: utf-8 -*-
'''
Created on 2020.

@author: aon
'''
from tools.DC import DCC
from api.formTools import style, _div, pyramid, pyramidInit, _mainPage
from api.classPage import Page

# *** *** ***


class u__people(Page):

    def __init__(self, dcUK):
        self.title = 'люди'
        self.noCaching = True
        self.jsCssUrl = [
            'jsv?api/react/_pyramid.js',
            'jsv?api/pages/u__people/u__people.js',
            'jsv?api/pages/u_human/u_human.js',
            'jsv?api/react/view.css']
        self.dbAlias = 'people'

        self.cats = {
            'Студенты': DCC(condition='True', sort='d.fullName', reverse=True,
                fixedSubCats=[
                    DCC(subCat='По\xa0сайтам', condition='d.site'),
                    DCC(subCat='По\xa0авторам', condition='d.creator'),
                ]
            ),
            'Подформы': DCC(condition='d.subform', sort='pageName', subCat='d.creator'),
            'Блоки': DCC(condition='d.block', sort='pageName', subCat='d.creator'),
        }

        super().__init__(dcUK)

    # *** *** ***

    def page(self, dcUK):
        dcVP = DCC(cats=self.cats, form='lk', dbAlias=dcUK.dbAlias)
        view = self.getViewObject('ViewPeople', dcVP)

        return _mainPage(className='page51', children=[
            pyramid(),

            _div(**style(maxWidth=1000, margin='auto'), className='cellbg-green', children=
                view.make()  # вид с кнопками слева  и тулбаром
            )
        ])

    def queryOpen(self, dcUK):
        dcUK.doc._page_ = '1'
        pyramidInit(dcUK)

# *** *** ***

