import telebot
from telebot import types
import sqlite3
import requests
import config
import json
import random
import mysql.connector
from connect import connect

def check_private(userid):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_users where userid = "{userid}"')
	row = q.fetchall()



def main_menu(userid):
	main_menu = types.InlineKeyboardMarkup()
	main_menu.add(types.InlineKeyboardButton(text='💌 Отправить смс',callback_data=f'send:qq'),types.InlineKeyboardButton(text='⚡️ Отправить ВК',callback_data=f'send:vk'))
	# main_menu.add(types.InlineKeyboardButton(text='✍️ Изменить отправителя',callback_data=f'edit_name'))
	# main_menu.add(types.InlineKeyboardButton(text='📞 Отправить звонок',url=f't.me/FilyaCallsBot?start=sender'))
	main_menu.add(types.InlineKeyboardButton(text='➕ Пополнить баланс',callback_data=f'add_balance:svoi'),types.InlineKeyboardButton(text='🔗 Сократитель',callback_data=f'сократитель'))
	#main_menu.add(types.InlineKeyboardButton(text='📈 Статистика',callback_data=f'статистика'))
	main_menu.add(types.InlineKeyboardButton(text='ℹ️ Информация',callback_data=f'информация'))
	if int(userid) in config.admin_list:
		main_menu.add(types.InlineKeyboardButton(text='😎 Админ',callback_data=f'admin_menu'))
	return main_menu


def short_menu(userid):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_short_link where userid = "{userid}"')
	row = q.fetchall()
	services = types.InlineKeyboardMarkup(row_width=3)
	btns = []
	for i in range(len(row)):
		try:
			btns.append(types.InlineKeyboardButton(text=f'{row[i][4]} | {row[i][5]}',callback_data=f'shurl:{row[i][4]}'))		
		except:
			continue
	while btns != []:
		try:
			services.add(
				btns[0],
				btns[1],
				btns[2]
				)
			del btns[2],btns[1], btns[0]
		except:
			services.add(btns[0])
			del btns[0]
	if len(row) != 0:
		services.add(types.InlineKeyboardButton(text='🔄 Обновить',callback_data='сократитель_обновить'))
	services.add(types.InlineKeyboardButton(text='🔗 Сократить ссылку',callback_data='сократить_ссылку'))
	services.add(types.InlineKeyboardButton(text='💥 Скрыть',callback_data=f'скрыть'))

	return services

admin = types.InlineKeyboardMarkup()
admin.add(types.InlineKeyboardButton(text='🧑‍💻 Рассылка',callback_data=f'Рассылка'),types.InlineKeyboardButton(text='📊 Статистика',callback_data=f'админ_стата'))
admin.add(types.InlineKeyboardButton(text='✏️ Изменить баланс',callback_data=f'работа_баланс'), types.InlineKeyboardButton(text='⚡️ Изменить цену',callback_data=f'работа_цена'))
admin.add(types.InlineKeyboardButton(text='✍️ Отправка SMS',callback_data=f'изм:отправка'))
admin.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'вернуться_главная'))

def spisok_names(userid):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_senders where private = "0"')
	row = q.fetchall()
	q.execute(f'SELECT * FROM ugc_senders where userid = "{userid}"')
	roww = q.fetchall()
	services = types.InlineKeyboardMarkup(row_width=3)
	btns = []
	for i in range(len(row)):
		try:
			btns.append(types.InlineKeyboardButton(text=f'{row[i][1]}',callback_data=f'edit_name:{row[i][2]}'))		
		except:
			continue
	for i in range(len(roww)):
		try:
			btns.append(types.InlineKeyboardButton(text=f'{roww[i][1]}',callback_data=f'edit_name:{roww[i][2]}'))		
		except:
			continue

	while btns != []:
		try:
			services.add(
				btns[0],
				btns[1],
				btns[2]
				)
			del btns[2],btns[1], btns[0]
		except:
			services.add(btns[0])
			del btns[0]
	services.add(types.InlineKeyboardButton(text='➕ Добавить отправителя',url='t.me/FilyaAdmin'))
	services.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'вернуться_главная'))
	return services

