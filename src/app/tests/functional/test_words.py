import logging

import pytest
from httpx import AsyncClient

from app.models import WordModel

logger = logging.getLogger(__name__)


@pytest.mark.asyncio(scope="function")
async def test_get_words_200(
    client: AsyncClient,
    test_created_word: WordModel,
):
    response = await client.get(
        "/v1/words",
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data["items"]) == 1


@pytest.mark.asyncio(scope="function")
async def test_get_words_include_only_synonyms_200(
    client: AsyncClient,
    test_created_word: WordModel,
):
    response = await client.get(
        "/v1/words?include=synonyms",
    )
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert len(data["items"]) == 1
    assert "translations" not in data["items"]
    assert "definitions" not in data["items"]
