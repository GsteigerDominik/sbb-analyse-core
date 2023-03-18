from flask import Flask

app = Flask(__name__)

import flaskr.api.route
import flaskr.jobs.jobs