from typing import TypeVar

import typeguard

T = TypeVar("T")


def check_type(value: object, expected_type: type[T]) -> T | None:
    try:
        return typeguard.check_type(value, expected_type)
    except typeguard.TypeCheckError:
        return None
