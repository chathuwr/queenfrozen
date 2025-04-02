import os
import re
import logging
import aiohttp
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes
from urllib.parse import quote

logger = logging.getLogger(__name__)

# Configuration
API_URL = "https://sadiya-tech-apis.vercel.app/download/fbdl"
DOWNLOAD_TIMEOUT = 300  # 5 minutes

class FrozenTheme:
    def box(self, title, content):
        return f"❄️ *{title}* ❄️\n\n{content}"

async def fb_download_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /fb command to download Facebook videos"""
    theme = FrozenTheme()
    
    if not update.message:
        return

    await update.message.reply_chat_action("typing")

    # Check if URL is provided
    if not context.args:
        await update.message.reply_text(
            theme.box("USAGE", "Command: /fb <url>\nExample: /fb https://fb.watch/xyz"),
            parse_mode="Markdown"
        )
        return

    url = context.args[0]
    fb_regex = r"(https?:\/\/)?(www\.)?(facebook|fb|m\.facebook|fb\.watch|web\.facebook)\.com\/(.*)"
    
    if not re.match(fb_regex, url, re.IGNORECASE):
        await update.message.reply_text(
            theme.box("ERROR", "Invalid Facebook video URL!"),
            parse_mode="Markdown"
        )
        return

    # Send processing message
    processing_msg = await update.message.reply_text(
        "🔍 Processing your Facebook video link...",
        parse_mode="Markdown"
    )

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL, params={"url": url}, timeout=10) as resp:
                if resp.status != 200:
                    raise Exception("API request failed")
                data = await resp.json()

        if not data.get("status"):
            await processing_msg.edit_text(
                theme.box("ERROR", "Video not found or private!"),
                parse_mode="Markdown"
            )
            return

        result = data.get("result", {})
        hd_url = result.get("hd")
        sd_url = result.get("sd")

        if not hd_url and not sd_url:
            await processing_msg.edit_text(
                theme.box("ERROR", "No downloadable video found!"),
                parse_mode="Markdown"
            )
            return

        # Try HD first, then fall back to SD
        video_url = hd_url or sd_url
        quality = "HD" if hd_url else "SD"

        await processing_msg.edit_text(
            f"⬇️ Downloading {quality} video..."
        )

        await update.message.reply_video(
            video=video_url,
            caption=f"🎥 Facebook Video ({quality})\n🔗 {url[:50]}...",
            supports_streaming=True
        )

        await processing_msg.delete()

    except Exception as e:
        logger.error(f"FB Download Error: {e}")
        try:
            await processing_msg.edit_text(
                theme.box("ERROR", f"Failed: {str(e)}"),
                parse_mode="Markdown"
            )
        except:
            await update.message.reply_text(
                theme.box("ERROR", f"Failed: {str(e)}"),
                parse_mode="Markdown"
            )

def register(application):
    """Register the plugin."""
    application.add_handler(CommandHandler("fb", fb_download_command))
    logger.info("Facebook Downloader plugin loaded!")
