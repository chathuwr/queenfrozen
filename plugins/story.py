from telegram.ext import CommandHandler, CallbackQueryHandler, MessageHandler, filters, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import os
import requests
from io import BytesIO
import urllib.parse
import json
import random

# States for conversation handler
TITLE_INPUT = 1
LANGUAGE_SELECTION = 2

# Path to default image (when API fails)
IMAGE_PATH = os.path.join("src", "frozen.jpg")

# API URLs
STORY_API_URL = "https://dev-pycodz-blackbox.pantheonsite.io/DEvZ44d/deepseek.php?text="
IMAGE_API_URL = "https://seaart-ai.apis-bj-devs.workers.dev/?Prompt="

# List of random titles for story generation
RANDOM_TITLES = [
    "The Frozen Heart",
    "Crystal Palace Mystery",
    "The Snow Princess",
    "Winter's Whisper",
    "The Ice Dragon",
    "Frost Enchantment",
    "The Eternal Winter",
    "Snowflake's Journey",
    "The Magic Sleigh",
    "Queen of Blizzards",
    "The Arctic Guardian",
    "Icicle Dreams"
]

# List of random Sinhala titles
RANDOM_SINHALA_TITLES = [
    "හිම රැජිනගේ රහස",
    "අයිස් මාළිගාව",
    "ශීත සුරංගනාවි",
    "මායාවී හිම",
    "සීතල හදවත",
    "හිම දරුවා",
    "අයිස් මැජික්",
    "සදාකාලික ශීතල",
    "හිම පත්වල මායාව",
    "හිම රැජිනගේ කතාව",
    "ක්‍රිස්ටල් වනාන්තරය",
    "මායාවී හිම රාත්‍රිය"
]

# Story generation functions
def generate_story_from_title(title, language="english"):
    try:
        if language.lower() == "sinhala":
            prompt = f"'{title}' නමින් හිම රැජිනගේ අයිස් රාජධානියේ පිහිටි මායාකාරී ෆැන්ටසි කතාවක් ලියන්න. කතාව ලස්සන, මායාකාරී විය යුතු අතර අවම වශයෙන් වචන 300ක් දිග විය යුතුය. අයිස් මැජික්, හිම සහ ශීත තේමා ඇතුළත් කරන්න."
        else:
            prompt = f"Write a magical fantasy story titled '{title}' set in the Frozen Queen's ice kingdom. The story should be beautiful, enchanting, and at least 300 words long. Include ice magic, snow, and winter themes."
        
        encoded_prompt = urllib.parse.quote(prompt)
        response = requests.get(f"{STORY_API_URL}{encoded_prompt}")
        
        if response.status_code == 200:
            try:
                json_response = json.loads(response.text)
                if isinstance(json_response, dict):
                    for field in ['text', 'content', 'story', 'generated_text', 'completion', 'result']:
                        if field in json_response:
                            story = json_response[field].strip()
                            break
                    else:
                        return generate_fallback_story(title, language)
                else:
                    return generate_fallback_story(title, language)
            except json.JSONDecodeError:
                story = response.text.strip()
            
            if len(story.split()) < 300:
                if language.lower() == "sinhala":
                    story += f"\n\n'{title}' කතාව හිම රැජිනගේ රාජධානියේ දිගටම විකසනය වුණා. අයිස් ක්‍රිස්ටල් මැජික් සමඟ වාතයේ නටමින් පැරණි රාජධානිය හරහා ගලා ගියා. රැජිනගේ බලය මීට පෙර දැක නොමැති ශීත ආශ්චර්යක් ඇති කළා. මායාකාරී හිම ඉරණම් රටා නිර්මාණය කරමින්, මෙම සදාකාලික අයිස් මායාකාරී භූමියේ ජීවත් වන සියල්ලන්ගේ ඉරණම් එකට එක් කළා."
                else:
                    story += f"\n\nThe tale of '{title}' continued to unfold in the Frozen Queen's realm. Ice crystals danced in the air as magic flowed through the ancient kingdom. The Queen's power brought forth a winter wonder unlike any seen before. The enchanted snow created patterns of destiny, weaving together the fates of all who lived in this magical land of eternal frost."
            
            return story
        else:
            return generate_fallback_story(title, language)
            
    except Exception as e:
        return generate_fallback_story(title, language)

