from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests


async def getimage(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    url = context.args[0]
    response = requests.get(url)
    with open('image.jpg', 'wb') as f:
        f.write(response.content)

token = '7166179712:AAHxerkHQIk8MPe35ik8AmvCeU4zXGd9rRI'
app = ApplicationBuilder().token(token).build()

app.add_handler(CommandHandler("getimage", getimage, has_args=True))

app.run_polling()

