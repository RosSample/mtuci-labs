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

token = "6663291550:AAGbOE7-em8S5Kgrtze0pN_kLL6e_iBOWk8"
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
        records = cursor.fetchall()
        text = f"{message.text}:\n"
        text += '_____\n'
        if week_number == 1:
            cursor.execute(f"SELECT subject FROM timetable where day = '{message.text.lower()} 1' or day = '{message.text.lower()} 0' order by start_time")
        else:
            cursor.execute(f"SELECT subject FROM timetable where day = '{message.text.lower()} 2' or day = '{message.text.lower()} 0' order by start_time")
        subjects = cursor.fetchall()
        teachers = []
        for j in range(len(subjects)):
            print(type(subjects[j][0]), subjects[j][0])
            cursor.execute(f"SELECT full_name FROM teacher where subject = '{subjects[j][0]}'")
            try:
                teachers.append(cursor.fetchone()[0])
            except:
                teachers.append('?')
        print(teachers)
        k = 0
        if not records:
            text += "Выходной\n"
        else:
            for j in records:
                text += f"Предмет: {j[2]} Кабинет: {j[3]} Время: {j[4]} Преподаватель: {teachers[k]}\n"
                k += 1
        k = 0
        text += "_____"
        bot.send_message(message.chat.id, text)
    elif 'текущую' in message.text.lower():
        text = ""
        for i in days_list:
            if week_number == 1:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            records = cursor.fetchall()
            text += f'{i.title()}:\n'
            text += '_____\n'
            if week_number == 1:
                cursor.execute(f"SELECT subject FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT subject FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            subjects = cursor.fetchall()
            teachers = []
            for j in range(len(subjects)):
                print(type(subjects[j][0]), subjects[j][0])
                cursor.execute(f"SELECT full_name FROM teacher where subject = '{subjects[j][0]}'")
                try:
                    teachers.append(cursor.fetchone()[0])
                except:
                    teachers.append('?')
            print(teachers)
            if not records:
                text += "Выходной\n"
            else:
                k = 0
                for j in records:
                    text += f"Предмет: {j[2]} Кабинет: {j[3]} Время: {j[4]} Преподаватель: {teachers[k]}\n"
                    k += 1
            k = 0
            text += "_____"
            text += '\n\n'
        bot.send_message(message.chat.id, text)
    elif 'следующую' in message.text.lower():
        text = ""
        for i in days_list:
            if week_number + 1 == 1:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT * FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            records = cursor.fetchall()
            text += f'{i.title()}:\n'
            text += '_____\n'
            if week_number + 1 == 1:
                cursor.execute(f"SELECT subject FROM timetable where day = '{i} 1' or day = '{i} 0' order by start_time")
            else:
                cursor.execute(f"SELECT subject FROM timetable where day = '{i} 2' or day = '{i} 0' order by start_time")
            subjects = cursor.fetchall()
            teachers = []
            for j in range(len(subjects)):
                print(type(subjects[j][0]), subjects[j][0])
                cursor.execute(f"SELECT full_name FROM teacher where subject = '{subjects[j][0]}'")
                try:
                    teachers.append(cursor.fetchone()[0])
                except:
                    teachers.append('?')
            print(teachers)
            if not records:
                text += "Выходной\n"
            else:
                k = 0
                for j in records:
                    text += f"Предмет: {j[2]} Кабинет: {j[3]} Время: {j[4]} Преподаватель: {teachers[k]}\n"
                    k += 1
            k = 0
            text += "_____"
            text += '\n\n'
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.infinity_polling()