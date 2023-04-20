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
    result = table_of_traintypes()
    traintypes = result[0]
    date = result[1]
    return flask.render_template('overview.html', data=traintypes, date=date)

@app.route('/web/map')
def map():
    return flask.render_template('map.html')

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

def table_of_traintypes():
    x = dbAccess.load_traintype_delay_all()[0][1]
    date = dbAccess.load_traintype_delay_all()[0][0]
    result = []
    for key, value in x.items():
        new_dict = {'name': key, 'delaysum': value['delaysum'], 'delaycount': value['delaycount'], 'totaldatapoints': value['totaldatapoints']}
        result.append(new_dict)

    return_value = (result, date)
    return return_value
