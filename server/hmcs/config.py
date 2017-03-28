import os
import sys
from collections import OrderedDict

DEBUG = os.environ.get('DEBUG', False)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,

    'root': {
        'level': 'DEBUG',
        'handlers': ['console'],
    },

    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s',
        },
        'standard': {
            'format': ' %(asctime)s %(message)s',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'stdout': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'stream': sys.stdout,
        },
    },

    'loggers': {
        'hmcs': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

SERVER_PORT = 5000

PLUGINS_ENABLED = OrderedDict([
    ('led_control_panel', 'hmcs.plugins.led_panel_control.LedPanelControlPlugin'),
    ('bt_connect', 'hmcs.plugins.bt_connect.BluetoothConnectPlugin'),
    ('lullaby_control', 'hmcs.plugins.lullaby_control.LullabyControlPlugin'),
    ('poweroff_device', 'hmcs.plugins.poweroff_device.PoweroffDevicePlugin'),
])


PLUGIN_CONFIG = {
    'led_control_panel': {
        'executable_cwd': os.environ['LED_CONTROL_CWD'],
        'executable_args': os.environ['LED_CONTROL_COMMAND'],
        'stop_command': os.environ['LED_CONTROL_STOP_COMMAND'],
    },
    'bt_connect': {
        'connect_cmd': os.environ['BT_CONNECT_COMMAND'],
    },
    'lullaby_control': {
        'file_path': os.environ['LULLABY_FILE_PATH'],
    },
    'poweroff_device': {
        'poweroff_device_cmd': os.environ['POWEROFF_DEVICE_CMD'],
    },
}
