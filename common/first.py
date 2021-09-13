# -*- coding: utf-8 -*-
import os, time
from datetime import datetime
import queue

# *** *** ***
sovaLogger = None
logQueue = queue.Queue()
# *** *** ***

class SvLogger(object):
    datefmt = '%d.%m.%Y %H:%M:%S'
    
    def __init__(self, mainProcess, prpr, logFile, logLev):
        logDir = logFile.rpartition(os.sep)[0]
        os.makedirs(logDir, exist_ok=True)

        self.mainProcess = mainProcess
        self.fileHandler = None
        self.logPath = logFile + '_%d.log'
        self.logFileName = None
        self.today = None
        self.prpr = prpr
        self.logLevel = logLev or 'INFO'

    def changeLogFile(self, maxLogFiles=7, maxLogSize=1024*1024): # количество журналов, макс. размер
        self.today = datetime.today().strftime('%Y-%m-%d')
        self.fileHandler and self.fileHandler.close()
        self.logFileMode = 'a'
        ls = {}
    
        for i in range(maxLogFiles):
            try:
                ls[i] = {'time': os.stat(self.logPath % i).st_mtime, 'size': os.stat(self.logPath % i).st_size}
            except:
                ls[i] = {'time': 0}
        
        i = sorted(ls.keys(), key=lambda x: ls[x]['time'], reverse=True)[0] # номер последнего журнала
        if ls[i]['time'] == 0:
            i = 0
        elif ls[i]['size'] > maxLogSize: # размер файла больше допустимого
                self.logFileMode = 'w'
                i += 1
                if i >= maxLogFiles:
                    i = 0
        self.logFileName = self.logPath % i
        self.fileHandler = open ( self.logFileName, mode=self.logFileMode, encoding='utf-8', errors='ignore' )

# *** *** ***

def initLog(mainProcess=True, prpr=True, logFile=f'log{os.sep}sova', logLevel=''):
    global sovaLogger
    sovaLogger = SvLogger(mainProcess, prpr, logFile, logLevel)
    snd('Logger started (%s)' % ('main process' if mainProcess else 'agent log'), 'level=' + logLevel, cat='logging')

# *** *** ***

def msgForLog(msg, cat, level):
    global sovaLogger
    if not sovaLogger:
        s = 'No log %s %s [%s] %s\n' % (datetime.now().strftime(SvLogger.datefmt), level, cat, msg)
        print(s)
        return

    if not sovaLogger.mainProcess: # for multiprocessing: порожденные процессы не пишут в файл
        logQueue.put([msg, cat, level])
        return

    try:
        if sovaLogger.today != datetime.today().strftime('%Y-%m-%d'):
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
                sovaLogger.fileHandler.write(s)
                sovaLogger.prpr and print(s)
            else:
                print(s)
            flag = True
        
        if level:
            s = f'{datetime.now().strftime(SvLogger.datefmt)} {level} [{cat}] {msg}\n'
            if sovaLogger:
                sovaLogger.fileHandler.write(s)
                sovaLogger.prpr and print(s)
            else:
                print(s)
            flag = True
            
        if flag:
            sovaLogger and sovaLogger.fileHandler.flush()
        
    except Exception as ex:
        s = f'{datetime.now().strftime(SvLogger.datefmt)} ERROR [LOGGING-ERROR] cat: {cat}\n{ex}\n'
        sovaLogger and sovaLogger.fileHandler.write(s)
        print(s)

def snd(*msg, cat='snd', noPrint=None):
    if sovaLogger and sovaLogger.logLevel.upper() in ['INFO', 'DEBUG']:
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
