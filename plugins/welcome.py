from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

# Path to the image
IMAGE_PATH = os.path.join("src", "frozen.jpg")

# Main welcome keyboard
def get_welcome_keyboard():
    keyboard = [
        [InlineKeyboardButton("❄️ Menu", callback_data="menu")],
        [InlineKeyboardButton("🌐 Support Group", url="https://t.me/yourgroup")],
        [InlineKeyboardButton("📢 Support Channel", url="https://t.me/yourchannel")],
        [InlineKeyboardButton("👑 Owner", callback_data="owner")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Sub-menu keyboard for "Menu"
def get_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("✨ Ice Magic", callback_data="ice_magic")],
        [InlineKeyboardButton("❄️ Snow Games", callback_data="snow_games")],
        [InlineKeyboardButton("🛡️ Frost Help", callback_data="frost_help")],
        [InlineKeyboardButton("⬅️ Back", callback_data="back")],
    ]
    return InlineKeyboardMarkup(keyboard)

def register(application):
    async def start(update, context):
        caption = (
            "✨ *Welcome to the Frozen Queen's Realm!* ✨\n"
            "I am the *Frozen Queen*, ruler of ice and magic. Explore my kingdom below!"
        )
        with open(IMAGE_PATH, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=get_welcome_keyboard()
            )

    async def button_handler(update, context):
        query = update.callback_query
        await query.answer()  # Acknowledge button press
        
        current_caption = query.message.caption
        new_caption = ""
        new_markup = None

        if query.data == "menu":
            new_caption = "❄️ *The Frozen Menu* ❄️\nChoose your icy path:"
            new_markup = get_menu_keyboard()
        elif query.data == "owner":
            new_caption = "👑 *The Frozen Queen’s Creator* 👑\nBow to the one who forged this realm!"
            new_markup = get_welcome_keyboard()
        elif query.data == "ice_magic":
            new_caption = "✨ *Ice Magic* ✨\nCast spells of frost and wonder!"
            new_markup = get_menu_keyboard()
        elif query.data == "snow_games":
            new_caption = "❄️ *Snow Games* ❄️\nPlay in the eternal snowfields!"
            new_markup = get_menu_keyboard()
        elif query.data == "frost_help":
            new_caption = "🛡️ *Frost Help* 🛡️\nNeed aid in the icy realm? Ask away!"
            new_markup = get_menu_keyboard()
        elif query.data == "back":
            new_caption = "✨ *Welcome to the Frozen Queen's Realm!* ✨\nI am the *Frozen Queen*, ruler of ice and magic."
            new_markup = get_welcome_keyboard()

        # Only edit if caption or markup changes
        if current_caption != new_caption or query.message.reply_markup != new_markup:
            await query.edit_message_caption(
                caption=new_caption,
                parse_mode="Markdown",
                reply_markup=new_markup
            )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))