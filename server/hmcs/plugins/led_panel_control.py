from .base import PluginBase
import logging
import subprocess
from signal import SIGINT

log = logging.getLogger(__name__)


class LedPanelControlPlugin(PluginBase):
    def register(self):
        self._manager.subscribe_to_socket_event(
            'set_led_panel_mode',
            self.on_mode_change,
        )

        self._running_instance = None

    def _start_instance(self):
        if self._running_instance:
            return

        self._running_instance = subprocess.Popen(
            self._config['executable_args'],
            cwd=self._config['executable_cwd'],
        )

    def _stop_instance(self):
        if not self._running_instance:
            return

        self._running_instance.send_signal(SIGINT)
        self._running_instance.wait(timeout=1)

        if self._running_instance.returncode is None:
            log.info('Process declines to stop, terminating...')
            self._running_instance.ternimate()

        self._running_instance = None

    def on_mode_change(self, data):
        new_mode = data['new_mode']

        log.info('Changing LED panel mode to: %s', new_mode)

        if new_mode:
            self._start_instance()
        else:
            self._stop_instance()
