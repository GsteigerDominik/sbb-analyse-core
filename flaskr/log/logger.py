import os
from datetime import datetime


def logInfo(msg):
    print('[' + str(datetime.now()) + '] [' + str(os.getpid()) + '] [INFO] ' + msg)


def logWarn(msg):
    print('[' + str(datetime.now()) + '] [' + str(os.getpid()) + '] [WARN] ' + msg)


def logError(msg):
    print('[' + str(datetime.now()) + '] [' + str(os.getpid()) + '] [ERROR] ' + msg)