def generate_fallback_story(title, language="english"):
    if language.lower() == "sinhala":
        return f"""# {title}

හිම රැජිනගේ රාජධානියේ හදවතේ, හිම පත් සදාකාලිකව නටන හා අයිස් ක්‍රිස්ටල් අුරෝරා බොරියලිස් ආලෝකය අල්ලා ගන්නා තැන, නව කතාවක් ගොඩනැගෙන්නට පටන් ගත්තා. වාතය ශීත මැජික් සමඟ තියුණු වූ අතර, දුරස්ථ ස්ලේ සීනු හඬ අයිස් කරන ලද මිටියාවත් හරහා ප්‍රතිරාවය විය.

හිම රැජින තම ක්‍රිස්ටල් කුළුණේ ඉහළ සිටියාය, ඇගේ සාය කවදාවත් නොදියවන මායාකාරී අයිස් සමඟ දිලිසෙමින්. ඇගේ ඇස්, පැරණි ග්ලැසියර් මෙන් ගැඹුරු නීල පැහැති, ඇගේ රාජධානිය ආඩම්බරය හා කනස්සල්ල යන දෙකම සමඟ සමීක්ෂණය කළාය. ඇගේ රාජධානියේ යමක් වෙනස් වෙමින් තිබුණා - ඇය ඇගේ පාද යටින් ඇති හිම තුළම එය දැනෙනවා.

"ඔබගේ මහත්මියනි," ඇයට පිටුපසින් හඬක් ඇසුණි. එය ෆ්රොස්ට්, ඇගේ පරිපූර්ණ ශීත මැජික් වලින් නිර්මාණය කරන ලද ඇගේ පරම ලෝයල් උපදේශකයායි. "සදාකාලික උද්‍යානයේ අයිස් රෝස මල් ඔවුන්ගේ කාලයෙන් පිටත පිපෙනවා."

රැජින හැරුණා, ඇගේ ප්‍රකාශනය බැරෑරුම්. "මැජික් තුලනය වෙනස් වෙනවා, ෆ්රොස්ට්. අපි ඒ ඇයි දැන ගන්න ඕනෑ."

මේ ආකාරයට රැජිනගේ ගමන ඇගේම රාජධානියේ ගැඹුරට, සියවස් ගණනාවක් තිස්සේ ඇය නොගිය ස්ථාන වලට ආරම්භ විය. ජීවමාන අයිස් වලින් කැටයම් කරන ලද ගස් ඇති වනාන්තර හරහා, ඇගේ යටත් වැසියන් මායාකාරී හිම වලින් ආශ්චර්යයන් නිර්මාණය කරන ගම්මාන පසුකර, සහ පුරාතන ශීත ආත්ම අති පිරිසිදු සුදු පැහැති ඇඳ ඇතිරිලි යට නිදා සිටින මිටියාවත් වලට.

ඇය සොයා ගත්තේ ආශ්චර්යමත් හා කරදරකාරී දෙකක් - හිම නොදියවා උණුසුම් ඇති කිරීමේ හැකියාව ඇති දරුවෙක්. ස්වභාවික විරුද්ධාභාසයක්, සදාකාලික ශීතල රාජධානියේ හාස්කමක්. සමහරුන් බිය වූයේ මෙම දරුවා ඔවුන්ගේ අයිස් ස්වර්ගයේ අවසානය ගෙන එනු ඇතැයි කියාය, නමුත් හිම රැජින දුටුවේ වෙනස් දෙයක් - පරිණාමය සඳහා, වර්ධනය සඳහා අවස්ථාවක්.

"මැජික් ස්ථිතික නොවේ," ඇය ඇගේ උසාවියට ප්‍රකාශ කළාය. "එය ජලය මෙන්, සුළඟේ හිම මෙන් ගලා යනවා සහ වෙනස් වෙනවා. මෙම දරුවා තර්ජනයක් නොව තෑග්ගක් - ශීතලේ හදවතේ පවා, ජීවිතයට හා උණුසුමට ඔවුන්ගේ ස්ථානය ඇති බව මතක් කර දෙනවා."

අවසානය."""
    else:
        return f"""# {title}

In the heart of the Frozen Queen's realm, where snowflakes danced eternally and ice crystals caught the light of the aurora borealis, a new tale began to unfold. The air was crisp with winter magic, and the sound of distant sleigh bells echoed through the frosted valleys.

The Frozen Queen stood atop her crystal tower, her gown shimmering with enchanted ice that never melted. Her eyes, deep blue like the ancient glaciers, surveyed her kingdom with both pride and concern. Something was changing in her realm - she could feel it in the very snow beneath her feet.

"Your Majesty," came a voice behind her. It was Frost, her loyal advisor, a being crafted from the purest winter magic. "The ice roses in the Eternal Garden are blooming out of season."

The Queen turned, her expression solemn. "The balance of magic shifts, Frost. We must discover why."

Thus began the Queen's journey into the depths of her own kingdom, places even she had not ventured in centuries. Through forests where trees were sculpted from living ice, past villages where her subjects crafted wonders from enchanted snow, and into valleys where ancient winter spirits slumbered beneath blankets of pristine white.

What she discovered was both wondrous and troubling - a child with the ability to create warmth without melting the snow. A paradox of nature, a miracle in the realm of eternal winter. Some feared this child would bring the end of their icy paradise, but the Frozen Queen saw something different - an opportunity for evolution, for growth.

"Magic is not static," she declared to her court. "It flows and changes like water, like snow in the wind. This child is not a threat but a gift - a reminder that even in the heart of winter, life and warmth have their place."

The End."""

