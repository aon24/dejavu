# -*- coding: utf-8 -*- 
'''
Created on 2022.

@author: aon
'''

# *** *** ***

from api.formTools import _span, style, _div, _field, _fileShow, label, _lf, _btnD

# *** *** ***

def profile(dcUK):
    fieldsL = [
        _lf('Фамилия', 'lastName'),
        _lf('Имя', 'firstName'),
        _lf('Отчество', 'MiddleName'),
        _lf('E-mail', 'email'),
        _lf('Пол', 'gender', 'lbsd', ['женский', 'мужской', 'паркет', 'ламинат', 'еще не решил(а)'], placeholder='Список'),
        _lf('День рождения', 'birthday', 'dt')
    ]
    fieldsR = [
        _div(**style(height=50, textAlign='center'), children=[
            _span('Аватар', className='lab', **style(verticalAlign='top', marginRight=10)),
            _field('avatar_FD', 'json', **style(width=50, height=50, display='inline-block', border='1px solid #eee')),
            ]),
        _lf('Телефон', 'phone', 'phone'),
        _lf('Город', 'city'),
        _lf('Страна', 'country'),
        _lf('', 'status', 'chb', ['общая подписка'], className='lab', **style(letterSpacing=1)),
        label(),
        _btnD('Установить пароль', 'setPassword'),
        # ],
        # # labField('входит в группы', 'groups'),
        # labField('Приветствие, обращение', 'greeting'),
        # labField('схема доступа', 'acrScheme'),
        # labField('Комментарий', 'NOTES'),
    ]
    
    st = style(verticalAlign='top', borderSpacing=1, padding='10px 20px', width=360, display='inline-block')
    return _div( children=[
                _div(**st, children=fieldsL),
                _div(**st, children=fieldsR),
                _div(**style(borderSpacing=1, padding=10), children=[
                    _lf('Комментарий', 'NOTES'),
                    label(),
                    _fileShow('FILES1_', wl=1, label='Аватар\xa0и\xa0другие\xa0файлы'),
                ])
            ])

# *** *** ***
        