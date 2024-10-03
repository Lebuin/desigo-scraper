import logging
import os

from selenium.webdriver.common.by import By, ByType
import pytz

from . import t

LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)

# How to reach selenium. If developing outside the docker container you will want to override this
# in your .env file.
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'selenium:4444')
# The path to the "db" file (which is not really a database, just a json file). If developing
# outside the docker you will want to override this in you .env file.
DB_PATH = os.environ.get('DB_PATH', '/db/sqlite_scraper.json')


# Every group has their own Desigo instance. Set their properties in the .env file.
DESIGO_INSTANCES: dict[t.Group, t.DesigoInstance] = {
    t.Group.BIOTOPE: t.DesigoInstance(
        group=t.Group.BIOTOPE,
        host=os.environ['BIOTOPE_HOST'],
        username=os.environ['BIOTOPE_USERNAME'],
        password=os.environ['BIOTOPE_PASSWORD'],
        timezone=pytz.timezone('Europe/Brussels'),
    )
}


# Chart views are the entrypoint of our scraping. Each chart view listed here is visited in turn,
# and all the data on these pages is downloaded and stored.
#
# To find the url of a specific chart view:
# - Visit https://{host}/finMobile/desigo#trends
# - Click one of the chart views
# - Copy the URL in the address bar
CHART_VIEWS: list[t.ChartView] = [
    t.ChartView(
        group=t.Group.BIOTOPE,
        name='Warmtepomp',
        path='/finMobile/desigo#trends?q=@29dea950-5e6d767b',
    ),
    t.ChartView(
        group=t.Group.BIOTOPE,
        name='KWh Telling BEO Veld',
        path='/finMobile/desigo#trends?q=@29dea58b-096c33ee'
    ),
]


# How long to wait for a chart view to load. These views are notoriously slow, so this timeout has
# to be very l
CHART_VIEW_TIMEOUT = 300

# The path for the Desigo login page
LOGIN_PATH = '/om/#/landing/login'

# All the selectors used during navigation. Scraping data from a table is not prescriped here,
# this is hardcoded in browser.Browser._download_data.
SELECTORS: dict[str, dict[str, tuple[ByType, str]]] = {
    'login': {
        'username': (By.CSS_SELECTOR, 'input[name="username"]'),
        'password': (By.CSS_SELECTOR, 'input[name="password"]'),
        'submit': (By.CSS_SELECTOR, '[type="submit"]'),
    },
    'main': {
        'navbar': (By.CSS_SELECTOR, '.navbar-primary'),
    },
    'chart_view': {
        'period_selector': (By.CSS_SELECTOR, '.period-selector .middle-button'),
        'period_selector_year': (By.CSS_SELECTOR, '.fin-date-selector .period-selector-list > li:last-child'),
        'period_selector_current': (By.CSS_SELECTOR, '.fin-date-selector .date-item.current'),
        'period_selector_apply': (By.CSS_SELECTOR, '.fin-date-selector .sel-btn.apply'),
        'previous_period': (By.CSS_SELECTOR, '.period-selector .previous-button'),

        'loader': (By.CSS_SELECTOR, '.loader-text'),

        'show_grid': (By.CSS_SELECTOR, '.link-button[data-action="grid"]'),
        'grid': (By.CSS_SELECTOR, '.data-grid-view > table'),
    }
}
