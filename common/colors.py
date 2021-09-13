# -*- coding: utf-8 -*- 
'''
AON 2020

'''
from xml.dom.minidom import parseString
from lxml import html, etree
import re

# *** *** ***

black = '''style="font-family: 'Courier New', monospace;
    background: #fff; 
    color: black;
    font-weight: bold;
    border: 1px solid #ddd;
    padding: 5px;
    text-align: left;
    white-space: pre;"'''
comm = 'style="color: red;"'
green = 'style="color: green; font-style: italic;"'
blue = 'style="color: blue;"'
darkBlue = 'style="color: #048;"'
darkRed = 'style="color: #840;"'
    
# *** *** ***

def oneRe(reStr, s, attr, ls, multiColor=False):
    '''
    Ищет в исходной строке s нужные блоки, добавляет в них разметку и сохраняет результат в массиве ls,
    на их место вставляет заглушки с номерами (<0>, <1> ...<1528>...).
    Возвращает результат в виде строки с заглушками.
    
    reStr - re
    s - строка
    attr - атрибуты style/class/etc
    ls - массив с разметкой
    multiColor=False, если надо убрать вложенную разметку
    '''
    i = len(ls) # номер очередной заглушки
    for block in set(re.findall(reStr, s)):
        toArr = block
        if not multiColor: # если multiColor==False, убрать вложенную разметку
            for prev in set(re.findall(r'<[\d]+>', block)): # ищем вложенность: <0> ... <21>
                iPrev = int(prev[1:-1], 10)                 # выделяем номер строки в массиве
                toArr = toArr.replace(prev, ls[iPrev][1])   # в строке '<0> qwe <21>' заменяем ссылки(<0>,<21>) на первонач. значения
        ls.append([f'<span {attr}>{toArr}</span>', toArr])  # в каждом элеменете массива ls 2 элемента: размеченный текст и оригинал 
        s = s.replace(block, f'<{i}>')              # заменяем блок текста на зауглушку с номером
        i += 1
    return s

# *** *** ***

def operColor(s, ls, color):
    '''
    раскрашивает операторы.
    Должна вызываться последней, когда в тексте не осталось ни строк, ни комментариев
    '''
    i = len(ls)
    for c in ['&lt;=', '&gt;=', '=&lt;', '=&gt;', '&lt;', '&gt;', '&amp;&amp;', '&amp;',
              '===', '!==', '==', '!=', '+=', '-=', '++', '--', '||']:
        ls.append([f'<span {color}>{c}</span>',0])
        s = s.replace(c, f'<{i}>')
        i += 1
    for c in '!|=+-?:,.[](){}%*/':
        ls.append([f'<span {color}>{c}</span>',0])
        s = s.replace(c, f'<{i}>')
        i += 1
    return s

# *** *** ***

def textToHtml(plain):
    return jsToHtml( pyToHtml( xmlToHtml(plain) ) )

# *** *** ***

def xmlToHtml(plain):
    ls = plain.split('<source lang="xml">')
    if len(ls) == 1:
        return plain
    
    result = ls[0]
    for code in ls[1:]:
        if '</source>' not in code:
            result += code
            continue

        co, _, tx = code.partition('</source>')
        if not co:
            result += tx 
            continue

        s = co.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        ls = []
        s = oneRe('"[\\s\\S]*?"', s, green, ls, multiColor=False)
        s = operColor(s, ls, darkBlue)

        for j in range(len(ls), 0, -1):
            s = s.replace(f'<{j-1}>', ls[j-1][0])
        
        result += f'<div {black}>{s}</div>{tx}'
        
    return f'<div>{result}</div>'

# *** *** ***

