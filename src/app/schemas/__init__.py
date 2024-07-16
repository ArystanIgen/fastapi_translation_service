from app.schemas.api.definition import DefinitionIn, DefinitionOut
from app.schemas.api.translation import TranslationIn, TranslationOut
from app.schemas.api.word import WordIn, WordOut, WordsPaginate
from app.schemas.models.definition import DefinitionUpdate
from app.schemas.models.translation import TranslationUpdate
from app.schemas.models.word import WordUpdate

__all__ = [
    "WordIn",
    "WordOut",
    "DefinitionIn",
    "DefinitionOut",
    "TranslationIn",
    "TranslationOut",
    "WordsPaginate",
    "WordUpdate",
    "TranslationUpdate",
    "DefinitionUpdate",
]
