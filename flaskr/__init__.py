from flask import Flask

app = Flask(__name__)
print('Hello Console')
from flaskr.api.route import *
from flaskr.jobs.jobs import *
print('Hello After Console')
