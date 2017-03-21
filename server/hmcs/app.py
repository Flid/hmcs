from logging.config import DictConfigurator

from flask import Flask
from flask_socketio import SocketIO

from . import config

app = Flask(__name__)
socketio = SocketIO(app)


def init():
    from . import websockets  # noqa
    from .plugins.base import PluginManager

    DictConfigurator(config.LOGGING).configure()

    app.plugin_manager = PluginManager()
    app.plugin_manager.init_plugins()

    socketio.run(
        app,
        debug=config.DEBUG,
        use_reloader=config.DEBUG,
        host='0.0.0.0',
        port=config.SERVER_PORT,
    )
