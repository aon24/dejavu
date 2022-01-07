# -*- coding: utf-8 -*-
'''
Created on 3 апр. 2020 г.

@author: aon
'''

from .. formTools import style, _div, _field, _btnD, _ol
from .... util.first import snd
from .... util.colors import pyToHtml
from .... util.htmlToPy import htmlToPy

import json

jsUrl = ['jsv?api/forms/mp_spa/prism.js', 'jsv?api/forms/js_to_react/jsToReact.js']
cssUrl = 'jsv?api/forms/js_to_react/jsToReact.css'

title = 'react-py.ru'
 
# *** *** ***

def page(dbAlias, mode, userName, multiPage):
    return _div(
        **style(padding=0, maxWidth=1000),
        className = 'page100',
        children=[
            _div(className='topnav', **style(width='100%'),
                children=[
                    _btnD('pyToHtml', 'showPy', 'p y T o H t m l . p y', title='pyToHtml.py'),
                    _btnD('jsToHtml', 'showPy', ' j s T o H t m l . p y', title='jsToHtml.py'),
                    _btnD('htmlToReact', 'showPy', ' h t m l T o R e a c t . p y ', title='htmlToReact.py'),
                    _btnD('GitHub', 'xopen', 'https://github.com/aon24/react-py', title='react-py на github.com'),
            ]),
            _div(**style(position='absolute', top=30, right=15, width=80, height=100),
                children=[_field('polygon_fd', 'json')]),
            _div( **style(overflow='auto', height='calc(100vh - 35px)', border='1px solid #aaa'), children=[
                _field('react_fd', 'json'),
            ]),
            _div(className='multiPageAbs', **style(display='none'))
        ]
    )
# *** *** ***

with open('home/hello.txt', 'r', encoding='utf-8') as f:
    _hello = htmlToPy(pyToHtml(f.read()))

_describe = '''В примерах раскраска файлов sample.py и sample.js:
Выберите sample.py или sample.js. В них то, что вы видите на экране. Форма на Python и подгружаемый javascript.
Раскраска (добавление html-разметки).
Преобразование html в компоненты React*.
Вывод результатов в это окно**.'''

_note = '''* Адаптировано под задачи, есть http://htmltoreact.com
** Фреймворк React-py отображает (транспилирует) не все html-теги'''

def queryOpen(d, mode, ground):
    d.db and snd(d.db.userName, cat='js_to_react')

    d.l_fd = 40
    d.t_fd = 40
    d.w_fd = 850
    d.h_fd = 550
        
    svg = htmlToPy(f'''<svg width="80" height="100">{'<polygon stroke-width="1"/>'*12}</svg>''')
    d._polygon_fd = json.dumps(svg)
    d._page_ = '1'
    
    p = _div(**style(background='#f8f8ff', font='normal 16px Verdana', paddingLeft=5), children=[
            _div('Добавление разметки в текст', **style(font='bold 16pt Verdana', textAlign='center')),
            _ol(_describe, **style(padding=0, border='0 solid #aaa', borderWidth='0 0 1px 0', margin='auto', width=400, font='normal 14px Verdana')),
            _div(_note, br=1, type='1', **style(margin='auto', width=400,font='normal 10px Verdana')),
            _div(**style(display='table', padding=5, width=372, margin='auto'), children=[
                _btnD('s a m p l e . p y', 'showFile', 'z_py| s a m p l e . p y ', className='toolbar-button', **style(width=160, zIndex=1)),
                _btnD('s a m p l e . j s', 'showFile', 'z_js| s a m p l e . j s ', className='toolbar-button', **style(width=160, zIndex=1)),
            ]),
            _div('''Чтобы не было скучно читать эту страницу, можно послушать Оскара Бентона.
                    Может это про тебя She say: "Ты are the best"''',
            **style(textAlign='center', font='normal 10px Verdana'), br=1), 
            dict( fileShow='FILES1_', **style(width=640, margin='auto'), readOnly=1 ),
            _hello[0],
        ])
    d.react_fd = json.dumps(p, ensure_ascii=False)

# *** *** ***
