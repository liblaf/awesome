from typing import TypeVar

import typeguard

_T = TypeVar("_T")


def check_type(value: object, expected_type: type[_T]) -> _T | None:
    try:
        return typeguard.check_type(value, expected_type)
    except typeguard.TypeCheckError:
        return None
