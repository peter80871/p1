import requests
from bs4 import BeautifulSoup
from lxml import html
import sqlite3
import parser
import db
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
     
@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text.lower() == 'create table' or message.text.lower() == 'создать таблицы':
        bot.send_message(message.chat.id, 'БД очищена')
    elif message.text.lower() == 'drop table' or message.text.lower() == 'удалить таблицы':
        bot.send_message(message.chat.id, 'БД создана')

    elif message.text.lower() == 'get r':
        r = parser.Parser.r()
        bot.send_message(message.chat.id, f'{r}')
    

bot.polling()
