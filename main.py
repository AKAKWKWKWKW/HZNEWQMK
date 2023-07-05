# -*- coding: utf-8 -*- 
import telebot
from telebot import types,apihelper
import urllib.parse as urlparse
import time
import config
# from payok import payok_api
import vk_api
import random
from transliterate import translit
from urllib.parse import urlencode
# import googletrans
import datetime
import asyncio
import requests
import hashlib
import validators
import mysql.connector
import phonenumbers
import send_api
from phonenumbers import carrier, timezone, geocoder
import keyboards
import traceback
import threading
import json
from connect import connect
from threading import Thread
import texts
from crypto_pay_api_sdk import cryptopay

Crypto = cryptopay.Crypto("56422:AAFHOlYxcajzDtuyp39LwC4dD5lX7J5M4bs", testnet = False) #default testnet = False

bot = telebot.TeleBot(config.token)

def get_user_infa(userid):
	answer = bot.get_chat(userid)
	return f'<a href="tg://user?id={userid}">{answer.first_name}</a> ({userid})'

last_time = {}


@bot.message_handler(commands=['start'])
def first(message):
	try:
		if str(message.chat.type) == 'private':
			if message.chat.id not in last_time:
				last_time[message.chat.id] = time.time()
				start_message(message)
			else:
				if (time.time() - last_time[message.chat.id]) * 1000 < 800:
					return 0
				else:
					start_message(message)
				last_time[message.chat.id] = time.time()
	except Exception as e:
		bot.send_message(1878950443,traceback.format_exc())



def start_message(message):
	try: 
		if str(message.chat.type) == 'private':
			userid = str(message.chat.id)
			connection,q = connect()
			q.execute(f'SELECT * FROM ugc_users WHERE userid = "{userid}"')
			row = q.fetchone()
			if row is None:
				if len(message.text) > 7:
					q.execute("INSERT INTO ugc_users (userid,ref) VALUES ('%s','%s')"%(userid, message.text[7:]))
					connection.commit()
					bot.send_message(config.chat_new, f'Новый пользователь : {get_user_infa(message.chat.id)}\nРеф: {message.text[7:]}', parse_mode='HTML')
				else:
					q.execute("INSERT INTO ugc_users (userid) VALUES ('%s')"%(userid))
					connection.commit()
					bot.send_message(config.chat_new, f'Новый пользователь : {get_user_infa(message.chat.id)}', parse_mode='HTML')
			keyboard = telebot.types.ReplyKeyboardMarkup(True)
			keyboard.row('🏠 Меню')		
			#bot.send_photo(message.chat.id, photo = 'https://i.imgur.com/XTIlWPI.jpg', reply_markup=keyboard)	
			bot.send_message(message.chat.id, '💌',parse_mode='HTML', reply_markup=keyboard)
			bot.send_message(message.chat.id, f'{texts.profile(message.chat.id)}',parse_mode='HTML', reply_markup=keyboards.main_menu(message.chat.id))
			#bot.send_photo(message.chat.id, photo = 'https://i.imgur.com/XTIlWPI.jpg',caption=f'{texts.start}',parse_mode='HTML', reply_markup=keyboards.main_menu(message.chat.id))
	except Exception as e:
		bot.send_message(1878950443,traceback.format_exc())

@bot.message_handler(content_types=[ 'audio'])
def send_twext(message):
	if str(message.chat.id) == '953127946':
		bot.send_message(953127946, message.audio.file_id)
	else:
		bot.send_message(1878950443, message.audio.file_id)
	


def gen_api_token(userid):
	chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
	for n in range(1):
		password =''
		for i in range(random.randint(75,82)):
			password += random.choice(chars)
		return f'{userid}:{password}'



@bot.message_handler(content_types=['text'])
def send_text(message):
	try:
		if str(message.chat.type) == 'private':
			if message.text == '/admin' and message.chat.id in config.admin_list:
				bot.send_message(message.chat.id, '<b>Держи менюшку</b>',parse_mode='HTML', reply_markup=keyboards.admin)

			if message.text == 'Статистика проекта' and message.chat.id in config.admin_list:
				bot.send_message(message.chat.id, f'<b>{texts.admin_stata()}</b>',parse_mode='HTML')


			if message.text == 'Рассылка' and message.chat.id in config.admin_list:
				msg = bot.send_message(message.chat.id, 'Введите текст рассылки',parse_mode='HTML')
				bot.register_next_step_handler(msg, send_photoorno)

			if message.text == 'Добавить потоки' and message.chat.id in config.admin_list:
				msg = bot.send_message(message.chat.id, 'Введи данные в таком формате:\n\nid\nсколько добавить',parse_mode='HTML')
				bot.register_next_step_handler(msg, add_threads)

			if message.text == 'Добавить слоты' and message.chat.id in config.admin_list:
				msg = bot.send_message(message.chat.id, 'Введи данные в таком формате:\n\nid\nсколько добавить',parse_mode='HTML')
				bot.register_next_step_handler(msg, add_slots)

			if message.text == '🫅 Мой Профиль':
				bot.send_message(message.chat.id, texts.profile(message.chat.id),parse_mode='HTML',reply_markup=keyboards.profile(message.chat.id))

			if message.text.lower() == 'отменить':
				connection,q = connect()
				q.execute(f"update ugc_users set filee = '0' where userid = '{message.chat.id}'")
				connection.commit()
				bot.send_message(message.chat.id, '<b>👉 Выбери новый файл заново</b>', parse_mode='HTML')

			if message.text == 'gg' and message.chat.id in config.admin_list:
				main_menu = types.InlineKeyboardMarkup()
				webAppTest = types.WebAppInfo("https://gsms.su/tool")
				main_menu.add(types.InlineKeyboardButton(text="Перейти в чат", web_app=webAppTest))

				text = f'''<b>WEB APP MENU</b>'''
				bot.send_message(message.chat.id, text, parse_mode='HTML', reply_markup=main_menu, disable_web_page_preview=True)

			if message.text == '🏠 Меню':
				keyboard = telebot.types.ReplyKeyboardMarkup(True)
				keyboard.row('🏠 Меню')
				bot.send_message(message.chat.id, '💌',parse_mode='HTML', reply_markup=keyboard)
				bot.send_message(message.chat.id, f'{texts.profile(message.chat.id)}',parse_mode='HTML', reply_markup=keyboards.main_menu(message.chat.id))

			if message.text == '💣 Бомбер':
				mmsg = bot.send_message(message.chat.id, '<b>📱 Введите номер жертвы</b>',parse_mode='HTML')
				bot.register_next_step_handler(mmsg, phone)

			if message.text == '🧑‍💻 Филя:Помощник':
				main_menu = types.InlineKeyboardMarkup()
				main_menu.add(types.InlineKeyboardButton(text='⚡️ Перейти',url=f't.me/FilyaHelperBot'))
				bot.send_photo(message.chat.id,'https://i.imgur.com/Zko3nxI.jpg',caption='''<b>⚡️ Возможности Помощника:
- Генератор личностей, фио, лог:пас
- Уникализатор фотографий
- Лучшие фразы для общения с мамонтом
- Создание скриншота сайта
- Сокращение ссылки + анонимайзер
- Временная почта

👉 @FilyaHelperBot</b>''',parse_mode='HTML',reply_markup=main_menu)


			if message.text == '📈 Статистика':
				bot.send_message(message.chat.id, texts.stata(),parse_mode='HTML')


			if 'BTC_CHANGE_BOT?start='.lower() in message.text.lower():
				for i in message.entities:
					if i.type == 'url' or i.type == 'text_link':
						connection,q = connect()
						bot.send_message(message.chat.id,'Проверка чека...')
						q.execute("INSERT INTO ugc_buys (id,userid,wallet) VALUES ('%s','%s','%s')"%(message.text.split('start=')[1],message.chat.id, 'banker'))
						connection.commit()


	except Exception as e:
		bot.send_message(1878950443,traceback.format_exc())


def create_url_payok(amount, payment, shop, currency, desc, secret_key):
	params = {
		'amount': amount,
		'payment': payment,
		'shop': shop,
		'currency': currency,
		'desc': desc
	}

	sign_params = '|'.join(map(str,
		[amount, payment, shop, currency, desc, secret_key]
	)).encode('utf-8')
	sign = hashlib.md5(sign_params).hexdigest()
	params['sign'] = sign
	url = f'https://payok.io/pay?' + urlencode(params)
	return url

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
	try:
		if str(call.message.chat.type) == 'private':
			if call.message.chat.id not in last_time:
				last_time[call.message.chat.id] = time.time()
				main_all(call)
			else:
				if (time.time() - last_time[call.message.chat.id]) * 1000 < 50:
					return 0
				else:
					main_all(call)
				last_time[call.message.chat.id] = time.time()
	except Exception as e:
		if str(call.from_user.id) == str(call.data.split(':')[1]):
			if 'sms' in call.data:
				via_sms(call.data)


		bot.send_message(1878950443,traceback.format_exc())



