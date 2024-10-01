# Debug a chart view

```py
host = 'x.x.x.x'
username = 'xxx'
password = 'xxx'
path = '/finMobile/desigo#trends?q=@29dea58b-096c33ee'

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.firefox.options import Options as FirefoxOptions

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


class Timeout(Exception):
    pass


def _wait(self, parent: WebElement | None=None, timeout=10.0):
    if parent is None:
        _driver = driver
    else:
        _driver = parent
    return WebDriverWait(_driver, timeout)


def wait_until_chart_view_loaded():
    _wait().until(EC.presence_of_element_located(SELECTORS['chart_view']['loader']))
    start = time.time()
    loader_text = ''
    while True:
        try:
            elem_loader = driver.find_element(*SELECTORS['chart_view']['loader'])
            try:
                text = elem_loader.text
                if text != loader_text:
                    loader_text = text
                    print(loader_text)
            except StaleElementReferenceException:
                pass
        except NoSuchElementException:
            return
        if time.time() - start > 300:
            raise Exception('Loading the chart view timed out')
        time.sleep(1)


options = FirefoxOptions()
driver = webdriver.Remote(
    command_executor=f'http://localhost:4444/wd/hub',
    options=options,
)

driver.get(f'https://{host}/om/#/landing/login')

self._wait().until(EC.element_to_be_clickable(SELECTORS['login']['username']))\
    .send_keys(username)

self._wait().until(EC.element_to_be_clickable(SELECTORS['login']['password']))\
    .send_keys(password)

self._wait().until(EC.element_to_be_clickable(SELECTORS['login']['submit']))\
    .click()

self._wait().until(EC.presence_of_element_located(SELECTORS['main']['navbar']))

driver.get(f'https://{host}{path}')

wait_until_chart_view_loaded()

# Do your stuff here
```
