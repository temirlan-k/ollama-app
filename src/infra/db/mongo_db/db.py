from beanie import init_beanie
from motor import motor_asyncio
from infra.db.mongo_db.models.analytics import Analytics
client = motor_asyncio.AsyncIOMotorClient("mongodb://root:root@mongo:27017/")


async def init_mongo():
    await init_beanie(database=client.analytics,document_models=[Analytics])

async def close_mongo():
    client.close()