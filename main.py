# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring

import os
import subprocess
import tempfile
import random
import json
from dotenv import load_dotenv
from telegram import Update
from telegram.error import TimedOut
from telegram.ext import Application, MessageHandler, filters, ContextTypes

load_dotenv()
show_errors_in_console = os.getenv("DEBUG")


def print_logs(text):
    if show_errors_in_console:
        print(text)

def load_responses():
    with open("responses.json", "r", encoding="utf-8") as file:
        data = json.load(file)
    return data["responses"]

responses = load_responses()


def cleanup_file(video_path):
    print_logs(f"Video to delete {video_path}")
    try:
        os.remove(video_path)
        os.rmdir(os.path.dirname(video_path))
        print_logs(f"Video deleted {video_path}")
    except Exception as cleanup_error:
        print_logs(f"Error deleting file: {cleanup_error}")


def download_video(url):
    temp_dir = tempfile.mkdtemp()
    command = [
        "yt-dlp.exe",
        "-S", "vcodec:h264,fps,res,acodec:m4a",
        url,
        "-o", os.path.join(temp_dir, "%(title)s.%(ext)s")
    ]

    try:
        subprocess.run(command, check=True, timeout=120)

        for filename in os.listdir(temp_dir):
            if filename.endswith(".mp4"):
                return os.path.join(temp_dir, filename)

        return None
    except subprocess.CalledProcessError as e:
        print_logs(f"Error downloading video: {e}")
        return None
    except subprocess.TimeoutExpired as e:
        print_logs(f"Download process timed out: {e}")
        return None
    except Exception as e:
        print_logs(f"An unexpected error occurred: {e}")
        return None


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE): # pylint: disable=unused-argument
    if not update.message or not update.message.text:
        return
    url = update.message.text

    if "ботяра" in url.lower():
        response = random.choice(responses)
        await update.message.reply_text(response)

    elif "instagram.com/stories/" in url:
        await update.message.reply_text("Сторіз не можу скачати. Треба логін")

    elif "instagram.com/reel/" in url or "tiktok.com/" in url:
        wait_message = await update.message.reply_text("Почекай пару сек...")

        video_path = download_video(url)

        if video_path and os.path.exists(video_path):
            with open(video_path, 'rb') as video_file:
                try:
                    await update.message.reply_video(video_file)
                    await wait_message.delete()
                except TimedOut as e:
                    print_logs(f"Telegram timeout while sending video. {e}")
                except Exception as e:
                    await update.message.reply_text(f"О Курва! Якась помилка. Спробуй ще. {e}")
                    return None
            cleanup_file(video_path)
        else:
            await wait_message.delete()
            await update.message.reply_text("О Курва! Якась помилка. Спробуй ще.")
    else:
        pass


def main():
    bot_token = os.getenv("bot_token")
    application = Application.builder().token(bot_token).build()
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot started. Ctrl+c to stop")
    application.run_polling()

if __name__ == "__main__":
    main()
