import logging

from flask_socketio import emit, join_room, leave_room

from . import formatters
from .app import socketio
from .db import Job, JobRecord

log = logging.getLogger(__name__)


@socketio.on('message')
def handle_message(message):
    log.info('received message: ' + message)


@socketio.on('connect', namespace='/')
def test_connect():
    log.error('New websocket connected')


@socketio.on('disconnect', namespace='/')
def test_disconnect():
    log.debug('Websocket has been disconnected')


@socketio.on('listening_job', namespace='/')
def on_listening_job(data):
    join_room('job_' + str(data['job_id']))

    # Send existing data
    items = JobRecord.query.filter_by(job_id=data['job_id']).order_by('seconds')
    to_send = [item.payload for item in items]

    if to_send:
        emit('new_data', to_send)


@socketio.on('listening_lobby', namespace='/')
def on_listening_job():
    join_room('lobby')

    # Send existing jobs
    items = Job.query.order_by('created_at').all()

    to_send = [formatters.format_job(item) for item in items]

    if to_send:
        emit('new_jobs', {
            'initial': True,
            'items': to_send,
        })
