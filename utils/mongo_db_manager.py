from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
from .logger import logger
from .config import settings
from pymongo import ASCENDING, DESCENDING
from mongo_collection_names import CollectionNames

class MongoDBManager:
    def __init__(self):
        self.client: Optional[AsyncIOMotorClient] = None
        self.database = None

    async def connect(self):
        try:
            logger.info(f"connecting to MongoDB: {settings.MONGODB_DATABASE}")

            self.client = AsyncIOMotorClient(settings.mongo_db_url)
            self.database = self.client[settings.MONGODB_DATABASE]

            # Create indexes for better performance
            await self._create_indexes()

        except Exception as e:
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise

    async def _create_indexes(self):
        try:
            #create unique index on email + start_date
            await self.database[CollectionNames.TRAVEL_COLLECTION].create_index(
                    [("email", ASCENDING), ("request.start_date", ASCENDING)],
                    unique=True, 
                    name="email_request_start_date_idx",
                )            
            logger.info("MongoDB indexes created successfully")
        except Exception as e:
            logger.warning(f"Error creating MongoDB indexes: {str(e)}")

    async def disconnect(self):

        """
        Close MongoDB connection
        """
        if self.client:
            self.client.close()
            client = None
            logger.info("MongoDB connection closed")


    async def health_check(self) -> bool:
        """
        Check if MongoDB connection is healthy
        """
        try:
            if self.client:
                await self.client.admin.command('ping')
                return True

            return False
        except Exception as e:
            logger.error(f"MongoDB health check failed: {str(e)}")
            return False

    def get_collection(self, collection_name: str):
        if self.database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self.database[collection_name]


# Global MongoDB manager instance
mongodb_manager = MongoDBManager()

