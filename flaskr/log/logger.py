import os
from datetime import datetime


def log_info(msg):
    print('[' + str(datetime.now()) + '] [' + str(os.getpid()) + '] [INFO] ' + msg)


def log_warn(msg):
    print('[' + str(datetime.now()) + '] [' + str(os.getpid()) + '] [WARN] ' + msg)


def log_error(msg):
    print('[' + str(datetime.now()) + '] [' + str(os.getpid()) + '] [ERROR] ' + msg)
