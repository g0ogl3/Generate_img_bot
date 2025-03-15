import os #для удаления изображения после отправки
from config import * #импорт переменных из файла config.py
from logic import * #импорт функций из файла logic.py
import telebot #импорт библиотеки для работы с Telegram

bot = telebot.TeleBot(token) #создание бота

@bot.message_handler(commands=['start']) #обработка команды /start
def start(message): #функция для обработки команды /start
    bot.send_message( #отправка сообщения
        message.chat.id, #отправка сообщения пользователю
        'Привет! Отправь мне текст, и я сгенерирую изображение. Используй /help для получения дополнительной информации.' #текст сообщения
    ) #отправка сообщения

@bot.message_handler(commands=['help']) #обработка команды /help
def help_command(message): #функция для обработки команды /help
    bot.send_message( #отправка сообщения
        message.chat.id, #отправка сообщения пользователю
        'Этот бот генерирует изображения по вашему текстовому запросу. Просто отправьте текст, и я создам картинку! ' #текст сообщения
        'Пожалуйста, не отправляйте слишком длинные запросы, так как это может занять много времени.' #текст сообщения
    ) #отправка сообщения

@bot.message_handler(func=lambda message: True) #обработка всех сообщений
def handle_message(message): #функция для обработки всех сообщений
    prompt = message.text #получение текста сообщения

    status_message = bot.send_message(message.chat.id, 'Генерирую картинку...') #отправляю сообщение о начале создания изображения
    
    bot.send_chat_action(message.chat.id, action='upload_photo') #делаю чтобы показывало что бот "печатает..."
    
    try: #обработка ошибок
        image_path = generate_img_from_text(prompt, url) #создание изображения
        
        with open(image_path, 'rb') as photo: #открываю изображение
            bot.send_photo(message.chat.id, photo) #отправляю изображение
        

        if os.path.exists(image_path): #удаление изображения после отправки
            os.remove(image_path) #удаление изображения
    finally: #выполнение кода после try
        bot.delete_message(message.chat.id, status_message.message_id) #удаляю сообщение о генерации изображения

if __name__ == '__main__': #проверка на то, что файл был запущен напрямую
    bot.polling(none_stop=True) #запуск бота
