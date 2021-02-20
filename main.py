import requests
from bs4 import BeautifulSoup
from lxml import html
import sqlite3
import parser
import schedule, time
import telebot

bot = telebot.TeleBot('1645528528:AAH3sDo1JUt2uLcLpY8RrB6JrVaXIT9N-LQ')

def append_data(user_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM BOT_USERS;')
    second_result = c.fetchmany(1000)
    
    for i in second_result:
        if user_id != i[0]:
            c.execute(f"INSERT INTO BOT_USERS (user_id) VALUES ({user_id});")
            conn.commit() 
            conn.close()
            return 1
        else:
            return 0

@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.from_user.id
    print(user_id)
    if append_data(user_id):
        bot.send_message(message.chat.id, 'Вы подписались на рассылку')
    else:
        bot.send_message(message.chat.id, 'Вы уже есть в базе рассылки')
     


bot.polling()
