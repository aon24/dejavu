# -*- coding: utf-8 -*- 
'''
AON 20 apr 2017

'''
# *** *** ***

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

def _table(*rows):
    ls = []
    for row in rows:
        rw = dict(r=[], rowClassName=None, rowStyle=None)
        for it in row:
            if type(it) is dict and (it.get('rowClassName') or it.get('rowStyle')):
                if it.get('rowClassName'):
                    rw['rowClassName'] = it.get('rowClassName')
                if it.get('rowStyle'):
                    rw['rowStyle'] = it.get('rowStyle')
            else:
                rw['r'].append(it)
        rw['r'] and ls.append(rw)
    return [_div(style=rw['rowStyle'], className=rw['rowClassName'] or 'rowf', children=rw['r']) for rw in ls]

def style(s='style', **par):
    return {s: {**par}}

def label(l=None, width=None, style=None, className='label', name=None):
    dic = {'className': className}
    if name:
        dic['name'] = name
    if style:
        dic['style'] = style
        if width:
            dic['style']['width'] = width
    elif width:
        dic['style'] = {'width': width}
    return _div(l or '\xa0', **dic)


def label_(l=None, width=None, style=None, className='label_'):
    return label(l, width, style, className)


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
        if k in ['br', 's2', 'classic', 'readOnly', 'edit', 'alias', 'saveAlias',
                 'ttaStyle', 'ttaClassName', 'sep']: 
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
        if k in ['br', 's2', 'classic', 'readOnly', 'edit', 'alias', 'saveAlias',
                 'ttaStyle', 'ttaClassName', 'sep']: 
            tg['fieldProps'][k] = v
        elif k == 'children':
            tg['children'] = v
        elif k != 'dropList':
            tg['attributes'][k] = v
    return tg

def _fileShow(fs, **kv):
    tg = {'fileShow': fs.upper(), 'fieldProps': {}, 'attributes': {}}
    for k, v in kv.items():
        if k in ['wl', 'label', 'ttaFileShow', 'readOnly']:
            tg['fieldProps'][k] = v
        else:
            tg['attributes'][k] = v
    return tg

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
                _field('tx', **style('ttaStyle', width='99%', font="normal 16px 'Courier New', monospace", whiteSpace='pre-wrap'))
            ]),
            mp,
        ]
    )
    
# *** *** ***

def docTitle(title, left=None, right=None, width='66%', name=None, classic=None, field=None):
    if left:
        lch = _field(left[0], 'chb', left[1], name=left[0].upper())
        if classic:
            lch['fieldProps'] = {'classic': 1}
            lch['attributes'] = {'className': 'ttar'}
    else:
        lch = _div('\xa0')

    if right:
        rch = _field(right[0], 'chb', right[1], name=right[0].upper())
        if classic:
            rch['fieldProps'] = {'classic': 1}
            rch['attributes'] = {'className': 'ttar'}
        else:
            rch['attributes'] = {'style': {'textAlign': 'right'}}
    else:
        rch = _div('\xa0')
        
    if field:
        center = _field(field, 'fd', **style(width=width))
    else:
        center = label(title, className=' ', width=width)
   
    return _div(className='cell-title row', **style(padding=2), name=name, children=[lch, center, rch])

# *** *** ***
