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


@app.route('/web', methods=('GET', 'POST'))
def web():
    if request.method == 'POST':
        stations = get_Array(dbAccess.load_station_delay_by_date(request.form['date'])[0][1])
    elif request.method == 'GET':
        stations = get_Array(dbAccess.load_station_delay_all())

    traintypes = get_Array(dbAccess.load_traintype_delay_all())
    dates = dbAccess.load_station_delay_dates()
    return flask.render_template('overview.html', trains=traintypes, stations=stations, dates=dates)


@app.route('/web/map')
def map():
    stations = get_Array(dbAccess.load_station_delay_all())
    return flask.render_template('map.html', stations=stations)

@app.route('/marker.png')
def marker_png():
    with open('static/marker.png', 'rb') as f:
        marker_png = f.read()
    return Response(marker_png, mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

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
    
def geometric_distribution():
    data = dbAccess.load_station_delay_all()
    delays = [d[0] for d in data]
    total_delays = len(delays)
    unique_delays, counts = np.unique(delays, return_counts=True)
    probabilities = counts / total_delays
    plt.stem(unique_delays, probabilities, use_line_collection=True)
    plt.title('Probability Mass Function of Delays')
    plt.xlabel('Delay (minutes)')
    plt.ylabel('Probability')
    plt.show()

    