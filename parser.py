import requests
from bs4 import BeautifulSoup
from lxml import html
import sqlite3

class Parser():
    def __init__(self, xsrf, laravel, user_xsrf):
        pass

    def get_cookie():
        response = requests.get('https://smart-tables.ru/team/Skenderbeu')   # make new session and generate xsrf token

        xsrf = response.headers['Set-Cookie'].split(';')[0]                  # get xsrf token from header
        laravel = response.headers['Set-Cookie'].split(',')[2].split(';')[0] # get laravel token
        soup = BeautifulSoup(response.text, 'html.parser')                   # make soup obj
        user_xsrf = soup.find_all(('meta', 'csrf-token'))[3]['content']      # get user token

        return [xsrf, laravel, user_xsrf]

    def get_html(command, howmuch, cookie, token):
        HEADERS ={
            'POST': '/show/trends_basic HTTP/1.1',
            'Host': 'smart-tables.ru',
            'Connection': 'keep-alive',
            'Content-Length': '652',
            'sec-ch-ua': '"Chromium";v="88", "Google Chrome";v="88", ";Not A Brand";v="99"',
            'Accept': 'text/plain, */*; q=0.01',
            'X-CSRF-TOKEN': f'{token}',
            'X-Requested-With': 'XMLHttpRequest',
            'sec-ch-ua-mobile': '?0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': 'https://smart-tables.ru',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cookie': f'{cookie}'}
        PARAMS = {
            'team': 'home',
            'name': f'{command}',
            'seasons': 'Все',
            'competitions': 'Все',
            'where': 'Все',
            'howmuch': f'{howmuch}',
            'stat': 'Голы',
            'half': 'Первый тайм',
            'lng': 'ru',
            'client': 'free',
            'answer_id': 'teamAnswer',
            'source': 'Основной источник',
            'oddsrange': '0.5 1.6',
            'situation': 'all',
            'coach_option': 'all',
            'after_int_cup': 'all'}

        html = requests.post('https://smart-tables.ru/show/constructed', headers=HEADERS, params=PARAMS).text

        return html

    def add_data(data, league, team):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()

        item_lxml = html.fromstring(data)
        soup = BeautifulSoup(data, 'html.parser')  
        all_mathes = soup.find_all('tr', class_='match-row')    

        q_m = len(all_mathes)
        
        team1 = [item_lxml.xpath(f'//*[@id="table-home"]/tbody/tr[{x+1}]/td[4]/a/@href')[0][6:] for x in range(q_m)]   # team 1
        team2 = [item_lxml.xpath(f'//*[@id="table-home"]/tbody/tr[{x+1}]/td[7]/a/@href')[0][6:] for x in range(q_m)]   # team 2
        t1 = [item_lxml.xpath(f'//*[@id="table-home"]/tbody/tr[{x+1}]/td[5]/text()')[0] for x in range(q_m)]           # Счет первой команды
        t2 = [item_lxml.xpath(f'//*[@id="table-home"]/tbody/tr[{x+1}]/td[6]/text()')[0] for x in range(q_m)]           # Счет второй команды
        date = [item_lxml.xpath(f'//*[@id="table-home"]/tbody/tr[{x+1}]/td[3]/@title')[0] for x in range(q_m)]         # Дата проведения матча
        t = [item_lxml.xpath(f'//*[@id="table-home"]/tbody/tr[{x+1}]/td[8]/text()')[0] for x in range(q_m)]
        for x in range(q_m): 
            data = (league, team, team1[x], team2[x], t1[x], t2[x], date[x], t[x])   # Вся информация о матче
            c.execute("INSERT INTO ALL_MATCHES VALUES(?, ?, ?, ?, ?, ?, ?, ?);", data)      # Добавление данных в БД
            conn.commit()
        conn.close()
        
    def get_commands():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute(f'SELECT * FROM "COMMAND_IN_LEAGUES"')
        c = c.fetchmany(100000)
        conn.close()
        return c 
    
    def db_cleaner():
        conn = sqlite3.connect('database.db')
        c = conn.cursor() 
        c.execute('CREATE TABLE "COMMAND_IN_LEAGUES" (league TEXT, command TEXT);')
        c.execute('CREATE TABLE "BOT_USERS" (user_id INT);')
        c.execute('CREATE TABLE "ALL_MATCHES" (league TEXT, team TEXT, team1 TEXT, team2 TEXT, t1 INTEGER, t2 INTEGER, date TEXT, t INTEGER);')
        conn.commit()
        conn.close()


def r():
    xsrf, laravel, user_xsrf = Parser.get_cookie()
    for i in Parser.get_commands():
        print(i[1])
        html = Parser.get_html(i[1], 100, f'{xsrf};{laravel}', user_xsrf)
        print('parsed')
        Parser.add_data(html, i[0], i[1])
        print('writed')

        return 0
