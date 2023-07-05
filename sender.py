import telebot
import time
import json
from telebot import types,apihelper
import datetime
import sqlite3 
import config
import mysql.connector
import requests
import threading
import random
import asyncio
from connect import connect

bot = telebot.TeleBot(config.token)


def add_send_message_db(senddate):
	connection,q = connect()
	q.execute(f"update ugc_temp_sending set send = send + '1' where date = '{senddate}'")
	connection.commit()
	return 'yes'

def sendmessage(users, aa, senddate):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_temp_sending where date = "{senddate}"')
	row = q.fetchone()
	spisok_use_users = []
	info = types.InlineKeyboardMarkup()
	info.add(types.InlineKeyboardButton(text='Купить рекламу',url=f'https://t.me/FilyaAdmin'))
	# info = types.InlineKeyboardMarkup()
	# info.add(types.InlineKeyboardButton(text="Купить рекламу",url=f'https://t.me/filyaadv'))
	colvo_dont_send_message_users = 0
	for i in users:
		spisok_use_users.append(i)
		if len(spisok_use_users) == 29:
			spisok_use_users.clear()
			time.sleep(1.5)
		add_send_message_db(senddate)
		if aa == 0:
			try:
				bot.send_message(i, str(row[1]), parse_mode='HTML',reply_markup=info)
				#add_send_message_db(senddate)
				print(i)
			except Exception as e:
				colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
		elif aa == 1:
			try:
				bot.send_message(i, str(row[1]),parse_mode='HTML',reply_markup=info)
				#add_send_message_db(senddate)
				print(i)
			except Exception as e:
				colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
		elif aa == 2:
			try:
				bot.send_message(i, str(row[1]),parse_mode='HTML',reply_markup=info)
				#add_send_message_db(senddate)
				print(i)
			except Exception as e:
				colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
		else:
			try:
				bot.send_photo(i, photo=str(row[2]), caption=str(row[1]),parse_mode='HTML',reply_markup=info)
				#add_send_message_db(senddate)
				print(i)
			except Exception as e:
				colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
	for b in config.admin_list:
		try:
			bott = telebot.TeleBot(config.token).send_message(b,f'<b>Рассылка завершена ✅\n\nВсего пользователей: <code>{len(users)}</code>\nНе пришло: {colvo_dont_send_message_users}</b>',parse_mode='HTML')
		except:
			pass

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

while True:
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_temp_sending')
	row = q.fetchall()
	now = datetime.datetime.now()
	today = str(now)
	for i in row:
		if str(today[:16]) == str(i[4]):
			colvo_dont_send_message_users = 0
			time.sleep(0.2)
			q.execute(f'SELECT userid FROM ugc_users')
			users = q.fetchall()
			user_list_nice = []
			for b in users:
				user_list_nice.append(b[0])
			aa = 0
			info = types.InlineKeyboardMarkup()
			info.add(types.InlineKeyboardButton(text='Купить рекламу',url=f'https://t.me/filyaadv'))
			if i[2].lower() != 'Нет'.lower():
				aa += 3
			if i[3] == '/':
				aa += 2
			spisok_use_users = []
			asdsad = list(split(user_list_nice, 3))
			# for user in users:
			am = threading.Thread(target=sendmessage, args=(asdsad[0], aa, i[4])).start()
			am = threading.Thread(target=sendmessage, args=(asdsad[1], aa, i[4])).start()
			am = threading.Thread(target=sendmessage, args=(asdsad[2], aa, i[4])).start()
			time.sleep(60)
				# print(user[0])
				# spisok_use_users.append(user[0])
				# if len(spisok_use_users) == 29:
				# 	spisok_use_users.clear()
				# 	time.sleep(2)
				# if aa == 0:
				# 	try:
				# 		# bot.send_message(user[0], str(i[1]), parse_mode='HTML',reply_markup=info)
				# 	except Exception as e:
				# 		colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
				# elif aa == 1:
				# 	try:
				# 		# bot.send_message(user[0], str(i[1]),parse_mode='HTML',reply_markup=info)
				# 	except Exception as e:
				# 		colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
				# elif aa == 2:
				# 	try:
				# 		# bot.send_message(user[0], str(i[1]),parse_mode='HTML',reply_markup=info)
				# 	except Exception as e:
				# 		colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
				# else:
				# 	try:
				# 		# bot.send_photo(user[0], photo=str(i[2]), caption=str(i[1]),parse_mode='HTML',reply_markup=info)
				# 	except Exception as e:
				# 		colvo_dont_send_message_users = colvo_dont_send_message_users + 1;
		
			# q.execute(f"DELETE FROM ugc_temp_sending WHERE date = '{i[4]}'")
			# connection.commit()
			# q.execute(f'SELECT COUNT(userid) FROM ugc_users')
			# users_count = q.fetchone()[0]
			# for b in config.admin_list:
			# 	try:
			# 		bott = telebot.TeleBot(config.token).send_message(b,f'<b>Рассылка завершена ✅\n\nВсего пользователей: <code>{users_count}</code>\nНе пришло: {colvo_dont_send_message_users}</b>',parse_mode='HTML')
			# 	except:
			# 		pass
	time.sleep(10)