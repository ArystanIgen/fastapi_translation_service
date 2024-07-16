from typing import List

from odmantic.session import AIOSession

from app.models import WordModel
from app.repository.base import BaseRepository
from app.schemas import WordIn, WordOut, WordsPaginate
from app.utils.params import IncludeFields


class WordRepository(BaseRepository[WordModel, WordIn]):
    model = WordModel

    async def get_words(
        self,
        session: AIOSession,
        *,
        sort_field: str | None = None,
        word: str | None = None,
        size: int | None = 20,
        page: int | None = 0,
        include_fields: List[IncludeFields],

    ) -> WordsPaginate:
        query = {}
        if word:
            query["word"] = {"$regex": word, "$options": "i"}

        total_count = await session.count(self.model, query)
        total_pages = (total_count + size - 1) // size

        fetched_words = await session.find(
            self.model,
            query,
            skip=(page - 1) * size,
            limit=size,
            sort=self.get_sort_option(sort_field=sort_field),

        )

        items: List[WordOut] = [
            WordOut.from_model(
                word,
                include_fields=include_fields
            )
            for word in fetched_words
        ]
        return WordsPaginate(
            items=items,
            total=total_count,
            page=page,
            size=size,
            pages=total_pages,
        )
