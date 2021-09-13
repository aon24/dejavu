'''
Created on 14 мар. 2021 г.

@author: aon
'''
from common.api.formTools import _table, _div

import json

[lim, width] = [0,0]

def row(part, rootIndex, add):
    global lim, width

    r = {'boxIndex': rootIndex+add, 'rect': {'height': part} }
    
    if add == 2:
        r['tuning'] = dict(bgStyle='color', backgroundColor='#fffFFF40',
            border='borEQ', borderWidth=1, borderColor='#aaa')

    elif add == 3: # кнопки на нижней части
        centr = width / 2
        rad = 25
        t = (part - rad) / 2
        r['boxes'] = [
            {   'rect': dict(top=t, left=centr-4*rad, height=rad, width=rad),
                'tuning': dict(bgStyle='color', backgroundColor='#00000060'),
                'float': 1,
                'boxIndex': rootIndex+add+1
            },
            {   'rect': dict(top=t, left=centr-(rad/2), height=rad, width=rad),
                'tuning': dict(bgStyle='color', backgroundColor='#00000060',
                   border='borEQ', borderWidth=2, borderRadius=50, borderColor='#ffffff',
                   shadow='outside', shadowX=0, shadowY=0, shadowR=0, shadowW=2, shadowColor='#00000080'),
                

                'float': 1,
                'boxIndex': rootIndex+add+2
            },
            {   'rect': dict(top=t-1, left=centr+2.5*rad, height=rad, width=rad),
                'tuning': dict(
                   border='borNE',
                   borderRightWidth=rad/2+1, borderRightColor='#00000060',
                   borderTopWidth=rad/2,
                   borderBottomWidth=rad/2,
                ),
                'float': 1,
                'boxIndex': rootIndex+add+3
            },
        ]

    lim += r['rect']['height']
    return r

def smartPhone(rootIndex, w, height, dim):  # dim - масштаб pagePlus
    global lim, width
    
    [lim, width] = [0, w];

    r = 20
    if rootIndex == 100:
        parts = [96, 800, 64]
        cells = [
            row(parts[0], rootIndex, 1), # boxIndex = 101 or 201 or 301...901
            row(parts[1], rootIndex, 2),
            row(parts[2], rootIndex, 3)
        ]
        top = parts[0]
        h = parts[1]
    else:
        top = 0
        h = height
        cells = []
    
    return dict( # root для данного экрана
        declare = f'{width}x{height}',
        boxIndex = rootIndex, # boxIndex = 100, 200,... 900
        type = 'rows',
        floating = 1,
        tuning = dict(
            pagePlusDim = dim,
            backgroundColor = '#ddeeff70',
            bgStyle = 'color',
            border = 'borEQ',
            borderWidth = r,
            borderColor = '#4488aa30',
            borderRadius = 40,
            borderRadius_metric = 'px',
            insideOnly = 1,
            position='relative',
            margin='auto',
        ),
        cells = cells,
        # 3 служебных ряда для смартфона: отступ сверху 16мм, экран 124мм, отступ снизу 10мм (Redmi Note 9)
        
        boxes = [
            dict(
                boxIndex=rootIndex*10, # boxIndex = 1000, 2000,... 9000 - главный бокс для страницы
                floating=True,
                rect=dict(left=0, top=top, width=width, height=h),
                tuning = dict(fixed=1, backgroundColor='#ffffff', bgStyle = 'color')
            )],

        rect=dict(width=width+2*r, height=(lim or h)+2*r, left=0, top=0),
    )

boxes=[smartPhone(100, 480, 960, 2), # rootIndex = 100, 200,... 900
       smartPhone(200, 600, 400, 3),
       smartPhone(300, 1200, 960, 4) ] # + [smartPhone(i, 600, 400, 3) for i in range(400, 1000, 100)]
    
blankScreens = json.dumps(
    dict(
        boxIndex=0, 
        tuning={'margin': 'auto', 'contur': 1, 'screen': 100}, # screen - номер экрана по умолчанию (100: рут=100 первый блок=1000
        boxes=boxes
    ),
    ensure_ascii=False)


# tuning.screen задает, какой режим выбрать. screen=0 - выбрать smartPhone(100,..) screen=1 - выбрать smartPhone(200, 
# boxIndex == 0 - служебный блок. Может содержать несколько страниц. Выбранная страница в переменной tuning.screen
# boxIndex == 100 or 200 or 300 ... or 900 - root для данной страницы: 100 - smartPhone, 200 - монитор...)





