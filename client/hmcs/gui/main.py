from kivy.app import App
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.label import Label


class BaseLCDControlSwitch(Button):
    action = None

    def on_press(self):
        App.get_running_app().api_client.set_baby_magnet_mode(self.new_mode)


class LCDControlSwitchOn(BaseLCDControlSwitch):
    new_mode = True


class LCDControlSwitchOff(BaseLCDControlSwitch):
    new_mode = False


class BaselLullabyControlSwitch(Button):
    action = None

    def on_press(self):
        App.get_running_app().api_client.set_lullaby_mode(self.new_mode)


class LullabyControlSwitchOn(BaselLullabyControlSwitch):
    new_mode = True


class LullabyControlSwitchOff(BaselLullabyControlSwitch):
    new_mode = False


class BluetoothConnectButton(Button):
    def on_press(self):
        App.get_running_app().api_client.connect_bluetooth()


class ErrorLabel(Label):
    def __init__(self, *args, **kwargs):
        super(ErrorLabel, self).__init__(*args, **kwargs)
        App.get_running_app().api_client.bind(on_error=self.on_error)

    def on_error(self, instance, message):
        self.text = message

        Clock.unschedule(self.clean_text, all=True)
        Clock.schedule_interval(self.clean_text, 2)

    def clean_text(self, instance):
        self.text = ''
