# Standard Library
import logging
from typing import Any, Generic, Type, TypeVar

from odmantic import Model
from odmantic.query import asc, desc
from odmantic.session import AIOSession
from pydantic import BaseModel

from app.exceptions import InvalidRequestError

logger = logging.getLogger(__name__)

ModelType = TypeVar("ModelType", bound=Model)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseRepository(Generic[ModelType, UpdateSchemaType]):
    """
    CRUD object with default methods to Create, Read, Update, Delete (CRUD).
    * `model`: A Odmantic model class
    """

    model: Type[ModelType]

    async def get(self, session: AIOSession, **data) -> ModelType | None:
        list_of_arguments = [
            getattr(self.model, field_name) == field_value
            for field_name, field_value in data.items()
            if hasattr(self.model, field_name)
        ]

        fetched_model = await session.find_one(self.model, *list_of_arguments)
        return fetched_model

    async def create(
        self, session: AIOSession, *, db_obj: ModelType
    ) -> ModelType | None:
        try:
            await session.save(db_obj)
            return db_obj
        except Exception as e:
            logger.error(f"Error creating {self.model.__name__}: {e}")
            return None

    @staticmethod
    async def update(
        session: AIOSession, *, instance: ModelType, obj_in: UpdateSchemaType
    ) -> ModelType | None:
        try:
            update_data = obj_in.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(instance, field, value)
            await session.save(instance)
            return instance
        except Exception as e:
            logger.error(f"Error updating {instance.__class__.__name__}: {e}")
            return None

    @staticmethod
    async def remove(
        session: AIOSession,
        *,
        instance: ModelType,
    ) -> None:
        try:
            await session.delete(instance)
        except Exception as e:
            logger.error(f"Error removing {instance.__class__.__name__}: {e}")

    def get_sort_option(self, *, sort_field: str | None) -> Any:
        if not sort_field:
            return None

        sort_direction = desc if sort_field.startswith("-") else asc
        field_name = sort_field.lstrip("-")

        # Check if the attribute exists in the model
        if not hasattr(self.model, field_name):
            raise InvalidRequestError(
                message=f"Invalid sort field: {field_name}"
            )

        field = getattr(self.model, field_name)

        return sort_direction(field)
