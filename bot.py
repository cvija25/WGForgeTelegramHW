from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import validators
from io import BytesIO
from yt_dlp import YoutubeDL
import os

async def getimage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a URL.")
        return
    
    url = context.args[0]
    if not validators.url(url):
        await update.message.reply_text("The provided string is not a valid URL.")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        image_stream = BytesIO(response.content)
        image_stream.name = "image.jpg"
        await update.message.reply_text("Here is your image")
        await update.message.reply_photo(photo=image_stream)
    except requests.RequestException as e:
        await update.message.reply_text(f"Failed to download the image: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

async def getvideo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.args:
        await update.message.reply_text("Please provide a URL.")
        return
    
    url = context.args[0]
    if not validators.url(url):
        await update.message.reply_text("The provided string is not a valid URL.")
        return
    
    await update.message.reply_text("Downloading...")
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }],
        'outtmpl': 'video',
        'noplaylist': True
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    await update.message.reply_video(video=open('video.mp4', 'rb'))
                    break
                except Exception:
                    if attempt < max_attempts - 1:
                        await update.message.reply_text("Timeout occurred, retrying...")
                    else:
                        await update.message.reply_text("Failed to upload video after several attempts. Adjust timeout or try smaller video.")
            os.remove('video.mp4')
    except Exception:
        await update.message.reply_text("Failed to download video.")



token = '7166179712:AAHxerkHQIk8MPe35ik8AmvCeU4zXGd9rRI'
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("getimage", getimage, has_args=True))
app.add_handler(CommandHandler("getvideo", getvideo, has_args=True))

app.run_polling()