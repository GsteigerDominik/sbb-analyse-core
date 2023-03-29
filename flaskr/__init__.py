import configparser
from flask import Flask

from flaskr.log import logger

logger.logInfo('Starting app...')

app = Flask(__name__)
from flaskr.api.route import *
from flaskr.jobs.jobs import *

config = configparser.ConfigParser()
config.read('flaskr/cfg/' + app.config.get('ENV') + '.ini')
logger.logInfo('Config APP-test: '+str(config.getint('APP', 'test')))