def get_user_infa(userid):
	answer = telebot.TeleBot(config.token).get_chat(userid)
	amm = f'{answer.first_name} {answer.last_name}'
	if 'filyabomber' in amm.lower():
		return 'True'
	else:
		return 'False'

def translate_lang():
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_translate')
	row = q.fetchall()
	services = types.InlineKeyboardMarkup(row_width=3)
	btns = []
	for i in range(len(row)):
		try:
			btns.append(types.InlineKeyboardButton(text=f'{row[i][1]}',callback_data=f'translate:{row[i][2]}'))		
		except:
			continue
	while btns != []:
		try:
			services.add(
				btns[0],
				btns[1],
				btns[2]
				)
			del btns[2],btns[1], btns[0]
		except:
			services.add(btns[0])
			del btns[0]
	services.add(types.InlineKeyboardButton(text='Нужна другая страна',url='t.me/FilyaAdmin'))
	services.add(types.InlineKeyboardButton(text='Скрыть',callback_data=f'скрыть'))

	return services

def pay_summa():
	menu = types.InlineKeyboardMarkup()
	menu.add(types.InlineKeyboardButton(text='Ввести свою сумму',callback_data=f'add_balance:svoi'))
	menu.add(types.InlineKeyboardButton(text='50₽',callback_data=f'add_balance:50'),types.InlineKeyboardButton(text='100₽',callback_data=f'add_balance:100'), types.InlineKeyboardButton(text='200₽',callback_data=f'add_balance:200'))
	menu.add(types.InlineKeyboardButton(text='500₽',callback_data=f'add_balance:500'), types.InlineKeyboardButton(text='1000₽',callback_data=f'add_balance:1000'))
	menu.add(types.InlineKeyboardButton(text='2000₽',callback_data=f'add_balance:2000'))
	menu.add(types.InlineKeyboardButton(text='«Назад',callback_data=f'вернуться_главная'))
	return menu

def profile(userid, stata=0):
	menu = types.InlineKeyboardMarkup()
	menu.add(types.InlineKeyboardButton(text='➕ Пополнить баланс',callback_data=f'add_balance:svoi'),types.InlineKeyboardButton(text='🌫 История',callback_data=f'история'))
	menu.add(types.InlineKeyboardButton(text='🤖 API',callback_data=f'API'))
	menu.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'вернуться_главная'))
	return menu



def api_keyboards(userid, api):
	menu = types.InlineKeyboardMarkup()
	if str(api) == '0':
		menu.add(types.InlineKeyboardButton(text='Неделя - 500₽',callback_data=f'API:buy:7'),types.InlineKeyboardButton(text='Месяц - 2000₽',callback_data=f'API:buy:3'))
		menu.add(types.InlineKeyboardButton(text='Навсегда - 4500₽',callback_data=f'API:buy:0'))
	else:
		menu.add(types.InlineKeyboardButton(text='🔐 Сгенерировать токен',callback_data=f'API:update'))
		menu.add(types.InlineKeyboardButton(text='📘 Документация',url=f'http://filya.site/sender/api'),types.InlineKeyboardButton(text='💰 Снижение стоимости',callback_data=f'API:minprice'))
	menu.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'вернуться_главная'))
	return menu

def history(userid):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_sms where status = "send" and userid = "{userid}" ORDER BY id DESC LIMIT 99')
	row = q.fetchall()
	services = types.InlineKeyboardMarkup(row_width=3)
	btns = []
	for i in range(len(row)):
		try:
			btns.append(types.InlineKeyboardButton(text=f'{row[i][3]}',callback_data=f'infa_{row[i][0]}'))		
		except:
			continue
	while btns != []:
		try:
			services.add(btns[0],btns[1],btns[2])
			del btns[2],btns[1], btns[0]
		except:
			services.add(btns[0])
			del btns[0]
	services.add(types.InlineKeyboardButton(text='Скрыть',callback_data=f'скрыть'))

	return services
