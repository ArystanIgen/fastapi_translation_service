import logging

import httpx

from app.core.config import CONFIG
from app.exceptions import BadGatewayError
from app.schemas import DefinitionIn, TranslationIn, WordIn

logger = logging.getLogger(__name__)


async def fetch_from_google_translate(
    *,
    word: str,
    source_lang: str = "en",
    dest_lang: str = "es",
) -> WordIn | None:
    async with httpx.AsyncClient() as client:

        response = await client.post(
            f"{CONFIG.translate_service_url}/translate",
            json={
                "text": word,
                "source_lang": source_lang,
                "dest_lang": dest_lang,
            },
        )
        if response.status_code != 200:
            logger.error(f"Failed to fetch translation: {response.json()}")
            raise BadGatewayError

        data = response.json()
        translations = []
        definitions = []

        for translation_list in data.get("translations", {}).values():
            for translation_dict in translation_list:
                translation_in = TranslationIn(
                    translation=translation_dict.get("translation", None),
                    synonyms=translation_dict.get("synonyms", []),
                )
                translations.append(translation_in)

        for _, definition_list in data.get(
            "definitions", {}
        ).items():
            for definition_dict in definition_list:
                synonyms_dict = definition_dict.get("synonyms", {})
                synonym_list = []
                for _, synonyms in synonyms_dict.items():
                    if isinstance(synonyms, list):
                        synonym_list.extend(synonyms)

                definition_in = DefinitionIn(
                    definition=definition_dict.get("definition", None),
                    example=definition_dict.get("example", None),
                    synonyms=synonym_list,
                )
                definitions.append(definition_in)

        return WordIn(
            word=word,
            examples=data["examples"],
            definitions=definitions,
            translations=translations,
        )
