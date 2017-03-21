from kivy.config import Config

SETTINGS_DEFAULTS = {
    'server_host': '192.168.0.11',
    'server_port': '5000',
}


def read_configs():
    output = {}

    for key, default_value in SETTINGS_DEFAULTS.items():
        output[key] = Config.getdefault(
            'main',
            key,
            default_value,
        )
    return output
