import logging

from flask_socketio import emit, join_room, leave_room

from .app import socketio, app

log = logging.getLogger(__name__)


@socketio.on('connect', namespace='/')
def test_connect():
    log.error('New websocket connected')


@socketio.on('disconnect', namespace='/')
def test_disconnect():
    log.debug('Websocket has been disconnected')


@socketio.on('set_led_panel_mode', namespace='/')
def on_set_led_panel_mode(new_mode):
    app.plugin_manager.socket_event_received(
        'set_led_panel_mode',
        {'new_mode': new_mode},
    )
