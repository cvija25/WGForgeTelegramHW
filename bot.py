from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests
import validators
from io import BytesIO

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
        await update.message.reply_text("here is your image")
        await update.message.reply_photo(photo=image_stream)
    except requests.RequestException as e:
        await update.message.reply_text(f"Failed to download the image: {str(e)}")
    except Exception as e:
        await update.message.reply_text(f"An error occurred: {str(e)}")

token = '7166179712:AAHxerkHQIk8MPe35ik8AmvCeU4zXGd9rRI'
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("getimage", getimage, has_args=True))

app.run_polling()

