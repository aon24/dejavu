# -*- coding: utf-8 -*- 
'''
Created on 7 apr 2018

@author: aon

'''
from api.formTools import _div, style, _btnD, btn3cix
from api.classReview import Review

# *** *** ***

w = [{'width': 80}, {'minWidth': 70}, {'minWidth': 90},
     {'width': 70}, {'width': 140},
     {'width': 110}, {'width': 75}]

class ViewPages(Review):
    def paging(self, dcUK):
        docs = self.viewReload(dcUK)

        mainDocs = []
        refsDocs = {}
        self.i = 0

        i = 0
        for d in docs:
            i += 1
            btnDocNo = [d.unid + ('+' if d.published else ''),
                    _btnD(f'{d.docNo}\n{d.D("created")}', 'previewNew', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (preview)&a_design',
                        title='быстрый просмотр (fast preview)', s2=1, className='docNo mCell', style=w[0], br=1)]
                        
            btnRt = _div(className='mCell', **style(**w[1], verticalAlign='middle'), children=[
                    _btnD('Real time', 'xopen', f'opendoc?dbAlias={dcUK.dbAlias}&unid={d.unid}&form=a_viewer',
                        title='просмотр изменений в реальном времени',
                        **style(display='block'))])

            btnEdit = _div(className='mCell', **style(**w[2], verticalAlign='middle'), children=[
                    _btnD( 'изменить', 'xopen', f'opendoc?dbAlias={dcUK.dbAlias}&unid={d.unid}&mode=edit',
                        className='armBtn armBtnRed', **style(display='block', margin=3))])

            # open, publish
            btn1 = _div(className='mCell', **style(**w[3], verticalAlign='middle', textAlign='left'), children=[ 
                # _btnD( '\xa0', 'openHtml', f'{dcUK.dbAlias}&{d.unid}&{d.docNo}',
                _btnD( '\xa0', 'xopen', f'openpage?dbAlias={dcUK.dbAlias}&unid={d.unid}&mode=html&docno={d.docNo}',
                        title='просмотр', className='forView_o'),
                _btnD( '\xa0', 'publish', f'dbAlias={dcUK.dbAlias}&unid={d.unid}',
                        title='опубликовано', className='forView_p'),
            ])
            
            # toHtml, toReact
            btn2 = _div(className='mCell', **style(**w[4], verticalAlign='middle', textAlign='left'), children=[
                _btnD( 'Html', 'previewNew', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (html)&a_toHtml',
                    title='HTML', className='forView fvh'),
                _btnD( 'React', 'previewNew', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (React)&a_toReact',
                    title='React JS', className='forView fvr'),
            ])


            if dcUK.userAgent == 'mobile':
                row = [ *btnDocNo, btnRt, btn1 ]
            else:
                row = [*btnDocNo, btnRt, btnEdit, btn1, btn2,
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
# *** *** ***
# *** *** ***

class ViewPeople(Review):
    sortBy ='fullName'
    reverse = False
    
    def paging(self, dcUK):
        docs = self.viewReload(dcUK)

        mainDocs = []
        self.i = 0
        stl = {'letterSpacing': 1, 'font': 'normal 14px Arial'}

        i = 0
        for d in docs:
            i += 1
            ls = d.fullName.split() + ['', '', '']

            fullName = f'{ls[0]}\n{ls[1]}'
            if ls[2]:
                fullName += f'\n{ls[2]}'
                
            
            btnFullName = [d.unid + ('+' if d.status == 'сотрудник' else ''),
                    _btnD(fullName, 'previewNew', f'{dcUK.dbAlias}&{d.unid}&_{ls[0]}_ (preview)&u_human',
                        title='быстрый просмотр (fast preview)', s2=1, className='mCell docNo', br='p',
                        **style(width=140, **stl)
                    )
            ]

            phoneEmail = _div(f'{d.phone}\n{d.email}', className='mCell',
                **style(width=140, **stl, borderLeftWidth=1, borderLeftColor='#cff'), br=1)

            btnEdit = _div(className='mCell', **style(width=120, verticalAlign='middle'), children=[
                    _btnD( 'изменить', 'xopen', f'opendoc?dbAlias={dcUK.dbAlias}&unid={d.unid}&mode=edit',
                        className='armBtn armBtnRed', **style(display='block', margin=3))])

            # toHtml, toReact
            btn2 = _div(className='mCell', **style(verticalAlign='middle', textAlign='left'), children=[
                _btnD( 'группы', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (html)&a_toHtml',
                    **style(minWidth=70), className='forView fvh'),
                _btnD( 'рассылки', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (React)&a_toReact',
                    **style(minWidth=85), className='forView fvh'),
                _btnD( 'платежи', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (React)&a_toReact',
                    **style(minWidth=80), className='forView fvh'),
            ])
            
            if dcUK.userAgent == 'mobile':
                row = [ *btnFullName, phoneEmail]
            else:
                row = [*btnFullName, phoneEmail, btnEdit, btn2,
                        btn3cix(f'{dcUK.dbAlias}&{d.unid}', f'_{ls[0]}_ (fields)&info'),
                ]
            mainDocs.append(row)
            self.i += 1
        
        return {'mainDocs': mainDocs}

# *** *** ***
# *** *** ***
# *** *** ***

class ViewTracks(Review):
    sortBy ='docNo'
    reverse = True
    
    def paging(self, dcUK):
        docs = self.viewReload(dcUK)

        mainDocs = []
        self.i = 0
        stl = {'letterSpacing': 1, 'font': 'normal 14px Arial'}

        i = 0
        for d in docs:
            i += 1
            
            btnDocNo = [d.unid + ('+' if d.published else ''),
                    _btnD(f'{d.docNo}\n{d.D("created")}', 'previewNew', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (preview)&v_track',
                        title='быстрый просмотр (fast preview)', s2=1, className='docNo mCell', style=w[0], br=1)]
                        

            phoneEmail = _div(f'{d.phone}\n{d.email}', className='mCell',
                **style(width=140, **stl, borderLeftWidth=1, borderLeftColor='#cff'), br=1)

            btnEdit = _div(className='mCell', **style(width=120, verticalAlign='middle'), children=[
                    _btnD( 'изменить', 'xopen', f'opendoc?dbAlias={dcUK.dbAlias}&unid={d.unid}&mode=edit',
                        className='armBtn armBtnRed', **style(display='block', margin=3))])

            # toHtml, toReact
            btn2 = _div(className='mCell', **style(verticalAlign='middle', textAlign='left'), children=[
                _btnD( 'группы', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (html)&a_toHtml',
                    **style(minWidth=70), className='forView fvh'),
                _btnD( 'рассылки', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (React)&a_toReact',
                    **style(minWidth=85), className='forView fvh'),
                _btnD( 'платежи', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (React)&a_toReact',
                    **style(minWidth=80), className='forView fvh'),
            ])
            
            if dcUK.userAgent == 'mobile':
                row = [ *btnDocNo, phoneEmail]
            else:
                row = [*btnDocNo, phoneEmail, btnEdit, btn2,
                        btn3cix(f'{dcUK.dbAlias}&{d.unid}', f'_{d.docNo}_ (fields)&info'),
                ]
            mainDocs.append(row)
            self.i += 1
        
        return {'mainDocs': mainDocs}

# *** *** ***

class ViewWell(Review):
    sortBy ='listName'
    reverse = False
    
    def paging(self, dcUK):
        docs = self.viewReload(dcUK)

        mainDocs = []
        self.i = 0
        stl = {'letterSpacing': 1, 'font': 'normal 14px Arial'}

        for d in docs:
            name = _btnD(d.listName, 'previewNew', f'{dcUK.dbAlias}&{d.unid}&_{d.listName}_ (preview)&w_list',
                title='быстрый просмотр (fast preview)', className='docNo mCell',
                **style(width=140, **stl, borderLeftWidth=1, borderLeftColor='#cff'))
            
            # name = _div(d.listName, className='mCell',
                # **style(width=140, **stl, borderLeftWidth=1, borderLeftColor='#cff'), br=1)

            notes = _div(d.notes, className='mCell',
                **style(width=240, **stl, borderLeftWidth=1, borderLeftColor='#cff'), br=1)

            btnEdit = _div(className='mCell', **style(width=120, verticalAlign='middle'), children=[
                    _btnD( 'изменить', 'xopen', f'opendoc?dbAlias={dcUK.dbAlias}&unid={d.unid}&mode=edit',
                        className='armBtn armBtnRed', **style(display='block', margin=3))])
            
            if dcUK.userAgent == 'mobile':
                row = [ d.unid, name]
            else:
                row = [ d.unid, name, notes, btnEdit,
                        btn3cix(f'{dcUK.dbAlias}&{d.unid}', f'_{d.name}_ (fields)&info'),
                ]
            mainDocs.append(row)
            self.i += 1
        
        return {'mainDocs': mainDocs}

# *** *** ***

class ViewGroups(Review):

    def paging(self, dcUK):
        docs = self.viewReload(dcUK)
    
        mainDocs = []

        self.i = 0
        stl = {'letterSpacing': 1, 'font': 'normal 14px Arial'}

        for d in docs:
            name = _btnD(d.groupName+'\nq\nq', 'openInDiv', f'{dcUK.dbAlias}&{d.unid}',
                className='docNo mCell',
                **style(width=140, **stl, borderLeftWidth=1, borderLeftColor='#cff'))
            
            row = [d.unid, name]
            mainDocs.append(row)
            self.i += 1

        return {'mainDocs': mainDocs}
    
# *** *** ***










