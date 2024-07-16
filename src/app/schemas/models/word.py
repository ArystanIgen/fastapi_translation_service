from typing import List

from pydantic import BaseModel

from app.schemas.models.definition import DefinitionUpdate
from app.schemas.models.translation import TranslationUpdate


class WordUpdate(BaseModel):
    examples: List[str] | None
    translations: List[TranslationUpdate] | None
    definitions: List[DefinitionUpdate] | None
