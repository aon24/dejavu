# -*- coding: utf-8 -*-

import time

usersByLogin = {}
CLS = {}

# *** *** ***

class DC(object):
    def __init__(self, dc=None, **kv):
        self.__dict__['_d_'] = {}
        if dc:
            if type(dc) is dict:
                self.__dict__['_f_'] = {k.upper(): v for (k,v) in dc.items()}
            else:
                self.__dict__['_f_'] = {k.upper(): v for (k,v) in dc._f_.items()}
        else:
            self.__dict__['_f_'] = {}
        for k, v in kv.items():
            self.__dict__['_f_'][k.upper()] = v
            
        
    def __getattr__(self, fieldName):
        if fieldName == 'doc':
            return self._d_
        if fieldName == '_KV_':
            return self._f_
        return self._f_.get(fieldName.upper(), '')
    
    def __setattr__(self, fieldName, fieldValue):
        if fieldName == 'doc':
            self.__dict__['_d_'] = fieldValue
        else:
            self._f_[fieldName.upper()] = str(fieldValue)
    
    def F(self, fieldName):
        return self._f_.get(fieldName.upper(), '')
    
    def A(self, fieldName):
        return self._f_.get(fieldName.upper(), '').split('\n')

    def S(self, fieldName, fieldValue):
        self._f_[fieldName.upper()] = str(fieldValue)

    def D(self, fieldName):
        s = ''
        for k in self._f_.get(fieldName.upper(), '').split('\n'):
            if k:
                try:
                    s += time.strftime('%d.%m.%Y\n', time.strptime(k.partition(' ')[0], '%Y-%m-%d'))
                except:
                    s += k + '\n'
        return s[:-1] if s else ''

    def DT(self, fieldName):
        dt = self._f_.get(fieldName.upper(), '')
        try:
            return time.strftime('%d.%m.%Y %H:%M:%S', time.strptime(dt, '%Y-%m-%d %H:%M:%S'))
        except:
            return ''

    def save(self):
        from tools.dbToolkit.Book import docSaveDB
        return docSaveDB(self)
    
    def __str__(self):
        return 'DC:\n' + '\n'.join( x[:200] for x in [k + ' = %r' % self.F(k) for k in sorted(self._f_)] )

# *** *** ***

config = DC()

# *** *** ***

# profiles = ['DRAFT', 'DOCNO', 'PEOPLE', 'TRACKS']

# *** *** ***

def well(*keys):
    cls = CLS
    for k in keys[:-1]:
        cls = cls.get(k)
        if not cls:
            return ''
    return cls.get(keys[-1], '')

def toWell(d, *keys):
    cls = CLS
    for k in keys[:-1]:
        CLS[k] = cls.get(k, {})
        cls = CLS[k]
    cls[keys[-1]] = d
    
def appendWell(x, *keys):
    cls = CLS
    for k in keys[:-1]:
        CLS[k] = cls.get(k, {})
        cls = CLS[k]
    if not cls.get(keys[-1]):
        cls[keys[-1]] = []
    cls[keys[-1]].append(x)

def profile(dbAlias):
    return CLS['profile'].get(dbAlias, '')

# *** *** ***

