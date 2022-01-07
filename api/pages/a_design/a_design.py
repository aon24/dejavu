# -*- coding: utf-8 -*- 
'''
Created on 2020.

@author: aon
'''
from .a_screens import blankScreens
from tools.DC import config, toWell

from api.sno import snoDB
from api.formTools import style, _div, _field
from api.toolbars import toolbar
from api.classPage import Page

# *** *** ***

class a_design(Page):
    def __init__(self, form):
        self.title = 'html-edit'
        self.jsCssUrlEdit = ['jsv?api/pages/a_design/a_design.js']
        self.jsCssUrlRead = ['jsv?api/pages/a_design/a_design_read.js']
        self.dbAlias = 'draft'
        super().__init__(form)

    
    def page(self, dcUK):
        if dcUK.mode == 'preview':
            return _div(
                **style(position='absolute', backgroundImage='url(/image?24x24LB.png)',
                        overflow='hidden', width='100%'), # height='100vh', 
                children=[
                    toolbar.design(dcUK.mode),
                    _div(className='pa-ge', **style(overflow='auto', height='calc(100vh - 160px', paddingTop=5), children=[
                        _field('root', 'box')
                ])
            ]
        )
                        
        return _div(
            **style(position='absolute', backgroundImage='url(/image?24x24LB.png)',
                    overflow='hidden', height='100vh', width='100%'),
            children=[
                toolbar.design(dcUK.mode),
                _div(className='page', **style(overflow='auto'), children=[
                    # _field('root', 'box' if dcUK.mode in ['new', 'edit', 'admin'] else 'fd')
                    _field('root', 'box'),
                ])
            ]
        )
    
    def queryOpen(self, dcUK):
        dcUK.doc.webSocketServer_FD = config.webSocketServer;
        dcUK.doc.created_FD = dcUK.doc.DT('created')
        dcUK.doc.modified_FD = dcUK.doc.DT('modified')
        dcUK.doc.published_FD = dcUK.doc.published
        dcUK.doc.creator_FD = dcUK.doc.creator
        dcUK.doc.modifier_FD = dcUK.doc.modifier
        
        dcUK.doc.dir = dcUK.doc.dir or '0'
        dcUK.doc.root = dcUK.doc.root or blankScreens
        dcUK.doc.rainbow = dcUK.doc.rainbow or '#ff3366ff\n#ff6633ff\n#FFCC33ff\n#33FF66ff\n#33CCFFff\n#3366FFff\n#CC33FFff'
        dcUK.doc.colorTexList = dcUK.doc.colorTexList or '#ff3366ff\n#ff6633ff\n#FFCC33ff\n#33FF66ff\n#33CCFFff\n#3366FFff\n#CC33FFff'


# *** *** ***

    def querySave(self, dcUK):
        if not dcUK.doc.docNo:
            dcUK.doc.docNo = snoDB(dcUK, 'inc')
        return True

# *** *** ***

    def afterSave(self, dcUK):
        toWell(None, f'viewloaded-{dcUK.dbAlias}-VIEWPAGES') # viewPages = view-field-name
        return True

# *** *** ***
    
