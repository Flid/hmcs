from logging.config import DictConfigurator

from flask import Flask
from flask_socketio import SocketIO

from . import config


app = Flask(__name__)
socketio = SocketIO(app)


def init():
    from . import websockets  # noqa
    DictConfigurator(config.LOGGING).configure()
    socketio.run(app, debug=config.DEBUG, use_reloader=config.DEBUG)
