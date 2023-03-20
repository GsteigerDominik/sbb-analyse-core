from flask import Flask

print('Starting app...')
app = Flask(__name__)
from flaskr.api.route import *
from flaskr.jobs.jobs import *
