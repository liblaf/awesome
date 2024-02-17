from typing import TypeVar

_T = TypeVar("_T")

def check_type(value: object, expected_type: type[_T]) -> _T | None: ...
