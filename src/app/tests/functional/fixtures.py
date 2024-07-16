from typing import Any, Dict

from pytest import fixture

from app.schemas import DefinitionIn, TranslationIn, WordIn


@fixture(scope="function")
def mock_word() -> WordIn:
    return WordIn(
        word="sample-word",
        examples=["example usage of the word"],
        translations=[
            TranslationIn(
                translation="translated-word",
                synonyms=["synonym1", "synonym2"]
            ),
        ],
        definitions=[
            DefinitionIn(
                definition="definition-word",
                synonyms=["synonym1", "synonym2"],
                example="example usage in definition"
            )
        ]

    )


@fixture(scope="function")
def mock_google_service_response() -> Dict[str, Any]:
    return {
        "word": "sample-word",
        "translation": None,
        "wordTranscription": None,
        "translationTranscription": None,
        "translations": {
            "Noun": [
                {
                    "translation": "translated-word",
                    "synonyms": ["synonym1", "synonym2"],
                    "frequency": None
                }
            ]
        },
        "definitions": {
            "Noun": [
                {
                    "definition": "definition-word",
                    "synonyms": {
                        "normal": ["synonym1", "synonym2"],
                        "informal": []
                    },
                    "example": "example usage in definition"
                }
            ]
        },
        "examples": ["example usage of the word"]
    }
