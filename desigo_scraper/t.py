import dataclasses
import enum
import typing
from datetime import datetime


class Group(enum.Enum):
    BIOTOPE = 'Biotope'
    SPORE = 'De Spore'
    WIJGAARD = 'Wijgaard'


@dataclasses.dataclass(frozen=True)
class DesigoInstance:
    group: Group
    host: str
    username: str
    password: str


@dataclasses.dataclass(frozen=True)
class ChartView:
    group: Group
    name: str
    path: str


@dataclasses.dataclass
class DataSeries:
    name: str
    unit: str
    data: list[tuple[datetime, float]] = dataclasses.field(default_factory=list)

    def merge(self, other: 'DataSeries'):
        if other.name != self.name:
            raise Exception('DataSeries\'s names don\'t match')

        self.data += other.data
        self.data.sort(key=lambda t: t[0])
