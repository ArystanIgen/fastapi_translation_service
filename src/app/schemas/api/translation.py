from typing import List, Optional

from pydantic import BaseModel


class TranslationIn(BaseModel):
    translation: Optional[str] = None
    synonyms: List[str] | None = []


class TranslationOut(BaseModel):
    translation: Optional[str] = None
    synonyms: List[str] | None = []
