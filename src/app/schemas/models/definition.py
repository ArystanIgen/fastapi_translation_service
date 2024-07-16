from typing import List

from pydantic import BaseModel


class DefinitionUpdate(BaseModel):
    definition: str | None
    example: str | None
    synonyms: List[str] | None
