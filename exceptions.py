from typing import NoReturn, TypeVar

from fastapi import HTTPException

T = TypeVar("T")


def not_found() -> NoReturn:
    raise HTTPException(status_code=404, detail="Book not found")


def get_or_404(items: T | None) -> T:
    if items is None:
        not_found()
    return items
