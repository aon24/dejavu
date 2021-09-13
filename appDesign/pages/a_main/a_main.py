# -*- coding: utf-8 -*- 
'''
Created on 2020.

@author: aon
'''
from common.dbToolkit.DC import config
from common.common import toWell
from common.colors import htmlToPython
from common.api.formTools import style, _div, _field, _a, label, _table, _img, _btnD
from common.api.classReview import viewDiv
from common.api.classPage import Page

import json
# *** *** ***

class a_main(Page):
    def __init__(self, dc):
        self.title = 'react-py.ru'
        self.jsCssUrl = ['jsv?appDesign/pages/a_main/a_main.js',
                         'jsv?appDesign/pages/a_viewer/a_viewer.js',
                         'jsv?common/css/view.css',
                         'jsv?appDesign/pages/a_main/a_main.css']
        self.dbAlias = 'draft'
        super().__init__(dc)

        toWell( 
            {'Все': ['* All', 'pg_a', 'pg_11'],
             'Сайты': ['aa', 'ss', 'qq'],
             'Подформы': ['pg_11', 'qwer'],
             'Элементы': ['pg_11', 'qwer'],
             'По\xa0авторам': ['aa', 'ss', 'qq'],
            }, 'dropList', 'lsCat')

    
    def page(self, dcUK):
        return _div(
        
        **style(backgroundImage='url(/images/bg51.jpg)', backgroundSize='100% 100%', overflow='auto', height='100vh'),
        focus='cat', children = [
        
        # pyramid
        _div(**style(position='absolute', bottom=10, right=25, width=60, height=100),
            children=[_field('polygon_fd', 'json')]),
        
        # view
        _div ( **style(width='100%', height='100vh', position='fixed'), children = [
            _div( 
                **style(maxWidth=1000, margin='auto'),
                className='row cellbg-green',

                children=[
                    _div( **style(width=85 if dcUK.userAgent == 'mobile' else 170), children=[
                        _div('repository', **style(font='normal 12px Verdana', color='#048')),
                        _field('repository', 'tx', readOnly=1,  **style('ttaStyle', font='normal 11px/1.4 Verdana')),
                        label(),
                        _div(className='navBtn', children=[_field('cat', 'list', 'lsCat', listItemClassName='rsvTop')]),
                        label(),
                        _field('subCat', 'list', 'CAT|||api.get/loadDropList?lsCat|{FIELD}',
                                **style(width='90%', margin='auto', display='block'),
                                saveAlias=1, evenColor='#f4f8ff'),
                    ]),
                    _div(children=[
                        _div(**style(padding=12, background='#dfe', 
                                     border='0 solid #eee', borderBottomWidth=2),
                            children=_table([
style('rowStyle', width='100%'),
None if dcUK.userAgent == 'mobile' else _div(**style(width='10%'), children=[_btnD('', 'xopen', 'opendoc?mode=new&form=a_design&dbAlias=draft', className=' ', children=[
    _img(title='создать новый документ', **style(width=25), src='images/new.png')] ) ]),
_div(**style(verticalAlign='middle'), children=[_field('published', 'chb3', 
    ['\xa0 черн.\xa0', 'опубл.'] if dcUK.userAgent == 'mobile' else [' \xa0 \xa0 черновики\xa0\xa0', 'опубликовано'],
    **style(margin='auto', letterSpacing=1))]),
None if dcUK.userAgent == 'mobile' else _div(**style(width='12%', paddingRight=10), children=[
    _btnD('Адреса', 'showHostAdr'),
                            ])
                        ])),
                        viewDiv(
                            fieldName = 'viewPM',
                            reviewClass='va_pm',
                            **style(background='#fff'), # стиль div, в котором будет вид, включая тулбар и хидер
                            **style('viewStyle', maxHeight='calc(100vh - 74px)', background='#fff'), # стиль вида
                            dbAlias=self.dbAlias,
                            toolbar='va_pm',
                            form='a_design',
                            title='new form',
                            limit=0,
                            addClassName='mRowPM' # подсвечивает строку, у которых unid+ (для подсветки опубликованных)
                        )
                    ]) # toolbar и сам вид
                ]) # кнопки слева, тудбар и сам вид
        ]) # вид с кнопками  и тулбаром
    ]) # пирамида и весь вид
    
    def queryOpen(self, dcUK):
        dcUK.doc.cat = '* All'
        dcUK.doc._page_ = '1'
        dcUK.doc.hostAddress_FD = f'{config.hostAddress}'

        svg = htmlToPython(f'''<svg width="80" height="100">{'<polygon stroke-width="1"/>'*12}</svg>''')
        dcUK.doc._polygon_fd = json.dumps(svg)

# *** *** ***
