'''
Created on 2022

@author: aon
'''
from tools.DC import DCC

# *** *** ***

all_ = {  # all - reserved built-in symbol
    'В работе': DCC(condition="d.key!='Archive'", sort='docNo', reverse=True, fixedSubCats=[
            DCC(subCat='3d-rooms', condition="d.key=='rooms'"),
            DCC(subCat='3d-cases', condition="d.key=='cases'"),
            DCC(subCat='3d-walls', condition="d.key=='walls'"),
            DCC(subCat='2d', condition="d.key not in ['rooms', 'cases', 'walls']"),
        ]
    ),
    'Архив': DCC(condition="d.key=='Archive'", sort='docNo', reverse=True, fixedSubCats=[
            DCC(subCat='3d-rooms (A)', condition="d.key_=='rooms'"),
            DCC(subCat='3d-cases (A)', condition="d.key_=='cases'"),
            DCC(subCat='3d-walls (A)', condition="d.key_=='walls'"),
            DCC(subCat='2d (A)', condition="d.key_ not in ['rooms', 'cases', 'walls']"),
        ]
    ),
    # 'Подформы': DCC(condition='d.subform', sort='pageName', subCat='d.creator'),
    # 'Блоки': DCC(condition='d.block', sort='pageName', subCat='d.creator'),
}

cases = {
    'Вся мебель': DCC(condition="d.key=='cases'", sort='docNo', reverse=True,
        fixedSubCats=[
            DCC(subCat='Кухня', condition="d.project=='Мебель для кухни'"),
            DCC(subCat='Комната', condition="d.project=='Мебель для комнаты'"),
            DCC(subCat='Санузел', condition="d.project=='Мебель для ванной'"),
        ]
    ),
    'Кухня': DCC(condition="d.key=='cases' and d.project=='Мебель для кухни'", sort='docNo', reverse=True,
        byFieldSubCats='d.pageName'  # формировать список дин.подкатегорий по полю 'pageName'
    ),
    'Комната': DCC(condition="d.key=='cases' and d.project=='Мебель для комнаты'", sort='docNo', reverse=True,
        byFieldSubCats='d.pageName'  # формировать список дин.подкатегорий по полю 'pageName'
    ),
    'Санузел': DCC(condition="d.key=='cases' and d.project=='Мебель для ванной'", sort='docNo', reverse=True,
        byFieldSubCats='d.pageName'  # формировать список дин.подкатегорий по полю 'pageName'
    ),
    'По авторам': DCC(condition="d.key=='cases'", sort='docNo', reverse=True,
        byFieldSubCats="d.creator.replace(' ', '\xa0')"  # формировать список дин.подкатегорий по полю 'creator'
    ), }

rooms = {
    # 'По номеру': DCC(condition="d.key=='rooms'", sort='docNo', reverse=True,
        # fixedSubCats=[
            # DCC(subCat='В работе', condition='not d.closed'),
            # DCC(subCat='Закрыт', condition='d.closed'),
        # ]
    # ),
    'Проекты': DCC(condition="d.key=='rooms'", sort='docNo', reverse=True,  # сортровка по полю 'name'
        byFieldSubCats='d.project'  # формировать список дин.подкатегорий по полю 'project'
    ),
    'Помещения': DCC(condition="d.key=='rooms'", sort='docNo', reverse=True,
        byFieldSubCats='d.pageName'  # формировать список дин.подкатегорий по полю 'pageName'
    ),
    'Стены': DCC(condition="d.key=='walls'", sort='docNo', reverse=True,
        byFieldSubCats='d.pageName'  # формировать список дин.подкатегорий по полю 'pageName'
    ),
    'Дом': DCC(condition="d.key=='home'", sort='docNo', reverse=True,
        byFieldSubCats='d.pageName'  # формировать список дин.подкатегорий по полю 'pageName'
    ),
    'По авторам': DCC(condition="d.key=='rooms'", sort='docNo', reverse=True,
        byFieldSubCats="d.creator.replace(' ', '\xa0')"  # формировать список дин.подкатегорий по полю 'creator'
    ),
}

