import json
import os.path
import tempfile
from datetime import datetime

from . import config, t

__all__ = [
    'load_data',
    'store_data',
]


def store_data(data: list[t.DataSeries]) -> None:
    data_serialized = serialize_data(data)
    write_file(data_serialized)


def load_data() -> list[t.DataSeries]:
    try:
        data_serialized = read_file()
    except FileNotFoundError:
        return []

    data = parse_data(data_serialized)
    return data




def read_file() -> list[t.DataSeriesSerialized]:
    with open(config.DB_PATH, 'r') as f:
        return json.load(f)


def write_file(data_serialized: list[t.DataSeriesSerialized]) -> None:
    # Don't write to the database file directy to avoid file corruption
    tmp_file = tempfile.NamedTemporaryFile(
        delete=False,
        dir=os.path.dirname(config.DB_PATH),
    )

    with open(tmp_file.name, 'w') as f:
        json.dump(data_serialized, f, ensure_ascii=False)

    os.replace(tmp_file.name, config.DB_PATH)




def serialize_data(data: list[t.DataSeries]) -> list[t.DataSeriesSerialized]:
    data_serialized = [
        serialize_data_series(data_series)
        for data_series in data
    ]
    return data_serialized


def parse_data(data_serialized: list[t.DataSeriesSerialized]) -> list[t.DataSeries]:
    data = [
        parse_data_series(data_series_serialized)
        for data_series_serialized in data_serialized
    ]
    return data



def serialize_data_series(data_series: t.DataSeries) -> t.DataSeriesSerialized:
    data_serialized = [
        (item[0].isoformat(), item[1])
        for item in data_series.data
    ]
    data_series_serialized: t.DataSeriesSerialized = {
        'group': data_series.group.value,
        'name': data_series.name,
        'unit': data_series.unit,
        'data': data_serialized,
    }
    return data_series_serialized


def parse_data_series(data_series_serialized: t.DataSeriesSerialized) -> t.DataSeries:
    group = t.Group(data_series_serialized['group'])
    data = [
        (datetime.fromisoformat(item[0]), item[1])
        for item in data_series_serialized['data']
    ]
    data_series = t.DataSeries(
        group=group,
        name=data_series_serialized['name'],
        unit=data_series_serialized['unit'],
        data=data
    )
    return data_series
