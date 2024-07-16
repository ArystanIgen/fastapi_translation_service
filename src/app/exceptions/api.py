from enum import Enum
from typing import Any, Dict

from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse


class Message(BaseModel):
    code: str
    message: str


class Code(str, Enum):
    Unauthorized = "Unauthorized"
    Forbidden = "Forbidden"

    BadGateway = "BadGateway"

    InvalidRequest = "InvalidRequest"
    GoogleWordNotFound = "GoogleWordNotFound"
    WordNotFound = "WordNotFound"


class APIError(Exception):
    __slots__ = ("code", "message", "status_code")

    def __init__(self, code: Code, message: str, status_code: int = 400):
        self.code = code
        self.message = message
        self.status_code = status_code

    def to_dict(self) -> Dict[str, str]:
        return {
            "code": self.code,
            "message": self.message,
        }

    def get_dict(self) -> Dict[str, str | int]:
        return {
            "code": self.code,
            "message": self.message,
            "status_code": self.status_code,
        }


async def api_error_handler(_: Request, error: APIError) -> JSONResponse:
    return JSONResponse(status_code=error.status_code, content=error.to_dict())


def openapi_handle_error(*args) -> Dict[int | str, Dict[str, Any]] | None:
    errors_dict = {}
    for error in args:
        error_dict = error().get_dict()
        errors_dict[error_dict["status_code"]] = {
            "model": Message,
            "description": error_dict["message"],
        }
    return errors_dict


class InvalidRequestError(APIError):
    def __init__(self, message: str = "Validation Error") -> None:
        super().__init__(
            code=Code.InvalidRequest,
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
        )


class UnauthorizedError(APIError):
    def __init__(self) -> None:
        super().__init__(
            code=Code.Unauthorized,
            message="Not authorized",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )


class ForbiddenError(APIError):
    def __init__(self) -> None:
        super().__init__(
            code=Code.Forbidden,
            message="Forbidden",
            status_code=status.HTTP_403_FORBIDDEN,
        )


class BadGatewayError(APIError):
    def __init__(self) -> None:
        super().__init__(
            code=Code.BadGateway,
            message="Error connecting to third party service. "
                    "Please try again later",
            status_code=status.HTTP_502_BAD_GATEWAY,
        )


class GoogleWordNotFoundError(APIError):
    def __init__(self) -> None:
        super().__init__(
            code=Code.GoogleWordNotFound,
            message="Word from Google translate not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )


class WordNotFoundError(APIError):
    def __init__(self) -> None:
        super().__init__(
            code=Code.WordNotFound,
            message="Word  not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )
