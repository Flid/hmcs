from kivy.config import Config


def read_configs():
    return {
        'server_url': Config.getdefault(
            'main',
            'server_url',
            'http://0.0.0.0',
        ),
    }
