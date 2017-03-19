import json

from flask.templating import render_template
from flask_socketio import emit

from .app import app


CACHED_PAGES = {}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/jobs/<int:job_id>')
def job_page(job_id):
    return render_template('job.html', job_id=job_id)

