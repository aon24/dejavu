# -*- coding: utf-8 -*-
'''
Created on 2022

@author: aon24
'''
from api.viewTools import docNoPreview, btn3cix
from api.formTools import _div, style, _btnD
from api.classReview import Review

# *** *** ***

w = [{'width': 80}, {'minWidth': 70}, {'minWidth': 90},
     {'width': 70}, {'width': 140},
     {'width': 110}, {'width': 75}]


class ViewLessons(Review):

    def paging(self, dcUK):
        docs = self.viewReload(dcUK)

        mainDocs = []
        refsDocs = {}
        self.i = 0

        i = 0
        for d in docs:
            i += 1
            unid = d.unid + ('+' if d.published else '')
            btnDocNo = docNoPreview(f'{d.docNo}\n{d.D("created")}', dcUK.dbAlias, d, 84)

            btnRt = _div(className='mCell', **style(**w[1], verticalAlign='middle'), children=[
                    _btnD('Real time', 'xopen', f'opendoc?dbAlias={dcUK.dbAlias}&unid={d.unid}&form=a_viewer',
                        title='просмотр изменений в реальном времени',
                        **style(display='block'))])

            btnEdit = _div(className='mCell', **style(**w[2], verticalAlign='middle'), children=[
                    _btnD('изменить', 'xopen', f'opendoc?dbAlias={dcUK.dbAlias}&unid={d.unid}&mode=edit',
                        className='armBtn armBtnRed', **style(display='block', margin=3))])

            # open, publish
            btn1 = _div(className='mCell', **style(**w[3], verticalAlign='middle', textAlign='left'), children=[
                # _btnD( '\xa0', 'openHtml', f'{dcUK.dbAlias}&{d.unid}&{d.docNo}',
                _btnD('\xa0', 'xopen', f'openpage?dbAlias={dcUK.dbAlias}&unid={d.unid}&mode=html&docno={d.docNo}',
                        title='просмотр', className='forView_o'),
                _btnD('\xa0', 'publish', f'dbAlias={dcUK.dbAlias}&unid={d.unid}',
                        title='опубликовано', className='forView_p'),
            ])

            # toHtml, toReact
            btn2 = _div(className='mCell', **style(**w[4], verticalAlign='middle', textAlign='left'), children=[
                _btnD('Html', 'previewNew', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (html)&a_toHtml',
                    title='HTML', className='forView fvh'),
                _btnD('React', 'previewNew', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (React)&a_toReact',
                    title='React JS', className='forView fvr'),
            ])

            if dcUK.userAgent == 'mobile':
                row = [unid, btnDocNo, btnRt, btn1 ]
            else:
                row = [unid, btnDocNo, btnRt, btnEdit, btn1, btn2,
                       _div(f'{d.pageName}\n{d.pageCat}\n{d.published}', className='mCell',
                        **style(borderLeftWidth=1, borderLeftColor='#cff'), s2=1, br=1),
                       btn3cix(f'{dcUK.dbAlias}&{d.unid}', f'_{d.docNo}_ (fields)&info'),
                    # _div(f'{d.D("MODIFIED")}\n{d.MODIFIER}', className='mCell', **style(textAlign='right', color='#aaa'), br=1, s2=1),
                ]
            mainDocs.append(row)
            self.i += 1

        if docs:
            refsDocs[docs[0].unid] = [ [docs[0].unid, _div('qqqqqqqqqqqqqqqq', className='mCell')] ]

        return {'mainDocs': mainDocs, 'refsDocs': refsDocs}

# *** *** ***

