# -*- coding: utf-8 -*-
'''
AON 20 apr 2017

'''

from tools.DC import config
from api.pages.colors import htmlToPython

import json

# *** *** ***


def _mainPage(**kv):
    kkv = {}
    kkv.update(kv)
    focus = kkv.get('focus')
    if focus:
        del kkv['focus']
        return _div(focus=focus, children=[_div(**kkv)])
    else:
        return _div(children=[_div(**kv)])


def _div(tx=None, **kv): return _teg('div', tx, **kv)


def _form(**kv): return _teg('form', **kv)


def _input(**kv): return _teg('input', **kv)


def _textarea(tx=None, **kv): return _teg('textarea', tx, **kv)


def _b(tx=None, **kv): return _teg('b', tx, **kv)


def _i(tx=None, **kv): return _teg('i', tx, **kv)


def _p(tx=None, **kv): return _teg('p', tx, **kv)


def _span(tx=None, **kv): return _teg('span', tx, **kv)


def _ul(tx=None, **kv): return _teg('ul', tx, **kv)


def _ol(tx=None, **kv): return _teg('ol', tx, **kv)


def _li(tx=None, **kv): return _teg('li', tx, **kv)


def _a(tx=None, **kv): return _teg('a', tx, **kv)


def _teg(teg, text=None, **kv):
    tg = {'_teg': teg, 'fieldProps': {}, 'attributes': {}}
    if text:
        tg['text'] = text
    for k, v in kv.items():
        if v:
            if k == 'children':
                tg['children'] = v
            elif k in ['s2', 'br', 'wl', '_cmd', '_param']:
                tg['fieldProps'][k] = v
            else:
                tg['attributes'][k] = v
    return tg


def _btnD(*p, **kv):
    return _button(*p, div=True, **kv)


def _button(*p, div=None, **kv):
    tg = {'_teg': 'button', 'text': p[0], 'fieldProps': {'_cmd': p[1]}, 'attributes': {}}
    if div:
        tg['fieldProps']['_div'] = 1
    if len(p) > 2:
        tg['fieldProps']['_param'] = p[2]
    for k, v in kv.items():
        if v:
            if k == 'children':
                tg['children'] = v
            elif k in ['s2']:
                tg['fieldProps'][k] = v
            else:
                tg['attributes'][k] = v
    return tg


def _img(src, **attr):
    return {'_teg': 'img', 'attributes': {'src': src, **attr} }


def _h2(tx, **attr):
    return _teg('h2', tx, **attr)


def _h3(tx, **attr):
    return _teg('h3', tx, **attr)


def _br():
    return {'_teg': 'br'}


def _table(*rows, rowStyle=None):
    ls = []
    for row in rows:
        rw = dict(r=[], rowStyle=None)
        for it in row:
            if type(it) is dict and it.get('rowStyle'):
                rw['rowStyle'] = it.get('rowStyle')
            else:
                rw['rowStyle'] = rowStyle
                rw['r'].append(it)
        rw['r'] and ls.append(rw)
    return [_div(style=rw['rowStyle'], className='rowf', children=rw['r']) for rw in ls]


def style(s='style', **par):
    return {s: {**par}}


def label(l=None, width=None, style=None, className='label', name=None):
    cn = f'{className} label' if className else 'label'
    dic = {'className': cn}
    if name:
        dic['name'] = name
    if style:
        dic['style'] = style
        if width:
            dic['style']['width'] = width
    elif width:
        dic['style'] = {'width': width}
    return _div(l or '\xa0', **dic)


def label_(l=None, width=None, style=None, name=None):
    return label(l, width, style, 'label_', name)


def labell(l=None, width=None, style=None, name=None):
    return label(l, width, style, 'labell', name)


def labelc(l=None, width=None, style=None, name=None):
    return label(l, width, style, 'labelc', name)


def _lf(lab, *p, **pp):
    return _div(children=[labell(lab), _field(*p, **pp)])


def labField(l, fname, ftype='tx', flab=None, **par):
    return [label(l), _lbf(fname, ftype, flab, **par)]


