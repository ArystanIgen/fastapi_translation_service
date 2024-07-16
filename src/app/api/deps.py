from typing import Annotated, AsyncGenerator

from fastapi import Depends
from odmantic.session import AIOSession

from app.db.client import Engine
from app.repository import WordRepository
from app.utils.params import WordsQueryParams


async def get_session() -> AsyncGenerator[AIOSession, None]:
    async with Engine.session() as session:
        yield session


def get_word_repo() -> WordRepository:
    return WordRepository()


# AIOSession Dependencies
SessionDep = Annotated[AIOSession, Depends(get_session)]

# Repository Dependencies
WordRepoDep = Annotated[WordRepository, Depends(get_word_repo)]

# Query Parameter Dependencies
WordParamsDep = Annotated[WordsQueryParams, Depends()]
