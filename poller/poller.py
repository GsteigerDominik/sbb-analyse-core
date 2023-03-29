import json
import sys
from datetime import datetime, timedelta

import requests

from flaskr.db import dbAccess
from flaskr.log import logger


def runPollJob():
    logger.logInfo("PollJob:  Status changed to started")
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime('%Y-%m-%d')
    response = requests.get(
        "https://data.sbb.ch/api/v2/catalog/datasets/ist-daten-sbb/records?limit=100&offset=0&timezone=UTC")
    response_dict = json.loads(response.content)
    logger.logInfo('PollJob: Size of Yesterday: '+ str(response_dict['total_count']))
    formatted_json_data = json.dumps(response_dict, ensure_ascii=False)
    dbAccess.saveUnprocessedData(formatted_date, formatted_json_data)
    timesToPoll = int(response_dict['total_count'] / 100) + 1
    nextUrl=findNextUrl(response_dict,' ')
    for x in range(0, timesToPoll):
        if nextUrl is not None:
            #TOOD Still not working right
            response_dict=processOneRequest(nextUrl,formatted_date)
            nextUrl=findNextUrl(response_dict,nextUrl)
            logger.logInfo('PollJob: Processed ' + str(x+1) + ' of ' + str(timesToPoll))
        else:
            break
    logger.logInfo("PollJob: Status changed to finished")

def processOneRequest(url,formatted_date):
    response = requests.get(url)
    response_dict = json.loads(response.content)
    formatted_json_data = json.dumps(response_dict, ensure_ascii=False)
    dbAccess.saveUnprocessedData(formatted_date, formatted_json_data)
    return response_dict

def findNextUrl(response_dict,nextUrl):
    if 'error_code' in response_dict:
        return
    for item in response_dict['links']:
        if item['rel'] == 'next':
            return item['href']