# -*- coding: utf-8 -*- 
'''
Created on 2020.

@author: aon
'''
from common.common import well, today, toWell
from common.api.formTools import _br, style, _div, _field, label, _btnD, _table, _img, _span, _br, labField
from common.api.classPage import Page


# *** *** ***

class a_setting(Page):
    def __init__(self, dc):
        self.title = 'react-py.ru'
        self.jsCssUrl = ['jsv?appDesign/pages/a_setting/a_setting.js']
        self.dbAlias = 'db_pages_2'
        super().__init__(dc)


    def page(self, dcUK):
        return _div(className='setting-page', children=[
            _div(name='setPage', children=self.settingPage()),
            _div(name='setBox', children=self.settingDiv()),
            _div(className='setting-head', children=[_div(className='setting-title')]),
        ])
        
    
    def queryOpen(self, dcUK):
        pass

# *** *** ***
    
    def settingDiv(self):
        return [
            _div(className='setting-head', **style(border=0), children=[
                _span('Бокс', className='setting-title'),
                ' ',
                _field('boxNo_FD', 'fd'),
                _field('hide0', 'chb', ['►', '▼'], title='сложить/показать', char=1, **style(float='right')),
            ]),
            _div(name='boxStyle', children=self.boxStyle(), className='setting-block'),

            _div(className='setting-head', children=[
                _span('Фон', className='setting-title'),
                _field('hide1', 'chb', ['►', '▼'], title='сложить/показать', char=1, **style(float='right')),
                _field('bgStyle', 'chb3', ['цвет|color', 'картинка|image'], name='hide1', **style(width='100%', margin='5px auto')),
            ]),
            _div(name='bgColor', children=self.bgColor(), className='setting-block'),
            _div(name='bgImage', children=self.bgImage(), className='setting-block'),
        
        
            _div(className='setting-head', children=[
                _span('Границы', className='setting-title'),
                _field('hide2', 'chb', ['►', '▼'], title='сложить/показать', char=1, **style(float='right')),
                _field('border', 'chb3', ['равны|borEQ', 'не равны|borNE'], name='hide2', **style(width='100%', margin='5px auto')),
            ]),
            *self.borderStyle(),
    
                
            _div(className='setting-head', children=[
                _span('Тень', className='setting-title'),
                _field('hide3', 'chb', ['►', '▼'], title='сложить/показать', char=1, **style(float='right')),
                _field('shadow', 'chb3', ['снаружи|outside', 'внутри|inset'], name='hide3', **style(width='100%', margin='5px auto')),
            ]),
            self.shadow(),

            _div(className='setting-head', children=[
                _span('Текст', className='setting-title'),
                _field('hide4', 'chb', ['►', '▼'], title='сложить/показать', char=1, **style(float='right')),
                _field('textOrButton', 'chb3', ['простой|showButton', 'редактор|showRtf'], name='hide4', **style(width='100%', margin='5px auto')),
            ]),
            _div(name='textStyle', children=self.textStyle(), className='setting-block'),
    ]


    def borderStyle(self):
        return [
            _div(name='borEQ', className='setting-block', children=[
                *self.brdStyle('')
            ]),
            
            _div(name='borNE', className='setting-block', children=[

                _field('borderSide', 'band', [
                    _div('слева', **style(width=40, height=20)),
                    _div('сверху', **style(width=40, height=20)),
                    _div('справа', **style(width=40, height=20)),
                    _div('снизу', **style(width=40, height=20)),
                ], **style(fontSize=14, color='#048', borderSpacing='5px', borderWidth=0)),

                *self.brdStyle('Left'),
                *self.brdStyle('Top'),
                *self.brdStyle('Right'),
                *self.brdStyle('Bottom'),
            ])
        ]

    rLabel ={'': 'Радиус', 'Left': 'R(лев-ниж)', 'Top': 'R(лев-вер)', 'Right': 'R(пр-вер)', 'Bottom': 'R(пр-ниж)'}
    
    def brdStyle(self, side):
        return [
            *_table( [
                _div(name=f'bor{side}', **style(width='22%', textAlign='center'), children=[
                    _div((side or '\xa0').lower(), **style(textAlign='center', font='bold 9pt Verdana, Arial', color='#048')),
                    _field(f'border{side}Color', 'input-color', colorList='colorList'),
                    _div('Цвет', **style(textAlign='center', font='bold 9pt Verdana, Arial', color='#048')),
                ]),
                
                _div(name=f'bor{side}', **style(paddingLeft=10, fontSize=6, textAlign='center', borderLeftWidth=1, border='0 solid #aaa'),
                    children=[
                        _field(f'border{side}Width', 'slip', [0, 100, 1, 'Ширина', 1000]),
                        _field(f'border{side}Radius', 'slip', [0, 100, 5, self.rLabel[side]], metric='px|%'),
                        _br(),
                ]),
            ]),
            _field(f'border{side}Style', 'band', [
                _div(**style(width=40, border='4px solid #5577cc', height=20, margin='auto')),
                _div(**style(width=40, border='4px dotted #5577cc', height=20, margin='auto')),
                _div(**style(width=40, border='4px dashed #5577cc', height=20, margin='auto')),
                _div(**style(width=40, border='4px double #5577cc', height=20, margin='auto')),
            ], name=f'bor{side}', **style(borderSpacing='5px 5px')),
        ]

    def trans(self, tr, d1, d2, step, digits=0):
        return _div(name=tr, children=_table([
                    style('rowStyle', border=0, padding=0, margin=0),
                    _field(f'{tr}X', 'slip', [d1, d2, step, 'X'], digits=digits, className='label'),
                    _field(f'{tr}Y', 'slip', [d1, d2, step, 'Y'], digits=digits, className='label'),
                ]))
        
        
    def boxStyle(self):
        return [
            *_table(
                [
                    label('ширина'),
                    _field('boxSizeX', 'number', min=5, max=2000, width=50),
                    _field('boxSizeXp', 'fd', className='label'),
                ],
                [
                    label('высота'),
                    _field('boxSizeY', 'number', min=5, max=2000, width=50),
                    _field('boxSizeYp', 'fd', className='label'),
                ]
            ),
            *_table(
                [
                    _field('insideOnly', 'chb', ['привязать'], name='insideOnly', title='запретить плавающему блоку выходить за грницы родителя', className='labell'),
                    _field('fixed', 'chb', ['не двигать'], **style(textAlign='left'), name='insideOnly', title='запретить двигать мышкой плавающий блок', className='labell'),
                ],
                [   style('rowStyle', border=0),
                _field('noIcons', 'chb', ['без иконок'], className='labell'),
                _field('anchor', 'chb', ['якорь'], title='для перехода при клике мышкой', className='labell'),
                ],
                [   style('rowStyle', border=0),
                _field('__', 'chb', ['__'], className='labell'),
                _field('showAnchor', 'fd', name='showAnchor', className='labell' ),
                ]
            ),
            _div(name='zIndex', children=
                _table([
                    _div(' '), label('z-index'),
                    _btnD('\u21D1', 'blPlus', className='metric'),
                    _field('boxLayer', 'fd', name='boxLayer', className='label', **style(textAlign='center')),
                    _btnD('\u21D3', 'blMinus', className='metric'), _div(' ')
                ])
            ),
            
            _div(name='zIndex', className='setting-line'),

            _field('trans', 'band', [
                _div('поворот', **style(width=40, height=20)),
                _div('наклон', **style(width=40, height=20)),
                _div('масштаб', **style(width=45, height=20)),
                _div('сдвиг', **style(width=35, height=20)),
                ], **style(fontSize=14, color='#048', borderSpacing='5px 0', borderWidth=0)
            ),
            self.trans('rotate', 0, 360, 15),
            self.trans('skew', -75, 75, 15),
            self.trans('scale', 0.25, 5, 0.25, 2),
            self.trans('translate', -200, 200, 10),

            # _div('Отступы', **style(marginTop=10, font='bold 12px Verdana', color='#048')),
            # *_table([
                # _field('marginLR', 'slip', [0, 20, 1, 'X'], className='label', **style(width='45%'), metric='em|px'),
                # _field('marginTD', 'slip', [0, 20, 1, 'Y'], className='label', **style(width='45%', paddingLeft=5), metric='em|px')
            # ]),

        ]

        
        
    def textStyle(self):
        def tx_1_2(lcr):
            return [
                _div(className='tx-1'),
                _div(className=f'tx-2-{lcr}'),
                _div(className='tx-1'),
                _div(className=f'tx-2-{lcr}'),
                _div(className='tx-1'),
            ]
        return [
            _field('textAlign', 'band', [
                _div(**style(width=30, margin='auto'), children=tx_1_2('l')),
                _div(**style(width=30, margin='auto'), children=tx_1_2('c')),
                _div(**style(width=30, margin='auto'), children=tx_1_2('q')),
                _div(**style(width=30, margin='auto'), children=tx_1_2('r')),
                ], **style(width='80%', margin='auto', borderSpacing='5px')),
            _div(name='isButton', children=[
                _div('Действие при клике мышкой', className='labell'),
                _field('buttonAction', 'lbsd', ['Отправить введенные данные на сервер (submit)|submit', 'url', 'перейти к якорю', 'javascript'], saveAlias=1, small='2'),
            ]),
            _field('actionText', 'tx', name='actionText'), 
            
            
            _div('Шрифт', className='labell', **style(borderWidth=0)),
            _field('fontFamily', 'lbsd', ['Arial', 'Courier', 'Futura PT'], small='2'),
            *_table( [
                _field('fontSize', 'slip', [1, 100, 1, 'Размер', 200], metric='rem|px', className='label', **style(width=170, paddingTop=10, marginLeft=5)),
                _div(children=[label('Цвет', **style(width=55)), _field('color', 'input-color', **style(marginLeft=20), colorList='colorList')]),
            ]),
            *_table([
                _field('fontWeight', 'chb', ['жирный|bold'], className='label'),
                _field('fontStyle', 'chb', ['курсив|italic'], className='label')
            ]),
            _div('Интервал', **style(marginTop=10, font='bold 12px Verdana', color='#048')),
            *_table([
                _field('letterSpacing', 'slip', [0, 50, 1, 'X', 100], className='label', **style(width='45%'), metric='em|px'),
                _field('lineHeight', 'slip', [0, 5, 0.1, 'Y', 10], digits=2, className='label', **style(width='45%', paddingLeft=5))
            ]),
            _div('Отступы', **style(marginTop=10, font='bold 12px Verdana', color='#048')),
            *_table([
                _field('paddingLR', 'slip', [0, 20, 1, 'X'], className='label', **style(width='45%'), metric='em|px'),
                _field('paddingTD', 'slip', [0, 20, 1, 'Y'], className='label', **style(width='45%', paddingLeft=5), metric='em|px')
            ]),
            _div(**style(margin='auto', width='90%'), children=_table(
                [_field('textIndent', 'slip', [0, 20, 1, 'Параграф'], className='label', metric='em|px')])),
            _div(className='setting-line'),
        ]

    def bgColor(self):
        return [
            *_table( [
                _div(**style(width='20%', textAlign='center'), children=[
                    _span('Цвет', **style(textAlign='center', font='bold 9pt Verdana, Arial', color='#048')),
                    _field('backgroundColor', 'input-color', colorList='colorList')
                ]),
                _div(**style(padding='0 10px', textAlign='center', borderLeftWidth=1, border='0 solid #aaa'), children=[
                    _field('gradient', 'chb', ['градиент'], **style(marginTop=10, float='left', font='bold 9pt Verdana, Arial', color='#048')),
                    _field('gradientColor', 'input-color', name='gradient', colorList='colorList'),
                    _br(),
                    _field('gradientDeg', 'slip', [0, 360, 15, 'Наклон'], name='gradient', className='label', **style(width=160)),
                ]),
            ]),
        ]
    
    def bgImage(self):
        return [
            _field('backgroundImage', 'lbse', [
                '/images/bear.png',
                '/images/24x24LB.png'
                ], small=2, onBlur='setBgImage', placeholder='скопируйте сюда url-ссылку'), #, kbEnter='setBgImage'),
                   
            *_table([
                style('rowStyle', width='100%'),
                _field('bgiSizeX', 'slip', [0, 100, 10, 'X'], className='label', metric='px|%'),
                _field('bgiSizeY', 'slip', [0, 100, 10, 'Y'], className='label', metric='px|%'),
            ]),
            
            *_table([
                style('rowStyle', margin='5px auto', width='100%'),
                _field('repeatX', 'chb', ['повтор X|repeat'], className='label'),
                _field('repeatY', 'chb', ['повтор Y|repeat'], className='label')
            ]),
        ]

    def shadow(self):
        return _div(name='shadow', className='setting-block', children=[
            *_table( [
                _div(**style(width='20%', textAlign='center'), children=[
                    _span('Цвет', **style(textAlign='center', font='bold 9pt Verdana, Arial', color='#048')),
                    _field('shadowColor', 'input-color', colorList='colorList')
                ]),
                _div(**style(paddingLeft=10, textAlign='center', borderLeftWidth=1, border='0 solid #aaa'), children=[
                    _field('shadowX', 'slip', [-100, 100, 1, 'сдвиг x', 1000], **style(display='block')),
                    _field('shadowy', 'slip', [-100, 100, 1, 'сдвиг y', 1000], **style(display='block')),
                    _field('shadowR', 'slip', [0, 100, 1, 'размытие', 1000], **style(display='block')),
                    _field('shadowW', 'slip', [0, 100, 1, 'ширина', 2000], **style(display='block')),
                    _br(),
                ]),
            ]),
        ])




