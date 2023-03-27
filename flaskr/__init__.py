import configparser

from flask import Flask

print('Starting app...')
app = Flask(__name__)
from flaskr.api.route import *
from flaskr.jobs.jobs import *

config = configparser.ConfigParser()
config.read('flaskr/cfg/' + app.config.get('ENV') + '.ini')
print(config.getint('APP', 'test'))
