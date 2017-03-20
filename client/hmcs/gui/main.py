from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from socketIO_client import SocketIO
from kivy.app import App

class BaseLCDControlSwitch(Button):
    action = None

    def on_press(self):
        App.get_running_app().api_client.set_baby_magnet_mode(self.new_mode)


class LCDControlSwitchOn(BaseLCDControlSwitch):
    new_mode = True


class LCDControlSwitchOff(BaseLCDControlSwitch):
    new_mode = False
