import logging
import os

from .base import PluginBase

log = logging.getLogger(__name__)


class BluetoothConnectPlugin(PluginBase):
    def register(self):
        self._manager.subscribe_to_socket_event(
            'connect_bluetooth',
            self.connect_bluetooth,
        )

    def connect_bluetooth(self, data):
        log.info('Trying to start bluetooth...')
        os.system(self._config['connect_cmd'])
