import configparser
from flask import Flask

from flaskr.log import logger
from flaskr.processor import processor
from flask_cors import CORS

logger.log_info('Starting app...')

app = Flask(__name__)
from flaskr.api.route import *
from flaskr.jobs.jobs import *
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

config = configparser.ConfigParser()
config.read('flaskr/cfg/' + app.config.get('ENV') + '.ini')
logger.log_info('Config APP-test: '+str(config.getint('APP', 'test')))

processor.run_initial()
