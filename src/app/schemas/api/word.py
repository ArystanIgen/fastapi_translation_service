from typing import List

from pydantic import BaseModel

from app.models.word import WordModel
from app.schemas.api.definition import DefinitionIn, DefinitionOut
from app.schemas.api.translation import TranslationIn, TranslationOut
from app.utils.params import IncludeFields


class WordIn(BaseModel):
    word: str
    examples: List[str] = []
    translations: List[TranslationIn] = []
    definitions: List[DefinitionIn] = []


class WordOut(BaseModel):
    word: str
    examples: List[str] = []
    translations: List[TranslationOut] | None = []
    definitions: List[DefinitionOut] | None = []
    synonyms: list[list[str]] | None = None

    @staticmethod
    def from_model(model: WordModel, include_fields: List[IncludeFields]):
        include_definitions = "definitions" in include_fields
        include_translations = "translations" in include_fields
        include_synonyms = "synonyms" in include_fields

        if include_synonyms:
            if not include_translations and not include_definitions:

                synonyms = []
                for defin in model.definitions:
                    if len(defin.synonyms) > 0:
                        synonyms.append(defin.synonyms)

                return WordOut(
                    word=model.word,
                    examples=model.examples,
                    synonyms=synonyms,
                    translations=None,
                    definitions=None
                )

        translations = (
            [
                TranslationOut(
                    translation=trans.translation,
                    synonyms=trans.synonyms if include_synonyms else None,
                )
                for trans in model.translations
            ]
            if include_translations
            else None
        )

        definitions = (
            [
                DefinitionOut(
                    definition=defin.definition,
                    example=defin.example,
                    synonyms=defin.synonyms if include_synonyms else None,
                )
                for defin in model.definitions
            ]
            if include_definitions
            else None
        )

        return WordOut(
            word=model.word,
            examples=model.examples,
            translations=translations,
            definitions=definitions,
        )


class WordsPaginate(BaseModel):
    items: list[WordOut]
    total: int = 0
    page: int
    size: int
    pages: int
