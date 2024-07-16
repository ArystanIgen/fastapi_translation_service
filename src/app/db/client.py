from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine

from app.core.config import CONFIG

MotorClient = AsyncIOMotorClient(  # type:ignore
    host=CONFIG.mongo.host,
    port=CONFIG.mongo.port,
    username=CONFIG.mongo.username,
    password=CONFIG.mongo.password,
)

Engine = AIOEngine(MotorClient, database=CONFIG.mongo.db)
