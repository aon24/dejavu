'''
Created on 2021

@author: aon
'''

from api.formTools import style, _div, _field
from api.classPage import Page
from api.pages.colors import boxToHtml
from api.toolbars import toolbar

# *** *** ***

class a_tohtml(Page):
    def __init__(self, form):
        self.jsCssUrl = ['jsv?api/pages/a_tohtml/a_to.js']
        super().__init__(form)
    
    def page(self, dcUK):
        return _div(children=[
                    toolbar.design(dcUK.mode),
                    _field('html_fd', 'fd',
                        **style(height=543, overflow='auto', display='block', font='normal 16px Courier', whiteSpace='pre'))
            ])

    
    def queryOpen(self, dcUK):
        self.title = f"_{dcUK.doc.docNo}_ от {dcUK.doc.D('created')}"
        dcUK.doc.html_fd = boxToHtml(dcUK.doc.root)
        

# *** *** ***
