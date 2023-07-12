# -*- coding: utf-8 -*-
'''
Created on 7 apr 2018

@author: aon

'''
from api.viewTools import docNoPreview, btn3cix
from api.formTools import _div, style, _btnD, _field
from api.classReview import Review

# *** *** ***

w = [{'width': 80}, {'minWidth': 70}, {'minWidth': 90},
     {'width': 70}, {'width': 140},
     {'width': 110}, {'width': 75}]


class ViewPages(Review):

    def paging(self, dcUK):
        self.dir_ = dcUK.dir_ or '0'
        docs = self.viewReload(dcUK)

        mainDocs = []
        self.i = 0

        i = 0
        for d in docs:
            i += 1
            unid = d.unid + ('+' if d.published else '')
            dba = f'dbAlias={dcUK.dbAlias}&unid={d.unid}'

            # форма a_design в режиме readOnly
            btnDocNo = docNoPreview(f'{d.docNo}\n{d.D("created")}', dcUK.dbAlias, d, width=100)

            btnEdit = _div(className='mCell', **style(width=100, verticalAlign='middle'), children=[
                _btnD('изменить', 'xopen_', f'{dba}&mode=edit',
                    className='rsvTop armBtnRed')])

            if dcUK.userAgent == 'mobile':
                row = [unid, btnDocNo]  # , btnRt,]# btn1 ]
            else:
                row = [unid, btnDocNo, btnEdit,  # btn1, btn2, btnRt,
                    _div(f'{d.pageName}\n{d.pageCat}\n{d.published}', className='mCell',
                            **style(borderLeftWidth=1, borderLeftColor='#cff'), s2=1, br=1),

                    # _div(**style(width=250, height=150), children=[
                    #     _field(f'r_{i}', 'box')
                    # ]),

                    btn3cix(dcUK.dbAlias, d.unid, f'_{d.docNo}_ (fields)&info'),
                ]
            mainDocs.append(row)
            self.i += 1

        return {'mainDocs': mainDocs}

# *** *** ***


class ViewPeople(Review):
    sortBy = 'fullName'
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

            btnFullName = docNoPreview(fullName, dcUK.dbAlias, d, br='p')

            phoneEmail = _div(f'{d.phone}\n{d.email}', className='mCell',
                **style(width=140, **stl, borderLeftWidth=1, borderLeftColor='#cff'), br=1)

            btnEdit = _div(className='mCell', **style(width=120, verticalAlign='middle'), children=[
                    _btnD('изменить', 'xopen', f'opendoc?dbAlias={dcUK.dbAlias}&unid={d.unid}&mode=edit',
                        className='armBtn armBtnRed', **style(display='block', margin=3))])

            # toHtml, toReact
            btn2 = _div(className='mCell', **style(verticalAlign='middle', textAlign='left'), children=[
                _btnD('группы', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (html)&a_toHtml',
                    **style(minWidth=70), className='forView fvh'),
                _btnD('рассылки', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (React)&a_toReact',
                    **style(minWidth=85), className='forView fvh'),
                _btnD('платежи', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (React)&a_toReact',
                    **style(minWidth=80), className='forView fvh'),
            ])

            if dcUK.userAgent == 'mobile':
                row = [ d.unid, btnFullName, phoneEmail]
            else:
                row = [d.unid, btnFullName, phoneEmail, btnEdit, btn2,
                        btn3cix(f'{dcUK.dbAlias}&{d.unid}', f'_{ls[0]}_ (fields)&info'),
                ]
            mainDocs.append(row)
            self.i += 1

        return {'mainDocs': mainDocs}

# *** *** ***


class ViewTracks(Review):
    sortBy = 'docNo'
    reverse = True
    dir_ = 'T'

    def paging(self, dcUK):
        docs = self.viewReload(dcUK)

        mainDocs = []
        self.i = 0
        stl = {'letterSpacing': 1, 'font': 'normal 14px Arial'}

        i = 0
        for d in docs:
            i += 1
            unid = d.unid + ('+' if d.STATUS == 'Обучение' else '')
            btnDocNo = docNoPreview(f'{d.docNo}\n{d.D("created")}', dcUK.dbAlias, d, 84)

            trackTitle = _div(f'{d.trackTitle}', className='mCell',
                **style(**stl, borderLeftWidth=1, borderLeftColor='#cff'), br=1)

            btnOpen = _div(className='mCell', **style(width=120, verticalAlign='middle'), children=[
                    _btnD('перейти', 'xopen', f'new?dbAlias={d.dbAlias}&form=t__list',
                        **style(display='block'))])

            btnEdit = _div(className='mCell', **style(width=120, verticalAlign='middle'), children=[
                    _btnD('изменить', 'xopen', f'opendoc?dbAlias={dcUK.dbAlias}&unid={d.unid}&mode=edit',
                        className='armBtn armBtnRed', **style(display='block', margin=3))])

            # toHtml, toReact
            btn2 = _div(className='mCell', **style(width=100, verticalAlign='middle', textAlign='left'), children=[
                _btnD('группы', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (html)&a_toHtml',
                    **style(minWidth=70), className='forView fvh'),
                # _btnD('рассылки', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (React)&a_toReact',
                    # **style(minWidth=85), className='forView fvh'),
                # _btnD('платежи', 'preview', f'{dcUK.dbAlias}&{d.unid}&_{d.docNo}_ (React)&a_toReact',
                    # **style(minWidth=80), className='forView fvh'),
            ])

            if dcUK.userAgent == 'mobile':
                row = [unid, btnDocNo, trackTitle, btnOpen]
            else:
                row = [unid, btnDocNo, trackTitle, btnOpen, btnEdit, btn2,
                        btn3cix(f'{dcUK.dbAlias}&{d.unid}', f'_{d.docNo}_ (fields)&info'),
                ]
            mainDocs.append(row)
            self.i += 1

        return {'mainDocs': mainDocs}

# *** *** ***


class ViewWell(Review):
    sortBy = 'listName'
    reverse = False
    dir_ = 'L'

    def paging(self, dcUK):
        docs = self.viewReload(dcUK)

        mainDocs = []
        self.i = 0
        stl = {'letterSpacing': 1, 'font': 'normal 14px Arial'}

        for d in docs:
            listName = docNoPreview(d.listName, dcUK.dbAlias, d)

            notes = _div(d.notes, className='mCell',
                **style(width=240, **stl, borderLeftWidth=1, borderLeftColor='#cff'), br=1)

            btnEdit = _div(className='mCell', **style(width=120, verticalAlign='middle'), children=[
                    _btnD('изменить', 'xopen', f'opendoc?dbAlias={dcUK.dbAlias}&unid={d.unid}&mode=edit',
                        className='armBtn armBtnRed', **style(display='block', margin=3))])

            if dcUK.userAgent == 'mobile':
                row = [d.unid, listName]
            else:
                row = [d.unid, listName, notes, btnEdit,
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
        for d in docs:
            unid = d.unid + ('+' if d.published else '')
            btnDocNo = docNoPreview(f'{d.docNo}\n{d.D("created")}', dcUK.dbAlias, d, 84)

            row = [unid, btnDocNo, d.GROUPNAME]
            mainDocs.append(row)

        return {'mainDocs': sorted(mainDocs, key=lambda x: x[2], reverse=True)}

# *** *** ***