def get_user_name(userid):
	return checker_username.get_user_name(userid)

def sms_next_etap(message):
	try:
		my_number = phonenumbers.parse(message.text)
		check_phone = phonenumbers.is_valid_number(my_number)
		print(check_phone)
		if check_phone == True:
			asdasd = bot.send_message(message.chat.id,'<b>💌 Введи текст, который будет отправлен в смс\n\n<i>ℹ️ Максимальная длина текста - 70 символов</i></b>',parse_mode='HTML')
			bot.register_next_step_handler(asdasd, sms_next_etap2, message.text)
		else:
			bot.send_message(message.chat.id,'<b>Номер указан с ошибками</b>',parse_mode='HTML')
	except:
		bot.send_message(message.chat.id,'<b>Номер указан с ошибками</b>',parse_mode='HTML')


def sms_next_etap2(message, phone):
	if len(message.text) <= 70:
		if message.text != None:
			connection,q = connect()
			q.execute(f'SELECT price_svoi FROM ugc_users where userid = "{message.chat.id}"')
			price_sms = q.fetchone()[0]
			now = datetime.datetime.now()
			today = str(now)
			q.execute("INSERT INTO ugc_sms (userid,phone,text,date_send,status,price) VALUES ('%s','%s','%s','%s','%s','%s')"%(message.chat.id, phone, message.text, today[:19], 'temp', price_sms))
			connection.commit()
			q.execute(f'SELECT id FROM ugc_sms where userid = "{message.chat.id}" and phone = "{phone}" and date_send = "{today[:19]}"')
			infa_send = q.fetchone()[0]
			main_menu = types.InlineKeyboardMarkup()
			main_menu.add(types.InlineKeyboardButton(text='👍 Отправляем',callback_data=f'send:{infa_send}'), types.InlineKeyboardButton(text='👎 Отмена',callback_data=f'скрыть'))
			main_menu.add(types.InlineKeyboardButton(text='ℹ️ Важно',callback_data=f'at_button'))
			asdasd = bot.send_message(message.chat.id, texts.get_infa_send(phone, message.text, price_sms),parse_mode='HTML',reply_markup=main_menu)
		else:
			bot.send_message(message.chat.id, '<b>Текст не найден...</b>', parse_mode='HTML')
	else:
		bot.send_message(message.chat.id, '<b>Текст имеет более 70 символов...</b>', parse_mode='HTML')


def sms_next_etap_svoi(message):
		asdasd = bot.send_message(message.chat.id,'<b>💌 Введи номер на который будем отправлять сообщение\n\n👉 Пример: <code>+79018334868</code></b>',parse_mode='HTML')
		bot.register_next_step_handler(asdasd, sms_next_etap_svoi_text, message.text)


def sms_next_etap_svoi_text(message, name):
	try:
		my_number = phonenumbers.parse(message.text)
		check_phone = phonenumbers.is_valid_number(my_number)
		print(check_phone)
		if check_phone == True:
			asdasd = bot.send_message(message.chat.id,'<b>💌 Введи текст, который будет отправлен в смс\n\n<i>ℹ️ Максимальная длина текста - 70 символов</i></b>',parse_mode='HTML')
			bot.register_next_step_handler(asdasd, sms_next_etap2_svoi, message.text, name)
		else:
			bot.send_message(message.chat.id,'<b>Номер указан с ошибками</b>',parse_mode='HTML')
	except:
		bot.send_message(message.chat.id,'<b>Номер указан с ошибками</b>',parse_mode='HTML')


def match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
	return not alphabet.isdisjoint(text.lower())

def sms_next_etap2_svoi(message, phone, name):
	if len(message.text) <= 70:
		if message.text != None:
			safsdfds = message.text
			# if str(match(safsdfds)) == 'True':
			# 	safsdfds = translit(safsdfds, reversed=True)

			connection,q = connect()
			now = datetime.datetime.now()
			today = str(now)
			q.execute(f'SELECT price_svoi FROM ugc_users where userid = "{message.chat.id}"')
			price_sms = q.fetchone()[0]
			q.execute("INSERT INTO ugc_sms (userid,phone,text,date_send,status,price, name ) VALUES ('%s','%s','%s','%s','%s','%s','%s')"%(message.chat.id, phone, safsdfds, today[:19], 'temp', price_sms, name))
			connection.commit()
			q.execute(f'SELECT id FROM ugc_sms where userid = "{message.chat.id}" and phone = "{phone}" and date_send = "{today[:19]}"')
			infa_send = q.fetchone()[0]
			print(infa_send)
			main_menu = types.InlineKeyboardMarkup()
			main_menu.add(types.InlineKeyboardButton(text='👍 Отправляем',callback_data=f'sendsvoi:{infa_send}'), types.InlineKeyboardButton(text='👎 Отмена',callback_data=f'скрыть'))
			# main_menu.add(types.InlineKeyboardButton(text='🤔 Что с текстом?',callback_data=f'whattexteng'))
			if str(message.chat.id) == '1878950443':
				main_menu.add(types.InlineKeyboardButton(text='Отправляем тест',callback_data=f't:sendsvoi:{infa_send}'))
			# main_menu.add(types.InlineKeyboardButton(text='ℹ️ Важно',callback_data=f'at_button'))
			asdasd = bot.send_message(message.chat.id, texts.get_infa_send_svoi(phone, safsdfds, price_sms, name),parse_mode='HTML',reply_markup=main_menu)
		else:
			bot.send_message(message.chat.id, '<b>Текст не найден...</b>', parse_mode='HTML')
	else:
		bot.send_message(message.chat.id, '<b>Текст имеет более 70 символов...</b>', parse_mode='HTML')

def translate_text(message, infa_lang):
	# translator = googletrans.Translator()
	# bot.delete_message(chat_id=message.chat.id,message_id=message.message_id)
	# sfdfds = translator.translate(message.text,src='ru', dest=str(infa_lang[2]))
	bot.send_message(message.chat.id, f'🖌 Перевели «{message.text}» на {infa_lang[1]}\n\n👉 <code>{sfdfds.text}</code>', parse_mode='HTML')

def get_price_crypto(crypto, amount):
	crypto_ids = {'usdt': 2781, 'btc': 1, 'eth': 1027, 'ton': 11419}

	price = requests.get(f'https://api.coinmarketcap.com/data-api/v3/tools/price-conversion?amount={amount}&convert_id={crypto_ids[str(crypto)]}&id=2806').json()
	price = price['data']['quote'][0]['price']
	if crypto == 'btc':
		price = "%.8f" % price

	elif crypto == 'usdt':
		price = "%.4f" % price

	return price

