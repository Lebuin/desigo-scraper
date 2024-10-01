import logging
import time
from datetime import datetime

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import (NoSuchElementException,
                                        StaleElementReferenceException)
from selenium.webdriver.common.by import By, ByType
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.remote.webelement import WebElement

from . import config, t, util

logger = logging.getLogger(__name__)


class Timeout(Exception):
    pass


class Browser:
    csv_cache: dict[tuple[t.Group, str], str]
    driver: webdriver.Remote


    @staticmethod
    def _get_url(group: t.Group, path: str):
        desigo_instance = config.DESIGO_INSTANCES[group]
        url = f'https://{desigo_instance.host}{path}'
        return url


    def __init__(self):
        options = FirefoxOptions()

        self.driver = webdriver.Remote(
            command_executor=f'http://{config.SELENIUM_HOST}/wd/hub',
            options=options,
        )


    def _get(self, url: str):
        logger.info(f'Visit {url}')
        self.driver.get(url)


    def _wait_for_element(
        self,
        by: ByType,
        selector: str,
        parent: WebElement | None=None,
        timeout: float=10,
        interval: float=.5,
    ):
        if parent is None:
            driver = self.driver
        else:
            driver = parent

        start = time.time()
        while True:
            try:
                return driver.find_element(by, selector)
            except NoSuchElementException:
                if time.time() - start > timeout:
                    raise Timeout()
                else:
                    time.sleep(interval)


    def _wait_until_chart_view_loaded(self):
        logger.info('Wait until the chart view has loaded...')
        self._wait_for_element(*config.SELECTORS['chart_view']['loader'])

        start = time.time()
        loader_text = ''

        while True:
            try:
                elem_loader = self.driver.find_element(*config.SELECTORS['chart_view']['loader'])
                try:
                    text = elem_loader.text
                    if text != loader_text:
                        loader_text = text
                        logger.info(loader_text)
                except StaleElementReferenceException:
                    pass
            except NoSuchElementException:
                return

            if time.time() - start > config.CHART_VIEW_TIMEOUT:
                raise Exception('Loading the chart view timed out')
            time.sleep(1)


    def fetch_data(self, chart_view: t.ChartView) -> list[t.DataSeries]:
        logger.info(f'Fetch data for {chart_view}')

        self._get_chart_view(chart_view)
        self._wait_until_chart_view_loaded()

        selectors = config.SELECTORS['chart_view']

        logger.info('Set the time range to the current year')
        self._wait_for_element(*selectors['period_selector']).click()
        self._wait_for_element(*selectors['period_selector_year']).click()
        self._wait_for_element(*selectors['period_selector_current']).click()
        self._wait_for_element(*selectors['period_selector_apply']).click()
        self._wait_until_chart_view_loaded()
        data_this_year = self._download_all_data(chart_view)

        logger.info('Set the time range to the previous year')
        self._wait_for_element(*selectors['previous_period']).click()
        self._wait_until_chart_view_loaded()
        data_last_year = self._download_all_data(chart_view)
        all_data = util.merge_data(data_this_year, data_last_year)

        return all_data


    def _get_chart_view(self, chart_view: t.ChartView):
        url = self._get_url(chart_view.group, chart_view.path)
        self._get(url)

        if self.driver.current_url == self._get_url(chart_view.group, config.LOGIN_PATH):
            logger.info(f'Not logged in yet')
            self._login(chart_view.group)
            self._get(url)


    def _login(self, group: t.Group):
        logger.info('Log in')
        url = self._get_url(group, config.LOGIN_PATH)
        self._get(url)

        desigo_instance = config.DESIGO_INSTANCES[group]

        elem_username = self._wait_for_element(*config.SELECTORS['login']['username'])
        elem_password = self._wait_for_element(*config.SELECTORS['login']['password'])
        elem_submit = self._wait_for_element(*config.SELECTORS['login']['submit'])

        elem_username.send_keys(desigo_instance.username)
        elem_password.send_keys(desigo_instance.password)
        elem_submit.click()

        self._wait_for_element(*config.SELECTORS['main']['navbar'])


    def _download_all_data(self, chart_view: t.ChartView) -> list[t.DataSeries]:
        logger.info('Download data')
        self._wait_for_element(*config.SELECTORS['chart_view']['show_grid'])
        elems_button = self.driver.find_elements(*config.SELECTORS['chart_view']['show_grid'])
        elems_container = [
            elem_button.find_element(By.XPATH, './../..')
            for elem_button in elems_button
        ]

        all_data = []
        for i, elem_container in enumerate(elems_container):
            logger.info(f'Download data for chart {i}')
            data = self._download_data(chart_view, elem_container)
            all_data.extend(data)

        return all_data


    def _download_data(self, chart_view: t.ChartView, elem_container: WebElement) -> list[t.DataSeries]:
        elem_button = elem_container.find_element(*config.SELECTORS['chart_view']['show_grid'])
        elem_button.click()

        elem_grid = self._wait_for_element(
            *config.SELECTORS['chart_view']['grid'],
            parent=elem_container,
            timeout=20,
        )
        html_grid = elem_grid.get_attribute('outerHTML') or ''
        soup = BeautifulSoup(html_grid, 'html.parser')

        data: list[t.DataSeries] = []

        for elem_header in soup.find_all('th')[1:]:
            name, unit = elem_header.text.split('\xa0')
            data_series = t.DataSeries(group=chart_view.group, name=name, unit=unit)
            data.append(data_series)

        for elem_row in soup.find_all('tr')[1:]:
            elems_cell = elem_row.find_all('td')
            elem_timestamp = elems_cell[0]
            timestamp = datetime.strptime(elem_timestamp.text, '%d.%m.%Y %H:%M:%S:%f')

            for i in range(1, len(elems_cell)):
                elem_data = elems_cell[i]
                if elem_data.text:
                    value = float(elem_data.text)
                    data[i - 1].data.append((timestamp, value))

        return data
