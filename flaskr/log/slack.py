import os

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from flaskr.db import dbAccess
from flaskr.log import logger

client = WebClient(token=os.environ.get("SLACK_BOT_TOKEN"))


def post_msg(message, channel_id="#sp-arbeit"):
    try:
        response = client.chat_postMessage(channel=channel_id, text=message)
    except SlackApiError as e:
        logger.log_error(f"Error: {e.response['error']}")


def handle_event(event):
    message = ""
    if 'help' in event['text']:
        message = ':male_mage: You can use following commands:\n' \
                  'data-status-raw\n'\
                  'data-status-traintype\n' \
                  'data-status-station'
    elif 'data-status-raw' in event["text"]:
        message = ':male_mage: We got a lot of raw data\n' \
                  'For all this dates we got raw data:'
        dates = dbAccess.load_unprocessed_dates()
        for date in dates:
            message += ' ' + date[0].strftime('%Y-%m-%d')
    elif 'data-status-traintype' in event["text"]:
        message = ':male_mage: We got a lot of processed data\n' \
                  'For all this dates we got processed data:'
        dates = dbAccess.load_traintype_delay_dates()
        for date in dates:
            message += ' ' + date[0].strftime('%Y-%m-%d')
    elif 'data-status-station' in event["text"]:
        message = ':male_mage: We got a lot of processed data\n' \
                  'For all this dates we got processed data:'
        dates = dbAccess.load_station_delay_dates()
        for date in dates:
            message += ' ' + date[0].strftime('%Y-%m-%d')
    else:
        message = ":male_mage: Hello, how can i help you? If you dont know me, use 'help'!"
    post_msg(message, event["channel"])


def post_job_finished_msg(date):
    message = ':construction_worker: Processed data of ' + date
    post_msg(message)
