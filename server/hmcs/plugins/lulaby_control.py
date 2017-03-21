import logging
import os
import subprocess
from signal import SIGINT

from .base import PluginBase

log = logging.getLogger(__name__)


class LullabyControlPlugin(PluginBase):
    def register(self):
        self._manager.subscribe_to_socket_event(
            'set_lullaby_mode',
            self.on_mode_change,
        )

        self._running_instance = None

    def _start_instance(self):
        pass # TODO

    def _stop_instance(self):
        pass # TODO

    def on_mode_change(self, data):
        new_mode = data['new_mode']

        log.info('Changing Lullaby mode to: %s', new_mode)

        if new_mode:
            self._start_instance()
        else:
            self._stop_instance()
