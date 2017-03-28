import logging
import os

from .base import PluginBase

log = logging.getLogger(__name__)


class PoweroffDevicePlugin(PluginBase):
    def register(self):
        self._manager.subscribe_to_socket_event(
            'power_off_device',
            self.power_off_device,
        )

    def power_off_device(self, data):
        log.info('Trying to power off...')
        os.system(self._config['poweroff_device_cmd'])