def labField_(l, fname, ftype='tx', flab=None, **par):
    return [label_(l), _lbf(fname, ftype, flab, **par)]


def _lbf(fname, ftype='tx', flab=None, **par):
    if 'dropList' in par:
        tg = {'field': (fname, ftype, par['dropList'])}
    elif flab:
        tg = {'field': (fname, ftype, flab)}
    else:
        tg = {'field': (fname, ftype)}
    tg.update({'fieldProps': {}, 'attributes': {}})

    for k, v in par.items():
        if k in ['br', 's2', 'classic', 'readOnly', 'edit', 'alias', 'saveAlias', 'sep']:
            tg['fieldProps'][k] = v
        elif k == 'children':
            tg['children'] = v
        elif k != 'dropList':
            tg['attributes'][k] = v
    return tg


def _field(*p, **dp):
    return _lbf(*p, **dp)


def _field4(fn, ft, dl1, dl2, **kv):
    tg = {'field': (fn, ft, dl1, dl2), 'attributes': {}, 'fieldProps': {}}
    for k, v in kv.items():
        if k in ['br', 's2', 'classic', 'readOnly', 'edit', 'alias', 'saveAlias', 'sep']:
            tg['fieldProps'][k] = v
        elif k == 'children':
            tg['children'] = v
        elif k != 'dropList':
            tg['attributes'][k] = v
    return tg


def _fileShow(fname, **kv):
    return _lbf(fname, 'fileShow', **kv)

# *** *** ***


def simlePage(toolbar, mode, multiPage, height):
    if multiPage:
        height = height
        mp = None
    else:
        height = 'calc(100vh - 45px)'
        mp = _div(className='multiPageAbs')

    return _div(
        className='page1000',
        focus='tx',
        **style(width='100%'),
        children=[
            toolbar,
            _div(className='z_d', **style(height=height), children=[
                _field('tx', **style(width='99%', font="normal 16px 'Courier New', monospace", whiteSpace='pre-wrap'))
            ]),
            mp,
        ]
    )

# *** *** ***


def docTitle(center, left=None, right=None, WLR='16%', name=None, classic=None):
    if left:
        if type(left) != list:
            lch = left
        else:
            lch = _field(left[0], 'chb', left[1], name=left[0].upper())
            if classic:
                lch['fieldProps'] = {'classic': 1}
                lch['attributes'] = {'className': 'ttar'}
    else:
        lch = None

    if right:
        if type(right) != list:
            rch = right
        else:
            rch = _field(right[0], 'chb', right[1], name=right[0].upper())
            if classic:
                rch['fieldProps'] = {'classic': 1}
                rch['attributes'] = {'className': 'ttar'}
            else:
                rch['attributes'] = {'style': {'textAlign': 'right'}}
    else:
        rch = None

    children = [_div(children=[lch], **style(textAlign='left', width=WLR))]
    children.append(_div(children=[center]))
    children.append(_div(children=[rch], **style(textAlign='right', width=WLR)))

    return _div(className='cell-title', name=name, children=children)

# *** *** ***


def _tab(width, tabs):
    '''
    width - width of headeritem
    tabs: [ [label, body_div], ...]
    '''
    header = []
    body = []
    for i in range(len(tabs)):
        it = tabs[i]
        header.append(_btnD(it[0], f'cmdTab_{i}', i, className='thItem', **style(width=width)))
        body.append(_div(name=f'TABLEBODY_{i}', className='tabBody', children=[it[1]]))

    header.append(_div(className='thItemLast'))

    return  _div(children=[
                _div(className='tabHeader', children=header),
                _div(children=body)
            ])

# *** *** **


def pyramid():
    if config.pyramid:
        return _div(**style(position='absolute', bottom=10, right=25, width=60, height=100),
                children=[_field('polygon_fd', 'json')])
    else:
        return None


_svgJS = json.dumps(htmlToPython(f'''<svg width="80" height="100">{'<polygon stroke-width="1"/>'*12}</svg>'''))


def pyramidInit(dcUK):
    dcUK.doc._polygon_fd = _svgJS

