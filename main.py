from config import *
from logic import *
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Привет! Отправь мне текст, и я сгенерирую изображение.')

def handle_message(update: Update, context: CallbackContext) -> None:
    prompt = update.message.text
    image_path = generate_img_from_text(prompt, url)
    update.message.reply_photo(photo=open(image_path, 'rb'))

def main() -> None:
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()  