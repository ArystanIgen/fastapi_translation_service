from typing import List, Optional

from odmantic import EmbeddedModel, Model


class TranslationModel(EmbeddedModel):
    translation: Optional[str] = None
    synonyms: List[str] = []


class DefinitionModel(EmbeddedModel):
    definition: Optional[str] = None
    example: Optional[str] = None
    synonyms: List[str] | None = []


class WordModel(Model):
    word: str
    examples: List[str] = []
    translations: List[TranslationModel]
    definitions: List[DefinitionModel]
