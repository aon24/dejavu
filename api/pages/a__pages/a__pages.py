# -*- coding: utf-8 -*-
'''
Created on 2020.

@author: aon
'''
from tools.DC import config, DCC
from api.formTools import style, _div, _field, _btnD, pyramid, pyramidInit, _mainPage
from api.classPage import Page

from .cats import *

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

        super().__init__(dcUK)

    # *** *** ***

    def page(self, dcUK):
        # dcUK.key доп. ключ формы. Позволяет создать несколько форм одного класса (аналог mode)

        viewKey = f"{dcUK.viewKey or 'all'}"

        dcVP = DCC(
            form=f'a_design',
            viewKey=viewKey,  # будет создано 3 объекта ViewPages: well('viewObjects', f'{className.upper()}-{dcVP.dbAlias}-{dcVP.viewKey}')
            dbAlias=dcUK.dbAlias,
            refs=1,
            noCaching=self.noCaching,
            newFormKey=viewKey  # newFormKey доп. ключ формы. Нужен в тулбаре, чтобы открыть форму a_design с параметром 3d
        )
# !!! костыль !!!!!!!!!!!!
        if 1 or dcUK.userAgent != 'mobile':
#
            # if viewKey == 'html':
                # dcVP.button = _div(**style(width='12%'), children=[_btnD('Адреса', 'showHostAdr')])
                # dcVP.checkBox = _div(
                    # **style(width=380, verticalAlign='middle'), children=
                    # [
                        # _field('published', 'chb3', [' \xa0 черновики\xa0\xa0', 'опубликовано'], **style(letterSpacing=1))
                    # ]
                # )
                #
                # dcVP.cats = html

            if viewKey == 'cases':
                dcVP.cats = cases
                self.title = 'мебель'

            elif viewKey == 'rooms':
                dcVP.cats = rooms
                self.title = 'помещения'

            else:  # key == 'all':
                dcVP.newFormKey = 'html'
                dcVP.cats = all_
                # dcVP.catDir = 'Archive|A'  # для категории Archive отбор с dir == 'A'
                self.title = '2d/3d/A'

        dcVP.downButtons = _field('downButtons', 'band', ['3d-r', '3d-i', 'html'],
            **style(position='absolute', left=0, right=0, bottom=0))

        view = self.getViewObject('ViewPages', dcVP)

        return _mainPage(className='page51', children=[
            pyramid(),

            _div(**style(maxWidth=1000, margin='auto'), className='cellbg-green', children=
                view.make()  # вид с кнопками слева  и тулбаром
            )
        ])

    def queryOpen(self, dcUK):
        dcUK.doc._page_ = 1

        pyramidInit(dcUK)

# *** *** ***
