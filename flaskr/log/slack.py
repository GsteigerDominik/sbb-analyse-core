import os
import pandas as pd

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
                  'help\n' \
                  'jobs\n' \
                  'data-status-raw\n' \
                  'data-status-traintype\n' \
                  'data-status-station'
    elif 'jobs' in event["text"]:
        # This import is needed to prevent a circular dependency
        from flaskr.bl.jobs import get_jobs
        message = ':male_mage: These are our Jobs, you can see when there next run is:\n'
        for job in get_jobs():
            message += job.name + ' ' + job.func_ref + ' ' + str(job.next_run_time) + '\n'
    elif 'data-status-raw' in event["text"]:
        message = ':male_mage: We got a lot of raw data\n' \
                  'For all this dates we got raw data:'
        dates = dbAccess.load_unprocessed_dates()
        message += calculate_date_interval(dates)
    elif 'data-status-traintype' in event["text"]:
        message = ':male_mage: We got a lot of traintype data\n' \
                  'For all this dates we got traintype data:'
        dates = dbAccess.load_traintype_delay_dates()
        message += calculate_date_interval(dates)
    elif 'data-status-station' in event["text"]:
        message = ':male_mage: We got a lot of station data\n' \
                  'For all this dates we got station data:'
        dates = dbAccess.load_station_delay_dates()
        message += calculate_date_interval(dates)
    else:
        message = ":male_mage: Hello, how can i help you? If you dont know me, use 'help'!"
    post_msg(message, event["channel"])


def post_job_finished_msg(date, name):
    message = ':construction_worker: ' + name + ' data of ' + date
    post_msg(message)


def calculate_date_interval(dates):
    df = pd.DataFrame(dates, columns=['date'])
    df = df.sort_values('date')
    df['date_diff'] = (df['date'] - df['date'].shift()).fillna(pd.Timedelta(days=1))
    df['interval'] = (df['date_diff'] > pd.Timedelta(days=1)).cumsum()
    intervals = df.groupby('interval')['date'].agg(['min', 'max']).reset_index()
    return ', '.join([f'{interval[1]["min"].strftime("%Y-%m-%d")} - {interval[1]["max"].strftime("%Y-%m-%d")}' for interval in intervals.iterrows()])
