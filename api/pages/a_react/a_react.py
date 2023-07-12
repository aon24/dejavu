'''
Created on 2022

@author: aon
'''

from api.formTools import style, _div, _field
from api.classPage import Page
from api.pages.colors import boxToHtml, htmlToPython
from api.toolbars import toolbar
from tools.DC import config

import json, re

# *** *** ***

reColor = re.compile(r'color: (#\w{8})(#\w{8});')


def rootToJson(root, styles, screen=1000):
        html = boxToHtml(root, screen)

        for r in re.finditer(reColor, html):
            color, _, background = r.group(0).rpartition('#')
            s = f'{color}; background-color: #{background}'
            html = html.replace(r.group(0), s)

        py = htmlToPython(html, styles)
        return json.dumps(py, ensure_ascii=False)

# *** *** ***


class a_react(Page):

    def __init__(self, form):
        self.jsCssUrl = ['jsv?api/pages/a_react/a_react.js']
        super().__init__(form)

    def page(self, dcUK):
        if dcUK.mode == 'preview':
            height = 543
        else:
            height = '100vh'
        return _div(children=[
                    _field('react_fd', 'json',
                        **style(height=height, overflow='auto', margin='auto', fontFamily='Verdana', whiteSpace='pre'))
            ])

    def queryOpen(self, dcUK):
        screen = int(dcUK.doc.screen or 1000)
        dcUK.doc.react_fd = rootToJson(dcUK.doc.root, dcUK.doc[f'root_styles_{screen}'], screen)

        # ***

        dcUK.doc.webSocketServer_FD = config.webSocketServer
        dcUK.doc.form = 'a_react'
        # dcUK.mode = 'read'
        dcUK.doc.created_FD = dcUK.doc.D('created')
        self.title = f"_{dcUK.doc.docNo}_ от {dcUK.doc.D('created')}"

        for f in ['root', 'root_styles', 'RAINBOW', '_CLASSES_', 'COLORTEXLIST', f'root_styles_{screen}']:
            dcUK.doc[f] = ''  # field is big and not need

# *** *** ***