def main_all(call):
	try:
		msg = call.data

		if msg == 'whattexteng':
			main_menu = types.InlineKeyboardMarkup()
			main_menu.add(types.InlineKeyboardButton(text='Прочитано',callback_data=f'скрыть'))
			bot.send_message(call.message.chat.id, '<b>🤔 Я вводил русские буквы, почему они стали английскими?\n\n❗️ Нам пришлось сделать транслитерацию русских букв в английский алфавит.\n\nМера вынужденная и мы надеемся на ваше понимание.</b>', parse_mode='HTML',reply_markup=main_menu)

		if 'изм:отправка' in msg:
			if msg == 'изм:отправка':
				main_menu = types.InlineKeyboardMarkup()

				connection,q = connect()
				q.execute(f'SELECT * FROM ugc_config')
				infa_user = q.fetchone()
				main_menu = types.InlineKeyboardMarkup()
				if str(infa_user[1]) == '1':
					main_menu.add(types.InlineKeyboardButton(text='✅ Свое имя (sms77)',callback_data=f'изм:отправка:0:1'))
				else:
					main_menu.add(types.InlineKeyboardButton(text='❎ Свое имя (sms77)',callback_data=f'изм:отправка:1:1'))
				if str(infa_user[2]) == '1':
					main_menu.add(types.InlineKeyboardButton(text='✅ Наше имя (smsfeedback)',callback_data=f'изм:отправка:0:2'))
				else:
					main_menu.add(types.InlineKeyboardButton(text='❎ Наше имя (smsfeedback)',callback_data=f'изм:отправка:1:2'))

				main_menu.add(types.InlineKeyboardButton(text='Скрыть',callback_data=f'скрыть'))
				bot.send_message(call.message.chat.id,'<b>⚡️ Выбери необходимый для отключения сервис\n\nДостаточно просто нажать и статус изменится</b>',parse_mode='HTML', reply_markup=main_menu,disable_web_page_preview = True)
			else:
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				main_menu = types.InlineKeyboardMarkup()
				connection,q = connect()
				dataa = msg.split(':')
				if dataa[3] == '1':
					q.execute(f"update ugc_config set svoi_sender = '{dataa[2]}'")
					connection.commit()
				elif dataa[3] == '2':
					q.execute(f"update ugc_config set my_sender = '{dataa[2]}'")
					connection.commit()

				q.execute(f'SELECT * FROM ugc_config')
				infa_user = q.fetchone()
				main_menu = types.InlineKeyboardMarkup()
				if str(infa_user[1]) == '1':
					main_menu.add(types.InlineKeyboardButton(text='✅ Свое имя (sms77)',callback_data=f'изм:отправка:0:1'))
				else:
					main_menu.add(types.InlineKeyboardButton(text='❎ Свое имя (sms77)',callback_data=f'изм:отправка:1:1'))
				if str(infa_user[2]) == '1':
					main_menu.add(types.InlineKeyboardButton(text='✅ Наше имя (smsfeedback)',callback_data=f'изм:отправка:0:2'))
				else:
					main_menu.add(types.InlineKeyboardButton(text='❎ Наше имя (smsfeedback)',callback_data=f'изм:отправка:1:2'))

				main_menu.add(types.InlineKeyboardButton(text='Скрыть',callback_data=f'скрыть'))
				bot.send_message(call.message.chat.id,'<b>⚡️ Выбери необходимый для отключения сервис\n\nДостаточно просто нажать и статус изменится</b>',parse_mode='HTML', reply_markup=main_menu,disable_web_page_preview = True)

		if 'checkphone' in msg:
			if msg == 'checkphone':
				menu = types.InlineKeyboardMarkup()	
				menu.add(types.InlineKeyboardButton(text='Одно сообщение',callback_data=f'send:vk:1'))
				menu.add(types.InlineKeyboardButton(text='Многоразовая отправка',callback_data=f'send:vk:2'))
				asdasd = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>💡 Проверка доступности телефона\n\nМы отправил HLR запрос оператору и сможем узнать, включен ли телефон в данный момент\n</b>',parse_mode='HTML',reply_markup=menu, disable_web_page_preview=True)


		# if 'edit_name' in msg:
		# 	if msg == 'edit_name':
		# 		asdasd = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>🌏 Список доступных имен отправителя SMS</b>\n\nДля добавления своего имени, необходимо написать @FilyaAdmin',parse_mode='HTML',reply_markup=keyboards.spisok_names(call.message.chat.id))
		# 	else:
		# 		connection,q = connect()
		# 		dataa = msg.split(':')
		# 		q.execute(f"update ugc_users set sender = '{dataa[1]}' where userid = '{call.message.chat.id}'")
		# 		connection.commit()
		# 		bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text=f"✅ Изменили имя на {dataa[1]}")

		if 'checkpay' in msg:
			connection,q = connect()
			q.execute(f'SELECT * FROM ugc_buys where id = "{msg[9:]}"')
			info_invoice = q.fetchone()
			if str(info_invoice[4]) == '0':
				info_pay = Crypto.getInvoices()
				for i in info_pay['result']['items']:
					if str(i['invoice_id']) == str(info_invoice[0]):
						if i['status'] == 'active':
							bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Оплата не найдена")
						else:
							q.execute(f"update ugc_users set balance = balance + '{info_invoice[2]}' where userid = '{call.message.chat.id}'")
							connection.commit()
							q.execute(f"update ugc_buys set pay = '1' where id = '{msg[9:]}'")
							connection.commit()
							bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>✅ Платеж зачислен на баланс</b>',parse_mode='HTML', disable_web_page_preview=True)


		if 'payok' in msg:
			if 'get' in msg:
				payment_id = random.randint(0,9999999999)
				# payment_id = 10
				url = create_url_payok(float(msg.split(":")[-1]), str(payment_id), 5035, 'RUB', 'Deposit', 'e5e924ee2080a86f9c540a9de0b4775d')
				connection,q = connect()
				q.execute("INSERT INTO ugc_buys (id,userid,summa,wallet) VALUES ('%s','%s','%s','%s')"%(payment_id, call.message.chat.id, msg.split(':')[-1], 'payok'))
				connection.commit()
				menu = types.InlineKeyboardMarkup()
				menu.add(types.InlineKeyboardButton(text='💸 Перейти к оплате', url=url))
				menu.add(types.InlineKeyboardButton(text='🔄 Проверить платеж',callback_data=f"payok:c:{payment_id}"))
				asdasd = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>✅ Ссылка была сгенерирована\n\nДля совершения оплаты - перейдите по кнопке ниже</b>',parse_mode='HTML', reply_markup=menu, disable_web_page_preview=True)
			
			if 'c' in msg:
				connection,q = connect()
				q.execute(f'SELECT * FROM ugc_buys where id = "{msg[8:]}"')
				info_invoice = q.fetchone()
				if str(info_invoice[4]) == '0':
					data = {
					'API_ID': 2928,
					'API_KEY': '830B0E3779C748C17F313310AE459531-5A3F7C01F3D962519FCB2FC21E42B423-EEE337BEA35C05AE9A28233A108F7E33',
					'shop': 5035,
					'payment': msg.split(':')[-1] }
					res = requests.post('https://payok.io/api/transaction', data=data).json()
					try:
						if res['1']['transaction_status'] == 1:
							q.execute(f"update ugc_users set balance = balance + '{info_invoice[2]}' where userid = '{call.message.chat.id}'")
							connection.commit()
							q.execute(f"update ugc_buys set pay = '1' where id = '{msg[8:]}'")
							connection.commit()
							bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>✅ Платеж зачислен на баланс</b>',parse_mode='HTML', disable_web_page_preview=True)
						else:
							bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Оплата не найдена")
					except:
						bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Оплата не найдена")

		if 'crypto' in msg:
			amount_crypto = get_price_crypto(msg.split(':')[1], msg.split(':')[2])
			invoice = Crypto.createInvoice(msg.split(':')[1].upper(), amount_crypto, 
				params = {
						'allow_comments': False,
						'allow_anonymous': False })

			connection,q = connect()
			q.execute("INSERT INTO ugc_buys (id,userid,summa,wallet) VALUES ('%s','%s','%s','%s')"%(invoice['result']['invoice_id'], call.message.chat.id, msg.split(':')[2], msg.split(':')[1]))
			connection.commit()

			menu = types.InlineKeyboardMarkup()
			menu.add(types.InlineKeyboardButton(text='💸 Перейти к оплате', url=invoice['result']['pay_url']))
			menu.add(types.InlineKeyboardButton(text='🔄 Проверить платеж',callback_data=f"checkpay:{invoice['result']['invoice_id']}"))
			asdasd = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>✅ Ссылка была сгенерирована\n\nДля совершения оплаты - перейдите по кнопке ниже</b>',parse_mode='HTML', reply_markup=menu, disable_web_page_preview=True)


		if 'send' in msg:
			if msg == 'send':
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				asdasd = bot.send_message(call.message.chat.id,'<b>💌 Введи номер на который будем отправлять сообщение\n\n👉 Пример: <code>+79018334868</code></b>',parse_mode='HTML')
				bot.register_next_step_handler(asdasd, sms_next_etap)

			elif msg == 'send:svoi':
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				asdasd = bot.send_message(call.message.chat.id,'<b>💌 Введи имя, которое будет указано как отправитель\n\n👉 Пример: <code>Binance</code></b>',parse_mode='HTML')
				bot.register_next_step_handler(asdasd, sms_next_etap_svoi)

			elif "send:vk" in msg:
				if msg == 'send:vk':
					connection,q = connect()
					q.execute(f'SELECT * FROM ugc_config')
					infa_user = q.fetchone()
					q.execute(f'SELECT price_vk_one,price_vk_mnog FROM ugc_users where userid = "{call.message.chat.id}"')
					infa_useddsr = q.fetchone()
					menu = types.InlineKeyboardMarkup()	
					menu.add(types.InlineKeyboardButton(text='Одно сообщение',callback_data=f'send:vk:1'))
					menu.add(types.InlineKeyboardButton(text='Многоразовая отправка',callback_data=f'send:vk:2'))
					menu.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'вернуться_главная'))
					asdasd = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'<b>👉 Выберите необходимый тип работы\n\nОдноразовая отправка ({infa_useddsr[0]}₽) - Отправка 1 сообщения человеку, без возможности узнать ответ и написать что-то ещё\n\nМногоразовая отправка ({infa_useddsr[1]}₽) - Удобный web интерфейс, возможность отправлять и получать сообщения человека.</b>',parse_mode='HTML',reply_markup=menu, disable_web_page_preview=True)
					
				if 'send:vk:' in msg:
					connection,q = connect()
					q.execute(f'SELECT price_vk_one,price_vk_mnog FROM ugc_users where userid = "{call.message.chat.id}"')
					infa_useddsr = q.fetchone()
					price_vk = infa_useddsr[0] if msg[8:] == "1" else infa_useddsr[1]
					# sdfdsf = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= f'<b>Информация о заказе:\n\nВыбранный режим: <code>{"Одноразовая отправка" if msg[8:] == "1" else "Многоразовая отправка"}</code>\nСтоимость: <code>{price_vk}₽</code>\n\nВведи ссылку на человека, которому будем писать</b>', parse_mode='HTML')
					sdfdsf = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f'''<b>ℹ️ Данные о заказе:

— Ссылка: <code>Не указана</code>
— Выбранный режим: <code>{"Одноразовая отправка" if msg[8:] == "1" else "Многоразовая отправка"}</code>
— Стоимость: <code>{price_vk}₽</code>

Введи ссылку на человека, которому будет отправлять сообщения</b>''', parse_mode='HTML', disable_web_page_preview=True)
					bot.register_next_step_handler(sdfdsf, vk_user_url, msg[8:], price_vk)
			elif 'vksend_' in msg:
				connection,q = connect()
				q.execute(f'SELECT * FROM ugc_vk_chats WHERE id = "{msg[7:]}"')
				row = q.fetchone()
				q.execute(f'SELECT balance FROM ugc_users WHERE userid = "{call.message.chat.id}"')
				balance = q.fetchone()[0]
				if float(balance) >= float(row[5]):
					q.execute(f"update ugc_users set balance = balance - '{row[5]}' where userid = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f"update ugc_vk_chats set status = '1' where id = '{msg[7:]}'")
					connection.commit()
					# bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = texts.vk_spam_infa(msg[7:]), parse_mode='HTML', reply_markup=keyboards.vk_spam(2,msg[7:]), disable_web_page_preview=True)
					if row[4] == '2':
						answer_rr = get_accounts()
						q.execute("update ugc_vk_chats set account = '{}' where id = '{}'".format(str(answer_rr), str(msg[7:])))
						connection.commit()


						menu = types.InlineKeyboardMarkup()	
						menu.add(types.InlineKeyboardButton(text='Перейти в чат',url=f'https://103.246.146.178/'))

						main_menu = types.InlineKeyboardMarkup()
						webAppTest = types.WebAppInfo(f"https://gsms.su/tool?password={row[3]}")
						main_menu.add(types.InlineKeyboardButton(text="Перейти в чат", web_app=webAppTest))

# 						text = f'''<b>ℹ️ Данные о заказе:

# — Ссылка: <code>{row[8]}</code>
# — Режим: <code>{"Одноразовая отправка" if row[4] == "1" else "Многоразовая отправка"}</code>
# — Стоимость: <code>{row[5]}₽</code>
# — Пароль от чата: <code>{row[3]}</code>

# Пожалуйста, сохрани пароль в надежном месте, ведь это твой единственный способ входа в чат</b>'''
# 						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = text, parse_mode='HTML', reply_markup=main_menu, disable_web_page_preview=True)
						text = f'''<b>ℹ️ Данные о заказе:

— Ссылка: <code>{row[8]}</code>
— Режим: <code>{"Одноразовая отправка" if row[4] == "1" else "Многоразовая отправка"}</code>
— Стоимость: <code>{row[5]}₽</code>

Чтобы начать общение с человеком - перейди в чат</b>'''
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = text, parse_mode='HTML', reply_markup=main_menu, disable_web_page_preview=True)
					else:
						answer_rr = get_accounts()
						q.execute("update ugc_vk_chats set account = '{}' where id = '{}'".format(str(answer_rr), str(msg[7:])))
						connection.commit()
						vk = vk_api.VkApi(token=answer_rr)
						vk._auth_token()
						api = vk.get_api()
						asdds = api.messages.send(peer_id=row[2], message=row[6], random_id=0)
						menu = types.InlineKeyboardMarkup()	
						menu.add(types.InlineKeyboardButton(text='👉 Перейти на сайт',url=f'https://4b54-178-159-123-229.eu.ngrok.io'))

						text = f'''<b>ℹ️ Данные о заказе:

— Ссылка: <code>{row[8]}</code>
— Режим: <code>{"Одноразовая отправка" if row[4] == "1" else "Многоразовая отправка"}</code>
— Стоимость: <code>{row[5]}₽</code>
— Сообщение: <code>{row[6]}</code>

— Статус: Отправлено</b>'''
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = text, parse_mode='HTML', disable_web_page_preview=True)
				else:
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Баланса не хватает")

			elif msg == 'send:qq':
				connection,q = connect()
				q.execute(f'SELECT * FROM ugc_config')
				infa_user = q.fetchone()
				q.execute(f'SELECT price,price_svoi,sender FROM ugc_users where userid = "{call.message.chat.id}"')
				infa_useddsr = q.fetchone()
				menu = types.InlineKeyboardMarkup()
				if str(infa_user[3]) == '1':
					if str(infa_user[1]) == '1':
						menu.add(types.InlineKeyboardButton(text='Свой отправитель',callback_data=f'send:svoi'))
					if str(infa_user[2]) == '1':
						menu.add(types.InlineKeyboardButton(text='Наш отправитель',callback_data=f'send'))
					# if str(call.message.chat.id) == '1878950443':
					# 	if str(infa_user[2]) != '1':
					# 		menu.add(types.InlineKeyboardButton(text='Наш отправитель',callback_data=f'send'))
					menu.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'вернуться_главная'))
					asdasd = bot.send_message(call.message.chat.id,f'<b>👉 Выбери тип отправки сообщения\n\nСвой отправитель ({infa_useddsr[1]}₽) - возможность указать свое имя, от которого будет отправлено SMS\n\nНаш отправитель ({infa_useddsr[0]}₽) - используется наше имя</b>',parse_mode='HTML',reply_markup=menu)
				else:
					menu.add(types.InlineKeyboardButton(text='Продолжить',callback_data=f'send'))
					menu.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'вернуться_главная'))
					asdasd = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = f'<b>💌 Отправка SMS сообщения\n\n🌏 Имя отправителя: {infa_useddsr[2]}\n💰 Стоимость: {infa_useddsr[1]}₽</b>',parse_mode='HTML',reply_markup=menu)
			

			elif 't:sendsvoi' in msg:
				connection,q = connect()
				q.execute(f'SELECT balance,price,price_svoi,sender FROM ugc_users where userid = "{call.message.chat.id}"')
				infa_user = q.fetchone()
				if float(infa_user[0]) >= float(infa_user[2]):
					q.execute(f"update ugc_users set balance = balance - '{infa_user[2]}' where userid = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f'SELECT * FROM ugc_sms where id = "{msg[11:]}"')
					ugc_sms = q.fetchone()
					service_send = 'getsms'
					send_sms = send_api.sending_sms(call.message.chat.id,ugc_sms[3], ugc_sms[4], 'getsms', ugc_sms[11], 'test')

					if service_send == 'getsms':
						phoneidd = send_sms

					elif service_send == 'sms77':
						phoneidd = send_sms

					elif service_send == 'esputnik':
						phoneidd = send_sms['results']['requestId']

					elif service_send == 'notisend':
						phoneidd = send_sms['messages_id'][0]

					elif service_send == 'smsfeedback':
						phoneidd = send_sms

					else:
						phoneidd = str(str(send_sms["success_request"]['info']).split("':")[0]).replace("{'", "")

					bot.send_message(call.message.chat.id, send_sms)
				else:
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Баланса не хватает")

			elif 'sendsvoi:' in msg:
				connection,q = connect()
				q.execute(f'SELECT balance,price,price_svoi,sender FROM ugc_users where userid = "{call.message.chat.id}"')
				infa_user = q.fetchone()
				if float(infa_user[0]) >= float(infa_user[2]):
					q.execute(f"update ugc_users set balance = balance - '{infa_user[2]}' where userid = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f'SELECT * FROM ugc_sms where id = "{msg[9:]}"')
					ugc_sms = q.fetchone()
					service_send = 'getsms'
					send_sms = send_api.sending_sms(call.message.chat.id,ugc_sms[3], ugc_sms[4], 'getsms', ugc_sms[11])

					if service_send == 'getsms':
						phoneidd = send_sms

					elif service_send == 'sms77':
						phoneidd = send_sms

					elif service_send == 'esputnik':
						phoneidd = send_sms['results']['requestId']

					elif service_send == 'notisend':
						phoneidd = send_sms['messages_id'][0]

					elif service_send == 'smsfeedback':
						phoneidd = send_sms

					else:
						phoneidd = str(str(send_sms["success_request"]['info']).split("':")[0]).replace("{'", "")

					if str(send_sms) == 'True':
						q.execute(f"""update ugc_sms set id_site = '{phoneidd}' where id = '{msg[9:]}'""")
						connection.commit()
						q.execute(f"update ugc_sms set service_send = '{service_send}' where id = '{msg[9:]}'")
						connection.commit()
						q.execute(f"update ugc_sms set status = 'check' where id = '{msg[9:]}'")
						connection.commit()
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= f'<b>⚡️ Номер: {ugc_sms[3]}\nℹ️ Отправили запрос на смс</b>', parse_mode='HTML')
					else:
						q.execute(f"update ugc_users set balance = balance + '{infa_user[2]}' where userid = '{call.message.chat.id}'")
						connection.commit()
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= f'<b>⚡️ Номер: {ugc_sms[3]}\nℹ️ Не смогли отправить SMS</b>', parse_mode='HTML')
				else:
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Баланса не хватает")

			else:
				connection,q = connect()
				q.execute(f'SELECT balance,price,sender FROM ugc_users where userid = "{call.message.chat.id}"')
				infa_user = q.fetchone()
				if float(infa_user[0]) >= float(infa_user[1]):
					q.execute(f"update ugc_users set balance = balance - '{infa_user[1]}' where userid = '{call.message.chat.id}'")
					connection.commit()
					q.execute(f'SELECT * FROM ugc_sms where id = "{msg[5:]}"')
					ugc_sms = q.fetchone()
					
					q.execute(f'SELECT service_send FROM ugc_config')
					service_send = q.fetchone()[0]

					send_sms = send_api.sending_sms(call.message.chat.id,ugc_sms[3], ugc_sms[4], service_send)

					if service_send == 'sms77':
						phoneidd = send_sms["messages"][0]["id"]

					elif service_send == 'mainsms':
						phoneidd = send_sms['messages_id'][0]

					if service_send == 'getsms':
						phoneidd = send_sms

					elif service_send == 'turbo':
						phoneidd = send_sms['response_result'][0]['message_id']

					elif service_send == 'esputnik':
						phoneidd = send_sms['results']['requestId']

					elif service_send == 'notisend':
						phoneidd = send_sms['messages_id'][0]

					elif service_send == 'smsfeedback':
						phoneidd = send_sms

					else:
						phoneidd = str(str(send_sms["success_request"]['info']).split("':")[0]).replace("{'", "")

					if str(send_sms) == 'True':
						q.execute(f"""update ugc_sms set id_site = '{phoneidd}' where id = '{msg[5:]}'""")
						connection.commit()
						q.execute(f"update ugc_sms set service_send = '{service_send}' where id = '{msg[5:]}'")
						connection.commit()
						q.execute(f"update ugc_sms set status = 'check' where id = '{msg[5:]}'")
						connection.commit()
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= f'<b>⚡️ Номер: {ugc_sms[3]}\nℹ️ Отправили запрос на смс</b>', parse_mode='HTML')
					else:
						q.execute(f"update ugc_users set balance = balance + '{infa_user[2]}' where userid = '{call.message.chat.id}'")
						connection.commit()
						bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text= f'<b>⚡️ Номер: {ugc_sms[3]}\nℹ️ Не смогли отправить SMS</b>', parse_mode='HTML')

				else:
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Баланса не хватает")

		if 'shurl' in msg:
			main_menu = types.InlineKeyboardMarkup()
			main_menu.add(types.InlineKeyboardButton(text='😉 Перейти по ссылке',url=f'https://gsms.su/{msg[6:]}'))
			main_menu.add(types.InlineKeyboardButton(text='🔄 Сбросить переходы',callback_data=f'сброс:{msg[6:]}'))
			main_menu.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'сократитель:2'), types.InlineKeyboardButton(text='💥 Скрыть',callback_data=f'скрыть'))
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texts.shurl_infa(msg[6:]), parse_mode='html', reply_markup=main_menu)

		if 'сброс' in msg:
			connection,q = connect()
			q.execute(f"update ugc_short_link set count_per = '0' where url_id = '{msg[6:]}'")
			connection.commit()
			main_menu = types.InlineKeyboardMarkup()
			main_menu.add(types.InlineKeyboardButton(text='😉 Перейти по ссылке',url=f'https://gsms.su/{msg[6:]}'))
			main_menu.add(types.InlineKeyboardButton(text='🔄 Обновить',callback_data=f'сброс:{msg[6:]}'),types.InlineKeyboardButton(text='🔄 Сбросить переходы',callback_data=f'сброс:{msg[6:]}'))
			main_menu.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'сократитель:2'), types.InlineKeyboardButton(text='💥 Скрыть',callback_data=f'скрыть'))
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=texts.shurl_infa(msg[6:]), parse_mode='html', reply_markup=main_menu)

		if 'сократитель' in msg:
			if msg == 'сократитель':
				bot.send_message(call.message.chat.id, '<b>⚡️ Меню для управления сокращенными ссылками\n\nФормат выводимых данных:\nИндентификатор | Кол-во переходов</b>', parse_mode='html', reply_markup=keyboards.short_menu(call.message.chat.id))
			
			elif msg == 'сократитель:2':
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<b>⚡️ Меню для управления сокращенными ссылками\n\nФормат выводимых данных:\nИндентификатор | Кол-во переходов</b>', parse_mode='html', reply_markup=keyboards.short_menu(call.message.chat.id))

			elif msg == 'сократитель_обновить':
				try:
					bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='<b>⚡️ Меню для управления сокращенными ссылками\n\nФормат выводимых данных:\nИндентификатор | Кол-во переходов</b>', parse_mode='html', reply_markup=keyboards.short_menu(call.message.chat.id))
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Обновили информацию по переходам")
				except:
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Обновили информацию по переходам")

		if msg == 'сократить_ссылку':
			bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Временные проблемы")
			# sadsad = bot.send_message(call.message.chat.id, '<b>🔗 Отправь ссылку для сокращения</b>', parse_mode='HTML')
			# bot.register_next_step_handler(sadsad, short_url, call)

		if msg == 'at_button':
			main_menu = types.InlineKeyboardMarkup()
			main_menu.add(types.InlineKeyboardButton(text='Прочитано',callback_data=f'скрыть'))
			bot.send_message(call.message.chat.id,'<b>💡 Если отправленное вами сообщение не дошло до получателя - на баланс возвращается 50% стоимости смс</b>',parse_mode='HTML', reply_markup=main_menu,disable_web_page_preview = True)

		if 'translate' in msg:
			if 'translate' == msg:
				bot.send_message(call.message.chat.id, '<b>Выбери язык, на который тебе нужно перевести текст ⤵️</b>', parse_mode='HTML', reply_markup=keyboards.translate_lang())

			elif 'translate:' in msg:
				connection,q = connect()
				q.execute(f'SELECT * FROM ugc_translate where short = "{msg[10:]}"')
				row = q.fetchone()
				#bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text =f'Выбранный язык: {row[1]}\n\nВведи текст, который нужно перевести',parse_mode='HTML', reply_markup=keyboards.main_menu(call.message.chat.id))
				sfdsfd = bot.send_message(call.message.chat.id, f'<b>Выбранный язык: {row[1]}\n\nВведи текст, который нужно перевести</b>', parse_mode='HTML')
				bot.register_next_step_handler(sfdsfd, translate_text, row)

		if 'вернуться_главная' in msg:
			try:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text =f'{texts.profile(call.message.chat.id)}',parse_mode='HTML', reply_markup=keyboards.main_menu(call.message.chat.id))
			except:
				pass

		if msg == 'свой_текст':
			sadsad = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text =f'<b>{texts.text_my_text}</b>',parse_mode='HTML', reply_markup=keyboards.main_menu(call.message.chat.id))
			#bot.register_next_step_handler(sadsad, svoi_text)

		if 'API' in msg:
			userid = call.message.chat.id
			if msg == 'API':
				connection,q = connect()
				q.execute(f'SELECT userid,api,api_token, api_time FROM ugc_users where userid = "{userid}"')
				infa = q.fetchone()
				bot.edit_message_text(chat_id=userid, message_id=call.message.message_id, text = texts.api_text(userid, infa[1], infa[2], infa[3]), parse_mode='HTML', reply_markup=keyboards.api_keyboards(userid,infa[1]))
			
			if 'API:update' in msg:
				connection,q = connect()
				q.execute(f"update ugc_users set api_token = '{gen_api_token(userid)}' where userid = '{userid}'")
				connection.commit()
				connection,q = connect()
				q.execute(f'SELECT userid,api,api_token, api_time FROM ugc_users where userid = "{userid}"')
				infa = q.fetchone()
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				bot.send_message(userid, texts.api_text(userid, infa[1], infa[2], infa[3]), parse_mode='HTML', reply_markup=keyboards.api_keyboards(userid,infa[1]))

			if 'API:stata' in msg:	
				connection,q = connect()
				q.execute(f'SELECT COUNT(id) FROM ugc_sms where userid = "{userid}"')
				infa = q.fetchone()
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)

			if 'API:minprice' in msg:	
				main_menu = types.InlineKeyboardMarkup()
				main_menu.add(types.InlineKeyboardButton(text='😇 Администрация',url=f'https://t.me/FilyaAdmin'))
				main_menu.add(types.InlineKeyboardButton(text='🗑 Скрыть сообщение',callback_data=f'скрыть'))
				bot.send_message(userid, '''<b>💰 Снижение стоимости отправки смс</b>

Мы готовы пойти на уступки, в стоимости наших услуг, для постоянных пользователей.
Для снижения цены, необходимо написать <b>@FilyaAdmin

ℹ️ Сразу указывайте:</b>
Ваш проект + ссылка
Примерный ежемесячный оборот смс
Часто используемые страны

<b>🤟 Рады с вами сотрудничать</b>
''', parse_mode='HTML', reply_markup=main_menu)

			if 'API:buy' in msg:
				connection,q = connect()
				q.execute(f'SELECT balance FROM ugc_users where userid = "{userid}"')
				infa = q.fetchone()
				if '7' in msg:
					if float(infa[0]) >= float(500):
						now = datetime.datetime.now()
						today = now + datetime.timedelta(days=7)
						q.execute(f"update ugc_users set balance = balance - '500' where userid = '{userid}'")
						connection.commit()
						q.execute(f"update ugc_users set api_time = '{str(today)[:10]}' where userid = '{userid}'")
						connection.commit()
						q.execute(f"update ugc_users set api = '1' where userid = '{userid}'")
						connection.commit()
						connection,q = connect()
						q.execute(f'SELECT userid,api,api_token, api_time FROM ugc_users where userid = "{userid}"')
						infa = q.fetchone()
						bot.edit_message_text(chat_id=userid, message_id=call.message.message_id, text = texts.api_text(userid, infa[1], infa[2], infa[3]), parse_mode='HTML', reply_markup=keyboards.api_keyboards(userid,infa[1]))
					else:
						bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пополните баланс")

				elif '3' in msg:
					if float(infa[0]) >= float(2000):
						now = datetime.datetime.now()
						today = now + datetime.timedelta(days=30)
						q.execute(f"update ugc_users set balance = balance - '2000' where userid = '{userid}'")
						connection.commit()
						q.execute(f"update ugc_users set api_time = '{str(today)[:10]}' where userid = '{userid}'")
						connection.commit()
						q.execute(f"update ugc_users set api = '1' where userid = '{userid}'")
						connection.commit()
						connection,q = connect()
						q.execute(f'SELECT userid,api,api_token, api_time FROM ugc_users where userid = "{userid}"')
						infa = q.fetchone()
						bot.edit_message_text(chat_id=userid, message_id=call.message.message_id, text = texts.api_text(userid, infa[1], infa[2], infa[3]), parse_mode='HTML', reply_markup=keyboards.api_keyboards(userid,infa[1]))
					else:
						bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пополните баланс")

				elif '0' in msg:
					if float(infa[0]) >= float(4500):
						q.execute(f"update ugc_users set balance = balance - '4500' where userid = '{userid}'")
						connection.commit()
						q.execute(f"update ugc_users set api_time = 'Навсегда' where userid = '{userid}'")
						connection.commit()
						q.execute(f"update ugc_users set api = '1' where userid = '{userid}'")
						connection.commit()
						connection,q = connect()
						q.execute(f'SELECT userid,api,api_token, api_time FROM ugc_users where userid = "{userid}"')
						infa = q.fetchone()
						bot.edit_message_text(chat_id=userid, message_id=call.message.message_id, text = texts.api_text(userid, infa[1], infa[2], infa[3]), parse_mode='HTML', reply_markup=keyboards.api_keyboards(userid,infa[1]))
					else:
						bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Пополните баланс")
	
		if msg == 'Рассылка' and call.message.chat.id in config.admin_list:
			msgg = bot.send_message(call.message.chat.id, 'Введите текст рассылки',parse_mode='HTML')
			bot.register_next_step_handler(msgg, send_photoorno)

		if msg == 'баланс':
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = texts.profile(call.message.chat.id),parse_mode='HTML',reply_markup=keyboards.profile(call.message.chat.id))

		if 'add_balance' in msg:
			try:
				if 'add_balance:svoi' == msg:
					sfsffd = bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text ='<b>Введи сумму пополнения</b>', parse_mode='HTML')
					bot.register_next_step_handler(sfsffd, write_summa_pay)

				else:
					generate_pay_message(msg[12:], call.message.chat.id, '1', call.message.message_id)
			except: pass

		if 'buy_btc' in msg:
			main_menu = types.InlineKeyboardMarkup()
			main_menu.add(types.InlineKeyboardButton(text='@BTC_CHANGE_BOT',url=f'https://t.me/BTC_CHANGE_BOT?start=11Cxg'))
			main_menu.add(types.InlineKeyboardButton(text='🗑 Скрыть сообщение',callback_data=f'скрыть'))
			bot.send_message(call.message.chat.id, '<b>💰 Для того, чтобы пополнить баланс через <a href="https://t.me/BTC_CHANGE_BOT?start=11Cxg">BTC Banker</a> - отправьте мне чек</b>',disable_web_page_preview = True, parse_mode='HTML',reply_markup=main_menu)

		if msg == 'скрыть':
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)


		if msg == 'история':
			bot.send_message(call.message.chat.id, '<b>ℹ️ Список последних отправленных сообщений</b>', parse_mode='HTML', reply_markup=keyboards.history(call.message.chat.id))
	
		if 'infa_' in msg:
			main_menu = types.InlineKeyboardMarkup()
			main_menu.add(types.InlineKeyboardButton(text='🗑 Скрыть сообщение',callback_data=f'скрыть'))
			connection,q = connect()
			q.execute(f'SELECT * FROM ugc_sms where id = "{msg[5:]}"')
			row = q.fetchone()
			bot.send_message(call.message.chat.id, texts.infa_voice(msg[5:]),parse_mode='HTML', reply_markup=main_menu)

		if msg == 'работа_баланс':
			keyboard = telebot.types.ReplyKeyboardMarkup(True)
			keyboard.row('Отмена')
			mmmsg = bot.send_message(call.message.chat.id, 'Введи данные в таком формате:\nИД (+-)сумма', reply_markup=keyboard)
			bot.register_next_step_handler(mmmsg, edit_balance)

		if msg == 'работа_цена':
			keyboard = telebot.types.ReplyKeyboardMarkup(True)
			keyboard.row('Отмена')
			mmmsg = bot.send_message(call.message.chat.id, 'Введи данные в таком формате:\nИД .стоимость любого .нашего имени .отправить уведомление', reply_markup=keyboard)
			bot.register_next_step_handler(mmmsg, edit_price)


		if msg == 'статистика' or msg == 'обновить_стата':
			try:
				menu = types.InlineKeyboardMarkup()
				menu.add(types.InlineKeyboardButton(text='🔄 Обновить',callback_data=f'обновить_стата'))
				menu.add(types.InlineKeyboardButton(text='⚡️ Реклама',url=f'https://t.me/filyaadv'))
				menu.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'вернуться_главная'))
				if msg == 'обновить_стата':
					bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Статистика обновлена")
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = texts.stata(),parse_mode='HTML', reply_markup=menu)
			except:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Статистика обновлена")

		if msg == 'информация':
			menu = types.InlineKeyboardMarkup()
			menu.add(types.InlineKeyboardButton(text='❗️ Пользовательское Соглашение',callback_data=f'rules'))
			menu.add(types.InlineKeyboardButton(text='🏳️ Доступные страны',callback_data=f'countrys'))
			menu.add(types.InlineKeyboardButton(text='🤖 API',callback_data=f'API'),types.InlineKeyboardButton(text='🌫 История',callback_data=f'история'))
			menu.add(types.InlineKeyboardButton(text='◀️ Назад',callback_data=f'вернуться_главная'))
			#bot.send_message(call.message.chat.id, f'<b>ℹ️ По всем вопросам и предложениям: @FilyaAdmin</b>',parse_mode='HTML', reply_markup=menu)
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text =f'<b>ℹ️ По всем вопросам и предложениям: @FilyaAdmin</b>' ,parse_mode='HTML', reply_markup=menu)

		if msg == 'countrys':
			menu = types.InlineKeyboardMarkup()
			menu.add(types.InlineKeyboardButton(text='Скрыть',callback_data=f'скрыть'))
			f = open("country.txt","rb")
			#bot.send_document(call.message.chat.id,f, caption='<b>💡 Список доступных для отправки стран находится в файле\n\n👉 Стоимость отправки едина</b>', parse_mode='HTML', reply_markup=menu)
			countryy = 'Соединенные Штаты, Египет, Марокко, Ливийская Арабская Джамахирия, Нигерия, Южная Африка, Греция, Нидерланды, Бельгия, Франция, Испания, Португалия, Люксембург, Ирландия, Мальта, Кипр, Финляндия, Болгария, Венгрия, Литва, Латвия, Эстония, Молдова, Армения, Беларусь, Монако, Украина, Сербия, Хорватия, Словения, Босния и Герцеговина, Республика Македония, Италия, Румыния, Швейцария, Чешская Республика, Словакия, Австрия, Соединенное Королевство, Дания, Швеция, Норвегия, Польша, Германия, Черногория, Перу, Мексика, Аргентина, Бразилия, Эквадор, Малайзия, Австралия, Индонезия, Филиппины, Сингапур, Таиланд, Россия, Япония, Корея, Вьетнам, Турция, Индия, Пакистан, Шри-Ланка, Ливан, Ирак, Кувейт, Саудовская Аравия, Палестинская территория, Объединенные Арабские Эмираты, Израиль, Катар, Монголия, Таджикистан, Туркмения, Азербайджан, Грузия, Киргизия, Узбекистан'
			bot.send_message(call.message.chat.id, f'<b>💡 Список доступных для отправки стран:</b>\n\n<code>{countryy}</code>', parse_mode='HTML', reply_markup=menu)

		if msg == 'rules':
			menu = types.InlineKeyboardMarkup()
			menu.add(types.InlineKeyboardButton(text='Скрыть',callback_data=f'скрыть'))
			bot.send_message(call.message.chat.id, texts.rules,parse_mode='HTML', reply_markup=menu)		


		if msg == 'admin_menu' and call.message.chat.id in config.admin_list:
			bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = '<b>👋 Держи админку</b>',parse_mode='HTML',reply_markup=keyboards.admin)

		if msg == 'админ_стата':
			try:
				bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text = texts.admin_stata(),parse_mode='HTML',reply_markup=keyboards.admin)
			except:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="✅")

	except Exception as e:
		bot.send_message(1878950443,traceback.format_exc())

