import logging

import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.gzip import GZipMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.api.v1.endpoints.health import router as health_router
from app.core.config import CONFIG
from app.core.middlewares import (
    add_process_time_header,
    log_requests,
    validation_exception_handler,
)
from app.exceptions.api import APIError, api_error_handler

logger = logging.getLogger(__name__)

main_app = FastAPI(
    title=CONFIG.api.title,
    debug=CONFIG.api.debug,
    version=CONFIG.api.version,
    openapi_url="/openapi.json",
)

main_app.add_middleware(
    CORSMiddleware,
    allow_origins=CONFIG.api.allowed_hosts or ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
main_app.add_middleware(GZipMiddleware, minimum_size=1000)
main_app.add_middleware(BaseHTTPMiddleware, dispatch=add_process_time_header)
main_app.add_middleware(BaseHTTPMiddleware, dispatch=log_requests)

main_app.add_exception_handler(
    RequestValidationError, validation_exception_handler  # type:ignore
)
main_app.add_exception_handler(APIError, api_error_handler)  # type:ignore

main_app.include_router(router=api_router, prefix=CONFIG.api.prefix)
main_app.include_router(
    router=health_router, prefix="/health", tags=["API Health"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:main_app", host="0.0.0.0", port=8000, workers=7
    )  # pragma: no cover
