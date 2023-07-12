# -*- coding: utf-8 -*-
'''
Created on 2020.

@author: aon
<svg width="100000" height="100000">
    <defs>
        <path id="myTextPath2" d="M40, 200 a 30,30 0 0 1 300,0"/>
     </defs>
    <text x="10" y="10" style={{stroke: '#048', font: 'normal 30px Times'}}>
        <textPath xlinkHref="#myTextPath2">
            look into the future
        </textPath>
    </text>
</svg>
'''
from .a_screens import blankScreens
from tools.DC import config, toWell
from tools.first import err
from tools.dbToolkit.Book import histFromDB

from api.sno import snoDB
from api.formTools import style, _div, _field
from api.toolbars import toolbar
from api.classPage import Page

import json

# *** *** ***


class a_design(Page):

    def __init__(self, form):
        self.title = 'html-edit'
        self.jsCssUrlEdit = ['jsv?api/pages/a_design/a_design.js']
        self.jsCssUrlRead = ['jsv?api/pages/a_design/a_design_read.js']
        self.dbAlias = 'draft'
        super().__init__(form)

    # *** *** ***

    def page(self, dcUK):
        if dcUK.mode == 'preview':
            hPage = 'calc(100% - 30px)'
            return _div(
                **style(overflow='hidden', height=hPage),  # backgroundImage='url(/image?24x24LB.png)',
                children=[
                    toolbar.info(dcUK.mode),
                    _div(**style(height='calc(100% - 30px)', overflow='auto'),
                        children=[_field('root', 'box', **style(margin='auto', height='calc(100% - 30px)'))]),
                ]
            )
        elif dcUK.mode == 'mockup':
            hPage = 'calc(100% - 30px)'
            
            return _div(
                **style(overflowY='auto', overflowX='hidden', height='calc(100% - 30px)'),
                children=[
                    _field('root', 'box', **style(margin='auto', height='calc(100% - 30px)'))
            ])

        return _div(
            **style(position='absolute', backgroundImage='url(/image?24x24LB.png)',
                    overflow='hidden', height='100vh', width='100%'),
            children=[
                toolbar.design(dcUK.mode),
                # _field('key', **style(margin='50px auto', width=120)),
                _div(className='page', **style(overflow='auto'), children=[_field('root', 'box')])
            ]
        )

    # *** *** ***

    def queryOpen(self, dcUK):
        self.title = dcUK.doc.title or 'html-edit'

        dcUK.doc.webSocketServer_FD = f'{config.ws_server}:{config.ws_port}'
        dcUK.doc.created_FD = dcUK.doc.DT('created')
        dcUK.doc.modified_FD = dcUK.doc.DT('modified')
        dcUK.doc.published_FD = dcUK.doc.published
        dcUK.doc.creator_FD = dcUK.doc.creator
        dcUK.doc.modifier_FD = dcUK.doc.modifier
        dcUK.doc._syles_ = ''
        dcUK.doc.docNo_FD = f"№ {dcUK.doc.pref}{dcUK.doc.docNo}{dcUK.doc.suff} от {dcUK.doc.D('created')}"

        dcUK.doc.dir = dcUK.doc.dir or '0'
        dcUK.doc.root = dcUK.doc.root or blankScreens(dcUK.key)
        dcUK.doc.rainbow = dcUK.doc.rainbow or '\n'.join(['#ff0000ff', '#ffa500ff', '#ffff00ff', '#008000ff', '#0000ffff', '#4b0082ff', '#ee82eeff'])
        dcUK.doc.key = dcUK.doc.key or dcUK.key
        if dcUK.doc.key != 'Archive':
            dcUK.doc.key_ = dcUK.doc.key

# *** *** ***

    def querySave(self, dcUK):
        if dcUK.doc.docNo:
            return True

        n = snoDB(dcUK, 'inc')
        if n:
            dcUK.doc.docNo = n
            return True

# *** *** ***

    def afterSave(self, dcUK):
        toWell(None, f'viewloaded-{dcUK.dbAlias}-VIEWPAGES')  # viewPages = view-field-name
        return True

# *** *** ***

    def getData(self, dcUK):
        return histFromDB(dcUK), 'application/json'

# *** *** ***


def delNecessary(dcUK):

    def oneBox(box, r2b):
        for k, v in box.items():
            if k in ['boxes', 'cells']:
                r2b[k] = []
                for it in v:
                    bc = {}
                    oneBox(it, bc)
                    r2b[k].append(bc)

            elif k == 'tuning':
                r2b[k] = {}
                for k1, v1 in v.items():
                    if v1:
                        r2b[k][k1] = v1
            elif k == 'content' and not v[0] and not v[1]:
                pass
            else:
                r2b[k] = v

    try:
        root = json.loads(dcUK.doc.root)
        r2 = {}
        oneBox(root, r2)
        dcUK.doc.root = json.dumps(r2, ensure_ascii=False)
    except Exception as ex:
        err(ex, cat='a_design.querySave.delete necessary')
