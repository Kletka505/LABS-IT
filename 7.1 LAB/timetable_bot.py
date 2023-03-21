from telebot import TeleBot, types
import psycopg2
import requests
from datetime import datetime

TOKEN = '6215323847:AAFX1grBvFG-z8oVR9AQgKZgnaMIWxDBpaI'
bot = TeleBot(TOKEN)
conn = psycopg2.connect(database='postgres',
                        user='postgres',
                        password='3478',
                        host='localhost',
                        port='5432')

cursor = conn.cursor()
week_number = datetime.today().isocalendar()[1]
weeks = ['Чётная', 'Нечётная']
week = weeks[week_number % 2]
days = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота']

def create_table(data, day):
    table = {
        '9:30 - 11:05': '<Нет занятия>',
        '11:20 - 12:55': '<Нет занятия>',
        '13:10 - 14:45': '<Нет занятия>',
        '15:25 - 17:00': '<Нет занятия>',
        '17:15 - 18:50': '<Нет занятия>'
    }
    for i in data:
        cursor.execute("SELECT full_name FROM teachers WHERE subject=%s", (i[0],))
        teacher_name = list(cursor.fetchall())[0][0]
        table[i[4]] = f"{i[0]} \n {teacher_name} | {i[3]}"
    table_s = f'{day} \n ————————— \n' \
              f'1. 9:30 - 11:05 \n {table["9:30 - 11:05"]} \n ————————— \n' \
              f'2. 11:20 - 12:55 \n {table["11:20 - 12:55"]} \n ————————— \n' \
              f'3. 13:10 - 14:45 \n {table["13:10 - 14:45"]} \n ————————— \n' \
              f'4. 15:25 - 17:00 \n {table["15:25 - 17:00"]} \n ————————— \n' \
              f'5. 17:15 - 18:50 \n {table["17:15 - 18:50"]}'
    return table_s


@bot.message_handler(commands=['start'])
def start_message(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row("/monday", '/tuesday', '/wednesday')
    keyboard.row("/thursday", '/friday', '/saturday')
    keyboard.row("/this_week", '/next_week', '/week')
    keyboard.row("/mtuci", '/help')
    bot.send_message(message.chat.id,
                     "Приветствую! Хотите узнать своё расписание?",
                     reply_markup=keyboard)


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday'])
def timetable_day(message):
    day= ''
    match message.text:
        case '/monday':
            cursor.execute("SELECT * FROM timetable WHERE day=%s AND week=%s", (days[0], week))
            day = days[0]
        case '/tuesday':
            cursor.execute("SELECT * FROM timetable WHERE day=%s AND week=%s", (days[1], week))
            day = days[1]
        case '/wednesday':
            cursor.execute("SELECT * FROM timetable WHERE day=%s AND week=%s", (days[2], week))
            day = days[2]
        case '/thursday':
            cursor.execute("SELECT * FROM timetable WHERE day=%s AND week=%s", (days[3], week))
            day = days[3]
        case '/friday':
            cursor.execute("SELECT * FROM timetable WHERE day=%s AND week=%s", (days[4], week))
            day = days[4]
        case '/saturday':
            cursor.execute("SELECT * FROM timetable WHERE day=%s AND week=%s", (days[5], week))
            day = days[5]
    data = list(cursor.fetchall())
    bot.send_message(message.chat.id, create_table(data, day))


@bot.message_handler(commands=['this_week', 'next_week'])
def timetable_week(message):
    table = ''
    w = week
    if message.text == '/next_week':
        if week_number == 0:
            w = 'Нечётная'
        else:
            w = 'Чётная'

    for i in days:
        cursor.execute("SELECT * FROM timetable WHERE day=%s AND week=%s", (i, w))
        data = list(cursor.fetchall())
        table += create_table(data, i) + "\n\n"

    bot.send_message(message.chat.id, table)


@bot.message_handler(commands=['week'])
def week_now(message):
    bot.send_message(message.chat.id, f"Сейчас идёт {week.lower()} неделя")


@bot.message_handler(commands=['help'])
def week_now(message):
    bot.send_message(message.chat.id,
                     "Вам доступны следующие команды: \n\n"
                     "/monday - расписание занятий в понедельник \n\n"
                     "/tuesday - расписание занятий во вторник \n\n"
                     "/wednesday - расписание занятий в среду \n\n"
                     "/thursday - расписание занятий в четверг \n\n"
                     "/friday - расписание занятий в пятницу \n\n"
                     "/saturday - расписание занятий в субботу \n\n"
                     "/this_week - расписание занятий на текущую неделю \n\n"
                     "/next_week - расписание занятий на следующую неделю \n\n"
                     "/week - текущая неделя (чётная/нечётная) \n\n"
                     "/mtuci - ссылка на официальный сайт МТУСИ \n\n"
                     "/help - список доступных команд \n\n")


@bot.message_handler(commands=['mtuci'])
def mtuci_link(message):
    bot.send_message(message.chat.id, 'https://mtuci.ru/')


@bot.message_handler(content_types=['text', 'document', 'sticker', 'audio'])
def bot_syntax_error(message):
    bot.send_message(message.chat.id, 'Извините, я Вас не понял')



bot.infinity_polling()
