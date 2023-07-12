# -*- coding: utf-8 -*-
'''
AON 2018

'''
from tools.common import well
from tools.DC import config
from tools.first import snd
from tools.checkRights import mainAdmin

from api.formTools import pyramid, pyramidInit, style, _div, _btnD, _field, _table, _tab
from api.classPage import Page

# *** *** ***


class irm(Page):

    def __init__(self, form):
        self.title = 'sova.online'
        self.noCaching = True
        self.dbAlias = 'arm'
        self.jsCssUrl = [
            'jsv?api/react/_pyramid.js',
            'jsv?api/pages/irm/irm.js',
            'jsv?api/pages/irm/irm.css',
            'jsv?api/react/view.css']
        super().__init__(form)

# *** *** ***

    def page(self, dcUK):
        who = well('who', dcUK.userName)
        if who:
            whoAcrScheme = who.A('ACRSCHEME') or 'guest'
        else:
            whoAcrScheme = 'guest'

        if len(whoAcrScheme) == 1 and whoAcrScheme[0] == 'student':
            panels = 'student'
            lsMenu = ['logoff']
        elif 'admin' in whoAcrScheme:
            panels = 'admin'
            lsMenu = ['logoff']
        else:
            panels = 'guest'
            # lsMenu = ['mainCls', 'users', 'life', 'setup', 'admin', 'log', 'logoff']
            # lsMenu = ['mainCls', 'life', 'log', 'logoff']
            lsMenu = ['showHostAdr', 'log', 'logoff']

        return _div(
            className='page51', **style(paddingTop=35),
            children=[
                pyramid(),
                self.menu(lsMenu),
                self.armPage(panels, dcUK)
                ]
        )

        # *** *** ***

    def menu(self, mlist):
        armMenuButtons = dict(
            mainCls=_btnD('Справочники', 'xopen', 'new?form=w__wells', title='Справочник организации', className='armMenuItem'),
            life=_btnD('Life', 'reload', title='Перезагрузка справочников', className='armMenuItem'),
            logoff=_btnD('Выход', 'logoff', title='Logoff', className='armMenuItem'),
            showHostAdr=_btnD('Адрес', 'showHostAdr', title='адрес компьютера в сети', className='armMenuItem'),

            log=_btnD('Log', 'xopen', 'new?form=ilog', title='syslog', className='armMenuItem'),

        )

        return _div(
            className='armMenu',
            children=[
                _div(
                    **style(display='table', width='auto', margin='auto'),
                    children=[armMenuButtons[x] for x in mlist]
                )
            ]
        )

    # *** *** ***

    def armPage(self, panels, dcUK):
        owlText = '''mobile
mobile
        mobile'''
        if dcUK.userAgent == 'mobile':
            wOwl = 390
        else:
            wOwl = 800
        hOwl = 340

        bottons = [
            _btnD('3d\nпомещения', 'xopen', 'pages?viewKey=rooms&mode=new&form=a__pages', className='btnArm'),
            _btnD('3d\nмебель', 'xopen', 'pages?viewKey=cases&mode=new&form=a__pages', className='btnArm'),
            _btnD('Все\n2d/3d/A', 'xopen', 'pages?viewKey=all&mode=new&form=a__pages', className='btnArm'),
        ]
        owl = _div(**style(
                    height=hOwl, position='relative',
                    background='url(image?owl.png) center top no-repeat',
                    backgroundSize='contain'),
                children=[
                    _field('demo', 'page', url=f"dbAlias=draft&unid=2e66524bfe754c638b1b21136f633ed1&rsMode=mockup"),
                    _div('sova.online\xa0\xa0', className='owlOnline')
            ])

        return _div(**style(height='calc(100vh - 35px)'), children=[
                    _div(**style(maxWidth=wOwl, margin='0 auto'), children=[
                        owl,
                        *_table(bottons, **style('rowStyle', margin='auto', width=390, borderSpacing='20px 0')),
                        _div(owlText, br='p', className='owlText'),
                    ])
        ])

    # *** *** ***

    def queryOpen(self, dcUK):
        dcUK.doc.userName = dcUK.userName
        dcUK.doc._page_ = 1
        dcUK.doc.hostAddress_FD = config.hostAddress

        # mainDName, ouDName = getOUdname(userName)

        pyramidInit(dcUK)

    # *** *** ***

