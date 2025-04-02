from telegram.ext import Application, CommandHandler
from telegram import Update
from pathlib import Path
import importlib.util
import os
import sys

TOKEN = "7692861322:AAEE0KXj4L3JPZivmiqh8NxHUGVNevHit0s"
OWNER_ID = 6772025275

def load_plugins(application):
    plugin_dir = Path("plugins")
    if not plugin_dir.exists():
        print(f"Plugin directory '{plugin_dir}' not found!")
        return
    
    for plugin_file in plugin_dir.glob("*.py"):
        if plugin_file.name.startswith("__"):
            continue
        plugin_name = plugin_file.stem
        spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        if hasattr(module, "register"):
            module.register(application)
            print(f"Loaded plugin: {plugin_name}")

async def restart(update, context):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Only the bot owner can restart me!")
        return
    await update.message.reply_text("Restarting now...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

# Stop command (owner only)
async def stop(update, context):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Only the bot owner can stop me!")
        return
    await update.message.reply_text("Stopping bot now...")
    sys.exit(0)  # Gracefully stop the bot

# Error handler
async def error_handler(update, context):
    error = context.error
    print(f"Error occurred: {error}")
    if "Conflict" in str(error):
        await update.message.reply_text("Bot conflict detected! Only one instance can run at a time.")
    else:
        await update.message.reply_text("Something went wrong!")

def main():
    application = Application.builder().token(TOKEN).build()

    async def start(update, context):
        await update.message.reply_text(
            "Welcome to Dream Weaver Bot! Add fragments with /add <word> and weave a story with /weave."
        )
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("stop", stop))  # Add stop command
    
    application.add_error_handler(error_handler)

    load_plugins(application)

    allowed_updates = [
        Update.MESSAGE,
        Update.EDITED_MESSAGE,
        Update.CHANNEL_POST,
        Update.EDITED_CHANNEL_POST,
        Update.INLINE_QUERY,
        Update.CHOSEN_INLINE_RESULT,
        Update.CALLBACK_QUERY,
        Update.SHIPPING_QUERY,
        Update.PRE_CHECKOUT_QUERY,
        Update.POLL,
        Update.POLL_ANSWER,
        Update.MY_CHAT_MEMBER,
        Update.CHAT_MEMBER,
        Update.CHAT_JOIN_REQUEST
    ]

    print("Dream Weaver Bot is running...")
    application.run_polling(allowed_updates=allowed_updates)

if __name__ == "__main__":
    main()