from enum import Enum
from typing import List

from fastapi import Query


class IncludeFields(str, Enum):
    definitions = "definitions"
    translations = "translations"
    synonyms = "synonyms"


class WordsQueryParams:
    __slots__ = ("word", "sort", "include", "size", "page")

    def __init__(
        self,
        word: str | None = Query(
            default=None,
            description="Filter by word (partial match)",
        ),
        sort: str | None = Query(
            default=None,
            description="Sort by field",
        ),
        include: List[IncludeFields] | None = Query(  # noqa
            default=[],
            description="Include fields",
        ),
        size: int = Query(
            default=50,
            description="Page size",
            le=100,
            ge=1,
        ),
        page: int = Query(
            default=1,
            description="Page number",
            ge=1,
        ),
    ):
        self.word = word
        self.sort = sort
        self.include = include
        self.size = size
        self.page = page
