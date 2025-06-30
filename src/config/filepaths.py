"""This config file contains paths to data and model directories."""

import os

from pathlib import Path

REPO_DIR = Path(__file__).parents[2]
REPO_SRC_DIR = Path(__file__).parents[1]

DATA_DIR = os.path.join(REPO_DIR, 'data')
RAW_DATA_DIR = os.path.join(DATA_DIR, 'raw')
RAW_DATA_FP = os.path.join(RAW_DATA_DIR, 'event_stream.csv')

LOG_DIR = os.path.join(DATA_DIR, 'logs')
INGESTION_PPL_LOGFILE = os.path.join(LOG_DIR, 'ingestion_ppl.log')
DASH_APP_LOGFILE = os.path.join(LOG_DIR, 'app.log')
