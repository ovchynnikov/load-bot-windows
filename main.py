# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import os
import random
import json
from functools import lru_cache
from dotenv import load_dotenv
import telegram
from telegram import Update
from telegram.error import TimedOut
from telegram.ext import Application, MessageHandler, filters, ContextTypes
from telegram.constants import MessageEntityType
from logger import print_logs
from video_utils import compress_video, download_video, cleanup_file

load_dotenv()

supported_sites = ["instagram.com/", "tiktok.com/", "reddit.com", "x.com", "**https:"]

@lru_cache(maxsize=1)
def load_responses():
    with open("responses.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["responses"]

responses = load_responses()


def spoiler_in_message(entities):
    if entities:
        for entity in entities:
            if entity.type == MessageEntityType.SPOILER:
                return True
    return False


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):  # pylint: disable=unused-argument
    if not update.message or not update.message.text:
        return

    url = update.message.text

    # Heartbeat word
    if "ботяра" in url.lower():
        response = random.choice(responses)
        await update.message.reply_text(response)
        return

    # Quick check before more expensive operations
    if not any(site in url for site in supported_sites):
        return

    if "instagram.com/stories/" in url:
        await update.message.reply_text("Сторіз не можу скачати. Треба логін")
        return

    url = url[2:] if url.startswith("**") else url  # Remove '**' if present

    # Download the video
    video_path = download_video(url)

    if not video_path or not os.path.exists(video_path):
        return

    # Compress video if it's larger than 50MB
    if os.path.getsize(video_path) / (1024 * 1024) > 50:
        compress_video(video_path)

    # Check if the message has a spoiler
    visibility_flag = spoiler_in_message(update.message.entities)

    # Send the video to the chat
    try:
        with open(video_path, 'rb') as video_file:
            await update.message.chat.send_video(
                video=video_file,
                has_spoiler=visibility_flag,
                disable_notification=True,
                write_timeout=8000,
                read_timeout=8000
            )
    except TimedOut as e:
        print_logs(f"Telegram timeout while sending video. {e}")
    except telegram.error.TelegramError:
        await update.message.reply_text(
            f"О kurwa! Compressed file size: "
            f"{os.path.getsize(video_path) / (1024 * 1024):.2f}MB. "
            f"Telegram API Max is 50MB"
        )

    # Clean up the video file after sending
    cleanup_file(video_path)

def main():
    bot_token = os.getenv("BOT_TOKEN")
    application = Application.builder().token(bot_token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot started. Ctrl+c to stop")
    application.run_polling()

if __name__ == "__main__":
    main()
