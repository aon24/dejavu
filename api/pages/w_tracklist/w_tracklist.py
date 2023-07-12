# -*- coding: utf-8 -*-
'''
Created on 2020.

@author: aon
'''
from tools.DC import DCC
from api.formTools import style, _div, pyramid, pyramidInit, _mainPage, _field
from api.classPage import Page

# *** *** ***


class w_tracklist(Page):

    def __init__(self, dcUK):
        self.title = 'курсы'
        self.noCaching = True
        self.jsCssUrl = [
            'jsv?api/react/_pyramid.js',
            'jsv?api/pages/w_tracklist/w_tracklist.js',
            'jsv?api/pages/w_track/w_track.js',
            'jsv?api/react/view.css']
        self.dbAlias = 'well'

        self.cats = {
            'Курсы': DCC(condition='True', sort='docNo', reverse=True,
                fixedSubCats=[
                    DCC(subCat='По\xa0названию', condition='True', sort='trackName'),
                ]
            ),
            'По\xa0категории': DCC(condition='True', sort='trackName', subCat="d.cat or '-'"),
            'По\xa0кураторам': DCC(condition='True', sort='trackName', subCat="d.curator or '-'"),
        }

        super().__init__(dcUK)

    def page(self, dcUK):
        dcVP = DCC(cats=self.cats, form='w_track', dbAlias=dcUK.dbAlias)

        dcVP['checkBox'] = _div(
            **style(width=380, verticalAlign='middle'), children=
            [
                _field('active', 'chb3', ['активные', 'ожидание'], **style(letterSpacing=1))
            ]
        )

        view = self.getViewObject('ViewTracks', dcVP)

        return _mainPage(className='page51', children=[
            pyramid(),

            _div(**style(maxWidth=1000, margin='auto'), className='cellbg-green', children=
                view.make()  # вид с кнопками слева  и тулбаром
            )
        ])

    def queryOpen(self, dcUK):
        dcUK.doc.cat = 'Все'
        dcUK.doc._page_ = '1'

        pyramidInit(dcUK)

# *** *** ***

