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
])

PLUGIN_CONFIG = {
    'led_control_panel': {
        'executable_cwd': os.environ['LED_CONTROL_CWD'],
        'executable_args': os.environ['LED_CONTROL_COMMAND'],
        'stop_command': os.environ['LED_CONTROL_STOP_COMMAND'],
    },
}
