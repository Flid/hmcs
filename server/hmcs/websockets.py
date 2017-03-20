import logging

from flask_socketio import emit, join_room, leave_room

from .app import socketio

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
