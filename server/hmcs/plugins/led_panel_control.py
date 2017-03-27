import logging
import os
import subprocess
from signal import SIGINT

from .base import PluginBase

log = logging.getLogger(__name__)


class LedPanelControlPlugin(PluginBase):
    def register(self):
        self._manager.subscribe_to_socket_event(
            'set_led_panel_mode',
            self.on_mode_change,
        )

        self._running_instance = None

    def _start_instance(self, brightness):
        if self._running_instance:
            return

        cmd = self._config['executable_args'].format(
            brightness=brightness,
        )

        self._running_instance = subprocess.Popen(
            cmd,
            cwd=self._config['executable_cwd'],
            shell=True,
        )

    def _stop_instance(self):
        if not self._running_instance:
            return

        self._running_instance.send_signal(SIGINT)

        try:
            self._running_instance.wait(timeout=1)
        except subprocess.TimeoutExpired:
            log.info('Process declines to stop, terminating...')
            self._running_instance.terminate()

        self._running_instance = None

        os.system(self._config['stop_command'])

    def on_mode_change(self, data):
        new_mode = data['new_mode']

        log.info('Changing LED panel mode to: %s', new_mode)

        if new_mode:
            self._start_instance(data.get('brightness') or 70)
        else:
            self._stop_instance()
