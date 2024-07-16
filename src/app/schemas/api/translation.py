from typing import List

from pydantic import BaseModel


class TranslationIn(BaseModel):
    translation: str | None = None
    synonyms: List[str] | None = []


class TranslationOut(BaseModel):
    translation: str | None = None
    synonyms: List[str] | None = []
