import logging

from . import config, db, t, util
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
    store_data(data)


def get_data_from_chart_views(chart_views: list[t.ChartView]) -> list[t.DataSeries]:
    data: list[t.DataSeries] = []

    browser = Browser()

    for chart_view in chart_views:
        chart_view_data = browser.fetch_data(chart_view)
        data.extend(chart_view_data)

    return data


def store_data(new_data: list[t.DataSeries]):
    old_data = db.load_data()
    data = util.merge_data(old_data, new_data)
    db.store_data(data)
