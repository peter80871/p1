import requests
import sqlite3
import parser
import line
import schedule, time
import telebot
from multiprocessing.context import Process
 
def nnn():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    user_id = 410250411
    c.execute(f"INSERT INTO BOT_USERS (user_id) VALUES ({user_id});")
    conn.commit()
    conn.close()

bot = telebot.TeleBot('1645528528:AAH3sDo1JUt2uLcLpY8RrB6JrVaXIT9N-LQ')

def get_users():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM BOT_USERS;')
    users = c.fetchall()
    conn.close()
    return users

def append_data(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    users = get_users()
    if len(users) == 0:
        nnn()

    status = 0
    for i in range(len(users)):
        if user_id == int(users[i][-1]):
            status = 1
    if status == 0:
        #c.execute(f"INSERT INTO BOT_USERS (user_id) VALUES ({user_id});")
        conn.commit() 
        conn.close()
        print(status)
        return 1
    else:
        print(status)
        conn.close()
        return 0


def send_message1():
    matches = line.get_message()
    for match in matches:
        #country, league, team1, team2, time_start_match, kf = msg
        country, league, team1 = match

        """msg = f'''Сигнал #1 🚨 
            {country} {league} 
            {team1} - {team2} 
            Начало матча {time_start_match}
            Ставка - ИТ1Б(0,5) в первом тайме 
            Коэффициент - {kf}'''"""

        msg = f'''Сигнал #1 🚨 
            {country} {league} 
            {team1}
            Начало матча time
            Ставка - ИТ1Б(0,5) в первом тайме'''

        for user_id in get_users():
            print(user_id[0])
            bot.send_message(user_id[0], msg)


schedule.every().day.at("08:54").do(send_message1)


@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    print(user_id)
    if append_data(user_id):
        bot.send_message(message.chat.id, 'Вы подписались на рассылку')
    else:
        bot.send_message(message.chat.id, 'Вы уже есть в базе рассылки') 

class ScheduleMessage():
    def try_send_schedule():
        while True:
            schedule.run_pending()
            time.sleep(1)
 
    def start_process():
        p1 = Process(target=ScheduleMessage.try_send_schedule, args=())
        p1.start()
 
 
if __name__ == '__main__':
    ScheduleMessage.start_process()
    try:
        bot.polling(none_stop=True)
    except:
        pass