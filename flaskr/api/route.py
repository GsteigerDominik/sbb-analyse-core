from datetime import datetime

from flask import request

from flaskr import app
from flaskr.db import dbAccess
from flaskr.jobs.jobs import scheduler


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
        return dbAccess.load_traintype_delay_by_date(date)
    else:
        return dbAccess.load_traintype_delay_all()


def validate_date(input_date):
    try:
        datetime.strptime(input_date, '%Y-%m-%d')
        return True
    except ValueError:
        return False
