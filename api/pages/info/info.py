# -*- coding: utf-8 -*- 
'''
AON 20 apr 2017

'''

from api.formTools import style, _div, _field
from api.toolbars import toolbar
from api.classPage import Page

import json

# *** *** ***

class info(Page):
    def __init__(self, form):
        self.title = 'Info'
        self.jsCssUrl = ['jsv?api/pages/info/info.js']
        super().__init__(form)

    
    def page(self, dcUK):
        height = 540 if dcUK.mode == 'preview' else 'calc(100vh - 30px)'
        return _div(
            **style(overflow='hidden'), #backgroundImage='url(/image?24x24LB.png)', 
            children=[
                toolbar.info(dcUK.mode),
                _div(**style(width=1000, height=height, margin='auto', overflow='auto'),
                    children=[_field('_fields_FD', 'json')]),
            ]
        )
    
# *** *** ***

    def queryOpen(self, dcUK):
        ls = []
        i = 0
        
        for fi in sorted(dcUK.doc._KV_):
            i += 1
            bg = '#f0f8ff' if i % 2 else '#f0fff8'
            if fi.startswith('FILES'):
                field = _div(**style(backgroundColor=bg, border='1px solid #aaa', borderTopWidth=0, padding=3),
                    children=[
                        _div(fi, className='label', **style(font='bold 12pt Courier')),
                        _field(fi, **style('ttaStyle', font='bold 12pt Courier', color='#o48'))]
                    )
            elif fi =='ROOT':
                field = _div(**style(display='table', width='100%', backgroundColor=bg, border='1px solid #aaa', borderTopWidth=0, padding=3),
                    children=[
                        _div(fi, className='label', **style(display='table-cell', font='bold 12pt Courier', width= 200, minWidth=200)),
                        _field(fi, **style(display='table-cell'), readOnly=1, **style('ttaStyle', font='bold 12pt Courier', color='#048'))] 
                    )
            else:
                field = _div(**style(display='table', width='100%', backgroundColor=bg, border='1px solid #aaa', borderTopWidth=0, padding=3),
                    children=[
                        _div(fi, className='label', **style(display='table-cell', font='bold 12pt Courier', width= 200, minWidth=200)),
                        _field(fi, **style(display='table-cell'), **style('ttaStyle', font='bold 12pt Courier'))] 
                    )
            
            ls.append(field)

        dcUK.doc._fields_FD = json.dumps(ls, ensure_ascii=False)
        
# *** *** ***






