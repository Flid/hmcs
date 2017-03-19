from kivy.config import Config
from kivy.uix.button import Button
from kivy.clock import Clock


def read_configs():
    return {
        'server_url': Config.getdefault(
            'main',
            'server_url',
            'http://0.0.0.0',
        ),
    }


class SaveSettingsButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self._load_settings, 0)

    def _load_settings(self, _):
        self.parent.server_url.text = read_configs()['server_url']

    def on_press(self):
        if not Config.has_section('main'):
            Config.add_section('main')

        Config.set('main', 'server_url', self.parent.server_url.text)
        Config.write()