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

from datetime import datetime, timedelta


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

def extract_delays():
    date = dbAccess.load_unprocessed_dates()
    delays = []

    for d in date:
        result = dbAccess.load_unprocessed_data(d)
        for row in result:
            if 'records' in row[2]:
                data_set = row[2]['records']
                for data_point in data_set:
                    if data_point['record']['fields']['ankunftsverspatung'] == 'true':
                        actual = datetime.fromisoformat(data_point['record']['fields']['an_prognose'])
                        planed = datetime.fromisoformat(data_point['record']['fields']['ankunftszeit'])
                        delays.append(int((actual - planed).total_seconds() / 60))

    return delays

@app.route('/stats.png') 
def boxplot():
    data = extract_delays()
    ax = plt.subplots()
    ax.boxplot(data, linewidth=5)
    plt.show()


def geometric_distribution_60():
    delays = extract_delays()
    total_delays = len(delays)
    unique_delays, counts = np.unique(delays, return_counts=True)
    probabilities = counts / total_delays
    
    # Filter delays and probabilities to include only values less than or equal to 60
    mask = unique_delays <= 60
    unique_delays = unique_delays[mask]
    probabilities = probabilities[mask]
    
    plt.pyplot.stem(unique_delays, probabilities, markerfmt='o', use_line_collection=False)
    plt.pyplot.title('Probability of unique Delays')
    plt.pyplot.xlabel('Delay (minutes)')
    plt.pyplot.ylabel('Probability')
    plt.pyplot.grid()
    plt.pyplot.xlim(0, 60)  # set the x-axis limit to 0-60
    plt.pyplot.show()
    
    return Response(plt.savefig('foo.png'), mimetype='image/png')