# Standard Library
import logging
import random
import string
import time

from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.exceptions.api import Code


async def validation_exception_handler(
    _: Request, exc: RequestValidationError
) -> JSONResponse:
    message = ""
    for err in exc.errors():
        message += f'Parameter: {".".join(map(str, err["loc"][1:]))}, Error: {err["msg"]};'  # noqa

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"code": Code.InvalidRequest, "message": message.strip()},
    )


async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


async def log_requests(request: Request, call_next):
    if request.url.path == "/healthz":
        response = await call_next(request)
        return response

    logger = logging.getLogger(__name__)
    rid = "".join(random.choices(string.ascii_uppercase + string.digits, k=16))
    x_headers = dict(
        filter(
            lambda h: h[0].lower().startswith("x-"), request.headers.items()
        )
    )
    logger.info(
        f"rid={rid} {request.method} {request.url.path} X-Headers: {x_headers}"
    )
    start_time = time.time()

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(e)
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )

    formatted_process_time = "{0:.2f}".format(
        (time.time() - start_time) * 1000
    )
    logger.info(
        f"rid={rid} completed in={formatted_process_time}ms status code={response.status_code}"  # noqa
    )

    return response
