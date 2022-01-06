# -*- coding: utf-8 -*- 
'''
Created on 2020.

@author: aon
'''
from tools.DC import config, DC
from api.formTools import style, _div, _field, _btnD, pyramid, pyramidInit, _mainPage
from api.classPage import Page

# *** *** ***

class a__pages(Page):
    def __init__(self, dcUK):
        self.title = 'pages'
        self.noCaching = True
        self.jsCssUrl = [
            'jsv?api/react/_pyramid.js',
            'jsv?api/pages/a__pages/a__pages.js',
            'jsv?api/pages/a_viewer/a_viewer.js',
            'jsv?api/react/view.css']
        self.dbAlias = 'draft'

        self.cats = {
            'Страницы': DC(condition='not (d.subform or d.block)', sort='docNo', reverse=True,
                fixedSubCats=[
                    DC(subCat='По\xa0сайтам', condition='d.site'),
                    DC(subCat='По\xa0авторам', condition='d.creator'),
                ]
            ),
            'Подформы': DC(condition='d.subform', sort='pageName', subCat='d.creator'),
            'Блоки': DC(condition='d.block', sort='pageName', subCat='d.creator'),
        }

        super().__init__(dcUK)

    # *** *** ***
    
    def page(self, dcUK):
        dcVP = dict(
            cats=self.cats,
            form = 'a_design',
            dbAlias = dcUK.dbAlias,
            refs = 1,
        )

        if dcUK.userAgent != 'mobile':
            dcVP['button'] = _div(**style(width='12%'), children=[_btnD('Адреса', 'showHostAdr')])
            dcVP['checkBox'] = _div(
                **style(width=380, verticalAlign='middle'), children=
                [
                    _field('published', 'chb3', [' \xa0 черновики\xa0\xa0', 'опубликовано'], **style(letterSpacing=1))
                ]
            )

        view = self.getViewObject('ViewPages', dcVP)

        return _mainPage(className='page51', children=[
            pyramid(),
            
            _div(**style(maxWidth=1000, margin='auto'), className='cellbg-green', children=
                view.make() # вид с кнопками слева  и тулбаром
            ) 
        ])

    def queryOpen(self, dcUK):
        dcUK.doc._page_ = 1
        dcUK.doc.hostAddress_FD = config.hostAddress

        pyramidInit(dcUK)
        
# *** *** ***
