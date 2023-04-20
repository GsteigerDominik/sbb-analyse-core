import io
import flask
from flaskr import app
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from flaskr.db import dbAccess

@app.route('/web')
def web():
    traintypes = get_Array(dbAccess.load_traintype_delay_all())
    stations = get_Array(dbAccess.load_station_delay_all())
    return flask.render_template('overview.html', trains=traintypes, stations=stations)

@app.route('/web/map')
def map():
    stations = get_Array(dbAccess.load_station_delay_all())
    return flask.render_template('map.html', stations=stations)

@app.route('/test.png')
def plot_png():
    fig = create_figure()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

def create_figure():
    fig = Figure()
    axis = fig.add_subplot(1, 1, 1)
    xs = range(100)
    ys = [random.randint(1, 50) for x in xs]
    axis.plot(xs, ys)
    return fig

def get_Array(x):
    result = []
    for key, value in x.items():
        new_dict = {'name': key, 'delaysum': value['delaysum'], 'delaycount': value['delaycount'], 'totaldatapoints': value['totaldatapoints']}
        result.append(new_dict)

    return result
