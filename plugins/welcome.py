from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import os

# Paths
IMAGE_PATH = os.path.join("src", "frozen.jpg")
AUDIO_PATH = os.path.join("src", "WhatsApp Audio 2025-03-18 at 3.25.32 AM.mpeg")

# Main welcome keyboard
def get_welcome_keyboard():
    keyboard = [
        [InlineKeyboardButton("❄️ Menu", callback_data="menu")],
        [InlineKeyboardButton("🌐 Support Group", url="https://t.me/yourgroup")],
        [InlineKeyboardButton("📢 Support Channel", url="https://t.me/yourchannel")],
        [InlineKeyboardButton("👑 Owner", callback_data="owner")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Sub-menu keyboard
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
        # First send the audio
        with open(AUDIO_PATH, "rb") as audio:
            await update.message.reply_audio(
                audio=audio,
                caption="🎵 *A magical gift from the Frozen Queen* 🎵",
                parse_mode="Markdown"
            )
        
        # Then send the welcome message with image
        caption = "✨ *Welcome to the Frozen Queen's Realm!* ✨\nI am the *Frozen Queen*!"
        with open(IMAGE_PATH, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=caption,
                parse_mode="Markdown",
                reply_markup=get_welcome_keyboard()
            )

    async def button_handler(update, context):
        query = update.callback_query
        await query.answer()
        
        # Menu navigation handling
        current_caption = query.message.caption
        new_caption = ""
        new_markup = None

        if query.data == "menu":
            new_caption = "❄️ *The Frozen Menu* ❄️"
            new_markup = get_menu_keyboard()
        elif query.data == "owner":
            new_caption = "👑 *The Frozen Queen's Creator* 👑"
            new_markup = get_welcome_keyboard()
        elif query.data == "back":
            new_caption = "✨ *Welcome back!* ✨"
            new_markup = get_welcome_keyboard()
        else:
            new_caption = f"❄️ *{query.data.replace('_', ' ').title()}* ❄️"
            new_markup = get_menu_keyboard()

        await query.edit_message_caption(
            caption=new_caption,
            parse_mode="Markdown",
            reply_markup=new_markup
        )

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))

# Audio download function
import requests
def download_audio():
    os.makedirs("src", exist_ok=True)
    url = "https://github.com/chathurahansaka1/help/raw/main/audio/WhatsApp%20Audio%202025-03-18%20at%203.13.40%20AM.mpeg"
    if not os.path.exists(AUDIO_PATH):
        print("Downloading audio file...")
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(AUDIO_PATH, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
            print("Audio downloaded successfully!")
        else:
            print(f"Failed to download audio. Status code: {r.status_code}")

if __name__ == "__main__":
    download_audio()