# Function to get an image URL based on the title using the provided API
def get_story_image(title, language="english"):
    try:
        if language.lower() == "sinhala":
            image_prompt = f"{title}, magical ice kingdom, frozen queen realm, fantasy scene, detailed ice artwork, winter wonderland, snow palace, high quality, 4k"
        else:
            image_prompt = f"{title}, magical ice kingdom, frozen queen realm, fantasy scene, detailed ice artwork, winter wonderland, snow palace, high quality, 4k"
        
        encoded_prompt = urllib.parse.quote(image_prompt)
        response = requests.get(f"{IMAGE_API_URL}{encoded_prompt}")
        
        if response.status_code == 200:
            try:
                json_data = response.json()
                for field in ['image_url', 'url', 'imageUrl', 'image', 'result']:
                    if field in json_data:
                        image_url = json_data[field]
                        if isinstance(image_url, str) and (image_url.startswith('http://') or image_url.startswith('https://')):
                            return image_url
                
                if 'data' in json_data and isinstance(json_data['data'], dict):
                    for field in ['image_url', 'url', 'imageUrl', 'image']:
                        if field in json_data['data']:
                            image_url = json_data['data'][field]
                            if isinstance(image_url, str) and (image_url.startswith('http://') or image_url.startswith('https://')):
                                return image_url
            except:
                import re
                urls = re.findall(r'https?://\S+\.(?:jpg|jpeg|png|gif)', response.text)
                if urls:
                    return urls[0]
                
                if response.text.startswith('http://') or response.text.startswith('https://'):
                    cleaned_url = response.text.strip().split('\n')[0]
                    if cleaned_url.endswith('.jpg') or cleaned_url.endswith('.png') or cleaned_url.endswith('.jpeg'):
                        return cleaned_url
        
        return None
            
    except Exception as e:
        return None

async def customstory_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton("English", callback_data="lang_english"),
            InlineKeyboardButton("සිංහල", callback_data="lang_sinhala")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "✨ *Create Your Frozen Tale* ✨\n\n"
        "Please select the language for your story:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return LANGUAGE_SELECTION

