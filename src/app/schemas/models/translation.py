from typing import List

from pydantic import BaseModel


class TranslationUpdate(BaseModel):
    translation: str | None
    synonyms: List[str] | None