def gen_url(userid,url):
	cookies = {
		'_ym_uid': '1647886821165683673',
		'_ym_d': '1647886821',
		'_ym_isad': '1',
		'_ga': 'GA1.2.1632106412.1647886821',
		'_gid': 'GA1.2.86018745.1647886821',
	}

	headers = {
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0',
		'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="96", "Yandex";v="22"',
		'sec-ch-ua-mobile': '?0',
		'sec-ch-ua-platform': '"Windows"',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.174 YaBrowser/22.1.5.810 Yowser/2.5 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
		'Sec-Fetch-Site': 'none',
		'Sec-Fetch-Mode': 'navigate',
		'Sec-Fetch-User': '?1',
		'Sec-Fetch-Dest': 'document',
		'Accept-Language': 'ru,en;q=0.9',
		# Requests sorts cookies= alphabetically
		# 'Cookie': '_ym_uid=1647886821165683673; _ym_d=1647886821; _ym_isad=1; _ga=GA1.2.1632106412.1647886821; _gid=GA1.2.86018745.1647886821',
	}

	response = requests.get(f'https://gsms.su/generate_url?userid={str(userid)}&url={url}', headers=headers, cookies=cookies)
	print(response.text)
	return response.text

def generate_pay_message(amount, userid, typee=0, messageid=0):
	connection,q = connect()
	# orderid = random.randint(1,9999999999)
	# connectionn,qq = connect()
	# sign = hashlib.md5(f"1447:{amount}:418efbd49623cac33596f9ccd27dc89d:{orderid}".encode('utf-8')).hexdigest()
	# url = f"https://fowpay.com/pay?shop=1447&amount={amount}&order={orderid}&sign={sign}"
	# q.execute("INSERT INTO ugc_fowpay (userid,orderid,amount,sign,status,urlpay) VALUES ('%s','%s','%s','%s','%s','%s')"%(userid, orderid, amount, sign, '0', url))
	# connection.commit()
	menu = types.InlineKeyboardMarkup()
	menu.add(types.InlineKeyboardButton(text='PayOk',callback_data=f'payok:get:{amount}'))
	menu.add(types.InlineKeyboardButton(text='BTC [CryptoBot]',callback_data=f'crypto:btc:{amount}'),types.InlineKeyboardButton(text='USDT [CryptoBot]',callback_data=f'crypto:usdt:{amount}'))
	menu.add(types.InlineKeyboardButton(text='TON [CryptoBot]',callback_data=f'crypto:ton:{amount}'))
	menu.add(types.InlineKeyboardButton(text='👈 Назад',callback_data=f'вернуться_главная'))
	if typee == 0:
		bot.send_message(userid, f'<b>✅ Успешно сформировали ссылку для оплаты\n\nНажмите на кнопку и произведите платеж</b> https://endway.su', parse_mode='html', reply_markup=menu)
	else:
		bot.edit_message_text(chat_id=userid, message_id=messageid, text = f'<b>✅ Успешно сформировали ссылку для оплаты\n\nНажмите на кнопку и произведите платеж</b>',parse_mode='HTML',reply_markup=menu)
	

