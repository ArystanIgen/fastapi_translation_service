from typing import AsyncGenerator

import pytest_asyncio
from odmantic.session import AIOSession

from app.models import WordModel
from app.repository import WordRepository
from app.schemas import WordIn


@pytest_asyncio.fixture(scope="function")
async def test_created_word(
    async_session: AIOSession,
    mock_word: WordIn
) -> AsyncGenerator[WordModel, None]:
    word_repo = WordRepository()

    word_instance: WordModel = await word_repo.create(
        session=async_session, db_obj=WordModel(**mock_word.model_dump())
    )

    yield word_instance
    await word_repo.remove(session=async_session, instance=word_instance)
