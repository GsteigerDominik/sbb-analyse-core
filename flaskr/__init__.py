import configparser
from flask import Flask

from flaskr.log import logger
from flaskr.processor import processor

logger.log_info('Starting app...')

app = Flask(__name__)
from flaskr.api.route import *
from flaskr.jobs.jobs import *

config = configparser.ConfigParser()
config.read('flaskr/cfg/' + app.config.get('ENV') + '.ini')
logger.log_info('Config APP-test: '+str(config.getint('APP', 'test')))

processor.process_station_delay('2023-03-28')
processor.process_station_delay('2023-03-29')
processor.process_station_delay('2023-03-30')
processor.process_station_delay('2023-03-31')
processor.process_station_delay('2023-04-01')