async def language_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    if query.data == "lang_english":
        context.user_data['language'] = "english"
        lang_text = "English"
    else:  # lang_sinhala
        context.user_data['language'] = "sinhala"
        lang_text = "සිංහල"
    
    keyboard = [
        [InlineKeyboardButton("Generate Random Title", callback_data="random_title")],
        [InlineKeyboardButton("Enter My Own Title", callback_data="own_title")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        f"✨ *Create Your Frozen Tale in {lang_text}* ✨\n\n"
        "Would you like to generate a random title or enter your own?",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )
    return TITLE_INPUT

async def title_button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    
    language = context.user_data.get('language', 'english')
    
    if query.data == "random_title":
        if language.lower() == "sinhala":
            title = random.choice(RANDOM_SINHALA_TITLES)
        else:
            title = random.choice(RANDOM_TITLES)
            
        context.user_data['story_title'] = title
        
        if language.lower() == "sinhala":
            await query.edit_message_text(
                f"✨ *'{title}' මායාකාරී කතාව* ✨\n\n"
                "හිම රැජින ඔබගේ මායාකාරී කතාව සාදමින් සිටී...\n"
                "අයිස් මැජික් ක්‍රියා කරන අතරතුර මොහොතක් රැඳී සිටින්න.",
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                f"✨ *Creating '{title}'* ✨\n\n"
                "The Frozen Queen is crafting your magical tale with this random title...\n"
                "Please wait a moment while the ice magic works.",
                parse_mode="Markdown"
            )
        
        await generate_and_send_story(query.message, context, title, language)
        return ConversationHandler.END
        
    elif query.data == "own_title":
        if language.lower() == "sinhala":
            await query.edit_message_text(
                "කරුණාකර ඔබගේ හිම රැජිනගේ මායාකාරී කතාව සඳහා මාතෘකාවක් ඇතුළත් කරන්න:",
                parse_mode="Markdown"
            )
        else:
            await query.edit_message_text(
                "Please enter a title for your magical tale in the Frozen Queen's realm:",
                parse_mode="Markdown"
            )
        return TITLE_INPUT

async def receive_title(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    title = update.message.text
    context.user_data['story_title'] = title
    language = context.user_data.get('language', 'english')
    
    if language.lower() == "sinhala":
        await update.message.reply_text(
            f"✨ *'{title}' මායාකාරී කතාව* ✨\n\n"
            "හිම රැජින ඔබගේ මායාකාරී කතාව සාදමින් සිටී...\n"
            "අයිස් මැජික් ක්‍රියා කරන අතරතුර මොහොතක් රැඳී සිටින්න.",
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text(
            f"✨ *Creating '{title}'* ✨\n\n"
            "The Frozen Queen is crafting your magical tale...\n"
            "Please wait a moment while the ice magic works.",
            parse_mode="Markdown"
        )
    
    await generate_and_send_story(update.message, context, title, language)
    return ConversationHandler.END

async def generate_and_send_story(message, context, title, language="english"):
    story = generate_story_from_title(title, language)
    image_url = get_story_image(title, language)
    
    if language.lower() == "sinhala":
        caption_prefix = f"📖 *{title}* 📖\n\n"
    else:
        caption_prefix = f"📖 *{title}* 📖\n\n"
    
    try:
        if image_url:
            image_response = requests.get(image_url, timeout=15)
            if image_response.status_code == 200:
                image_data = BytesIO(image_response.content)
                image_data.name = "story_image.jpg"
                await message.reply_photo(
                    photo=image_data,
                    caption=caption_prefix + story[:1000] + ("..." if len(story) > 1000 else ""),
                    parse_mode="Markdown"
                )
            else:
                with open(IMAGE_PATH, "rb") as photo:
                    await message.reply_photo(
                        photo=photo,
                        caption=caption_prefix + story[:1000] + ("..." if len(story) > 1000 else ""),
                        parse_mode="Markdown"
                    )
        else:
            with open(IMAGE_PATH, "rb") as photo:
                await message.reply_photo(
                    photo=photo,
                    caption=caption_prefix + story[:1000] + ("..." if len(story) > 1000 else ""),
                    parse_mode="Markdown"
                )
        
        if len(story) > 1000:
            remaining_text = story[1000:]
            chunks = [remaining_text[i:i+4000] for i in range(0, len(remaining_text), 4000)]
            for chunk in chunks:
                await message.reply_text(chunk)
                
    except Exception as e:
        await message.reply_text(
            caption_prefix + story[:4000],
            parse_mode="Markdown"
        )
        if len(story) > 4000:
            remaining_chunks = [story[i:i+4000] for i in range(4000, len(story), 4000)]
            for chunk in remaining_chunks:
                await message.reply_text(chunk)

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    language = context.user_data.get('language', 'english')
    if language.lower() == "sinhala":
        await update.message.reply_text(
            "කතා නිර්මාණය අවලංගු කරන ලදී. /customstory සමඟ නැවත ආරම්භ කළ හැකිය"
        )
    else:
        await update.message.reply_text(
            "Story creation cancelled. You can start again with /customstory"
        )
    return ConversationHandler.END

async def story_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command_text = update.message.text.lower()
    if "si" in command_text.split(" ")[0]:
        language = "sinhala"
        random_titles = RANDOM_SINHALA_TITLES
        wait_message = "හිම රැජින ඔබගේ මායාකාරී කතාව සාදමින් සිටී..."
    else:
        language = "english"
        random_titles = RANDOM_TITLES
        wait_message = "The Frozen Queen is crafting your magical tale..."
    
    if not context.args or len(context.args) == 0:
        title = random.choice(random_titles)
        if language == "sinhala":
            await update.message.reply_text(
                f"මාතෘකාවක් ලබා නොදුන් බැවින්, අහඹු මාතෘකාවක් සමඟ කතාවක් ජනනය කිරීම: *{title}*",
                parse_mode="Markdown"
            )
        else:
            await update.message.reply_text(
                f"No title provided, generating a random story with title: *{title}*",
                parse_mode="Markdown"
            )
    else:
        title = " ".join(context.args)
    
    message = await update.message.reply_text(
        f"✨ *{title}* ✨\n\n"
        f"{wait_message}",
        parse_mode="Markdown"
    )
    
    story = generate_story_from_title(title, language)
    image_url = get_story_image(title, language)
    
    if language.lower() == "sinhala":
        caption_prefix = f"📖 *{title}* 📖\n\n"
    else:
        caption_prefix = f"📖 *{title}* 📖\n\n"
    
    try:
        if image_url:
            image_response = requests.get(image_url, timeout=15)
            if image_response.status_code == 200:
                image_data = BytesIO(image_response.content)
                image_data.name = "story_image.jpg"
                await update.message.reply_photo(
                    photo=image_data,
                    caption=caption_prefix + story[:1000] + ("..." if len(story) > 1000 else ""),
                    parse_mode="Markdown"
                )
            else:
                with open(IMAGE_PATH, "rb") as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption=caption_prefix + story[:1000] + ("..." if len(story) > 1000 else ""),
                        parse_mode="Markdown"
                    )
        else:
            with open(IMAGE_PATH, "rb") as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=caption_prefix + story[:1000] + ("..." if len(story) > 1000 else ""),
                    parse_mode="Markdown"
                )
        
        if len(story) > 1000:
            remaining_text = story[1000:]
            chunks = [remaining_text[i:i+4000] for i in range(0, len(remaining_text), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
                
    except Exception as e:
        await update.message.reply_text(
            caption_prefix + story[:4000],
            parse_mode="Markdown"
        )
        if len(story) > 4000:
            remaining_chunks = [story[i:i+4000] for i in range(4000, len(story), 4000)]
            for chunk in remaining_chunks:
                await update.message.reply_text(chunk)
    
    await message.delete()

def register(application):
    """Register the plugin handlers with the application."""
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('customstory', customstory_start)],
        states={
            LANGUAGE_SELECTION: [CallbackQueryHandler(language_callback)],
            TITLE_INPUT: [
                CallbackQueryHandler(title_button_callback),
                MessageHandler(filters.TEXT & ~filters.COMMAND, receive_title)
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler('story', story_command))
    application.add_handler(CommandHandler('storysi', story_command))