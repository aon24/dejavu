# -*- coding: utf-8 -*- 

from xml.dom.minidom import parseString
from lxml import html, etree

# *** *** ***

_react = ''

def htmlToReact(buf):
    '''
    buf - html-строка
    возвращает ReactJS-строку 
    '''
    global _react
    _react = ''

    try:
        r = re.search('<[\\s\\S]+>', buf)
        if r:
            doc = html.fromstring(r.group(0))
            ht = etree.tostring(doc, encoding='utf-8').decode()
            xHtmlToReact(parseString(ht).childNodes[0], '')
            return _react
        else:
            return '<empty/>'
    except Exception as ex:
        s = f'htmlToReact: \n{ex}'
        print(s)
        return s

# *** *** ***

def sU(a, c):
    '''
    xlink:show   ->  xlinkShow
    font-weight  ->  fontWeight
    '''
    l, _, r = a.partition(c)
    return ( (l + r[0].upper() + r[1:]) if r else a).strip()

# *** *** ***

def xHtmlToReact(n, shift='\n    '):
    '''
    Нужен для показа реакт-кода
    на входе нода, рекурсия по нодам с заменой минусов на upperCase
    результат формирует в global переменной _react
    '''
    global _react

    if n.nodeName.lower() in ['head', 'script']:
        return
    
    _react += shift + '<' + n.nodeName.lower()
    if n.attributes:
        for k, v in n.attributes.items():
            if k == 'style':
                style = ''
                for s in v.split(';'):
                    if s.strip():
                        l, _, r = s.partition(':')
                        style += f'''{sU(l, '-')}: "{r.strip()}", '''
                if style:
                    _react += ' style={{' + style + '}}'
            elif k == 'class':
                _react += f' className="{v}"'
            else:
                kk = k.replace('xlink:href', 'href') # deprcated
                _react += f''' {sU( sU(kk, ':'), '-' )}="{v}"'''
        
    _react += '>'
    if n.childNodes:
        for child in n.childNodes:
            if  child.nodeName == '#text':
                tx = child.nodeValue
                for x in ['{', '}', '<', '>']:
                    tx = tx.replace(x, '{"' + x + '"_{_')
                tx = tx.replace('_{_', '}')
                if tx[-1] == ' ':
                    tx = tx[:-1] + '\xa0'
                _react += tx.replace('\n', '<br/>')
            else:
                xHtmlToReact(child)
                
    _react += f'{shift}</{n.nodeName.lower()}>'

# *** *** ***
