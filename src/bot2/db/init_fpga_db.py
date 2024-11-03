import sqlite3 as s3

'''
Модуль инициализации БД. Имя баз данных задается setup.py
'''

connection = s3.connect('fpga_news_boot.db')
cursor = connection.cursor()

'''
Таблица User_Step. Сохранение статуса сообщения.
id - номер записи
u_name - уникальный ник юзера
u_info - словарь состояния
'''

cursor.execute('''
CREATE TABLE IF NOT EXISTS User_Step(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	u_id TEXT NOT NULL,
	u_info TEXT NOT NULL
	)
	''')
connection.commit()

'''
Таблица User_Msg. Сохранение статуса сообщения.
id - номер записи
u_name - уникальный ник юзера
msg_state - завершено?
msg_data - дата и время события
'''

cursor.execute('''
CREATE TABLE IF NOT EXISTS User_Msg(
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	u_id TEXT NOT NULL,
	msg_data TEXT NOT NULL
	)
	''')
connection.commit()

'''

cursor.execute(
CREATE TABLE IF NOT EXISTS User_Log(
	id INTEGER PRIMARY KEY,
	log_msg TEXT NOT NULL
	)
	)
connection.commit()
connection.close()
'''
