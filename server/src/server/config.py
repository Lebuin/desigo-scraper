import os
from datetime import timedelta

DB_PATH = os.environ.get('DB_PATH', '/db/sqlite_scraper.json')

BASIC_AUTH_USERNAME = os.environ['BASIC_AUTH_USERNAME']
BASIC_AUTH_PASSWORD = os.environ['BASIC_AUTH_PASSWORD']
BASIC_AUTH_FORCE = True

DEFAULT_TIME_RANGE = timedelta(days=3)
