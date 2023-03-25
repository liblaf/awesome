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
    try:
        result = sorted(result)
    except:
        if isinstance(result[0], dict):
            for key in sorted(result[0].keys()):
                try:
                    result = sorted(result, key=lambda x: x[key])
                except:
                    pass
                else:
                    break
    return result
