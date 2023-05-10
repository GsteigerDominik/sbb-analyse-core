import datetime
import io
import flask
from flaskr import app
import io
import random
from flask import Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flaskr.db import dbAccess
import matplotlib as plt
import seaborn as sns
from scipy.stats import geom
import numpy as np


@app.route('/web', methods=('GET', 'POST'))
def web():
    if request.method == 'POST':
        if request.form['date'] == 'all':
            stations = get_Array(dbAccess.load_station_delay_all())
            traintypes = get_Array(dbAccess.load_traintype_delay_all())
        else:
            stations = get_Array(dbAccess.load_station_delay_by_date(request.form['date'])[0][1])
            traintypes = get_Array(dbAccess.load_traintype_delay_by_date(request.form['date'])[0][1])
        scope = request.form['date']
    elif request.method == 'GET':
        stations = get_Array(dbAccess.load_station_delay_all())
        traintypes = get_Array(dbAccess.load_traintype_delay_all())
        scope = 'all'

    dates = dbAccess.load_station_delay_dates()
    dates.sort()
    dates.insert(0, 'all')

    return flask.render_template('base.html', trains=traintypes, stations=stations, dates=dates, scope=scope)

@app.route('/marker.png')
def marker_png():
    with open('static/marker.png', 'rb') as f:
        marker_png = f.read()
    return Response(marker_png, mimetype='image/png')

def get_Array(dict):
    result = []
    for key, value in dict.items():
        if "geopos_lat" in value:
            new_dict = {"name": key, "delaysum": value["delaysum"], "delaycount": value["delaycount"], "totaldatapoints": value["totaldatapoints"], "geopos_lat": value["geopos_lat"], "geopos_lon": value["geopos_lon"]}
        else:
            new_dict = {"name": key, "delaysum": value["delaysum"], "delaycount": value["delaycount"], "totaldatapoints": value["totaldatapoints"]}

        result.append(new_dict)
    return result

def boxplot():
    data = dbAccess.load_station_delay_all()
    sns.boxplot(data, linewidth=5)
    
@app.route('/stats.png')
def geometric_distribution():
    data = dbAccess.load_station_delay_all()
    delays = [d[0] for d in data]
    total_delays = len(delays)
    unique_delays = list(set(data))
    probabilities = 5 / total_delays
    plt.pyplot.stem(unique_delays, probabilities, use_line_collection=True)
    plt.pyplot.title('Probability Mass Function of Delays')
    plt.pyplot.xlabel('Delay (minutes)')
    plt.pyplot.ylabel('Probability')
    plt.pyplot.show()
    return Response(plt.savefig('foo.png'), mimetype='image/png')