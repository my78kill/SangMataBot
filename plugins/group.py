# Copyright @ISmartDevs
# Channel t.me/TheSmartDev
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from core import bot_data
from utils import LOGGER
from config import BOT_USERNAME
from datetime import datetime

# Handler for when the bot is added to a group
@Client.on_message(filters.group & filters.new_chat_members)
async def on_bot_added(client, message):
    bot_id = (await client.get_me()).id
    if bot_id in [member.id for member in message.new_chat_members]:
        chat_id = message.chat.id
        chat_type = "group"
        
        # Store group in MongoDB with last_active timestamp
        try:
            bot_data.update_one(
                {"chat_id": chat_id},
                {"$set": {"chat_type": chat_type, "last_active": datetime.utcnow()}},
                upsert=True
            )
            LOGGER.info(f"Bot added to group {chat_id}, stored in database")
        except Exception as e:
            LOGGER.error(f"Failed to store group {chat_id}: {e}")
        
        # Send welcome message
        welcome_message = (
            "**Thanks For Adding Me To This Group** 🎉\n\n"
            f"I'm {BOT_USERNAME}! Make sure I have **ADMIN** permissions with \"Manage Group\" to function properly.\n"
            "Type `/help` or join @TheSmartDev for support."
        )
        try:
            await client.send_message(
                chat_id=chat_id,
                text=welcome_message,
                parse_mode=ParseMode.MARKDOWN
            )
            LOGGER.info(f"Sent welcome message to group {chat_id}")
        except Exception as e:
            LOGGER.error(f"Failed to send welcome message to group {chat_id}: {e}")