def pyToHtml(plain):
    '''
    Ищет в тексте блоки, ограниченные тегами  <source lang="python"> .. </source>
    и заменяет в них строки, комментарии и ключевые слова на теги "span" с нужным стилем
    Возвращает html в виде строки
    '''
    ls = plain.split('<source lang="python">')
    if len(ls) == 1:
        return plain
    
    result = ls[0]
    for code in ls[1:]:
        if '</source>' not in code:
            result += code
            continue

        co, _, tx = code.partition('</source>')
        if not co:
            result += tx 
            continue

        s = co.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
        
        ls = []

        i = 0
        rere = [
            r'\bf"[\s\S]*?"', r"\bf'[\s\S]*?'",
            r'\bf"""[\s\S]*?"""', r"\bf'''[\s\S]*?'''",
            ]
        for gr in rere: # раскраска переменных внутри f-строк
            for fStr in set(re.findall(gr, s)):
                newFstr = fStr
                for val in set(re.findall(r"\{[\s\S]+?\}", fStr)):
                    ls.append([f'<span {darkRed}>{val}</span>', val])
                    newFstr =newFstr.replace(val, f'<{i}>')
                    i += 1
                s = s.replace(fStr, newFstr)

        rere = [
            r'\bf"""[\s\S]*?"""', r"\bf'''[\s\S]*?'''",  # убираем из кода f-строки в массив ls
            r'\bf"[\s\S]*?"', r"\bf'[\s\S]*?'",
            ]
        for gr in rere:
            s = oneRe(gr, s, green, ls, multiColor=True)
        
        rere = [
            "'''[\\s\\S]+?'''", '"""[\\s\\S]+?"""',     # убираем из кода многостроки в массив ls 
            "'[\\s\\S]*?'", '"[\\s\\S]*?"',             # убираем из кода строки в массив ls
            ]
        for gr in rere:
            s = oneRe(gr, s, green, ls, multiColor=False)

        s = oneRe(r'#[\s\S]+?\n+?', s, comm, ls, multiColor=False) # убираем из кода комментарии в массив ls (лучший цвет - красный)
        
        # теперь можно раскрасить синтаксис
        i = len(ls)
        for c in ['None', 'True', 'False', 'class', 'from', 'import', 'set', 'list', 'dict', 'def', 'for', 'in', 'if', 'elif', 'else', 'return', 'and', 'or', 'not']:
            ls.append([f'<span {blue}>{c}</span>', 0])
            s = re.sub (f'\\b{c}\\b', f'<{i}>', s)
            i += 1

        s = operColor(s, ls, darkBlue) # теперь можно раскрасить операторы
    
        for j in range(len(ls), 0, -1):  # восстанавливаем строки и комментарии с новым окрасом
            s = s.replace(f'<{j-1}>', ls[j-1][0])
        
        result += f'<div {black}>{s}</div>{tx}'
        
    return f'<div>{result}</div>'

# *** *** ***

def jsToHtml(plain):
    '''
    Заменяет строки, комментарии и ключевые слова на элементы дизайна "span".
    '''
    ls = plain.split('<source lang="javascript">')
    if len(ls) == 1:
        return plain
    
    result = ls[0]
    for code in ls[1:]:
        if '</source>' not in code:
            result += code
            continue

        co, _, tx = code.partition('</source>')
        if not co:
            result += tx 
            continue

        s = co.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')

        ls = []
    
        i = 0
        for mStr in set(re.findall(r'`[\s\S]+?`', s)): # раскраска переменных внутри многострок
            newFstr = mStr
            for val in set(re.findall(r"\$\{[\s\S]+?\}", mStr)):
                ls.append([f'<span {darkRed}>{val}</span>', val])
                newFstr =newFstr.replace(val, f'<{i}>')
                i += 1
            s = s.replace(mStr, newFstr)
            
        s = oneRe(r'`[\s\S]+?`', s, green, ls, multiColor=True) # убираем из кода `многостроки` в массив ls
        s = oneRe(r"'[\s\S]*?'", s, green, ls, multiColor=False) # убираем из кода 'строки' в массив ls
        s = oneRe(r'"[\s\S]*?"', s, green, ls, multiColor=False) # убираем из кода "строки" в массив ls
        s = oneRe(r'/[\s\S].*?/g\b', s, green, ls, multiColor=False) # убираем из кода re-строки в массив ls
        s = oneRe(r'/[\s\S].*?/\.', s, green, ls, multiColor=False) # убираем из кода re-строки в массив ls
        s = oneRe(r'/\*[\s\S]+?\*/', s, comm, ls, multiColor=False) # убираем из кода /* комментарии */ в массив ls (лучший цвет - красный)
        s = oneRe(r'//[\s\S]*?\n', s, comm, ls, multiColor=False) # убираем из кода // комментарии в массив ls (лучший цвет - красный)
    
        i = len(ls)
    
        # теперь можно раскрасить синтаксис
        for c in ['new', 'JSON', 'Promise', 'then', 'catch', 'let', 'const', 'var', 'true', 'false', 'class', 'from', 'import', 'set', 'list', 'for', 'in', 'if', 'else', 'return', 'null']:
            ls.append([f'<span {blue}>{c}</span>',0])
            s = re.sub (r'\b%s\b' % c, f'<{i}>', s)
            i += 1
    
        # теперь можно раскрасить мои переменные
        for c in ['window', 'doc', 'cmd', 'init','init2', 'recalc', 'hide', 'readOnly', 'validate']:
            ls.append([f'<span {darkRed}>{c}</span>',0])
            s = re.sub (r'\b%s\b' % c, f'<{i}>', s)
            i += 1
    
        s = operColor(s, ls, darkBlue) # теперь можно раскрасить операторы
    
        for j in range(len(ls), 0, -1):  # восстанавливаем операторы, переменные, комментарии, строки с новым окрасом
            s = s.replace(f'<{j-1}>', ls[j-1][0])

        result += f'<div {black}>{s}</div>{tx}'
        
    return f'<div>{result}</div>'

