from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


class MainMenuScreen(Screen):
    _name = 'menu_main'


class SettingsMenuScreen(Screen):
    _name = 'menu_settings'


class MainIngameScreen(Screen):
    _name = 'main_ingame'


class MyGameApp(App):
    def build(self):
        for path in [
            'design/debug.kv',
            'design/menu/main.kv',
            'design/menu/settings.kv',
            'design/main/board.kv',
            'design/main/panels.kv',

            'design/main/ingame.kv',
        ]:
            Builder.load_file(path)

        self.sm = ScreenManager()
        self.screens = {}

        for screen_cls in [
            MainIngameScreen,
            MainMenuScreen,
            SettingsMenuScreen,
        ]:
            screen = screen_cls(name=screen_cls._name)
            self.screens[screen_cls._name] = screen
            self.sm.add_widget(screen)

        return self.sm

    def switch_screen(self, screen_name, direction='left'):
        self.sm.transition.direction = direction
        self.sm.current = screen_name