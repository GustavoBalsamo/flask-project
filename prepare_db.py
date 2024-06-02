import mysql.connector
from mysql.connector import errorcode
from flask_bcrypt import generate_password_hash

print("Connecting...")
try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='balsamo123'
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print('Something is wrong with the username or password')
    else:
        print(err)

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")

cursor.execute("CREATE DATABASE `jogoteca`;")

cursor.execute("USE `jogoteca`;")

# creating tables
TABLES = {}
TABLES['Games'] = ('''
    CREATE TABLE `games` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `name` varchar(50) NOT NULL,
    `category` varchar(40) NOT NULL,
    `console` varchar(20) NOT NULL,
    PRIMARY KEY (`id`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Users'] = ('''
    CREATE TABLE `users` (
    `name` varchar(20) NOT NULL,
    `nickname` varchar(8) NOT NULL,
    `password` varchar(100) NOT NULL,
    PRIMARY KEY (`nickname`)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for table_name in TABLES:
    table_sql = TABLES[table_name]
    try:
        print('Creating table {}:'.format(table_name), end=' ')
        cursor.execute(table_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Already exists')
        else:
            print(err.msg)
    else:
        print('OK')

# inserting users
user_sql = 'INSERT INTO users (name, nickname, password) VALUES (%s, %s, %s)'
users = [
    ("Bruno Divino", "BD", generate_password_hash("alohomora").decode('utf-8')),
    ("Camila Ferreira", "Mila", generate_password_hash("paozinho").decode('utf-8')),
    ("Guilherme Louro", "Cake", generate_password_hash("python_is_life").decode('utf-8'))
]
cursor.executemany(user_sql, users)

cursor.execute('SELECT * FROM jogoteca.users')
print(' -------------  Users:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserting games
games_sql = 'INSERT INTO games (name, category, console) VALUES (%s, %s, %s)'
games = [
    ('Tetris', 'Puzzle', 'Atari'),
    ('God of War', 'Hack n Slash', 'PS2'),
    ('Mortal Kombat', 'Fighting', 'PS2'),
    ('Valorant', 'FPS', 'PC'),
    ('Crash Bandicoot', 'Hack n Slash', 'PS2'),
    ('Need for Speed', 'Racing', 'PS2'),
]
cursor.executemany(games_sql, games)

cursor.execute('SELECT * FROM jogoteca.games')
print(' -------------  Games:  -------------')
for game in cursor.fetchall():
    print(game[1])

# committing so that changes take effect
conn.commit()

cursor.close()
conn.close()
