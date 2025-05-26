# Copyright @ISmartDevs
# Channel t.me/TheSmartDev

from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB
from utils import LOGGER

# Initialize MongoDB client
try:
    LOGGER.info("Creating Mongo Client From MONGO_URI")
    mongo_client = MongoClient(MONGO_URI)
    db = mongo_client[MONGO_DB]

    # Collections
    bot_data = db["bot_data"]            # Collection for users and groups
    user_history = db["user_history"]    # Collection for user name/username history

    # Ensure indexes for efficient querying
    bot_data.create_index("chat_id", unique=True)
    user_history.create_index("user_id", unique=True)

    LOGGER.info("MongoDB client initialized and indexes created successfully!")

except Exception as e:
    LOGGER.error(f"Failed to initialize MongoDB client: {e}")
    raise
