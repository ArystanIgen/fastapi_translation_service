import logging

from fastapi import APIRouter, status

from app.api.deps import SessionDep, WordParamsDep, WordRepoDep
from app.exceptions import (
    GoogleWordNotFoundError,
    WordNotFoundError,
    openapi_handle_error,
)
from app.models import WordModel
from app.schemas import WordIn, WordOut, WordsPaginate
from app.utils.google_service import fetch_from_google_translate

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/{word}",
    response_model=WordOut,
    status_code=status.HTTP_200_OK,
    responses=openapi_handle_error(GoogleWordNotFoundError),
    summary="GetWordDetails",
    description="Get Word Details",
    operation_id="GetWordDetails",
    response_description="Word Details was retrieved successfully",
    response_model_exclude_none=True,
)
async def get_word_details_api(
    word: str,
    session: SessionDep,
    word_repo: WordRepoDep,
) -> WordModel:
    fetched_word: WordModel | None = await word_repo.get(session, word=word)
    if not fetched_word:
        word_details: WordIn = await fetch_from_google_translate(
            word=word
        )
        if (
            not word_details.definitions
        ) and (
            not word_details.examples
        ) and (
            not word_details.translations
        ):
            raise GoogleWordNotFoundError
        return await word_repo.create(
            session, db_obj=WordModel(**word_details.model_dump())
        )
    return fetched_word


@router.get(
    "",
    response_model=WordsPaginate,
    status_code=status.HTTP_200_OK,
    # responses=openapi_handle_error(DataRequirementNotFoundError),
    summary="GetListOfWords",
    description="Get List of Words",
    operation_id="GetListOfWords",
    response_description="List of words were retrieved successfully",
    response_model_exclude_none=True,
)
async def get_list_of_words_api(
    word_params: WordParamsDep,
    session: SessionDep,
    word_repo: WordRepoDep,
) -> WordsPaginate:
    return await word_repo.get_words(
        session,
        sort_field=word_params.sort,
        word=word_params.word,
        size=word_params.size,
        page=word_params.page,
        include_fields=word_params.include
    )


@router.delete(
    "/{word}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=openapi_handle_error(WordNotFoundError),
    summary="DeleteWordDetails",
    description="Delete Word Details",
    operation_id="DeleteWordDetails",
    response_description="Word details were deleted successfully",
    response_model_exclude_none=True,
)
async def delete_word_api(
    word: str,
    session: SessionDep,
    word_repo: WordRepoDep,
) -> None:
    fetched_word: WordModel | None = await word_repo.get(session, word=word)
    if not fetched_word:
        raise WordNotFoundError
    return await word_repo.remove(session, instance=fetched_word)
