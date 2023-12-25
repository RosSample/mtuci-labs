import telebot
from telebot import types
from datetime import datetime
import psycopg2

conn = psycopg2.connect(database="bot_db",
                        user="postgres",
                        password="18012004",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()

token = "6523145927:AAH6K47WRXlDHwhqa7ZK4D7VimBugsCzn5I"
bot = telebot.TeleBot(token)

days_list = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
week_number = datetime.today().isocalendar()[1] % 2

@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Расписание на текущую неделю", "Расписание на следующую неделю")
    keyboard.row("Понедельник", "Вторник", "Среда")
    keyboard.row("Четверг", "Пятница", "Суббота")
    bot.send_message(message.chat.id, "Привет, {name}, Данный бот был создан для того, чтобы показать расписание МТУСИ."
                                    "\nВы можете ознакомится с возможностями данного бота, используя команду /help.".format(name=message.from_user.first_name), reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def weekNumber(message):
    bot.send_message(message.chat.id, "Описание доступных команд:"
                                      "\n/help - Узнать команды бота"
                                      "\n/week - Узнать какая сейчас неделя (четная/нечетная)"
                                      "\n/date - Узнать какая сейчас дата"
                                      "\n/thefog - Он идет"
                                      "\n/mtuci - Официальный сайт вуза"
                                      "\n<Расписание на текущую неделю> - Узнать расписание на эту неделю"
                                      "\n<Расписание на следующую неделю> - Узнать расписание на следующую неделю"
                                      "\n<Понедельник - Суббота> - Узнать расписание на определенный день")


@bot.message_handler(commands=['date'])
def date(message):
    bot.send_message(message.chat.id,"Дата " + datetime.now().strftime("%y.%m.%d %H:%M:%S"))


@bot.message_handler(commands=['mtuci'])
def mtuci(message):
    bot.send_message(message.chat.id, "Официальный сайт вуза - https://mtuci.ru/")


@bot.message_handler(commands=['week'])
def weekNumber(message):
    if week_number == 1:
        bot.send_message(message.chat.id, "Сейчас нечетная неделя")
    else:
        bot.send_message(message.chat.id, "Сейчас четная неделя")


@bot.message_handler(commands=['thefog'])
def cat(message):
    bot.send_video(message.chat.id, 'https://media.tenor.com/gbQyDmWmNEAAAAAC/maxwell.gif')


@bot.message_handler(content_types='text')
def reply(message):
    if message.text.lower() in days_list:
        if week_number == 1:
            cursor.execute(f"SELECT * FROM timetable where day = '{message.text.lower()} 1' or day = '{message.text.lower()} 0' order by start_time")
        else:
            cursor.execute(f"SELECT * FROM timetable where day = '{message.text.lower()} 2' or day = '{message.text.lower()} 0' order by start_time")
        records = list(cursor.fetchall())
        text = f"{message.text}:\n"
        text += '____________________________________________________________\n'
        for i in records:
            text += f"Предмет: {i[2]}; Кабинет: {i[3]}; Время: {i[4]}"
        # Преподаватель: {}
        cursor.execute(f"SELECT subject FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
        subject = cursor.fetchone()[0]
        cursor.execute(f"SELECT full_name FROM teacher where subject = '{subject}'")
        text += f"Преподаватель: {teacher}\n"
        text += "____________________________________________________________"
        bot.send_message(message.chat.id, text)
    elif 'текущую' in message.text.lower():
        text = ""
        for i in days_list:
            if week_number == 1:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            records = list(cursor.fetchall())
            bot.send_message(message.chat.id, records)
            text += f'{i.title()}:\n'
            text += '____________________________________________________________\n'
            if not records:
                text += "Выходной\n"
            else:
                for j in records:
                    text += f"Предмет: {j[2]} Кабинет: {j[3]} Время: {j[4]}"
                cursor.execute(f"SELECT subject FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
                subject = cursor.fetchone()[0]
                cursor.execute(f"SELECT full_name FROM teacher where subject = '{subject}'")
                teacher = cursor.fetchone()[0]
                text += f"Преподаватель: {teacher}\n"
            text += "____________________________________________________________"
            text += '\n\n'
        bot.send_message(message.chat.id, text)
    elif 'следующую' in message.text.lower():
        text = ""
        for i in days_list:
            if week_number + 1 == 1:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            records = list(cursor.fetchall())
            text += f'{i.title()}:\n'
            text += '____________________________________________________________\n'
            if not records:
                text += "Выходной\n"
            else:
                for j in records:
                    text += f"Предмет: {j[2]} Кабинет: {j[3]} Время: {j[4]}"
                bot.send_message(message.chat.id, records)
                cursor.execute(f"SELECT full_name FROM teacher where subject = {records[1]}")
                teacher = cursor.fetchall()
                text += f"Преподаватель: {teacher}\n"
            text += "____________________________________________________________"
            text += '\n\n'
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.infinity_polling()