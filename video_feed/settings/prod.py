from .base import *
import os




DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'django_errors.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': True,
        },
    },
}

print("AWS_ACCESS_KEY_ID:", AWS_ACCESS_KEY_ID)
print("DEFAULT_FILE_STORAGE:", DEFAULT_FILE_STORAGE)
