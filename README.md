# Video Downloader Bot Setup Guide

![python-version](https://img.shields.io/badge/python-3.9_|_3.10_|_3.11_|_3.12_|_3.13-blue.svg)
[![license](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

This guide provides step-by-step instructions on how to install and run the Instagram bot on a Linux system.
- Backend code uses [yt-dlp](https://github.com/yt-dlp/yt-dlp) which is released under [The Unlicense](https://unlicense.org/). All rights for yt-dlp belong to their respective authors. 
---

## 1. Install Required Packages

You can install the required dependencies using one of the following methods:

### Installation:

1. Clone the repository:
   ```sh
   git clone https://github.com/ovchynnikov/load-bot-windows.git
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up FFmpeg:
   - Download FFmpeg from [FFmpeg Windows builds](https://www.ffmpeg.org/download.html#build-windows)
   - Extract the downloaded archive
   - Place ffmpeg.exe in your bot's folder

4. Install required Python packages:
   ```cmd
   pip install python-telegram-bot python-dotenv
   ```
   This installs:
   - python-telegram-bot: For Telegram bot functionality 
   - python-dotenv: For loading environment variables

5. Set up the bot token in the `.env` file and other variables.
  Edit `.env` file with your variables. Use `.env.example` as a reference.

## Usage

Follow these simple steps to set up and use the bot:

### 1. Create Your Telegram Bot
- Follow this guide to create your Telegram bot and obtain the bot token:  
  [How to Get Your Bot Token](https://www.freecodecamp.org/news/how-to-create-a-telegram-bot-using-python/).
  Make sure you put a token in `.env` file.

### 2. Start the bot
Run `start_bot.bat` to start the bot
or 
```cmd
python main.py
```

### 3. Health Check
- Verify the bot is running by sending a message with the trigger word:
```sh
bot_health
```
or
```sh
ботяра
```

If the bot is active, it will respond accordingly.

### 3. Once the bot is started:
  1. Send a URL from **YouTube Shorts**, **Instagram Reels**, or similar platforms to the bot.
  Example:
  ```
  https://youtube.com/shorts/kaTxVLGd6IE?si=YaUM3gYjr1kcXqTm
  ```
  2. Wait for the bot to process the URL and respond.

### Supported platforms by default:
   ```
   instagram reels
   facebook reels
   tiktok
   reddit
   x.com
   youtube shorts
   ```

### Additionally, the bot can download videos from other sources (for example YouTube). Usually, videos shorter than 10 minutes work fine. Telegram limitation is 50 MB for a video.
Bot will try to compress the video to < 50 MB.

- To download the full video from YouTube add two asterisks before the url address.
Example:
```
  **https://www.youtube.com/watch?v=rxdu3whDVSM
```
or with a space
```
  ** https://www.youtube.com/watch?v=rxdu3whDVSM
``` 

- Full list of supported sites here: [yt-dlp Supported Sites](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md)
---
### The bot can use 'Safelist' to restrict access for users or groups.
Ensure these variables are set in your `.env` file, without them or with the chat ID and username.
You can get your `chat_id` or `username` by setting `LIMIT_BOT_ACCESS=True` first. Then, send a link, and the bot will answer you with the chat ID and username.
- Allowed Group Chat priority is highest. All users in the Group Chat can use the bot even if they have no access to the bot in private chat.
- When `LIMIT_BOT_ACCESS=True` to use the bot in private messages add the username to the `ALLOWED_USERNAMES` variable.
- If you want a bot in your Group Chat with restrictions, leave `ALLOWED_CHAT_IDS` empty and define the `ALLOWED_USERNAMES` variable list.
```ini
LIMIT_BOT_ACCESS=False  # If True, the bot will only work for users in ALLOWED_USERNAMES or ALLOWED_CHAT_IDS
ALLOWED_USERNAMES= # a list of allowed usernames as strings separated by commas. Example: ALLOWED_USERNAMES=username1,username2,username3
ALLOWED_CHAT_IDS= # a list of allowed chat IDs as strings separated by commas. Example: ALLOWED_CHAT_IDS=-12349,12345,123456
```
---
