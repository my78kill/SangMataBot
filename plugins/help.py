# Copyright @ISmartDevs
# Channel t.me/TheSmartDev
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from config import COMMAND_PREFIXES, BOT_USERNAME
from utils import LOGGER

# Help command to explain bot functionality
@Client.on_message(filters.command("help", prefixes=COMMAND_PREFIXES, case_sensitive=False))
async def help_command(client, message):
    LOGGER.info(f"Help command received: '{message.text}' from user {message.from_user.id} in chat {message.chat.id} (type: {message.chat.type})")
    try:
        help_message = (
            f"**Welcome to {BOT_USERNAME}!** 🎉\n"
            "I'm a feature-packed bot designed to assist you in private chats and groups. Here's what I can do:\n\n"
            "✨ **Available Commands** ✨\n"
            f"- **/start**: Get a welcome message and start interacting with me in private chats.\n"
            f"- **/history [user_id or @username]**: View a user's name and username change history. Use a user ID or username as an argument, or omit for your own history. Works in private chats and groups.\n"
            f"- **/help**: Show this help message.\n\n"
            "🌐 **Group Features** 🌐\n"
            "- **Welcome Message**: When I'm added to a group, I send a welcome message to thank you and remind you to grant me admin permissions with \"Manage Group\" for full functionality.\n"
            "- **User Tracking**: In groups, I monitor members' messages to track username and name changes, storing them in my database. If a user changes their username or name, I announce it in the group, e.g., `User <user_id> changed username from @Old to @New`.\n"
            "- **History Lookup**: Use `/history` in groups to check any user's change history by their ID or username.\n\n"
            "💡 **Tips** 💡\n"
            f"- Commands work with prefixes: {', '.join(f'`{p}`' for p in COMMAND_PREFIXES)} (e.g., `/start`, `.start`).\n"
            "- In groups, ensure I have admin permissions to send messages and track changes effectively.\n"
            "- For support or updates, join @TheSmartDev!\n\n"
            f"Have fun with {BOT_USERNAME}! 🚀"
        )
        await client.send_message(
            chat_id=message.chat.id,
            text=help_message,
            parse_mode=ParseMode.MARKDOWN
        )
        LOGGER.info(f"Help message sent to user {message.from_user.id} in chat {message.chat.id}")
    except Exception as e:
        LOGGER.error(f"Error in help command for user {message.from_user.id}: {e}", exc_info=True)
        await client.send_message(
            chat_id=message.chat.id,
            text="Error processing help command. Check logs for details.",
            parse_mode=ParseMode.MARKDOWN
        )