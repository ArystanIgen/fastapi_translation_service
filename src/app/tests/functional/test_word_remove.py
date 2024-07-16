import logging

import pytest
from httpx import AsyncClient

from app.models import WordModel
from app.schemas import WordIn

logger = logging.getLogger(__name__)


@pytest.mark.asyncio(scope="function")
async def test_delete_word_that_exists_in_db_204(
    client: AsyncClient,
    test_created_word: WordModel,
):
    response = await client.delete(
        f"/v1/words/{test_created_word.word}",
    )
    assert response.status_code == 204


@pytest.mark.asyncio(scope="function")
async def test_delete_word_that_does_not_exist_in_db_404(
    client: AsyncClient,
    mock_word: WordIn
):
    response = await client.delete(
        f"/v1/words/{mock_word.word}",
    )
    assert response.status_code == 404
