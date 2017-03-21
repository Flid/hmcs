from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager
from .api_client import APIClient


class MainScreen(Screen):
    _name = 'main'


class SettingsMenuScreen(Screen):
    _name = 'settings'


class HMCSApp(App):
    def build(self):
        self.register_event_type('on_settings_changed')

        self.api_client = APIClient()

        for path in [
            'design/debug.kv',
            'design/main_screen.kv',
            'design/settings_screen.kv',
        ]:
            Builder.load_file(path)

        self.sm = ScreenManager()
        self.screens = {}

        for screen_cls in [
            MainScreen,
            SettingsMenuScreen,
        ]:
            screen = screen_cls(name=screen_cls._name)
            self.screens[screen_cls._name] = screen
            self.sm.add_widget(screen)

        return self.sm

    def on_settings_changed(self):
        pass

    def switch_screen(self, screen_name, direction='left'):
        self.sm.transition.direction = direction
        self.sm.current = screen_name
