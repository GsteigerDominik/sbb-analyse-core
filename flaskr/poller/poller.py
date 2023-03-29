import json
from datetime import datetime, timedelta

import requests

from flaskr.db import dbAccess
from flaskr.log import logger


def run_poll_job():
    logger.log_info("PollJob:  Status changed to started")
    yesterday = datetime.now() - timedelta(days=1)
    formatted_date = yesterday.strftime('%Y-%m-%d')
    response_dict = process_one_request(
        "https://data.sbb.ch/api/v2/catalog/datasets/ist-daten-sbb/records?limit=100&offset=0&timezone=UTC",
        formatted_date)
    logger.log_info('PollJob: Size of Yesterday: ' + str(response_dict['total_count']))
    times_to_poll = int(response_dict['total_count'] / 100) + 1
    next_url = find_next_url(response_dict)
    for x in range(0, times_to_poll):
        if next_url is not None:
            response_dict = process_one_request(next_url, formatted_date)
            next_url = find_next_url(response_dict)
            logger.log_info('PollJob: Processed ' + str(x + 1) + ' of ' + str(times_to_poll))
        else:
            break
    logger.log_info("PollJob: Status changed to finished")


def process_one_request(url, formatted_date):
    response = requests.get(url)
    response_dict = json.loads(response.content)
    formatted_json_data = json.dumps(response_dict, ensure_ascii=False)
    dbAccess.save_unprocessed_data(formatted_date, formatted_json_data)
    return response_dict


def find_next_url(response_dict):
    if 'error_code' in response_dict:
        return
    for item in response_dict['links']:
        if item['rel'] == 'next':
            return item['href']
