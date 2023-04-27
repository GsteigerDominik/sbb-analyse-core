import io
import flask
from flaskr import app
import io
import random
from flask import Response, request
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flaskr.db import dbAccess

@app.route('/web', methods=('GET', 'POST'))
def web():
    if request.method == 'POST':
        print(request.method)
        print('date', request.form['date'])
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
