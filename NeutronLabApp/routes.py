import numpy as np
import random
import time

from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.widgets import Tabs, Panel

from flask import render_template, url_for, jsonify

from NeutronLabApp.forms import SimplePlotForm
from NeutronLabApp import celery
from NeutronLabApp import app


@app.route('/')
def index():
    return render_template(
        "index.html",
        test_plot=url_for('test_plot'),
        taskbar_example=url_for('task_bar_example'),
        pinhole_sans=url_for('pinhole_sans')
    )


@app.route('/test-plot', methods=['GET', 'POST'])
def test_plot():
    form = SimplePlotForm()
    x1, x2 = 0., 1.
    if form.validate_on_submit():
        x1, x2 = map(float, form.data["xs"].replace(' ', '').split(','))

    xs = np.linspace(x1, x2, 100)
    ys = np.sin(xs)

    panels = []
    for axis_type in ["linear", "log"]:
        fig = figure(title='y = sin(x)', x_axis_label='x', y_axis_label='y', y_axis_type=axis_type)
        fig.line(xs, ys, line_width=2)

        panel = Panel(child=fig, title=axis_type)
        panels.append(panel)

    script, div = components(Tabs(tabs=panels))

    return render_template(
        "simple-plot.html",
        form=form,
        script=script,
        div=div
    )


@app.route('/taskbar-example', methods=['GET', 'POST'])
def task_bar_example():
    return render_template(
        'taskbar-example.html'
    )


@celery.task(bind=True)
def long_task(self):
    """Background task that runs a long function with progress reports."""
    verb = ['Starting up', 'Booting', 'Repairing', 'Loading', 'Checking']
    adjective = ['master', 'radiant', 'silent', 'harmonic', 'fast']
    noun = ['solar array', 'particle reshaper', 'cosmic ray', 'orbiter', 'bit']
    message = ''
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = '{0} {1} {2}...'.format(random.choice(verb),
                                              random.choice(adjective),
                                              random.choice(noun))
        self.update_state(state='PROGRESS',
                          meta={'current': i, 'total': total,
                                'status': message})
        time.sleep(1)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': 42}


@app.route('/longtask', methods=['POST'])
def longtask():
    task = long_task.apply_async()
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    task = long_task.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current', 0),
            'total': task.info.get('total', 1),
            'status': task.info.get('status', '')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