# *** *** ***

def showCode(plain):
    '''
    Наипримитивнейший раскрасчик кода.
    Заменяет строки, комментарии и ключевые слова на элементы дизайна "div".
    Границами нового элемента служат сочетания "{_" и "_}" без пробела.
    '''
    result = ''
    for code in plain.split('CODE__\n'):
        if '\n__CODE' not in code:
            result += code
            continue

        co, _, tx = code.partition('\n__CODE')
        if not co:
            result += tx
            continue

        s = co.replace('{_', '{ _').replace('_}', '_ }').replace('\\', '\\\\').replace('"', '\\"').replace('\\"\'', '"\'').replace('\'\\"', '\'"')
        
        i = 0
        ls = []
        for c in set(re.findall("'''[\\s\\S]+?'''", s)):   # убираем из кода многостроки в массив ls
            ls.append('{_{"div": "%s", "style": {"color": "green", "display":"inline", "fontWeight": "bold"}}_}' % c.replace('\n', '\\n'))
            s = s.replace(c, '___%d___' % i)
            i += 1
        for c in set(re.findall("'[\\s\\S]*?'", s)):   # убираем из кода строки в массив ls
            ls.append('{_{"div": "%s", "style": {"color": "green", "display":"inline", "fontWeight": "bold"}}_}' % c)
            s = s.replace(c, '___%d___' % i)
            i += 1
        for c in set(re.findall('#[\\s\\S]+?\n', s)):    # убираем из кода комментарии в массив ls (лучший цвет - красный)
            ls.append('{_{"div": "%s", "style": {"color": "red", "display":"inline", "fontWeight": "bold"}}_}\n' % c[0:-1])
            s = s.replace(c, '___%d___' % i)
            i += 1
        for c in set(re.findall('//[\\s\\S]+?\n', s)):    # убираем из кода комментарии в массив ls (лучший цвет - красный)
            ls.append('{_{"div": "%s", "style": {"color": "red", "display":"inline", "fontWeight": "bold"}}_}\n' % c[0:-1])
            s = s.replace(c, '___%d___' % i)
            i += 1
    
        # теперь можно раскрасить синтаксис
        for c in ['let', 'None', 'true', 'window','class', 'from', 'import', 'set', 'list', 'dict', 'def', 'for', 'in', 'if', 'elif', 'else', 'return', 'and', 'or', 'not']:
            s = re.sub ('\\b%s\\b' % c, '{_{"div": "%s", "style": {"color": "blue", "display":"inline", "fontWeight": "bold"}}_}' % c, s)
    
        for j in range(i):  # восстанавливаем строки и комментарии с новым окрасом
            s = s.replace('___%d___' % j, ls[j])
        
        result += s + tx
    return result

# *** *** ***

_react = ''

def htmlToJsReact(buf):
    '''
    buf html-строка
    возвращает jsReact-строку 
    '''
    global _react
    _react = ''

    try:
        r = re.search('<[\\s\\S]+>', buf)
        if r:
            doc = html.fromstring(r.group(0))
            ht = etree.tostring(doc, encoding='utf-8').decode()
            xHtmlToJsReact(parseString(ht).childNodes[0], '')
            return _react
        else:
            return '<empty/>'
    except Exception as ex:
        return f'Error-colors.py.htmlToReact: \n{ex}'

# *** *** ***

def sU(a, c):
    '''
    xlink:show   ->  xlinkShow
    font-weight  ->  fontWeight
    '''
    l, _, r = a.partition(c)
    return ( (l + r[0].upper() + r[1:]) if r else a).strip()

# *** *** ***

def xHtmlToJsReact(n, shift='\n    '):
    '''
    Нужен для показа реакт-кода
    на входе нода, рекурсия по нодам с заменой минусов на upperCase
    результат формирует в global _react
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
                xHtmlToJsReact(child)
                
    _react += f'{shift}</{n.nodeName.lower()}>'

# *** *** ***

def htmlToPython(buf):
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
        return {'_teg': 'div', 'text': f'ERROR:{ex}'}

# *** *** ***

if __name__ == '__main__':
    r = htmlToPython('<p>ttt</p>\n<div>d</div>')
    print(r)
    
    
    
    
    
    
    