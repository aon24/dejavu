# -*- coding: utf-8 -*-
'''
Created on 2020.

@author: aon
'''
from api.formTools import _tab, style, _div, _field, label, _btnD, _table, _span, labField, _br, labell, labelc, _teg
from api.classPage import Page

# *** *** ***


class a_setting(Page):
    delay = 1000

    def __init__(self, form):
        self.title = 'Setting'
        self.jsCssUrl = ['jsv?api/pages/a_setting/a_setting.js',
                         'jsv?api/pages/a_setting/table.js',
                         'jsv?api/pages/a_setting/table.css'
                        ]
        self.dbAlias = 'db_pages_2'
        super().__init__(form)

    def page(self, dcUK):
        self.d3 = dcUK.key
        return _div(className='setting-page', children=[
            _div(name='setPage', children=self.settingPage()),
            _div(name='setBox', children=self.settingDiv()),
        ])

    def queryOpen(self, dcUK):
        pass

# *** *** ***

    def settingPage(self):
        if self.d3:
            screen = _field('screen', 'band', [
                _div(className='tb-pc', children=[
                    _div(className='tb-pc-screen'),
                    _div(className='tb-pc-ground',
                        children=[
                            _div(**style(width='35%', borderBottomRightRadius=7)),
                            _div(**style(width='30%', background='#888')),
                            _div(**style(width='35%', borderBottomLeftRadius=7))
                        ]),
                ]),
                _div(className='tb-phone'),
            ], className='screens')
        else:
            screen = _field('screen', 'band', [
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
                ]),
            ], className='screens')

        body = [
           screen,

            _div(className='setting-line'),
            _div(wl=50, **style(width=255), children=_table(
                    labField('проект', 'project'),
                    labField('имя', 'pageName'),
                    labField('url', 'pageUrl'),
                    labField('title', 'title'),
                    # labField('js', 'script'),
                    # labField('css', 'css'),
                    labField('notes', 'notes'),
                    labField('key', 'key', 'lbsd', ['Помещения|rooms', 'Мебель|cases', 'Стены|walls', 'Дом|home', '2d html|html', 'Архив|Archive'], alias=1, small='2'),
                )
            ),
            _div(className='setting-line'),
            _div(**style(width=255, paddingBottom=5), children=_table([
                _field('phoneContur', 'chb', ['контур'], className='labelc'),
                # _field('pagePlusPreview', 'chb', ['preview'], className='labelc')
                ])
            ),

            # not self.d3 and _div(className='setting-line'),
            # not self.d3 and _div(**style(width=270), children=_table([
                # _field('pagePlusDim', 'slip', [1, 5, 0.5, 'Mасштаб'], digits=2, className='label'),
                # _div(''),
                # ])
            # ),

            # not self.d3 and _div(className='setting-line'),
            # not self.d3 and _field('table', 'chb', ['таблица'], **style(margin=10, textAlign='center')),
            # not self.d3 and _div(name='isTable', children=[
    # #            _tab(30, [ self.tabItem(i) for i in range(1, 10) ]),
                # _field('tableSize', 'slip', [0, 9, 1, 'число закладок'], className='label', **style(display='block', margin='10px auto', width=200)),
                # _btnD('создать', 'crtTable', **style(margin='10px auto', width=100))
            # ]),
        ]

        # ***

        return [
        _div(**style(textAlign='center'), children=[_field('docNo_FD', 'fd', className='h3')]),
        _div(className='setting-line'),

        *body,

        _div(className='setting-line'),

        _div(wl=75, **style(width=255, marginBottom=5), children=_table(
            labField('создан', 'created_FD', 'fd', className='tta', **style(display='table-cell')),
            labField('автор', 'creator_FD', 'fd', className='tta', **style(display='table-cell')),
            labField('изменен', 'modified_FD', 'fd', className='tta', **style(display='table-cell')),
            labField('редактор', 'modifier_FD', 'fd', className='tta', **style(display='table-cell')),
            labField('закрыт' , 'closed', 'dt') if self.d3 else
            labField('опубликован', 'published', 'dt'),
            )
        ),
    ]

    # *** *** ***

    # def tabItem(self, i):
        # f = _div(**style(padding=10), children=[
            # _field(f'tabBtn_{i}', 'chb', ['добавить заголовок']), _field(f'tab_{i}')])
        # return f'T{i}', f

    # *** *** ***

    def settingDiv(self):

        return [

         # типы стрелок
        _div(name='arrow', id='arrow', children=self.arrow()),

        # общие поля rooms
        _div(name='is3d0', **style(background='#ffd8d8'),
            children=self.is3d0()),

        # свойства rooms: ширина, длина, высота, Толщина стен
        _div(name='is3d1',
            children=self.is3d1()),

        # свойства стены
        _div(name='walls',
            children=self.is3wall1()),

        # таблица внутри 3д-блока
        _div(name='m3tab', **style(background='#f7d98b'), children=self.m3tab()),
        
        # общие поля одиноких стен и кирпичей: bb3d2, поворот , наклон
        _div(name='mmmNotRooms', **style(background='#f7d98b'), children=self.mmmNotRooms()),

        # свойства одинокого блокa
        _div(name='bricksOne', children=self.bricksOne()),
        _div(name='bricksEdge', children=self.bricksEdge()),

        # свойства блокa в стене
        _div(name='bricksM3t', children=self.bricksM3t()),
        
        # свойства box: bb, масштаб, см/мм, создать 3д
        _div(name='bb', children=self.box2d0()),

        # свойства 3d-rooms: показать потолок, пер-ва, cm/mm, угол скрытия etc
        _div(name='is3d1',
            children=self.is3d2()),

        # свойства стены
        _div(name='walls',
            children=self.is3wall2()),

        # мебель
        _div(name='furniture',
            children=self.furniture()),

        # fixes, lineOff, insideOff
        _div(name='is3d4', **style(background='#ffd8d8'),
            children=self.is3d4()),

        _div(name='tumba', className='tumba',
            children=self.tumba()),

        # все свойства бокса, кроме фона
        _div(name='bb', children=self.box2d1())
    ]
    # *** *** ***

    # bb3d, поворот 3d, наклон 3d
    def is3d0(self):
        return [
            _field('bb3d', 'band', ['\xa03d \xa0', 'стены', 'мебель', 'эл-ка'],
                **style(fontSize=14, color='#048', borderSpacing='4px')
            ),

            *_table([
                _field('rotate3Z', 'slip', [-360, 360, 15, 'поворот'], className='label'),
                _field('rotate3X', 'slip', [-90, 90, 15, 'наклон'], className='label'),
            ]),

            _div(name='wedWall', **style(padding='3px 0'), children=[
                _div(className='setting-line', **style(margin='3px 0 0 0')),
                labelc('Показать'),
                _field('wedWall', 'chb3', ['\xa0\xa0Все стены\xa0|wed1', 'Только одну|wed2'], noEmpty=1, **style(margin='0 auto')),
            ]),
            
            _div(className='setting-line'),
            _div(className='setting-head', children=[
                _span('Масштаб', className='setting-title'),
                _field('hide33', 'chb', ['▼', '►'], title='сложить/показать', char=1, **style(float='right')),
            ]),
            _field('scale3d', 'slip', [0.05, 2, 0.05, ' ', 10], name='hide33', digits=2, className='label', **style(margin='0 auto 7px'), delay=self.delay),
            _field('cm', 'chb3', ['размер в см|cm', 'размер в мм|mm'], name='hide33', noEmpty=1, **style(margin='0 auto')),

            # фасад/грани для стены
            _div(name='wall_wed', **style(paddingBottom=3, background='#ffe39c'), children=[
                    _div(className='setting-line', **style(margin='0px 0 0 0')),
                    labelc('Редактировать 3d блок (is3d0)'),
                    _field('wall_wed', 'band', ['таблица', 'фасад', 'грани'], **style(margin='0 auto')),
              ]),
        ]

    # *** *** ***

    # Размеры, наклон стен
    def is3d1(self):
        return [
            _div(className='setting-line'),

            _div(children=_table(
                [
                    labelc('ширина'), labelc('длина'), labelc('высота')
                ],
                [
                    style('rowStyle', border=0, padding=0, margin=0),
                    _field('is3dX', 'number', max=100000, digits=1, width=70, className='label labelc', delay=self.delay),
                    _field('is3dY', 'number', max=100000, digits=1, width=70, className='label labelc', delay=self.delay),
                    _field('is3dZ', 'number', max=100000, digits=1, width=70, className='label labelc', delay=self.delay)
                ]
            )),
            _div(children=_table([
                label('Толщина стен', **style(verticalAlign='middle')),
                _field('w3', 'number', max=100000, digits=1, width=50, className='label labelc'),
                 label(' ')
            ])),
        ]

    def is3d2(self):
        return [
            # показать потолок
            _div(className='setting-line'),
            _div(**style(width=180, margin='auto', border='0 solid #555', borderBottomWidth=1),
                children=[_field('coverOn', 'chb', ['показать потолок'])
            ]),

            # перспектива
            _div(children=[
                _field('persOn', 'chb', ['перспектива'], **style(margin=3, textAlign='center')),
                _div(name='perspective', children=_table(
                    [
                        _field('perspectiveOriginX', 'slip', [0, 100, 1, 'X'], className='label'),
                        _field('perspectiveOriginY', 'slip', [0, 100, 1, 'Y'], className='label'),
                    ],
                    [
                        _field('perspective', 'slip', [100, 5000, 100, 'Z'], className='label'),
                    ]
                )),
            ]),
            _div(className='setting-line'),

            # размер в см|mm

            * _table([
                _field('angleHide', 'slip', [0, 90, 5, 'угол скрытия стен'], className='label labelc'),
                _div(' ', **style(width=10, border='0px solid #888', borderRightWidth=1)),
                _field('sweep', 'slip', [0, 90, 5, 'угол наклона стен'], className='label labelc'),
            ]),

            #  копировать удалить
            _div(className='setting-line'),
            _div(children=_table([
                    _btnD('Копировать', 'copy3d'),
                    _btnD('Удалить 3d', 'del3d', className='rsvTop armBtnRed'),
                ], **style('rowStyle', borderSpacing='8px 0'))
            ),

            # тень для 3д
            _div(className='setting-head', children=[
                _span('Тень', className='setting-title'),
                _field('hide31', 'chb', ['▼', '►'], title='сложить/показать', char=1, **style(float='right')),
            ]),

            _div(name='shadow3', children=[
                _div(className='setting-line'),
                *_table([
                    _div(**style(width='20%', textAlign='center'), children=[
                        _span('Цвет', **style(textAlign='center', font='bold 9pt Verdana, Arial', color='#048')),
                        _field('shadowColor3', 'input-color', colorList='rainbow')
                    ]),
                    _div(**style(paddingLeft=10, textAlign='center', borderLeftWidth=1, border='0 solid #aaa'), children=[
                        _field('shadowW3', 'slip', [0, 200, 1, 'ширина', 2000], **style(display='block')),
                        _field('shadowR3', 'slip', [0, 200, 1, 'размытие', 2000], **style(display='block')),
                        _br(),
                    ]),
                ]),
            ]),
        ]

    # *** *** ***

    def is3d4(self):
        return [
            _div(className='setting-line'),
            *_table([
                _field('mmm_fixed', 'chb', ['не двигать'], title='запретить двигать мышкой 3d блок'),
                _field('turnOn', 'chb', ['вращать']),
            ],
            [_div('', **style(height=5))],
            [
                _field('lineOff', 'chb', ['скрыть\xa0размер'], title='не показывать линии с размерами'),
                _field('insideOff', 'chb', ['скрыть\xa0мебель'], title='не показывать линии с размерами'),
            ]),
            _div(className='setting-line'),
        ]

    # *** *** ***
    
    def m3tab(self):
        return [
            labelc('Редактировать 3d блок (m3tab)'),
            _field('m3tab_wed', 'band', ['таблица', 'фасад', 'грани'], **style(margin='0 auto 5px')),

            # _div(className='setting-line', **style(margin=0)),
            # *_table(
            #     [ labelc('ширина'), labelc('высота'), labelc('глубина') ],
            #     [
            #         style('rowStyle', border=0, padding=0, margin=0),
            #         _field('m3tab_is3dX', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
            #         _field('m3tab_is3dY', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
            #         _field('m3tab_is3dZ', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
            #     ],
            # ),
            # _div(className='setting-line', **style(margin=3)),
        ]
        
    # *** *** ***
    
    def mmmNotRooms(self):
            return [
            *_table([
                _field('m3table_rotate3Y', 'slip', [-360, 360, 15, 'поворот'], className='label'),
                _field('m3table_rotate3X', 'slip', [-90, 90, 15, 'наклон'], className='label'),
            ]),

            _div(className='setting-line'),

            _div(className='setting-head', children=[
                _span('Масштаб', className='setting-title'),
                _field('m3table_hide33', 'chb', ['▼', '►'], title='сложить/показать', char=1, **style(float='right')),
            ]),
            _field('m3table_scale3d', 'slip', [0.05, 2, 0.05, ' ', 10], name='m3table_hide33', digits=2, className='label', **style(margin='0 auto 7px')),
            _field('m3table_cm', 'chb3', ['размер в см|cm', 'размер в мм|mm'], name='m3table_hide33', noEmpty=1, **style(margin='0 auto')),

            _div(className='setting-line'),

            labelc('Редактировать 3d блок (mmmNotRooms)'),
            _field('m3table_wed', 'band', ['таблица', 'фасад', 'грани'], **style(margin='0 auto 5px')),

            _div(className='setting-line', **style(margin=0), name='mmmNotRooms2', children=
                _table(
                    [ labelc('ширина'), labelc('высота'), labelc('глубина') ],
                    [
                        style('rowStyle', border=0, padding=0, margin=0),
                        _field('m3table_is3dX', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
                        _field('m3table_is3dY', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
                        _field('m3table_is3dZ', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
                    ],
                ),
            ),
  
            #  копировать удалить
            _div(name='copyDel3d2', children=[
                _div(className='setting-line'),
                _div(children=_table([
                        _btnD('Копировать', 'copy3d2'),
                        _btnD('Удалить 3d', 'del3d2', className='rsvTop armBtnRed'),
                    ], **style('rowStyle', borderSpacing='8px 0'))
                ),
            ]),

            _div(className='setting-line'),
            *_table(
                [
                _field('m3table_fixed', 'chb', ['не двигать'], title='запретить двигать мышкой 3d блок'),
                _field('m3table_turnOn', 'chb', ['вращать']),
                ],
                [
                _field('m3table_insideOnly', 'chb', ['привязать'], title='запретить 3d блоку выходить за грницы родителя'),
                _field('m3table_turnOnQQ', 'chb', [' '], title=''),
                ]
            ),
            _div(className='setting-line'),
        ]
    #
    # def m3tableInside(self):
    #         return [
    #
    #         _div(className='setting-line'),
    #
    #         labelc('Редактировать 3d блок'),
    #         _field('mi_wed', 'band', ['таблица', 'фасад', 'грани'], **style(margin='0 auto 5px')),
    #
    #         _div(className='setting-line', **style(margin=0), name='mmmNotRooms2', children=
    #             _table(
    #                 [ labelc('ширина'), labelc('высота'), labelc('глубина') ],
    #                 [
    #                     style('rowStyle', border=0, padding=0, margin=0),
    #                     _field('mi_is3dX', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
    #                     _field('mi_is3dY', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
    #                     _field('mi_is3dZ', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
    #                 ],
    #             ),
    #         ),
    #
    #         #  копировать удалить
    #         # _div(name='copyDel3d2', children=[
    #         #     _div(className='setting-line'),
    #         #     _div(children=_table([
    #         #             _btnD('Копировать', 'copy3d2'),
    #         #             _btnD('Удалить 3d', 'del3d2', className='rsvTop armBtnRed'),
    #         #         ], **style('rowStyle', borderSpacing='8px 0'))
    #         #     ),
    #         # ]),
    #
    #         _div(className='setting-line'),
    #         _field('mi_insideOnly', 'chb', ['привязать'], **style(textAlign='center'), title='запретить 3d блоку выходить за грницы родителя'),
    #
    #     ]
    #
    #

    # *** *** ***
    
    def bricksEdge(self):
        return [
            labelc('Редактировать (bricksEdge)'),
            _div(children=[
                _field('brickEdge_wed', 'band', ['фасад', 'грани'], **style(margin='0 auto 5px'))
            ]),
        ]
        
    def bricksOne(self):
        return [
            _div(**style(paddingTop=5, textAlign='center'), name='bricksOne2', children=[
                _span('Масштаб', className='setting-title'),
                _field('brick_hide35', 'chb', ['▼', '►'], title='сложить/показать', char=1, **style(float='right')),
             
                _field('brick_scale3d', 'slip', [0.05, 2, 0.05, ' ', 10], name='brick_hide35', digits=2, className='label', **style(margin='0 auto 7px')),
                _field('brick_cm', 'chb3', ['размер в см|cm', 'размер в мм|mm'], name='brick_hide35', noEmpty=1, **style(margin='0 auto')),

                _div(className='setting-line'),
            ]),

            _div(name='bricksOne4', children=[
                labelc('Редактировать (bricksOne)'),
                _div(children=[
                    _field('brick_wed', 'band', ['фасад', 'грани'], **style(margin='0 auto 5px'))
                    ]),
            ]),

  
            _div(className='setting-line', **style(margin=0)),
            *_table(
                [ labelc('ширина'), labelc('высота'), labelc('глубина') ],
                [
                    style('rowStyle', border=0, padding=0, margin=0),
                    _field('brick_is3dX', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
                    _field('brick_is3dY', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
                    _field('brick_is3dZ', 'number', max=100000, digits=1, width=70, className='labelc', delay=self.delay),
                ],
            ),

            
            _div(className='setting-line'),

            _field('brick_rotate3X', 'slip', [-360, 360, 1, 'наклон блока'], className='label', digits=1),
            _field('brick_rotate3Y', 'slip', [-360, 360, 1, 'поворот блока'], className='label', digits=1),
            _field('brick_rotate3Z', 'slip', [-360, 360, 1, 'поворот блока Z'], className='label', digits=1),

            _div(className='setting-line'),
            _div('сдвиг', className='label labelc_', **style(width=70, margin='auto')),
            _div(children=_table(
                    [
                        labelc('лев/прав'), labelc('верх/низ'), labelc('туда/сюда')
                    ],
                    [
                _field('brick_left', 'slip', [-10000, 10000, 1, '', 100000, -100000], className='label'),
                _field('brick_top', 'slip', [-10000, 10000, 1, '', 100000, -100000], className='label'),
                _field('brick_translateZ', 'slip', [-10000, 10000, 1, '', 100000, -100000], className='label'),
                ]
            )),
                
            #  копировать удалить
            _div(className='setting-line'),
            
            _field('brick2_insideOnly', 'chb', ['привязать'], name='bricksOne3', **style(textAlign='center'), title='запретить 3d блоку выходить за грницы родителя'),
            
            _div(name='bricksOne2', children=[
                _div(children=_table([
                        _btnD('Копировать', 'copy3d2'),
                        _btnD('Удалить 3d', 'del3d2', className='rsvTop armBtnRed'),
                    ], **style('rowStyle', borderSpacing='8px 0'))
                ),
                _div(className='setting-line'),
                *_table(
                    [
                    _field('brick_fixed', 'chb', ['не двигать'], title='запретить двигать мышкой 3d блок'),
                    _field('brick_turnOn', 'chb', ['вращать']),
                    ],
                    [
                    _field('brick_insideOnly', 'chb', ['привязать'], title='запретить 3d блоку выходить за грницы родителя'),
                    _field('brick_turnOnQQ', 'chb', [' '], title=''),
                    ]
                ),
            ]),
            
            _div(className='setting-line'),
        ]


    def bricksM3t(self):
        return [
            _div(className='setting-line', **style(margin=0)),
            *_table(
                [
                    labelc('ширина', name='m3t_is3dX'),
                    labelc('высота', name='m3t_is3dY'),
                    _div(**style(width=60)),
                    labelc('глубина', name='m3t_is3dZ')
                ],
                [
                    _field('m3t_is3dX', 'number', max=100000, digits=1, width=70, name='m3t_is3dX', className='labelc', delay=self.delay),
                    _field('m3t_is3dY', 'number', max=100000, digits=1, width=70, name='m3t_is3dY', className='labelc', delay=self.delay),

                    _field('m3t_metric', 'chb', ['%', 'px'], **style(width=15), name='m3t_is3dZ', title='переключить', char=1, className='metric'),
                    _div(**style(width=30)),
                    _field('m3t_is3dZ', 'number', max=100000, digits=1, width=70, name='m3t_is3dZ', className='labelc', delay=self.delay),
                ],
            ),
            _field('m3t_fixedSize', 'chb', ['не менять размер'], name='m3t_fixed', title='зафиксировать размер ячейки', **style(marginLeft=5)),

            _div(className='setting-line'),

            _field('m3t_rotate3X', 'slip', [-90, 90, 1, 'наклон блока'], className='label'),
            _field('m3t_rotate3Y', 'slip', [-90, 90, 1, 'поворот блока'], className='label'),
            _field('m3t_rotate3Z', 'slip', [-90, 90, 1, 'поворот блока Z'], className='label'),

            _div(className='setting-line'),
            _div('сдвиг', className='label labelc_', **style(width=70, margin='auto')),
            _div(children=_table(
                [
                    labelc('лев/прав'), labelc('верх/низ'), labelc('туда/сюда')
                ],
                [
            _field('m3t_translateX', 'slip', [-1000, 1000, 1, '', 100000, -100000], className='label'),
            _field('m3t_translateY', 'slip', [-1000, 1000, 1, '', 100000, -100000], className='label'),
            _field('m3t_translateZ', 'slip', [-1000, 1000, 1, '', 100000, -100000], className='label'),
                ]
            )),
        ]

    def is3wall1(self):
        return [

        _div(className='setting-line', **style(margin='0 0 3px 0')),
        *_table(
            [
                label('ширина'),
                _field('w_is3dX', 'number', max=100000, digits=1, width=50, delay=self.delay),
                label('высота'),
                _field('w_is3dY', 'number', max=100000, digits=1, width=50, delay=self.delay),
            ]
        ),
        _div(className='setting-line'),

        # ***
        *_table(
            [
                label('слева'),
                _field('w_left', 'number', max=100000, digits=1, width=50, delay=self.delay),
                label('сверху'),
                _field('w_top', 'number', max=100000, digits=1, width=50, delay=self.delay),
            ]
        ),
        _div(className='setting-line'),

        # ***
        *_table(
            [
                labell(''),
                labell('толщина'),
                _field('w_is3dZ', 'number', max=100000, digits=1, width=50, delay=self.delay),
                labell(''),
        ]),
    ]
        # ***

    def is3wall2(self): return [

        # ***
        _field('w_rotateGr', 'slip', [-90, 90, 1, 'поворот пола'], className='label', name='rotGr'),
        _field('w_shiftGr', 'slip', [-1000, 1000, 1, 'сдвиг пола', 10000, -10000], className='label', name='rotGr'),


        _field('w_rotate', 'slip', [-90, 90, 1, 'поворот стены'], className='label', name='rotShift'),
        _field('w_shift', 'slip', [-1000, 1000, 1, 'сдвиг стены', 10000, -10000], className='label', name='rotShift'),
        _field('w_skewY', 'slip', [-360, 360, 15, 'наклон стены'], digits=1, className='label', name='rotShift'),

        _field('w_rotateTop1', 'slip', [-90, 90, 1, 'наклон потолка 1'], className='label', name='rshTop'),
        _field('w_rotateTop2', 'slip', [-90, 90, 1, 'наклон потолка 2'], className='label', name='rshTop'),
        _field('w_shiftTop', 'slip', [-1000, 1000, 1, 'сдвиг потолка', 10000, -10000], className='label', name='rshTop'),

        # *** кнопки 'окно' дверь
        _div(name='winDoor', children=[
            _div(className='setting-line'),
            * _table(
                [
                    # label('', 40),
                    _btnD('окно/дверь', 'winDoor', 'www', className='rsvTop'),
                    label('', 5),
                    _btnD('добавить\xa0стену', 'addWall', className='rsvTop'),
                    # label('', 40)
            ]),
        ]),
    ]
    # ***

    def furniture(self):

        def buttons(add, whence):
            return [
                _div(f'Мебель для комнаты ({whence})', className='label labelc',
                    children=[
                        _field(f'room{add}', 'band',
                           ['мягкая', 'корпусная', 'техника'],
                           **style(border='1px solid #aaa', fontSize=14, color='#048', borderSpacing='10px'),
                           rowLength=3, recalcText=1,
                           **style('itemStyle', width=70)
                        )
                    ],
                    **style(margin='7px 3px')
                ),
                _div(f'Мебель для кухни ({whence})', className='label labelc',
                    children=[
                        _field(f'kitchen{add}', 'band',
                           ['напольная', 'навесная', 'техника'],
                           **style(border='1px solid #aaa', fontSize=14, color='#048', borderSpacing='10px'),
                           rowLength=3, recalcText=1,
                           **style('itemStyle', width=70)
                        )
                    ],
                    **style(margin='7px 3px')
                ),
            ]

        return [

            _tab(130, [
                ['Home', _div(**style(overflow='auto'),
                    className='insideHome', children=buttons('', 'локально'))],
                ['Sova.online', _div(**style(overflow='auto'),
                    className='insideSova', children=buttons('S', 'с сервера'))],
            ]),

            # Вставить 3d в 3d можно только в режиме "мебель", если clip.boxClipboard() === '3d'
            _btnD('Вставить 3d', 'paste3d', name='paste3d', **style(width='90%', margin='7px auto')),
        ]

    # *** *** ***

    def arrow(self):

        d = 48

        return [
            _field('arrowType', 'band', [
                    _div(**style(width=d, height=d, padding='3px 0'), children=[
                        _div(**style(width=d, height=d - 6, backgroundSize='100% 100%', background='url(/images/arrHor.jpg)')),
                    ]),
                    _div(**style(width=d, height=d, padding='0 3px'), children=[
                        _div(**style(height=d, backgroundSize='100% 100%', background='url(/images/arrVer.jpg)')),
                    ]),
                    _div(**style(width=d, height=d, padding='3px 0'), children=[
                        _div(**style(width=d, height=d - 6, backgroundSize='100% 100%', background='url(/images/arr3.jpg)')),
                    ]),
                    _div(**style(width=d, height=d, padding='0 3px'), children=[
                        _div(**style(height=d, backgroundSize='100% 100%', background='url(/images/arr4.jpg)')),
                    ]),
                    _div(**style(width=d, height=d, padding=3), children=[
                        _div(**style(height=d - 6, backgroundSize='100% 100%', background='url(/images/arrVH.jpg)')),
                    ]),
                ],
                    **style('itemStyle', padding=0),
                    **style(width='auto', margin='auto', borderSpacing=7)
            ),

            _div(className='setting-line'),
            _div(**style(width='90%'), children=_table(
                [
                    label('X1'),
                    _field('x1', 'number', max=100000, width=60),
                    label('X2'),
                    _field('x2', 'number', max=100000, width=60),
                ]
            )), _div(**style(width='90%', padding='5px 0'), children=_table(
                [
                    label('Y1'),
                    _field('y1', 'number', max=100000, width=60),
                    label('Y2'),
                    _field('y2', 'number', max=100000, width=60),
                ]
            )),
            _div(**style(width=120, margin='auto'), children=_table(
                labField('длина', 'len', 'number', digits=1, readOnly=1, width=60),
            )),
            _div(className='setting-line'),
            _field('io', 'chb', ['не выходить за границы блока|1']),  # insideOnly
            _field('linked', 'chb', ['привязать к размерам блока|1']),  # insideOnly
            _btnD('удалить линию', 'deleteLine', className='rsvTop armBtnRed', **style(margin=7)),
        ]

    # *** *** ***

    def tumba(self):
        return [
            *_table([
                _div(className='btn_90', **style(borderLeftWidth=0), children=[
                    labelc('слева'),
                    _field('f_left', 'number', max=100000, digits=1, width=50),
                ]),

                _field('f_rotate3Y', 'slip', [-180, 180, 30, 'поворот'], name='ground', **style(width=160), className='label'),

                # _div('Навесная мебель', name='noGround', **style(paddingTop=10, width=160), className='labelc'),

                _div(name='noGround', className='btn_90', children=[
                    labelc('от пола'),
                    _field('f_bottom', 'number', max=100000, digits=1, width=50),
                ]),

                _div(className='btn_90', children=[
                    labelc('сверху'),
                    _field('f_top', 'number', max=100000, digits=1, width=50),
                ]),
            ]),

            _div(className='setting-line'),
            *_table([
                _field('f_fixed', 'chb', ['не двигать'], title='запретить двигать мышкой 3d блок'),
                _field('f_insideOnly', 'chb', ['привязать'], title='привязать к границам стены'),
                ],
                [_div('', **style(height=5))],
                [
                    _field('f_lineOff', 'chb', ['скрыть размер'], title='скрыть'),
                    _field('f_hide', 'chb', ['скрыть'], title='скрыть'),
                ],
                [_div('', **style(height=5))],
                [_div(className='setting-line')],
            ),
            *_table([
                _div(className='btn_90', **style(borderLeftWidth=0, width='33%'), children=[
                    labelc('ширина'),
                    _field('tumba_is3dX', 'number', max=100000, digits=1, width=50, delay=self.delay),
                ]),

                _div(className='btn_90', **style(borderLeftWidth=0, width='34%'), children=[
                    labelc('глубина'),
                    _field('tumba_is3dZ', 'number', max=100000, digits=1, width=50, delay=self.delay),
                ]),

                _div(className='btn_90', **style(borderLeftWidth=0, width='33%'), children=[
                    labelc('высота'),
                    _field('tumba_is3dY', 'number', max=100000, digits=1, width=50, delay=self.delay),
                ]),
            ]),

            _div(className='setting-line'),
            *_table([
                _div(className='btn_f_delete3d', children=[_btnD('копировать', 'f_copy3d', className='btn_f_gray')]),
                _div(className='btn_f_delete3d', children=[_btnD('удалить', 'f_delete3d')]),
            ]),
        ]

    # *** *** ***

    def box2d0(self):
        return [
            _field('bb', 'band', ['\xa0\xa0\xa0', 'бокс', 'бордюр', 'тень', 'html'],
                **style(fontSize=14, color='#048', borderSpacing='4px')),
            _div(name='scale2d', className='setting-line'),
            _field('scale2d', 'slip', [0.05, 3, 0.05, 'масштаб', 10], name='scale2d', digits=2, className='label'),
            _field('cm2d', 'chb3', ['размер в см|cm', 'размер в мм|mm'], name='scale2d', noEmpty=1, **style(margin='10px auto')),
            _div(className='setting-line', name='make3d'),
            _btnD('создать 3d', 'make3d', name='make3d', className='rsvTop armBtnRed', **style(width=150, margin='0 auto 5px')),
        ]

    def box2d1(self):
        return [
            _div(name='boxStyle', children=self.boxStyle(), className='setting-block'),

            # ***

            _div(className='setting-head', name='borders', children=[
                _span('Границы', className='setting-title'),
                _field('border', 'chb3', ['равны|borEQ', 'не равны|borNE'], **style(width='100%', margin='5px auto')),
                *self.borderStyle(),
            ]),

            # ***

            _div(name='boxContent', className='setting-head', children=[
                _span('Бокс контент', className='setting-title'),
                _field('boxContent', 'band',
                    ['\xa0\xa0\xa0\xa0', 'текст', 'редактор', 'кнопка'],  # , 'поле\xa0БД', 'SVG', 'виджет', ''],
                    rowLength=4)
            ]),

            _div(name='isField', **style(background='#def'), children=[
                labell('Имя поля'),
                _field('fieldName', 'tx'),
                labell('Тип'),
                _field('fieldType', 'lbsd', [
                    'нередактируемый текст|fd',
                    'текст|tx',
                    'дата|dt',
                    'список (один из)|lbsd',
                    'список (multivalue)|lbmd',
                    'список + текст|lbme',
                    'файлшоу|fileShow',
                ], alias=1, small='2'),
                labell('Выпадающий список', name='dropList'),
                _field('dropList', 'tx', name='dropList'),
                labell('Стиль'),
                _field('fieldStyle', 'chb3', ['стандартный|0', 'настроить|1'], **style(width='100%', margin='5px auto')),
                _teg('hr', color='#00f', size=3)
            ]),

            # стиль текста
            _div(name='textStyle', children=self.textStyle(), className='setting-block'),

            # *** Тень
            _div(name='shadow', className='setting-head', children=[
                _span('Тень', className='setting-title'),
                _field('shadow', 'chb3', ['снаружи|outside', 'внутри|inset'], **style(width='100%', margin='5px auto')),
                self.shadow(),
            ]),
        ]

    # *** *** ***

    def borderStyle(self):
        return [
            _div(name='borEQ', className='setting-block', children=[
                *self.brdStyle('')
            ]),

            _div(name='borNE', className='setting-block', children=[
                _field('borderSide', 'band', ['слева', 'сверху', 'справа', 'снизу'],
                    **style(fontSize=14, color='#048', borderSpacing='5px')),

                *self.brdStyle('Left'),
                *self.brdStyle('Top'),
                *self.brdStyle('Right'),
                *self.brdStyle('Bottom'),
            ])
        ]

    rLabel = {'': 'Радиус', 'Left': 'R(лев-ниж)', 'Top': 'R(лев-вер)', 'Right': 'R(пр-вер)', 'Bottom': 'R(пр-ниж)'}

    def brdStyle(self, side):
        return [
            *_table([
                _div(name=f'bor{side}', **style(width='22%', textAlign='center'), children=[
                    _div((side or '\xa0').lower(), **style(textAlign='center', font='bold 9pt Verdana, Arial', color='#048')),
                    _field(f'border{side}Color', 'input-color', colorList='rainbow'),
                    _div('Цвет', **style(textAlign='center', font='bold 9pt Verdana, Arial', color='#048')),
                ]),

                _div(name=f'bor{side}', **style(paddingLeft=10, fontSize=6, textAlign='center', borderLeftWidth=1, border='0 solid #aaa'),
                    children=[
                        _field(f'border{side}Width', 'slip', [0, 100, 1, 'Ширина', 10000]),
                        _field(f'border{side}Radius', 'slip', [0, 100, 5, self.rLabel[side], 10000], metric='px|%'),
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
                    None if tr == 'skew' else _field(f'{tr}Z', 'slip', [d1, d2, step, 'Z'], digits=digits, className='label'),
                ],
            ))

    def boxStyle(self):
        return [
            _div(className='setting-head'),

            _div(name='boxSizeX', children=_table(
                [
                    label('ширина X'),
                    _field('boxSizeX', 'number', max=100000, digits=1, width=50, delay=self.delay),
                    _field('boxSizeXp', 'fd', className='label'),
                ],
            )),
            _div(name='boxSizeY', children=_table(
                [
                    label('высота Y'),
                    _field('boxSizeY', 'number', max=100000, digits=1, width=50, delay=self.delay),
                    _field('boxSizeYp', 'fd', className='label'),
                ]
            )),
            _div(className='setting-line', name='floatBox'),
            _div(name='floatBox', children=_table(
                [
                    label('отступ X'),
                    _field('rectLeft', 'number', max=100000, digits=1, width=50),
                    label('отступ Y'),
                    _field('rectTop', 'number', max=100000, digits=1, width=50),
                ]
            )),

            _div(className='setting-line'),

            _field('insideOnly', 'chb', ['привязать к родителю'], name='floatBox', title='запретить плавающему блоку выходить за грницы родителя', **style(display='block')),
            _field('fixed', 'chb', ['не двигать'], name='floatBox', title='запретить двигать мышкой плавающий блок', **style(display='block')),
            _field('noIcons', 'chb', ['скрыть иконки'], name='noIcons', **style(display='block')),
            _div(**style(padding='4px 0'), children=[
                _field('anchor', 'chb', ['якорь'], title='для перехода при клике мышкой', **style(display='inline')),
                _field('showAnchor', 'fd', name='showAnchor', **style(padding='10px 0 5px 10px', display='inline')),
            ]),

            _div(className='setting-line'),
            labell('overflow'),
            _field('overflow', 'lbsd', ['auto', 'hidden', 'scroll', 'visible', 'inherit'], small='2'),
            _div(className='setting-line'),

            _div(name='zIndex', children=
                _table([
                    _div(' '), label('z-index'),
                    _btnD('\u21D1', 'blPlus', className='metric'),
                    _field('boxLayer', 'fd', name='boxLayer', className='labelc'),
                    _btnD('\u21D3', 'blMinus', className='metric'), _div(' ')
                ])
            ),

            _div(name='zIndex', className='setting-line'),

            _div(children=[
                _field('trans', 'band', ['сдвиг', 'поворот', 'наклон']),

                self.trans('translate', -10000, 10000, 1),
                self.trans('rotate', 0, 360, 1),
                self.trans('skew', -90, 90, 15),
            ])
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
            _div(className='setting-line'),
            _div(name='isButton', **style(background='#ffc6b5'), children=[
                labell('Действие'),
                _field('buttonAction', 'lbsd', ['javascript', 'Отправить данные (submit)|submit', 'url', 'перейти к якорю'], alias=1, small='2'),
                _field('buttonUrl', 'tx', name='buttonUrl'),
                _div(wl=80, name='buttonCmd', children=_table(
                    labField('Команда', 'buttonCmd'),
                    labField('Надпись', 'buttonLabel'),
                )),
                _teg('hr', color='#00f', size=3)
            ]),

            _field('textAlign', 'band', [
                _div(**style(width=30, height=30, margin='auto'), children=tx_1_2('l')),
                _div(**style(width=30, height=30, margin='auto'), children=tx_1_2('c')),
                _div(**style(width=30, height=30, margin='auto'), children=tx_1_2('q')),
                _div(**style(width=30, height=30, margin='auto'), children=tx_1_2('r')),
                ], name='textAlign', **style(width='80%', margin='auto', borderSpacing='5px')),

            labell('Шрифт'),
            _field('fontFamily', 'lbsd', ['Verdana', 'Arial', 'Courier', 'Futura PT'], small='2'),
            *_table([
                _field('fontSize', 'slip', [1, 100, 1, 'Размер', 2000], metric='rem|px', className='label', **style(width=170, paddingTop=10, marginLeft=5)),
                _div(children=[label('Цвет', **style(width=55)), _field('color', 'input-color', **style(marginLeft=20), colorList='rainbow')]),
            ]),
            *_table([
                _field('fontWeight', 'chb', ['жирный|bold'], className='label'),
                _field('fontStyle', 'chb', ['курсив|italic'], className='label')
            ]),
            _div(className='setting-line', **style(marginTop=8)),
            labelc('Интервал'),
            *_table([
                _field('letterSpacing', 'slip', [0, 50, 1, 'X', 1000], className='label', **style(width='45%'), metric='em|px'),
                _field('lineHeight', 'slip', [0, 5, 0.1, 'Y', 10], digits=2, className='label', **style(width='45%', paddingLeft=5))
            ]),
            _div(className='setting-line'),
            labelc('Отступы'),
            *_table([
                _field('paddingLR', 'slip', [0, 100, 1, 'X', 10000], className='label', **style(width='45%'), metric='em|px'),
                _field('paddingTD', 'slip', [0, 100, 1, 'Y', 10000], className='label', **style(width='45%', paddingLeft=5), metric='em|px')
            ]),
            _div(**style(margin='auto', width='90%'), children=_table(
                [_field('textIndent', 'slip', [0, 200, 1, 'Параграф', 2000], className='label', metric='em|px')])),
        ]

    def shadow(self):
        return _div(className='setting-block', name='shadowOn', children=[
            *_table([
                _div(**style(width='20%', textAlign='center'), children=[
                    _span('Цвет', **style(textAlign='center', font='bold 9pt Verdana, Arial', color='#048')),
                    _field('shadowColor', 'input-color', colorList='rainbow')
                ]),
                _div(**style(paddingLeft=10, textAlign='center', borderLeftWidth=1, border='0 solid #aaa'), children=[
                    _field('shadowW', 'slip', [0, 200, 1, 'ширина', 2000], **style(display='block')),
                    _field('shadowR', 'slip', [0, 100, 1, 'размытие', 2000], **style(display='block')),
                    _field('shadowX', 'slip', [-100, 100, 1, 'сдвиг x', 2000], **style(display='block')),
                    _field('shadowy', 'slip', [-100, 100, 1, 'сдвиг y', 2000], **style(display='block')),
                    _br(),
                ]),
            ]),
        ])

    # *** *** ***