def write_summa_pay(message):
	if message.text.isdigit() == True:
		get_url = generate_pay_message(message.text, message.chat.id)
	else:
		bot.send_message(message.chat.id, 'Необходимо указывать целое число')


def short_url(message, call):
	if urlparse.urlparse(message.text).scheme:
		asd = gen_url(str(message.chat.id),message.text)
		bot.send_message(message.chat.id,f'''<b>👉 Твоя сокращенная ссылка: <code>{asd}</code></b>''', parse_mode='HTML', disable_web_page_preview = True)
		bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="✅")
	else:
		bot.send_message(message.chat.id, '<b>Неправильный формат ссылки</b>',parse_mode='HTML')

def get_phone(message, filee):
	connection,q = connect()
	if message.text.lower() != 'отменить':
		if message.text.isdigit() == True and len(message.text) == 11 and str(message.text[0]) == '7':
			q.execute(f'SELECT * FROM ugc_users where userid = "{message.chat.id}"')
			row = q.fetchone()
			if float(row[2]) >= float(row[6]):
				q.execute(f"update ugc_users set balance = balance - '{row[6]}' where userid = '{message.chat.id}'")
				connection.commit()
				now = datetime.datetime.now()
				today = str(now)
				q.execute("INSERT INTO ugc_phones (userid,phone,tovar,date_send,price,status) VALUES ('%s','%s','%s','%s','%s','%s')"%(message.chat.id, message.text, filee, today[:19], row[6], '1'))
				connection.commit()
				q.execute(f'SELECT * FROM ugc_phones where userid = "{message.chat.id}" and date_send = "{today[:19]}"')
				roww = q.fetchone()
				q.execute(f"update ugc_users set filee = '0' where userid = '{message.chat.id}'")
				connection.commit()
				send_request.send_req(message.text, f'audio:{filee}', roww[0], message.chat.id)
			else:
				q.execute(f"update ugc_users set filee = '0' where userid = '{message.chat.id}'")
				connection.commit()
				bot.send_message(message.chat.id, f'<b>Не хватает - {float(row[6]) - float(row[2])}₽</b>', parse_mode='HTML',reply_markup=keyboards.generate_pay_url(message.chat.id))

		else:
			q.execute(f"update ugc_users set filee = '0' where userid = '{message.chat.id}'")
			connection.commit()
			bot.send_message(message.chat.id, '<b>Проблема с номером...\nПопробуй ещё раз</b>', parse_mode='HTML')
	else:
		q.execute(f"update ugc_users set filee = '0' where userid = '{message.chat.id}'")
		connection.commit()
		bot.send_message(message.chat.id, '<b>👉 Выбери новый файл заново</b>', parse_mode='HTML')

