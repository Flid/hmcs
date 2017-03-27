import logging
from pygame import mixer
from .base import PluginBase

log = logging.getLogger(__name__)


class LullabyControlPlugin(PluginBase):
    def register(self):
        self._manager.subscribe_to_socket_event(
            'set_lullaby_mode',
            self.on_mode_change,
        )

        self._playing = False

    def _start_instance(self):
        if self._playing:
            return

        mixer.init()
        mixer.music.load(self._config['file_path'])
        mixer.music.play(loops=-1)
        self._playing = True

    def _stop_instance(self):
        if not self._playing:
            return

        mixer.music.stop()
        mixer.quit()
        self._playing = False

    def on_mode_change(self, data):
        new_mode = data['new_mode']

        log.info('Changing Lullaby mode to: %s', new_mode)

        if new_mode:
            self._start_instance()
        else:
            self._stop_instance()
