"""This script contains log configs for this repo."""

import logging
import logging.config

from src.config.filepaths import INGESTION_PPL_LOGFILE, DASH_APP_LOGFILE

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'file_handler_ingestion_ppl': {
            'class': 'logging.FileHandler',
            'filename': INGESTION_PPL_LOGFILE,
            'formatter': 'standard',
            'level': 'INFO',
        },
        'file_handler_app': {
            'class': 'logging.FileHandler',
            'filename':  DASH_APP_LOGFILE,
            'formatter': 'standard',
            'level': 'INFO',
        },
    },
    'loggers': {
        'ingestion_ppl_logger': {
            'handlers': ['file_handler_ingestion_ppl'],
            'level': 'INFO',
            'propagate': False
        },
        'app_logger': {
            'handlers': ['file_handler_app'],
            'level': 'INFO',
            'propagate': False
        },
    }
}

def setup_logging():
    logging.config.dictConfig(LOGGING_CONFIG)
