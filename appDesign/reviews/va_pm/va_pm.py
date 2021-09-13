# -*- coding: utf-8 -*- 
'''
Created on 7 apr 2018

@author: aon

'''

from common.common import well
from common.dbToolkit.Book import viewReload
from common.api.formTools import _div, style, _btnD
from common.api.classReview import Review

# *** *** ***

class va_pm(Review):
    
    def paging(self, dcUK):
        viewReload(dcUK.dbAlias, 'appDesign_page')

        mainDocs = []
        refsDocs = {}
        self.i = 0
        w = [{'minWidth': 75}, {'minWidth': 70},
             {'minWidth': 90}, {'minWidth': 110}, {'minWidth': 90}]

        docs = well(dcUK.dbAlias, dcUK.filtered)
        i = 0
        for d in docs:
            i += 1
            btnDocNo = [d.unid + ('+' if d.published else ''),
                    _btnD(f'{d.docNo}\n{d.D("created")}', 'docPreview', f'{self.dbAlias}&{d.unid}|-:min:max:smallCls',
                        title='быстрый просмотр (fast preview)', s2=1, className='mCell docNo', style=w[0], br=1)]
                        
            btnRt = _div(className='mCell', **style(**w[2], verticalAlign='middle'), children=[
                    _btnD('Real time', 'xopen', f'opendoc?dbAlias={self.dbAlias}&unid={d.unid}&form=a_viewer',
                        title='просмотр изменений в реальном времени',
                        **style(display='block'))])

            btnEdit = _div(className='mCell', **style(**w[3], verticalAlign='middle'), children=[
                    _btnD( 'изменить', 'xopen', f'opendoc?dbAlias={self.dbAlias}&unid={d.unid}&mode=edit',
                        className='armBtn armBtnRed', **style(display='block', margin=3))])

            btnRead = _div(className='mCell', **style(**w[4], verticalAlign='middle', padding='0 0px'), children=[
                    _btnD( 'просмотр', 'xopen', f'opendoc?dbAlias={self.dbAlias}&unid={d.unid}&mode=edit',
                        **style(display='block'))])


            btn2 = [
                _div(className='mCell', **style(verticalAlign='middle', textAlign='left'), children=[
                    _btnD( 'C', 'xcopy', f'dbAlias={self.dbAlias}&unid={d.unid}',
                        title='скопировать документ', className='forView'),
                    _btnD( 'A', 'toArchive', f'dbAlias={self.dbAlias}&unid={d.unid}',
                        title='убрать в архив', className='forView'),
                ])
            ]
            
            if dcUK.userAgent == 'mobile':
                row = [ *btnDocNo, btnRt, btnRead ]
            else:
                row = [*btnDocNo, btnRt, btnEdit, btnRead,
                       _div(f'{d.pageName}\n{d.pageCat}\n{d.published}', className='mCell',
                        **style(**w[1], borderLeftWidth=1, borderLeftColor='#cff'), s2=1, br=1),
                       *btn2,
                    # _div(f'{d.D("MODIFIED")}\n{d.MODIFIER}', className='mCell', **style(textAlign='right', color='#aaa'), br=1, s2=1),
                ]
            mainDocs.append(row)
            self.i += 1
        
        if docs:
            refsDocs[docs[0].unid] = [ [docs[0].unid, _div('qqqqqqqqqqqqqqqq', className='mCell')] ]
        
        header = [
                    _div('№', style=w[0], className= 'hCell'),
                    _div('отчет', style=w[1], className= 'hCell'),
                    _div('начало', style=w[2], className= 'hCell'),
                    _div('конец', style=w[3], className= 'hCell'),
                    _div('\xa0', style=w[4], className= 'hCell'),
                ]
        return {'mainDocs': mainDocs, 'refsDocs': refsDocs, 'header': None}

# *** *** ***
