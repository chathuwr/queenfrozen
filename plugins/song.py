from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import requests
import random
import time
import urllib.parse

user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36'
]

def get_headers():
    return {
        'User-Agent': random.choice(user_agents),
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Referer': 'https://www.google.com'
    }

async def song_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Please provide a YouTube link after the command. Example: /song https://youtu.be/VIDEO_ID or /song https://www.youtube.com/watch?v=VIDEO_ID")
        return

    youtube_url = context.args[0]

    # Normalize and extract video ID
    parsed_url = urllib.parse.urlparse(youtube_url)
    if not parsed_url.scheme:
        youtube_url = f"https://{youtube_url}"

    video_id = None
    if 'youtu.be' in youtube_url:
        video_id = youtube_url.split('/')[-1].split('?')[0]
    elif 'watch' in youtube_url:
        video_id = urllib.parse.parse_qs(parsed_url.query).get('v', [None])[0]

    if not video_id:
        await update.message.reply_text("Invalid YouTube link. Please provide a valid link (e.g., https://youtu.be/VIDEO_ID or https://www.youtube.com/watch?v=VIDEO_ID).")
        return

    # Construct the standardized URL
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    # Initial status message
    status_message = await update.message.reply_text("Preparing to download the song from the Frozen Queen's vault...")

    try:
        # Small delay for stability
        time.sleep(random.uniform(1, 2))

        # Use the API to download MP3
        api_url = f"https://apis-keith.vercel.app/download/dlmp3?url={urllib.parse.quote(youtube_url, safe=':/')}"

        # Update status
        await status_message.edit_text("Downloading the song... Please wait as the ice melts.")

        mp3_response = requests.get(api_url, headers=get_headers(), allow_redirects=True, timeout=30)

        if mp3_response.status_code == 200:
            # Use video ID as filename
            song_name = video_id or "downloaded_song"
            await update.message.reply_audio(audio=mp3_response.content, filename=f"{song_name}.mp3")
            await status_message.edit_text(f"Here is your song! Enjoy the melody of the Frozen Queen.")
        else:
            await status_message.edit_text(f"API error: Status code {mp3_response.status_code}. Details: {mp3_response.text}")
            print(f"API Response for URL {youtube_url}: {mp3_response.text}")

    except requests.Timeout:
        await status_message.edit_text("Download timed out. The Frozen Queen's network is slow today!")
    except requests.ConnectionError:
        await status_message.edit_text("Connection failed. Check your internet or try again later.")
    except Exception as e:
        await status_message.edit_text(f"An unexpected error occurred: {str(e)}")
        print(f"Error downloading song for URL {youtube_url}: {str(e)}")

def register(application):
    application.add_handler(CommandHandler("song", song_command))