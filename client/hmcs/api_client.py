import logging

from hmcs.utils import read_configs
from kivy.app import App
from kivy.event import EventDispatcher
from socketIO_client import LoggingNamespace, SocketIO
from socketIO_client.exceptions import ConnectionError

log = logging.getLogger(__name__)


class APIClient(EventDispatcher):
    def __init__(self):
        self.register_event_type('on_error')
        App.get_running_app().bind(on_settings_changed=self.on_settings_changed)
        self._socket = None

    def on_error(self, message):
        pass

    def on_settings_changed(self, instance):
        log.info('Settings changed, restarting conenction')
        if self._socket and self._socket.connected:
            self._socket.disconnect()

        self._socket = None

    def _connect(self):
        try:
            if not self._socket:
                self._socket = SocketIO(
                    read_configs()['server_host'],
                    read_configs()['server_port'],
                    LoggingNamespace,
                    wait_for_connection=False,
                )
            self._socket.connect()
            return True
        except ConnectionError:
            log.error('Failed to connect')
            self.dispatch('on_error', 'Failed to connect to server')
            return False

    def set_baby_magnet_mode(self, mode):
        if not self._connect():
            return

        self._socket.emit('set_led_panel_mode', mode)
