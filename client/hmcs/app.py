from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


class MainScreen(Screen):
    _name = 'main'


class SettingsMenuScreen(Screen):
    _name = 'settings'


class HMCSApp(App):
    def build(self):
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

    def switch_screen(self, screen_name, direction='left'):
        self.sm.transition.direction = direction
        self.sm.current = screen_name
