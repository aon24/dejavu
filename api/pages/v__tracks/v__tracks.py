# -*- coding: utf-8 -*- 
'''
Created on 2020.

@author: aon
'''
from tools.DC import DC, well, toWell
from api.formTools import style, _div, pyramid, pyramidInit, _mainPage, _field
from api.classPage import Page
from api.reviews.reviews import ViewTracks


# *** *** ***

class v__tracks(Page):
    def __init__(self, dcUK):
        self.title = 'курсы'
        self.noCaching = True
        self.jsCssUrl = [
            'jsv?api/react/_pyramid.js',
            'jsv?api/pages/v__tracks/v__tracks.js',
            'jsv?api/pages/v__tracks/v__tracks.js',
            'jsv?api/react/view.css']
        self.dbAlias = 'courses'

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
        dcVP = dict(cats=self.cats, form='v_track', dbAlias=dcUK.dbAlias)
        
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
                view.make() # вид с кнопками слева  и тулбаром
            ) 
        ])
    
    def queryOpen(self, dcUK):
        dcUK.doc.cat = 'Все'
        dcUK.doc._page_ = '1'

        pyramidInit(dcUK)

# *** *** ***

    
