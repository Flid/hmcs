import logging

from .app import app, socketio

log = logging.getLogger(__name__)


@socketio.on('connect', namespace='/')
def test_connect():
    log.error('New websocket connected')


@socketio.on('disconnect', namespace='/')
def test_disconnect():
    log.debug('Websocket has been disconnected')


@socketio.on('set_led_panel_mode', namespace='/')
def on_set_led_panel_mode(data):
    app.plugin_manager.socket_event_received(
        'set_led_panel_mode',
        data,
    )


@socketio.on('set_lullaby_mode', namespace='/')
def on_set_lullaby_mode(data):
    app.plugin_manager.socket_event_received(
        'set_lullaby_mode',
        data,
    )


@socketio.on('connect_bluetooth', namespace='/')
def on_connect_bluetooth(data):
    app.plugin_manager.socket_event_received(
        'connect_bluetooth',
        data,
    )


@socketio.on('power_off_device', namespace='/')
def on_power_off_device(data):
    app.plugin_manager.socket_event_received(
        'power_off_device',
        data,
    )


@socketio.on_error_default
def error_handler(e):
    log.exception('Failed to process event')
