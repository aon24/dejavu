# -*- coding: utf-8 -*- 
'''
AON 2018

'''
from tools.common import well
from tools.DC import config
from tools.first import err, dbg, snd
from tools.checkRights import mainAdmin

from api.formTools import style, _div, _img, _btnD, label, _table, _tab
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
            lsMenu = ['mainCls', 'users', 'life', 'setup', 'admin', 'log', 'logoff']
    
        if config._video_:
            return _div(
                **style(height='100vh', paddingTop=30, overflow='hidden'),
                children=[
                {'video': 'vi', 'id': 'vi', 'preload': 'auto', 'src': 'image?%s' % config._video_, 'loop':'loop', 'muted': 'muted',
                    **style(position='absolute', zIndex=-1, left=0, top=-200,
                            height='calc(100vh + 240px)', minHeight=854, width='100vw', minWidth=1519)
                },        
                self.armPage(panels, dcUK)
                ]
            )
            
        else:
            return _div(
                **style( height='100vh',
                        background='url(/image?bg51.jpg)',
                        backgroundSize='auto 100%',
                        paddingTop=35,
                        overflow='hidden'
                        ),
                children=[
                    self.menu(lsMenu),
                    self.armPage(panels, dcUK)
                    ]
            )
        
        # *** *** ***
    
    
    def menu(self, mlist):
        armMenuButtons = dict(
            mainCls = _btnD('Справочники', 'xopen', 'new?form=w__wells', title='Справочник организации', className='armMenuItem'),
            users = _btnD('Сотрудники', 'statOpen', '', title='Менеджер отчетов', className='armMenuItem'),
            
            setup = _btnD('Setup', 'xopen', 'setup?SETUP', title='настройки', className='armMenuItem'),
            admin = _btnD('Admin', 'xopen', 'newdoc?&availablebysrv', title='Список журналов', className='armMenuItem'),
            
            life = _btnD('Life', 'reload', title='Перезагрузка справочников', className='armMenuItem'),
            logoff = _btnD('Выход', 'logoff', title='Logoff', className='armMenuItem'),
            
            log = _btnD('Log', 'xopen', 'new?form=ilog', title='syslog', className='armMenuItem'),
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
        if dcUK.userAgent == 'mobile':
            wOwl = 390
            zOwl = 200
            s1 = '''
'''
            s2 = '''
'''
        else:
            s1 = '''Sova.online - отечественная бесплатная
платформа для подготовки, продажи
и проведения онлайн-курсов.

Программ может быть установлена
на ПК под ОС Windows7+
(с доступом из локальной сети)
или на арендуемый вами
VDS (VPS) сервер под
ОС Linux с доступом
из интернета.''' # образовательные проекты
            s2 = ''
            wOwl = 800
            zOwl = 340
        owl = _div( **style(display='table', width='100%',
                background='url(image?owl.png) center top 10px no-repeat', 
                backgroundSize=zOwl),
            children=_table(
                [
                _div(s1, br=1,className='owlTab'),
                _div(s2, br=1,className='owlTab', **style(textAlign='right')),
                ],
                [ _div(**style(width='100%'), children=_table([
                _div(children=[
                        _btnD('HTML', 'xopen', 'pages', className='btnArm'),
                        label('', 20),
                        _btnD('Рассылки', 'xopen', 'new?form=a__mailing', className='btnArm')
                    ], **style(padding='15px 10px 0 5px')),
                _div('sova.online\xa0\xa0', className='owlOnline'),
                _div(children=[
                        _btnD('Платежи', 'xopen', 'new?form=p__payments', className='btnArm'),
                        label('', 20),
                        _btnD('Аренда', 'xopen', 'new?form=b__booking', className='btnArm'),
                    ], **style(padding='15px 5px 0 0')),
                ]))] ,
            )
        )
        return _div(**style(height='calc(100vh - 35px', overflowY='auto'),
                    children=[_div(**style(width=wOwl, margin='auto'),
                    children=[
            owl, 
            _div(**style(width=300, margin='auto', boxShadow='0 0 12px 9px rgb(190,204,215)')),
            _div(**style(display='table', width=400, margin='auto', borderSpacing='30px 5px'), children=[
                _btnD('Курсы', 'xopen', 'new?form=v__tracks', className='btnArm'),
                _btnD('Группы', 'xopen', 'new?form=g__groups', className='btnArm'),
                _btnD('Студенты', 'xopen', 'new?form=u__people', className='btnArm'),
            ]),
            _tab('armHelp', 110, [
                ['Приступая к работе', _div('b1 Курсы')],
                ['HTML-редактор', _div('b1 Курсы')],
                ['Люди', _div('b1 Консультации')],
                ['Курсы', _div('b1 Общение')],
                ['e-mail рассылки', _div('b1 Рассылки')],
                ['Платежи', _div('b1 Платежи')],
                ['Аренда помещений', _div('b1 Платежи')],
        ]),
            
        ])])
    # *** *** ***

    def queryOpen(self, dcUK):
        dcUK.doc.userName = dcUK.userName
        dcUK.doc._page_ = 1
        # mainDName, ouDName = getOUdname(userName)

    # *** *** ***