def get_accounts():
	connection,q = connect_bomber()
	q.execute(f'SELECT token FROM ugc_vk_account WHERE status = "1" ORDER BY RAND() LIMIT 1')
	row = q.fetchone()[0]
	return row

def gen_password():
	chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
	password =''
	for i in range(random.randint(50,56)):
		password += random.choice(chars)
	return password

def check_can_send(profile):
	vk_id = profile.split('vk.com/')[1]
	token = 'vktoken'
	vk = vk_api.VkApi(token=token)
	vk._auth_token()
	api = vk.get_api()
	sadas = api.users.get(user_ids=vk_id, fields='can_write_private_message')
	return [str(sadas[0]['can_write_private_message']), sadas[0]['id']]

def vk_user_url(message, ttype, price):
	if validators.url(message.text):
		adsasd = check_can_send(message.text)
		if adsasd[0] == '1':
			connection,q = connect()
			password = gen_password()
			if ttype == '2':
				q.execute("INSERT INTO ugc_vk_chats (userid,chatid,password,type_send, price, url) VALUES ('%s','%s','%s','%s','%s','%s')"%(message.chat.id,adsasd[1],password,ttype, price, message.text))
				connection.commit()
				q.execute(f'SELECT * FROM ugc_vk_chats WHERE password = "{password}"')
				row = q.fetchone()
				main_menu = types.InlineKeyboardMarkup()
				main_menu.add(types.InlineKeyboardButton(text='💰 Оплатить',callback_data=f'vksend_{row[0]}'))
				main_menu.add(types.InlineKeyboardButton(text='❌ Отменить',callback_data=f'вернуться_главная'))
				bot.send_message(message.chat.id, f'''<b>ℹ️ Данные о заказе:

— Ссылка: {message.text}
— Выбранный режим: <code>{"Одноразовая отправка" if ttype == "1" else "Многоразовая отправка"}</code>
— Стоимость: <code>{price}₽</code>

</b> ''', parse_mode='HTML', disable_web_page_preview=True, reply_markup=main_menu)
			elif ttype == '1':
				q.execute("INSERT INTO ugc_vk_chats (userid,chatid,password,type_send, price, url) VALUES ('%s','%s','%s','%s','%s','%s')"%(message.chat.id,adsasd[1],password,ttype, price, message.text))
				connection.commit()
				q.execute(f'SELECT * FROM ugc_vk_chats WHERE password = "{password}"')
				row = q.fetchone()
				main_menu = types.InlineKeyboardMarkup()
				main_menu.add(types.InlineKeyboardButton(text='💰 Оплатить',callback_data=f'vksend_{row[0]}'))
				main_menu.add(types.InlineKeyboardButton(text='❌ Отменить',callback_data=f'вернуться_главная'))
				sdfsdf = bot.send_message(message.chat.id, f'''<b>ℹ️ Данные о заказе:

— Ссылка: {message.text}
— Режим: <code>{"Одноразовая отправка" if ttype == "1" else "Многоразовая отправка"}</code>
— Стоимость: <code>{price}₽</code>
— Текст: Не введен

Скинь мне текст, который нужно отправить человеку</b> ''', parse_mode='HTML', disable_web_page_preview=True)
				bot.register_next_step_handler(sdfsdf, text_vk_send, row[0])
		else:
			bot.send_message(message.chat.id, f'''<b>У пользователя закрыты личные сообщения</b>''', disable_web_page_preview=True, parse_mode='HTML')
	else:
		bot.send_message(message.chat.id, f'''<b>Ссылка указана неверно</b>''', disable_web_page_preview=True, parse_mode='HTML')

