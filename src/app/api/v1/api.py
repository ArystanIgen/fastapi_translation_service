from fastapi import APIRouter

from app.api.v1.endpoints import word

api_router = APIRouter()
api_router.include_router(word.router, prefix="/words", tags=["words"])
