import logging
from datetime import datetime

from . import config, t
from .browser import Browser

logger = logging.getLogger(__name__)
import sys

logging.basicConfig(
    stream=sys.stdout,
    level=config.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

def scrape():
    data = get_data_from_chart_views(config.CHART_VIEWS)
    print_series(data[t.Group.BIOTOPE][0])


def get_data_from_chart_views(chart_views: list[t.ChartView]) -> dict[t.Group, list[t.DataSeries]]:
    data: dict[t.Group, list[t.DataSeries]] = {}

    browser = Browser()

    for chart_view in chart_views:
        logger.info(f'Download data for chart view {chart_view.name}')
        view_data = browser.fetch_jsons(chart_view)
        data.setdefault(chart_view.group, []).extend(view_data)

    return data


def print_series(data_series: t.DataSeries):
    s = ''
    for timestamp, value in data_series.data:
        s += f'{timestamp},{value}\n'
    logger.info(s)
