# -*- coding: utf-8 -*- 
import telebot
from telebot import types,apihelper
import time
import datetime
from connect import connect


while True:
	print('check_api')
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_users where api = "1"')
	infad = q.fetchall()
	print(infad)
	for infa in infad:
		if infa[9] != 'Навсегда':
			now = datetime.datetime.now()
			if str(infa[9]) == str(now)[:10]:
				q.execute(f"update ugc_users set api = '0' where userid = '{infa[1]}'")
				connection.commit()
				q.execute(f"update ugc_users set api_time = '0' where userid = '{infa[1]}'")
				connection.commit()
				bot.send_message(infa[1],'<b>❗️ Время аренды API закончилось</b>', parse_mode='HTML')
	time.sleep(120)