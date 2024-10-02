from typing import TypedDict


class DataSeriesSerialized(TypedDict):
    group: str
    name: str
    unit: str
    data: list[tuple[str, float]]
