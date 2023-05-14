import json
from datetime import datetime

from flask import request, Response

from flaskr import app
from flaskr.bl.jobs import get_jobs
from flaskr.log.slack import handle_event


@app.route('/')
def index():
    return 'Hello World!'


@app.route("/jobs")
def jobs():
    html = "<p>Use LocalTime in DevEnvironment</p> <br><table><tr><th>Name</th><th>Function</th><th>Next " \
           "Execution</th></tr> "
    for job in get_jobs():
        html += "<tr><td>" + job.name \
                + "</td><td>" + job.func_ref + "</td><td>" + str(job.next_run_time) + "</td></tr>"
    return html + "</table>"


@app.route("/slack/events", methods=["POST"])
def slack_events():
    request_body = request.get_data().decode("utf-8")
    request_dict = json.loads(request_body)

    if "challenge" in request_dict:
        return Response(request_dict["challenge"], mimetype="text/plain")

    if "event" in request_dict:
        event = request_dict["event"]
        if event["type"] == "app_mention":
            handle_event(event)

    return Response(status=200)


def validate_date(input_date):
    if input_date is None:
        return False
    try:
        datetime.strptime(input_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False
