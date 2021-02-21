import sqlite3

def db_create():
    conn = sqlite3.connect('database.db')
    c = conn.cursor() 
    c.execute('CREATE TABLE "COMMAND_IN_LEAGUES" (league TEXT, command TEXT);')
    c.execute('CREATE TABLE "ALL_MATCHES" (league TEXT, team TEXT, team1 TEXT, team2 TEXT, t1 INTEGER, t2 INTEGER, date TEXT, t INTEGER);')
    c.execute('CREATE TABLE "BOT_USERS" (user_id INT);')
    conn.commit()
    conn.close()

def db_drop():
    conn = sqlite3.connect('database.db')
    c = conn.cursor() 
    c.execute('DROP TABLE ALL_MATCHES')
    c.execute('DROP TABLE COMMANDS_IN_LEAGUES')
    c.execute('DROP TABLE BOT_USERS')
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