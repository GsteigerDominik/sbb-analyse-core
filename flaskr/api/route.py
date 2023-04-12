import json
from datetime import datetime

from flask import request, Response
from slack_sdk.errors import SlackApiError

import flaskr.log.logger
from flaskr import app
from flaskr.db import dbAccess
from flaskr.jobs.jobs import scheduler
from flaskr.log import slack
from flaskr.log.slack import client


@app.route('/')
def index():
    return 'Hello World!'


@app.route("/jobs")
def jobs():
    html = "<p>Use LocalTime in DevEnvironment</p> <br><table><tr><th>Name</th><th>Function</th><th>Next " \
           "Execution</th></tr> "
    for job in scheduler.get_jobs():
        html += "<tr><td>" + job.name \
                + "</td><td>" + job.func_ref + "</td><td>" + str(job.next_run_time) + "</td></tr>"
    return html + "</table>"


@app.route("/api/station")
def station():
    date = request.args.get('date')
    if validate_date(date):
        return dbAccess.load_station_delay_by_date(date)
    else:
        return dbAccess.load_station_delay_all()


@app.route("/api/traintype")
def traintype():
    date = request.args.get('date')
    if validate_date(date):
        print(date)
        return dbAccess.load_traintype_delay_by_date(date)
    else:
        return dbAccess.load_traintype_delay_all()


@app.route("/slack/events", methods=["POST"])
def slack_events():
    request_body = request.get_data().decode("utf-8")
    request_dict = json.loads(request_body)

    if "challenge" in request_dict:
        return Response(request_dict["challenge"], mimetype="text/plain")

    if "event" in request_dict:
        event = request_dict["event"]
        if event["type"] == "app_mention":
            channel_id = event["channel"]
            message = "Hello, you can interact with me (Available commands: data-status)"
            if 'data-status' in event["text"]:
                message='We got allot of data :male_mage:\n' \
                        'For all this dates we got data:\n'
                dates=dbAccess.load_unprocessed_dates()
                for date in dates:
                    message+=date[0].strftime('%Y-%m-%d')+'\n'

            try:
                response = client.chat_postMessage(channel=channel_id, text=message)
            except SlackApiError as e:
                print(f"Error: {e.response['error']}")

    return Response(status=200)


def validate_date(input_date):
    if input_date is None:
        return False
    try:
        datetime.strptime(input_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False
