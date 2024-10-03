import dataclasses
import enum
from datetime import datetime
from typing import TypedDict
import pytz.tzinfo


class Group(enum.Enum):
    BIOTOPE = 'Biotope'
    SPORE = 'De Spore'
    WIJGAARD = 'Wijgaard/WGC'


@dataclasses.dataclass(frozen=True)
class DesigoInstance:
    group: Group
    host: str
    username: str
    password: str
    timezone: pytz.tzinfo.StaticTzInfo | pytz.tzinfo.DstTzInfo


@dataclasses.dataclass(frozen=True)
class ChartView:
    """A web page in the Desigo interface containing charts.

    These are the entrypoints for the scraping.
    """
    group: Group
    name: str
    path: str

    def __str__(self):
        return f'ChartView: {self.group.value} - {self.name}'


@dataclasses.dataclass
class DataSeries:
    group: Group
    name: str
    unit: str
    data: list[tuple[datetime, float]] = dataclasses.field(default_factory=list)

    def merge(self, other: 'DataSeries'):
        if other.name != self.name:
            raise Exception('DataSeries\'s names don\'t match')

        self.unit = other.unit
        data = self.data + other.data
        data_dict = {
            timestamp: value
            for timestamp, value in data
        }
        data_deduped = sorted(data_dict.items(), key=lambda t: t[0])
        self.data = data_deduped

    def __str__(self):
        return f'DataSeries: {self.group.value} - {self.name} ({self.unit})'


class DataSeriesSerialized(TypedDict):
    group: str
    name: str
    unit: str
    data: list[tuple[str, float]]
