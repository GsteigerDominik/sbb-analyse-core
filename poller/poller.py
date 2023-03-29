import json
import sys
from datetime import datetime, timedelta

import requests

from flaskr.db import dbAccess
from flaskr.log import logger


def runPollJob():
    logger.logInfo("Poll Job starting...")
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime('%Y-%m-%d')
    response = requests.get(
        "https://data.sbb.ch/api/v2/catalog/datasets/ist-daten-sbb/records?limit=100&offset=0&timezone=UTC")
    response_dict = json.loads(response.content)
    logger.logInfo('Size of Yesterday'+ str(response_dict['total_count']))
    formatted_json_data = json.dumps(response_dict, ensure_ascii=False)
    dbAccess.saveUnprocessedData(formatted_date, formatted_json_data)
    timesToPoll = int(response_dict['total_count'] / 100) + 1
    for x in range(0, timesToPoll):
        logger.logInfo('Processed ' + str(x) + ' of ' + str(timesToPoll))
        processOneRequest(response_dict['links'][3]['href'],formatted_date)
    logger.logInfo("Poll Job finished")

def processOneRequest(url,formatted_date):
    response = requests.get(url)
    response_dict = json.loads(response.content)
    formatted_json_data = json.dumps(response_dict, ensure_ascii=False)
    dbAccess.saveUnprocessedData(formatted_date, formatted_json_data)
