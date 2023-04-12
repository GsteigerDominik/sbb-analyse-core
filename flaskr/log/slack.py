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
        message = 'You can use following commands:\n' \
                  'data-status'
    elif 'data-status' in event["text"]:
        message = 'We got allot of data :male_mage:\n' \
                  'For all this dates we got data:'
        dates = dbAccess.load_unprocessed_dates()
        for date in dates:
            message += ' '+ date[0].strftime('%Y-%m-%d')
    else:
        message = "Hello, how can i help you? If you dont know me use 'help'!"
    post_msg(message, event["channel"])
