import logging
from typing import Any, Dict

import pytest
from httpx import AsyncClient, Response

from app.core.config import CONFIG
from app.models import WordModel

logger = logging.getLogger(__name__)


@pytest.mark.asyncio(scope="function")
async def test_get_word_that_exists_in_db_200(
    client: AsyncClient,
    test_created_word: WordModel,
):
    response = await client.get(
        f"/v1/words/{test_created_word.word}",
    )
    assert response.status_code == 200
    data = response.json()
    assert data["word"] == test_created_word.word


@pytest.mark.asyncio(scope="function")
async def test_get_word_that_does_not_exist_in_db_200(
    client: AsyncClient,
    respx_mock,
    mock_google_service_response: Dict[str, Any]
):
    respx_mock.post(f"{CONFIG.translate_service_url}/translate").mock(
        return_value=Response(200, json=mock_google_service_response)
    )

    response = await client.get("/v1/words/sample-word")
    assert response.status_code == 200
