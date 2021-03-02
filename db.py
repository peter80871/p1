import sqlite3

def db_create():
    conn = sqlite3.connect('database.db')
    c = conn.cursor() 
    c.execute('CREATE TABLE "TEAM_IN_LEAGUES" (country TEXT, league TEXT, team TEXT);')
    c.execute('CREATE TABLE "ALL_MATCHES" (league TEXT, series TEXT, team TEXT, team1 TEXT, team2 TEXT, t1 INTEGER, t2 INTEGER, date TEXT, t INTEGER);')
    c.execute('CREATE TABLE "UPCOMING_MATCHES" (league TEXT, team1 TEXT, team2 TEXT,  date TEXT);')
    c.execute('CREATE TABLE "BOT_USERS" (user_id INT);')
    conn.commit()
    conn.close()

def db_drop():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    #c.execute('DROP TABLE UPCOMING_MATCHES;')
    c.execute('DROP TABLE ALL_MATCHES;')
    #c.execute('DROP TABLE BOT_USERS;')

    #c.execute('CREATE TABLE "BOT_USERS" (user_id INT);')
    c.execute('CREATE TABLE "ALL_MATCHES" (league TEXT, series TEXT, team TEXT, team1 TEXT, team2 TEXT, t1 INTEGER, t2 INTEGER, date TEXT, t INTEGER);')
    #c.execute('CREATE TABLE "UPCOMING_MATCHES" (league TEXT, team1 TEXT, team2 TEXT,  date TEXT);')
    conn.commit()
    conn.close()

def show_tables():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("""select * from sqlite_master
            where type = 'table'""")
    tables = c.fetchall()
    conn.close()

    return(tables)

def show_data_in_table(table):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute(f'SELECT * FROM "{table}"')
    
    c = c.fetchall()
    conn.close()

    return c

#for i in show_data_in_table('UPCOMING_MATCHES'):
#    if i[2] == 'Girona':
#        print(i)