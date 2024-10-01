import dataclasses
import enum
from datetime import datetime
from typing import TypedDict


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


@dataclasses.dataclass(frozen=True)
class ChartView:
    """A web page in the Desigo interface containing charts.

    These are the entrypoints for the scraping.
    """
    group: Group
    name: str
    path: str


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
        self.data += other.data
        self.data.sort(key=lambda t: t[0])


class DataSeriesSerialized(TypedDict):
    group: str
    name: str
    unit: str
    data: list[tuple[str, float]]
