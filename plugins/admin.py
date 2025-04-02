from telegram.ext import CommandHandler

OWNER_ID = 6772025275

def register(application):
    async def status(update, context):
        if update.effective_user.id != OWNER_ID:
            await update.message.reply_text("Owner only!")
            return
        await update.message.reply_text("Bot is dreaming smoothly!")
    
    application.add_handler(CommandHandler("status", status))