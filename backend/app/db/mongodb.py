from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
MONGODB_DB = os.getenv("MONGODB_DB", "image_moderation")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[MONGODB_DB]

# Create indexes
async def create_indexes():
    await db.tokens.create_index("token", unique=True)
    await db.usages.create_index("token")
    await db.usages.create_index("timestamp") 