from telegram.ext import Application, CommandHandler, ContextTypes
from telegram import Update, error
from pathlib import Path
import importlib.util
import os
import sys
import logging

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7692861322:AAEE0KXj4L3JPZivmiqh8NxHUGVNevHit0s"
OWNER_ID = 6772025275

def load_plugins(application):
    plugin_dir = Path("plugins")
    if not plugin_dir.exists():
        logger.error(f"Plugin directory '{plugin_dir}' not found!")
        return
    
    for plugin_file in plugin_dir.glob("*.py"):
        if plugin_file.name.startswith("__"):
            continue
        plugin_name = plugin_file.stem
        try:
            spec = importlib.util.spec_from_file_location(plugin_name, plugin_file)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "register"):
                module.register(application)
                logger.info(f"Successfully loaded plugin: {plugin_name}")
        except Exception as e:
            logger.error(f"Failed to load plugin {plugin_name}: {str(e)}")

async def restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Only the bot owner can restart me!")
        return
    await update.message.reply_text("Restarting now...")
    os.execv(sys.executable, [sys.executable] + sys.argv)

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("Only the bot owner can stop me!")
        return
    await update.message.reply_text("Stopping bot now...")
    sys.exit(0)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error
    logger.error(f"Error occurred: {error}", exc_info=True)
    
    try:
        # Handle different types of updates
        if update and update.callback_query:
            # For callback queries, try to edit the original message
            try:
                await update.callback_query.message.edit_text("⚠️ Something went wrong!")
            except:
                pass
        elif update and update.message:
            # For regular messages
            await update.message.reply_text("⚠️ Something went wrong!")
        
        # Handle specific error types
        if isinstance(error, error.BadRequest):
            if "Query is too old" in str(error):
                logger.info("Ignoring expired callback query")
                return
            elif "Conflict" in str(error):
                await update.message.reply_text("Bot conflict detected! Only one instance can run at a time.")
    except Exception as e:
        logger.error(f"Error in error handler: {e}")

def main():
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("restart", restart))
    application.add_handler(CommandHandler("stop", stop))
    
    # Add error handler
    application.add_error_handler(error_handler)

    # Load plugins
    load_plugins(application)

    # Define allowed updates
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

    logger.info("Dream Weaver Bot is starting...")
    try:
        application.run_polling(
            allowed_updates=allowed_updates,
            drop_pending_updates=True,
            close_loop=False
        )
    except Exception as e:
        logger.critical(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
