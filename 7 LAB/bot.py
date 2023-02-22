import random
from config import TOKEN
import requests
from telebot import TeleBot, types
from jpg import N_JPG, URLS_JPG
from facts import N_FACTS, FACTS


bot = TeleBot(TOKEN)
city = "Moscow"
appid = "4262adf3731b8021960720b0087658fc"
res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                   params={'q': city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
data = res.json()


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("Хочу", "Как дела?", "Расскажи о себе")
    keyboard.row("/meme", "/weather", "/facts")
    keyboard.row("/help")
    bot.send_message(message.chat.id,
                     "Привет! Хочешь узнать свежую информацию о МТУСИ?",
                     reply_markup=keyboard)


@bot.message_handler(commands=["help"])
def help_message(message):
    bot.send_message(message.chat.id,
                     "Я умею... \n\n"
                     "/meme - случайный мем \n\n"
                     "/weather - погода на сегодня в Москве \n\n"
                     "/facts - случайный интересный факт \n\n")


@bot.message_handler(commands=["weather"])
def help_message(message):
    bot.send_message(message.chat.id,
                     f"Город: {city} \n\n"
                     f"Погодные условия:{data['weather'][0]['description']} \n\n"
                     f"Температура: {data['main']['temp']} \n\n"
                     f"Минимальная температура: {data['main']['temp_min']} \n\n"
                     f"Максимальная температура: {data['main']['temp_max']} \n\n"
                     f"Скорость ветра: {data['wind']['speed']} \n\n"
                     f"Видимость {data['visibility']} \n\n")


@bot.message_handler(commands=["meme"])
def meme_message(message):
    bot.send_photo(message.chat.id, photo=URLS_JPG[random.randint(0, N_JPG)])


@bot.message_handler(commands=["facts"])
def fact_message(message):
    bot.send_message(message.chat.id, f"{FACTS[random.randint(0, N_FACTS)]}")


@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text.lower() == "хочу":
        bot.send_message(message.chat.id,
                         "Тогда тебе сюда - https://mtuci.ru/")
    if message.text.lower() == "как дела?":
        bot.send_message(message.chat.id,
                         "Да в целом пойдёт, давай лучше команду")
    if message.text.lower() == "расскажи о себе":
        bot.send_message(message.chat.id,
                         "Я - очередной бот, написанный на Python каким-то студентиком. \n"
                         "Вообщем... Ничего интересного.")


bot.infinity_polling()



