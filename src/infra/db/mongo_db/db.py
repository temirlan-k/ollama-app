from beanie import init_beanie
from motor import motor_asyncio
from infra.db.mongo_db.models.analytics import Analytics
from core.log import setup_logging

client = motor_asyncio.AsyncIOMotorClient("mongodb://root:root@mongo:27017/")
logger = setup_logging()

async def init_mongo():
    try:
        database = client.analytics
        await init_beanie(database=database, document_models=[Analytics])
        logger.info("MongoDB connected and Beanie initialized.")
    except Exception as e:
        logger.error(f"Error initializing MongoDB: {e}")
        raise

async def close_mongo():
    try:
        client.close()
        logger.info("MongoDB connection closed.")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")
        raise
