from . import t


def merge_data(data1: list[t.DataSeries], data2: list[t.DataSeries]) -> list[t.DataSeries]:
    data = {
        series.name: series
        for series in data1
    }

    for series in data2:
        if series.name in data:
            data[series.name].merge(series)
        else:
            data[series.name] = series

    return list(data.values())
