import logging
import os

from selenium.webdriver.common.by import By, ByType

from . import t

LOG_LEVEL = os.environ.get('LOG_LEVEL', logging.INFO)
FOLDER_DOWNLOADS = '/downloads'
FOLDER_DOWNLOADS_LOCAL = os.environ.get('FOLDER_DOWNLOADS', FOLDER_DOWNLOADS)
SELENIUM_HOST = os.environ.get('SELENIUM_HOST', 'selenium:4444')


DESIGO_INSTANCES: dict[t.Group, t.DesigoInstance] = {
    t.Group.BIOTOPE: t.DesigoInstance(
        group=t.Group.BIOTOPE,
        host=os.environ['BIOTOPE_HOST'],
        username=os.environ['BIOTOPE_USERNAME'],
        password=os.environ['BIOTOPE_PASSWORD'],
    )
}

CHART_VIEWS: list[t.ChartView] = [
    t.ChartView(
        group=t.Group.BIOTOPE,
        name='Warmtepomp',
        path='/finMobile/desigo#trends?q=@29dea950-5e6d767b',
    ),
]


LOGIN_PATH = '/om/#/landing/login'
CHART_VIEW_TIMEOUT = 300
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
