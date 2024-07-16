from typing import List

from pydantic import BaseModel


class DefinitionIn(BaseModel):
    definition: str | None = None
    example: str | None = None
    synonyms: List[str] | None = []


class DefinitionOut(BaseModel):
    definition: str | None = None
    example: str | None = None
    synonyms: List[str] | None = []
