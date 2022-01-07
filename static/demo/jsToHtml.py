# -*- coding: utf-8 -*- 
'''
AON 2020

'''

import re

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

def jsToHtml(s):
    '''
    Демонстрационный раскрасчик кода.
    Заменяет строки, комментарии и ключевые слова на элементы разметки <span>.
    '''

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
    red2 = 'style="color: #840;"'

    s = s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')   # экранируем символы '&', '<', '>'

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

    return f'<div {black}>{s}</div>'

# *** *** ***
