'''
Created on 2021

@author: aon
'''

from common.dbToolkit.DC import config, DC
from common.dbToolkit.Book import docFromDB
from common.api.formTools import style, _div
from common.api.classPage import Page

# *** *** ***

class a_viewer(Page):
    def __init__(self, dc):
        self.jsCssUrl = ['jsv?appDesign/pages/a_viewer/a_viewer.js']
        self.dbAlias = 'draft'
        self.title = 'sova-online'
        super().__init__(dc)
    
    def page(self, dcUK):
        return _div(**style(overflow='auto', textAlign='center', height='100vh', backgroundImage='url(/images/24x24LB.png)'),
                    children=[
                        _div(id='a_viewer',
                             **style(position='relative', margin='auto'))
                    ])
    
    def queryOpen(self, dcUK):
        dcUK.doc.root = '' # root is big and not need
        dcUK.doc.webSocketServer_FD = config.webSocketServer
        dcUK.doc.form = 'a_viewer'
        dcUK.mode = 'read'
        dcUK.doc.created_FD = dcUK.doc.D('created')
        self.title = f"_{dcUK.doc.docNo}_ от {dcUK.doc.D('created')}"

# *** *** ***
