# -*- coding: utf-8 -*-
import os, time
from datetime import datetime
import queue

# *** *** ***
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.environ.get('ECLIPSE', BASE_DIR)

sovaLogger = None
logQueue = queue.Queue()

TIME_LOOP = 60*60*6 # проверять переполнение журналов каждые 6 часов
maxLogFiles = 10 # количество журналов
maxLogSize = 512*1024 # макс. размер

# *** *** ***

class SvLogger(object):
    datefmt = '%d.%m.%Y %H:%M:%S'
    
    def __init__(self, mainProcess, prpr, logLev):
        logDir = os.path.join(BASE_DIR, 'log')
        os.makedirs(logDir, exist_ok=True)

        self.mainProcess = mainProcess
        self.fileHandler = None
        self.logPath = os.path.join(logDir, 'sova_%d.log')
        self.logFileName = None
        self.prpr = prpr
        self.logLevel = logLev or 'INFO'
        self.startTime = 0

    def changeLogFile(self):
        if self.logFileName:
            try:
                if os.stat(self.logFileName).st_size < maxLogSize:
                    return
            except:
                pass
            
        self.fileHandler and self.fileHandler.close()
        logFileMode = 'a'
        ls = {}
    
        for i in range(maxLogFiles):
            try:
                ls[i] = {'time': os.stat(self.logPath % i).st_mtime, 'size': os.stat(self.logPath % i).st_size}
            except:
                ls[i] = {'time': 0}
        
        i = sorted(ls.keys(), key=lambda x: ls[x]['time'], reverse=True)[0] # номер последнего журнала
        if ls[i]['time'] == 0: # список журналов пуст
            i = 0
        elif ls[i]['size'] > maxLogSize: # размер файла больше допустимого
                logFileMode = 'w'
                i += 1
                if i >= maxLogFiles:
                    i = 0
        self.logFileName = self.logPath % i
        self.fileHandler = open(self.logFileName, mode=logFileMode, encoding='utf-8', errors='ignore')

# *** *** ***

def initLog(mainProcess=True, prpr=True, logLevel=''):
    global sovaLogger
    sovaLogger = SvLogger(mainProcess, prpr, logLevel)
    snd(f"Logger started ({'main process' if mainProcess else 'agent log'})", f'level={logLevel}', cat='logging')

# *** *** ***

def msgForLog(msg, cat, level):
    global sovaLogger
    if not sovaLogger:
        s = f'No log {datetime.now().strftime(SvLogger.datefmt)} {level} [{cat}] {msg}\n'
        print(s)
        return

    if not sovaLogger.mainProcess: # for multiprocessing: порожденные процессы не пишут в файл
        logQueue.put([msg, cat, level])
        return

    try:
        if time.time() - sovaLogger.startTime > TIME_LOOP:
            sovaLogger.startTime = time.time()
            try:
                sovaLogger.changeLogFile()
            except Exception as ex:
                sovaLogger = None
                print(f'{datetime.now().strftime(SvLogger.datefmt)} ERROR [LOGGING-ERROR] cat: {cat}\n{ex}\n')
    
        flag = False
        while not logQueue.empty():
            ls = logQueue.get()
            s = f'{datetime.now().strftime(SvLogger.datefmt)} {ls[2]} [{ls[1]} 2] {ls[0]}\n'
            if sovaLogger:
                (sovaLogger.prpr or level == 'ERROR') and print(s)
                sovaLogger.fileHandler.write(s+'¤')
            else:
                print(s)
            flag = True
        
        if level:
            s = f'{datetime.now().strftime(SvLogger.datefmt)} {level} [{cat}] {msg}\n'
            if sovaLogger:
                (sovaLogger.prpr or level == 'ERROR') and print(s)
                sovaLogger.fileHandler.write(s+'¤')
            else:
                print(s)
            flag = True
            
        if flag:
            sovaLogger and sovaLogger.fileHandler.flush()
        
    except Exception as ex:
        s = f'{datetime.now().strftime(SvLogger.datefmt)} ERROR [LOGGING-ERROR] cat: {cat}\n{ex}\n'
        print(s)
        sovaLogger and sovaLogger.fileHandler.write(s+'¤')

def snd(*msg, cat='snd', noPrint=None):
    if sovaLogger and sovaLogger.logLevel:
        s = ', '.join(str(x) for x in msg)
        msgForLog(s, cat, 'INFO')

def dbg(*msg, cat='all'):
    if sovaLogger and sovaLogger.logLevel == 'DEBUG':
        s = ', '.join(str(x) for x in msg)
        msgForLog(s, cat, 'DEBUG')

def err(*msg, cat='all', noLog=None, noPrint=None):
    s = ', '.join(str(x) for x in msg)
    msgForLog(s, cat, 'ERROR')

# *** *** ***

def logLoop(): # запускать из главного процесса, если используется multiprocessing
    while True:
        msgForLog(None, None, None)
        time.sleep(60)
