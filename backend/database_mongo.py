"""
MongoDB database connection and initialization using Motor and Beanie
"""
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from config import settings
from models_mongo import Goal, Plan, Task
import logging

logger = logging.getLogger(__name__)

# MongoDB client
mongodb_client: AsyncIOMotorClient = None


async def connect_to_mongodb():
    """Connect to MongoDB database"""
    global mongodb_client
    
    try:
        logger.info(f"Connecting to MongoDB at {settings.MONGODB_URL}")
        mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
        
        # Test connection
        await mongodb_client.admin.command('ping')
        logger.info("✓ Successfully connected to MongoDB")
        
        # Initialize Beanie with document models
        await init_beanie(
            database=mongodb_client[settings.MONGODB_DB_NAME],
            document_models=[Goal, Plan, Task]
        )
        logger.info("✓ Beanie ODM initialized")
        
    except Exception as e:
        logger.error(f"✗ Failed to connect to MongoDB: {e}")
        raise


async def close_mongodb_connection():
    """Close MongoDB connection"""
    global mongodb_client
    
    if mongodb_client:
        mongodb_client.close()
        logger.info("✓ MongoDB connection closed")


def get_database():
    """Get MongoDB database instance"""
    if mongodb_client is None:
        raise Exception("MongoDB client not initialized")
    return mongodb_client[settings.MONGODB_DB_NAME]
