from .base import PluginBase
import logging

log = logging.getLogger(__name__)


class LedPanelControlPlugin(PluginBase):
    def __init__(self, manager):
        super().__init__(manager)

        manager.subscribe_to_socket_event(
            'set_led_panel_mode',
            self.on_mode_change,
        )

    def on_mode_change(self, new_mode):
        log.info('Changing LED panel mode to: %s', new_mode)