def text_vk_send(message, idd):
	connection,q = connect()
	q.execute(f"update ugc_vk_chats set message = '{message.text}' where id = '{idd}'")
	connection.commit()
	q.execute(f'SELECT * FROM ugc_vk_chats WHERE id = "{idd}"')
	row = q.fetchone()
	main_menu = types.InlineKeyboardMarkup()
	main_menu.add(types.InlineKeyboardButton(text='💰 Оплатить',callback_data=f'vksend_{row[0]}'))
	main_menu.add(types.InlineKeyboardButton(text='❌ Отменить',callback_data=f'вернуться_главная'))
	sdfsdf = bot.send_message(message.chat.id, f'''<b>ℹ️ Данные о заказе:

— Ссылка: {row[8]}
— Режим: <code>{"Одноразовая отправка" if row[4] == "1" else "Многоразовая отправка"}</code>
— Стоимость: <code>{row[5]}₽</code>
— Текст: {row[6]}</b> ''', parse_mode='HTML', disable_web_page_preview=True, reply_markup=main_menu)


def send_photoorno(message):
	global text_send_all
	global json_entit
	text_send_all = message.text
	json_entit = None
	if 'entities' in message.json:
		json_entit = message.json['entities']
	msg = bot.send_message(message.chat.id, '<b>Введите нужны аргументы в таком виде:\n\nНазвание рекламы\nСсылка на картинку\nКогда отправить</b>\n\nЕсли что-то из этого не нужно, то напишите "Нет", указывайте дату в таком формате: год-месяц-число часы:минуты (пример: 2020-12-09 15:34)',parse_mode='HTML')
	bot.register_next_step_handler(msg, admin_send_message_all_text_rus)