# *** *** ***

    def settingPage(self):
        return [
        _field('docNo', 'fd', className='h3'),
        _div(className='setting-line'),
        
        _field('screen', 'band', [
            _div(className='tb-phone'),
            _div(className='tb-tablet'),
            _div(className='tb-pc', children=[
                _div(className='tb-pc-screen'),
                _div(className='tb-pc-ground',
                    children=[
                        _div(**style(width='35%', borderBottomRightRadius=7)),
                        _div(**style(width='30%', background='#888')),
                        _div(**style(width='35%', borderBottomLeftRadius=7))
                    ]),
            ] ),
        ], className='screens'),
        
        _div(className='setting-line'),
            
        _div(wl=75, **style(width=255), children=_table(
            labField('создан', 'created_FD', 'fd', className='tta'),
            labField('автор', 'creator_FD', 'fd', className='tta'),
            labField('изменен', 'modified_FD', 'fd', className='tta'),
            labField('редактор', 'modifier_FD', 'fd', className='tta'),
            labField('на сайте', 'published', 'tx', className='tta'),
            )
        ),
        _div(className='setting-line'),
        _div(wl=50, **style(width=255), children=_table(
            labField('имя', 'pageName'),
            labField('url', 'pageUrl'),
            labField('кат', 'pageCat'),
            labField('title', 'title'),
            labField('js', 'script'),
            labField('css', 'css'),
            labField('notes', 'notes'),
            )
        ),
        _div(className='setting-line'),
        _div(**style(width=255), children=_table([
            _field('contur', 'chb', ['контур'], **style(textAlign='center'), className='label'),
            _field('reserv', 'chb', ['_'], **style(textAlign='center'), className='label')
            ])
        ),
        _div(className='setting-line'),
        _div(**style(width=270), children=_table([
            _field('gridX', 'slip', [0, 50, 10, 'сетка-x'], className='label'),
            _field('gridY', 'slip', [0, 50, 10, 'сетка-y'], className='label'),
            ])
        ),
        _div(className='setting-line'),
        _div(**style(width=270), children=_table([
            _field('pagePlusDim', 'slip', [1, 5, 0.5, 'Mасштаб'], digits=2, className='label'),
            _div(''),
            # _field('gridY', 'slip', [0, 50, 10, 'сетка-y'], className='label'),
            ])
        ),
            


    ]






