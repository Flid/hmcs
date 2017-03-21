import importlib
from collections import defaultdict

from axel import Event

from hmcs import config


class PluginManager():
    def __init__(self):
        self.system_init = Event()
        self.socket_event_received = Event()
        self.socket_event_received += self._on_socket_event_received
        self._socket_event_subscribers = defaultdict(list)
        self._plugins = []

    def _import_class(self, full_path):
        path, class_name = full_path.rsplit('.', 1)
        return getattr(importlib.import_module(path), class_name)

    def init_plugins(self):
        for name, path in config.PLUGINS_ENABLED.items():
            cls = self._import_class(path)
            obj = cls(self, config.PLUGIN_CONFIG.get(name, {}))
            obj.register()
            self._plugins.append(obj)

        self.system_init()

    def subscribe_to_socket_event(self, event_name, callback):
        assert callable(callback)

        self._socket_event_subscribers[event_name].append(callback)

    def _on_socket_event_received(self, event_name, data):
        for callback in self._socket_event_subscribers[event_name]:
            callback(data)


class PluginBase():
    def __init__(self, manager, plugin_config):
        self._manager = manager
        self._config = plugin_config

    def register(self):
        """
        Plugins should do some initialization here, like subscribe to events.
        """
