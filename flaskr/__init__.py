from flask import Flask

from flaskr.bl import processor
from flaskr.log import logger

logger.log_info('Starting app...')

app = Flask(__name__)
from flaskr.api.route import *
from flaskr.web.web import *
from flaskr.bl.jobs import *
from flaskr.bl import processor

processor.boxplot_one()
processor.geometric_distribution_60()