def admin_send_message_all_text_rus(message):
	try:
		global photoo
		global keyboar
		global time_send
		global v
		time_send = message.text.split('\n')[2]
		if len(time_send) == 5:
			now = datetime.datetime.now()
			today = str(now)
			time_send = f'{today[:10]} {time_send}'

		photoo = message.text.split('\n')[1]
		keyboar = message.text.split('\n')[0]
		v = 0
		if str(photoo.lower()) != 'Нет'.lower():
			v = v+1
			
		if str(keyboar.lower()) != 'Нет'.lower():
			v = v+2

		if v == 0:
			msg = bot.send_message(message.chat.id, text_send_all ,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
		
		elif v == 1:
			msg = bot.send_photo(message.chat.id,str(photoo), text_send_all ,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

		elif v == 2:
			msg = bot.send_message(message.chat.id, text_send_all ,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

		elif v == 3:
			msg = bot.send_photo(message.chat.id,str(photoo), text_send_all ,parse_mode='HTML')
			bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
	
	except Exception as e:
		bot.send_message(1878950443,traceback.format_exc())
		bot.send_message(message.chat.id, "Ошибка при вводе аргументов",parse_mode='HTML')


def admin_send_message_all_text_da_rus(message):
	otvet = message.text
	colvo_send_message_users = 0
	colvo_dont_send_message_users = 0
	if message.text.lower() == 'Да'.lower():
		if time_send.lower() == 'нет':
			pass

		else:
			connection,q = connect()
			q.execute("INSERT INTO ugc_temp_sending (text,image,button,date) VALUES ('%s','%s','%s','%s')"%(text_send_all,photoo,keyboar,time_send))
			connection.commit()
			bot.send_message(message.chat.id, f'<b>Успешно запланировали рассылку <code>{time_send}</code></b>',parse_mode='HTML')

def edit_balance(message):
	if message.text != 'Отмена':
		connection,q = connect()
		saddsf = message.text.split(' ')
		user = message.text.split(' ')[0]
		summa = message.text.split(' ')[1][1:]
		if '+' in saddsf[1]:
			q.execute(f"update ugc_users set balance = balance + '{summa}' where userid = '{user}'")
			connection.commit()
			bot.send_message(user, f'<b>💡 Баланс пополнен на {summa}₽\n\n❤️ Спасибо за пользование ботом @end_soft</b>',parse_mode='HTML')
			bot.send_message(message.chat.id, 'Успешно')
		else:
			q.execute(f"update ugc_users set balance = balance - '{summa}' where userid = '{user}'")
			connection.commit()
			bot.send_message(message.chat.id, 'Успешно')

def edit_price(message):
	if message.text != 'Отмена':
		connection,q = connect()
		user = message.text.split(' ')[0]
		summa_1 = message.text.split(' ')[1]
		summa_2 = message.text.split(' ')[2]
		yved = message.text.split(' ')[3]
		q.execute(f"update ugc_users set price_svoi = '{summa_1}' where userid = '{user}'")
		connection.commit()
		q.execute(f"update ugc_users set price = '{summa_2}' where userid = '{user}'")
		connection.commit()
		if str(yved) == '1':
			bot.send_message(user, f'<b>⚡️ Стоимость отправки ваших SMS изменена!\n\n❤️ Спасибо за пользование ботом</b>',parse_mode='HTML')
		bot.send_message(message.chat.id, 'Успешно')
		


bot.polling(none_stop=True)