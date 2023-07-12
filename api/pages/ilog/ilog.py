# -*- coding: utf-8 -*- 
'''
Created on 2020.

@author: aon
'''
from api.formTools import style, _div, _field, navigator, _mainPage
from api.classPage import Page
from tools.first import sovaLogger, err

import re, os

# *** *** ***

class ilog(Page):
    def __init__(self, form):
        self.title = 'Log'
        self.jsCssUrl = ['jsv?api/pages/ilog/ilog.js']
        self.subCats = {}
        self.DBC = {}
        self.noCaching = True
        super().__init__(form)
    
    def page(self, dcUK):
        dcUK._KV_['CATS'] = {'__Все__': '', 'Ошибки': '', 'Сообщения': '', 'Отладка': ''}
        dcUK.form = dcUK.form  or self.form

        btns = [_div(f'{i+1}' , title='Системный журнал') for i in range(len(self.logList)) ]
        
        return _mainPage(className='page51', children=[
            _div(**style(margin='auto'), className='cellbg-green', children=[
            _div(**style(width='100%', display='table', tableLayout='fixed'), children=[
                navigator(dcUK, 'calc(100vh - 180px'),
                
                _div( **style(display='table-cell', background='#dfe'), children=[
                    _div(**style(padding=3, background='#dfe', border='0 solid #eee', borderBottomWidth=2),
                        children=[_field('log_0_6', 'band', btns, className='logband')]              
                    ),
                    _div(**style(height='calc(100vh - 50px)', maxWidth='calc(100vw - 170px)', overflow='auto', background='#fff'),
                         children=[_field('msg', 'fd', br=1, **style(font='normal 14px Courier'))]
                    )
                ])
            ]) 
            ]) 
        ])
    
    # *** *** ***
    
    def queryOpen(self, dcUK):
        dcUK.doc.msg = 'загрузка...'

        self.logList = []
        for i in range(10):
            try:
                f = sovaLogger.logPath % i
                self.logList.append({'time': os.stat(f).st_mtime, 'file': f})
            except:
                pass
        self.logList = sorted(self.logList, key=lambda x: x['time'], reverse=True)

        try:
            self.loadLog(0)
        except Exception as ex:
            err(f'queryOpen: {ex}', cat='classPage: log')
            self.subCats = {'__Все__': [], 'Отладка': [], 'Ошибки': [], 'Сообщения': []}
    
    # *** *** ***

    def loadLog(self, num):
        ALL = '__Все__'
        self.DBC = {}
        self.subCats = {ALL: [], 'Отладка': [], 'Ошибки': [], 'Сообщения': []}

        with open(self.logList[int(num)]['file'], 'rt', encoding='utf-8', errors='ignore') as f:
            lsMsg = f.read().split('¤')
        
        reCat = re.compile(r' \[(.+?)\] ')
        
        for msg in lsMsg:
            if ' DEBUG [' in msg:
                cat = 'Отладка'
            elif ' ERROR [' in msg:
                cat = 'Ошибки'
            else:
                cat = 'Сообщения'

            m = re.search(reCat, msg)
            if m:
                subCat = m.group(1)
            elif msg.strip():
                subCat = '_no cat_'
            else:
                continue
            
            if subCat not in self.subCats[ALL]:
                self.subCats[ALL].append(subCat)
            if subCat not in self.subCats[cat]:
                self.subCats[cat].append(subCat)

            for k in [f'{ALL}|', f'{ALL}|{subCat}', f'{cat}|', f'{cat}|{subCat}']:
                self.DBC[k] = self.DBC.get(k, [])
                self.DBC[k].append(msg)
        
        # dcUK.doc.msg = ''.join(reversed(self.DBC['__Все__|']))

        for k in self.subCats:
            self.subCats[k] = sorted(self.subCats[k], key=lambda k: k.lower())
        
    # *** *** ***
    
    def getData(self, dcUK):
        if dcUK.key:
            return ''.join(reversed(self.DBC.get(dcUK.key, []))),

        try: 
            self.loadLog(dcUK.log)
            return '',
        except:
            return '',
    
# *** *** ***
