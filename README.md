### 1. Installation of packages 
```
pip install -r requirements.txt
```
or install manually 
  ```
pip install python-telegram-bot python-dotenv yt-dlp ffmpeg
```
### 2. Set your telegram bot token as BOT_TOKEN in .env file
```
BOT_TOKEN = "your_telegram_bot_token_here"
```
### 2.1 If you have sound problems with videos from x.com and reddit then download ffmpeg and place ffmpeg.exe in the same folder as yt-dlp.exe
```
https://www.ffmpeg.org/download.html#build-windows
```
### 2.1.2 Set your FFPROBE_PATH in .env file specifying the ffmpeg location
```
FFPROBE_PATH = "C:\\Users\\User\\Desktop\\ffmpeg\\bin\\ffprobe.exe"
```
### 3. Start 
```
double-click on start_bot.bat
```
or
```
python main.py
```
