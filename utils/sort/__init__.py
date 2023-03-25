import collections
import typing


def sort(data: typing.Any) -> typing.Any:
    match data:
        case dict():
            return sort_dict(data=data)
        case list():
            return sort_list(data=data)
        case _:
            return data


def sort_dict(data: dict) -> dict:
    result = collections.OrderedDict()
    for key in sorted(data.keys()):
        result[key] = sort(data[key])
    return dict(result)


def sort_list(data: list) -> list:
    result: list = list()
    for value in data:
        result.append(sort(value))
    return sorted(result)
