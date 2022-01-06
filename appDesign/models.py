# -*- coding: utf-8 -*- 
'''
Created 2020

@author: aon

_m.py makemigrations appDesign
_m.py migrate
_m.py createsuperuser
'''

from django.db import models

import uuid

# *** *** ***

class Page(models.Model):
    unid = models.UUIDField('uuid', default=uuid.uuid4, db_index=True)
    xfields = models.TextField('xfields', blank=True)
    xmdf = models.DateTimeField('Дата перехода в архив', null=True, blank=True, db_index=True)
    
    objects = models.Manager()  # Менеджер по умолчанию

    def __str__(self):
        return f'{self.pk}:unid:{self.unid}:xmdf:{self.xmdf}'


    def save(self, force_insert=False, force_update=False, using='draft', update_fields=None):
        models.Model.save(self, force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields)
        
# *** *** ***

