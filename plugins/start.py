# Copyright @ISmartDevs
# Channel t.me/TheSmartDev
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from utils import LOGGER
from config import BOT_USERNAME, COMMAND_PREFIXES

# Start command handler
@Client.on_message(filters.command("start", prefixes=COMMAND_PREFIXES))
async def start_command(client, message):
    LOGGER.info(f"Received start command from {message.from_user.id}")
    
    # Define the start message with Markdown formatting
    start_message = (
        "Hello! 👋\n\n"
        "**If you're a group admin:**\n"
        "You can add this bot by clicking the button below. "
        "Make sure that you add the SangMata bot as **ADMIN** with \"Manage Group\" permission so that it can work properly!\n\n"
        "**If you need help:**\n"
        "Just type and send \"help\" in the chat or join our support group @TheSmartDev to ask for help."
    )
    
    # Create the inline keyboard with the "Add to Group" button
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    "➕ Add Sangmata to my Group",
                    url=f"https://t.me/{BOT_USERNAME}?startgroup"
                )
            ]
        ]
    )
    
    # Send the start message with the button using client.send_message
    await client.send_message(
        chat_id=message.chat.id,
        text=start_message,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )