# -*- coding: utf-8 -*- 
"""
AON 20 apr 2018

"""
import tools.first as log
from tools.DC import DC, toWell
from tools.sovaWS import startWebSocketServer
from tools.common import setVersionJS
from tools.appConfig import loadIniFile, loadPeople

from django.apps import AppConfig

import os


# *** *** ***

class DesignConfig(AppConfig):
    name = 'appDesign' # путь к файлам приложения
    def __init__(self, app_name, app_module):
        BASE_DIR = log.BASE_DIR

        for s in ['index', 'open']:
            try:
                path = os.path.join(BASE_DIR, 'api', 'react', f'{s}.html')
                with open(path, 'r', encoding='utf-8') as f:
                    html = setVersionJS(f.read(), BASE_DIR)[0]
                    _fo = DC({'html': html})
                    toWell(_fo, 'groundForms', s)
            except:
                log.err(f'file "{path}" not loaded', cat=self.name)
            
        log.initLog(mainProcess=True, prpr=True, logLevel='INFO')
        path = os.path.join(BASE_DIR, 'DB', f'{self.name}.ini')
        loadIniFile(path)
        
        loadPeople()
    
        startWebSocketServer()


        AppConfig.__init__(self, app_name, app_module)

# *** *** ***



