import os
import sys


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


PLUGINS_ENABLED = [
    'hmcs.plugins.led_panel_control.LedPanelControlPlugin'
]
