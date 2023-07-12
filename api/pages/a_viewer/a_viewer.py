'''
Created on 2021

@author: aon
'''

from api.formTools import style, _div
from api.classPage import Page
from tools.DC import config

# *** *** ***

class a_viewer(Page):

    def __init__(self, form):
        self.jsCssUrl = ['jsv?api/pages/a_viewer/a_viewer.js']
        self.dbAlias = 'draft'
        self.title = 'sova-online'
        super().__init__(form)

    def page(self, dcUK):
        return _div(**style(overflow='auto', textAlign='center', height='100vh', backgroundImage='url(/image?24x24LB.png)'),
                    children=[
                        _div(id='a_viewer',
                             **style(position='relative', margin='auto'))
                    ])

    def queryOpen(self, dcUK):
        dcUK.doc.root = ''  # root is big and not need
        dcUK.doc.root_styles = ''  # root_styles is big and not need
        dcUK.doc.webSocketServer_FD = config.webSocketServer
        dcUK.doc.form = 'a_viewer'
        dcUK.mode = 'read'
        dcUK.doc.created_FD = dcUK.doc.D('created')
        self.title = f"_{dcUK.doc.docNo}_ от {dcUK.doc.D('created')}"

# *** *** ***
