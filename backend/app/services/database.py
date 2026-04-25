from urllib.parse import quote_plus
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

client: AsyncIOMotorClient = None

def build_mongo_url():
    user = quote_plus(settings.mongodb_user)
    password = quote_plus(settings.mongodb_password)
    return f"mongodb+srv://{user}:{password}@{settings.mongodb_host}/?appName={settings.mongodb_app_name}"

def get_db():
    return client[settings.db_name]

async def connect():
    global client
    client = AsyncIOMotorClient(build_mongo_url())

async def disconnect():
    global client
    if client:
        client.close()
