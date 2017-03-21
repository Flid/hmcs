from kivy.config import Config
from kivy.uix.button import Button
from kivy.clock import Clock
from hmcs.utils import read_configs
from kivy.app import App


class SaveSettingsButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self._load_settings, 0)

    def _load_settings(self, _):
        self.parent.server_host.text = read_configs()['server_host']
        self.parent.server_port.text = read_configs()['server_port']

    def on_press(self):
        if not Config.has_section('main'):
            Config.add_section('main')

        Config.set('main', 'server_host', self.parent.server_host.text)
        Config.set('main', 'server_port', self.parent.server_port.text)
        Config.write()

        App.get_running_app().dispatch('on_settings_changed')
