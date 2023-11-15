import telebot
from get_gpt import gpt_main


TOKEN = "6791742558:AAHX70MEtrOLhMiwiPABV2rgdJsvsSUbMqI"
bot = telebot.TeleBot(TOKEN)

user_data = {}


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_data[message.chat.id] = []
    bot.reply_to(message, '''Внимание! Скрипт проводит поиск и запись значений по первой строке (по заголовку)

Для ввода значений по умолчанию введите 1
Аккаунт для добавления в google sheets dc-electro-gpt-gs@helical-analyst-404413.iam.gserviceaccount.com

Значение которые принимает скрипт, вводятся по очереди, некоторые не обязательны к заполнению:
1. Ссылка на google sheets таблицу
2. Первая часть запроса для GPT (По умолчанию: "Напишите описание товара на 300 символов: ") 
3. Значение первой стройки у столбца с второй частью запроса для GPT (По умолчанию: "Название элемента")
4. Значение первой строки у столбца в который будет записываться результат (По умолчанию: "Подробное описание")''')


@bot.message_handler(commands=['clear'])
def handle_clear(message):
    user_data[message.chat.id] = []
    bot.reply_to(message, "Данные очищены. Для ввода новых значений введите команду /start")


@bot.message_handler(func=lambda message: True)
def main(message):
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = []
    if len(user_data[chat_id]) < 4:
        user_data[chat_id].append(message.text)
        if len(user_data[chat_id]) == 4:
            bot.reply_to(message, "Запускаю скрипт...")
            gpt_main(user_data[chat_id])
            bot.reply_to(message, "Скрипт завершил работу!")
        else:
            bot.reply_to(message, say_bot(len(user_data[chat_id])))
    else:
        bot.reply_to(message, f"Список значений уже сформирован, для очистки данных введите команду /clear")


def say_bot(len_data):
    switcher = {
        1: "Введите запрос для GPT",
        2: "Введите название заголовка столбца с значениями для второй части запроса",
        3: "Введите название заголовка столбца для вывода запроса",
    }

    return switcher[len_data]


# Запускаем бота
bot.polling(none_stop=True)

main()
