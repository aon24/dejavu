# -*- coding: utf-8 -*-
'''
AON 2022

'''
from api.toolbars import toolbar
from tools.first import err
from tools.DC import config
from tools.imgHeader import what

from api.formTools import style, _div, _btnD, _img, _tab
from api.classPage import Page

import os

# *** *** ***


class img(Page):

    def __init__(self, form):
        self.title = 'Pictures'
        self.noCaching = True
        self.dbAlias = 'arm'
        self.jsCssUrl = ['jsv?api/pages/img/img.js', 'jsv?api/pages/img/img.css']
        super().__init__(form)

# *** *** ***

    def page(self, dcUK):
        if config.server:
            return _div(
                **style(backgroundImage='url(/image?24x24LB.png)'),
                        # overflow='hidden', margin='auto', width='100%', height='80vh'),
                children=[
                    # toolbar.design('read'),
                    _div(**style(overflow='auto', height='calc(80vh - 30px)'), children=self.pictures(dcUK))
                ]
            )
        else:
            return _div(
                **style(backgroundImage='url(/image?24x24LB.png)'),
                        # overflow='hidden', margin='auto', width='100%', height='80vh'),
                children=[
                    # toolbar.design('read'),
                    _div(**style(overflow='auto', height='calc(80vh - 25px)'), children=[
                        _tab(140, [
                            ['Изображения', _div(**style(overflow='auto', height='calc(80vh - 60px)'),
                                children=self.pictures('xdg_pictures', dcUK.key))],
                            ['Загрузки', _div(**style(overflow='auto', height='calc(80vh - 60px)'),
                                children=self.pictures('xdg_download', dcUK.key))],
                            ['Sova.online', _div(**style(overflow='auto', height='calc(80vh - 60px)'),
                                children=self.pictures('xdg_sova_pictures', dcUK.key))],
                        ]),
                    ])
            ])

    # *** *** ***

    def pictures(self, xdg, subDir):  # AnyDesk
        try:
            path = os.path.join(config[xdg], subDir)
            lsfiles = os.listdir(path)
        except Exception:
            try:
                subDir = ''
                path = config[xdg]
                lsfiles = os.listdir(path)
            except Exception as ex:
                s = f'404 pages.img: os.listdir-error({path}): {ex}'
                err(s, cat='pages.img')
                return [_div(s)]

        ls = []
        btn = []
        if subDir:
            p = os.path.split(subDir)[0]
            btn.append(
                _btnD('⇑', 'chDir', p, className='chDir', title='вернуться', children=[
                    _div('⇑ ⇑', **style(padding=2)),
                    _div('⇑ ⇑ ⇑', **style(padding=3)),
                    _div('вернуться'),
                ])
            )
            subDir += os.sep

        for k in lsfiles:
            fil = os.path.join(path, k)
            if os.path.isfile(fil) and what(fil):
                ls.append(
                    _btnD('', 'oneImg', f'{xdg}::{subDir}{k}', className='chDir',
                        title=f'Выбрать файл "{k}"',
                        **style(margin=5),
                        children=[
                            _img(f'image?{xdg}::{subDir}{k}', alt=k, **style(width=200, height=200))
                        ],
                ))
            elif os.path.isdir(fil):
                btn.append(
                    _btnD('', 'chDir', f'{subDir}{k}', className='chDir', title='открыть', children=[
                        _img(f'/image?folder.png'),
                        _div(k, **style(padding='0 10px'))
                    ])
                )
        if btn:
            ls = [_div(children=btn, **style(textAlign='center', margin=5))] + \
                 [_div(children=ls, **style(textAlign='center', margin=0))]

        return ls

    # *** *** ***

    def queryOpen(self, dcUK):
        dcUK.doc._TABHEADER = dcUK.tabHeader or '0'

    # *** *** ***

