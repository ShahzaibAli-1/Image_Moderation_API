import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv

async def init_db():
    # Load environment variables
    load_dotenv()
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
    db = client[os.getenv("MONGODB_DB", "image_moderation")]
    
    # Check if admin token exists
    admin_token = os.getenv("ADMIN_TOKEN")
    if not admin_token:
        print("ADMIN_TOKEN not set in environment variables")
        return
    
    # Create admin token if it doesn't exist
    token_doc = await db.tokens.find_one({"token": admin_token})
    if not token_doc:
        token = {
            "token": admin_token,
            "is_admin": True,
            "created_at": datetime.utcnow()
        }
        await db.tokens.insert_one(token)
        print("Admin token initialized successfully")
    else:
        print("Admin token already exists")
    
    # Close connection
    client.close()

if __name__ == "__main__":
    asyncio.run(init_db()) 