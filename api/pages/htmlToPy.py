# -*- coding: utf-8 -*- 
'''
AON 2020

'''
from xml.dom.minidom import parseString
from lxml import html, etree
import re

# *** *** ***

def sU(a, c):
    '''
    xlink:href   ->  xlinkHref
    font-weight  ->  fontWeight
    '''
    l, _, r = a.partition(c)
    return ( (l + r[0].upper() + r[1:]) if r else a).strip()

# *** *** ***

def htmlToPy(buf):
    '''
    создает словарь для отправки в реакт-ру
    на входе html, 
    html -> xhtml_dom -> рекурсия по нодам с заменой минусов на upperCase
    возвращает dom-словарь для отправки в json-поле
    '''
    def childNode(n):
        if n.nodeName.lower() in ['head', 'script']:
            return
        
        svgEl = {'_teg': n.nodeName.lower()}
        if n.attributes:
            attributes = {}
            for k, v in n.attributes.items():
                if k == 'style':
                    style = {}
                    for s in v.split(';'):
                        l, _, r = s.partition(':')
                        l = sU(l, '-')
                        if l:
                            style[l] = r.strip()
                    attributes['style'] = style
                elif k == 'class':
                    attributes['className'] = v
                else:
                    kk = k.replace('xlink:href', 'href') # deprcated
                    attributes[sU( sU(kk, ':'), '-' )] = v
            if attributes:
                svgEl['attributes'] = attributes
            
        if n.childNodes:
            chNo = []
            for child in n.childNodes:
                if  child.nodeName == '#text':
                    tx = child.nodeValue.replace('\r', '')
                    if tx:
                        if '\n' in tx:
                            ls = []
                            for s in tx.split('\n'):
                                ls += [s,  {'_teg': 'br'}]
                            chNo += ls[0:-1]
                        else:
                            chNo.append(tx)
                else:
                    chNo.append( childNode(child) )
            if chNo:
                svgEl['children'] = chNo
        return svgEl
    # *** ***
    
    try:
        r = re.search('<[\\s\\S]+>', buf)
        if r:
            doc = html.fromstring(r.group(0))
            ht = etree.tostring(doc, encoding='utf-8').decode()
            return [childNode(parseString(ht).childNodes[0])]
        return {}
    except Exception as ex:
        return {'_teg': 'div', 'text': f'ERROR:{ex}\n\n{ht}'}

# *** *** ***
