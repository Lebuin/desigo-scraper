import json
from datetime import datetime, timezone

from flask import request
from flask.wrappers import Request
from flask_basicauth import BasicAuth

from . import t
from .app import app

# We don't need to apply this decorator to individual routes, because we have
# `BASIC_AUTH_FORCE = True` in our config.
basic_auth = BasicAuth(app)


@app.route('/data', methods=['GET'])
def data():
    now = datetime.now(tz=timezone.utc)
    start = parse_datetime(request, 'start', now - app.config['DEFAULT_TIME_RANGE'])
    end = parse_datetime(request, 'end', now)

    data = get_data()
    filtered_data = filter_data(data, start, end)

    return filtered_data


def parse_datetime(request: Request, arg: str, default: datetime):
    arg_value = request.args.get(arg)
    if arg_value is None:
        return default
    else:
        try:
            dt = datetime.fromisoformat(arg_value)
        except ValueError:
            raise Exception(f"'{arg}': provide a valid ISO 8601 datetime")

        # If not timezone is provided we fall back to the server's timezone
        if dt.tzinfo is None:
            dt = dt.astimezone(timezone.utc)
        return dt


def get_data() -> list[t.DataSeriesSerialized]:
    try:
        with open(app.config['DB_PATH'], 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return []


def filter_data(
    data: list[t.DataSeriesSerialized],
    start: datetime,
    end: datetime,
) -> list[t.DataSeriesSerialized]:
    data_filtered = [
        filter_data_series(data_series, start, end)
        for data_series in data
    ]
    return data_filtered


def filter_data_series(
    data_series: t.DataSeriesSerialized,
    start: datetime,
    end: datetime,
) -> t.DataSeriesSerialized:
    data_filtered = [
        item
        for item in data_series['data']
        if start <= datetime.fromisoformat(item[0]) <= end
    ]
    data_series_filtered: t.DataSeriesSerialized = {  # type: ignore
        **data_series,
        'data': data_filtered,
    }
    return data_series_filtered


app.logger.info('Server started')
