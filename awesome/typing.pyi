from typing import TypeVar

T = TypeVar("T")

def check_type(value: object, expected_type: type[T]) -> T | None: ...
