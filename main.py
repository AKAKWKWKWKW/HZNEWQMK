# -*- coding: utf-8 -*-
from __future__ import print_function
from pprint import pprint
from messente_api import OmnimessageApi, SMS, Omnimessage, Configuration, ApiClient
from messente_api.rest import ApiException
import telebot
import datetime
from telebot import types, apihelper
import sqlite3
import config
import random
import time
import json
from light_qiwi import Qiwi, OperationType
import keyboards
import requests
import transliterate
import sys

configuration = Configuration()
configuration.username = "63ea746bfc3449b2a1c7a88866cd11e9"
configuration.password = "ea6813327c16427cb9c910306e963c3b"

api_instance = OmnimessageApi(ApiClient(configuration))

number_send_sms = '+79950104458'
id_compani_prozvon = '1690659919'
api_prozvon = 'e2637e021c1238f6f481f9b6cc0ace36'


clck_url = 'https://clck.ru/--?url='
clck_url_2 = 'https://uni.su/api/?url='
clck_url_3 = 'https://is.gd/create.php?format=simple&url='
clck_url_4 = 'https://v.gd/create.php?format=simple&url='

# create an instance of the API class

bot = telebot.TeleBot(config.bot_token)

bot2 = telebot.TeleBot(config.bot_token)


@bot.message_handler(commands=['start'])
def start_message(message):
	userid = str(message.chat.id)
	username = str(message.from_user.username)
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	q = q.execute('SELECT * FROM ugc_users WHERE id IS '+str(userid))
	row = q.fetchone()
	if row is None:
		q.execute("INSERT INTO ugc_users (id,name,balans,ref,ref_colvo,rules,rules_1,statys) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')"%(userid,username,'0','0','0','12','20','Активен'))
		connection.commit()
		if message.text[7:] != '':
			if message.text[7:] != userid:
				q.execute("update ugc_users set ref = " + str(message.text[7:])+ " where id = " + str(userid))
				connection.commit()
				q.execute("update ugc_users set ref_colvo =ref_colvo + 1 where id = " + str(message.text[7:]))
				connection.commit()
				bot.send_message(message.text[7:], f'Новый реферал! <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML')
		msg = bot.send_message(message.chat.id,f'👑 Добро пожаловать, <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)
	else:
		if row[3] == '0':
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT * FROM reklama")
			row = q.fetchall()
			#text = ''
			#keyboard = types.InlineKeyboardMarkup()
			#for i in row:
	#			text = f'{text}<a href="{i[2]}">{i[1]}</a>\n➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖\n'
#			keyboard.add(types.InlineKeyboardButton(text='💰 Купить ссылку',callback_data='buy_reklama'))
#			bot.send_message(message.chat.id, f'''<b>💎 Реклама:</b>

#{text}
#''' ,parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)
			bot.send_message(message.chat.id,f'👑 Добро пожаловать, <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)
		else:
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT * FROM reklama")
			row = q.fetchall()
			#text = ''
			#keyboard = types.InlineKeyboardMarkup()
			#for i in row:
				#text = f'{text}<a href="{i[2]}">{i[1]}</a>\n➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖\n'
			#keyboard.add(types.InlineKeyboardButton(text='💰 Купить ссылку',callback_data='buy_reklama'))
			#bot.send_message(message.chat.id, f'''<b>💎 Реклама:</b>

#{text}
#''' ,parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)
			bot.send_message(message.chat.id,f'👑 Добро пожаловать, <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)

@bot.message_handler(content_types=['text'])
def send_text(message):
	connection = sqlite3.connect('database.sqlite')
	q = connection.cursor()
	q = q.execute(f'SELECT statys FROM ugc_users WHERE id = {message.chat.id}')
	botb = q.fetchone()
	if botb[0] == 'Активен':

		if message.text.lower() == '/admin':
			if message.chat.id == config.admin:

				msg = bot.send_message(message.chat.id, '<b>Привет, админ!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
		elif message.text.lower() == 'добавление':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, '<b>Введите новые параметры в таком виде:\n\nСервис\n\nТекст смс</b>\n\n<i>Список сервисов:</i> <code>avito</code>,<code>avito_2</code>,<code>youla</code>,<code>youla_2</code>,<code>tk</code>,<code>tk_2</code>,',parse_mode='HTML',reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg, new_nametovars)

		elif message.text.lower() == 'удаление':
			if message.chat.id == config.admin:
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("SELECT * FROM sms")
				row = q.fetchall()
				q.close()
				text = ''
				for i in row:
					text = f'{text}id: <code>{i[0]}</code>| Текст сообшения: <code>{i[2]}</code>\n'
				msg = bot.send_message(message.chat.id, f'<b>Введите ID для удаления</b>\n\n<i>Список сервисов:</i>\n{text}',parse_mode='HTML',reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg, del_sms)

		
		elif message.text.lower() == 'добавить баланс':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, '<b>Введи id пользователя</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg, add_money1)

		elif message.text.lower() == 'снять с баланса':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, '<b>Введи id пользователя</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg, remove_money1)

		elif message.text.lower() == 'изменить прайс':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, '<b>Введи id пользователя</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg, edit_prace)

		elif message.text.lower() == 'изменить статус':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, '<b>Введите новый текст</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg, new_hellotext)

		elif message.text.lower() == 'изменить номер':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, '<b>Введите новый номер</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg, new_phone)

		elif message.text.lower() == 'изменить токен':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, '<b>Введите новый токен</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
				bot.register_next_step_handler(msg, new_token)

		elif message.text.lower() == 'пользователи':
			if message.chat.id == config.admin:
				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Найти пользователя',callback_data='admin_search_user'))
				bot.send_message(message.chat.id, '<b>Нажми на кнопку</b>',parse_mode='HTML', reply_markup=keyboard)

		elif message.text.lower() == 'настройки':
			if message.chat.id == config.admin:
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("SELECT qiwi_phone FROM config  where id = "+str(1))
				qiwi_phone = q.fetchone()
				q.execute("SELECT qiwi_token FROM config  where id = "+str(1))
				qiwi_token = q.fetchone()
				q.execute("SELECT rules FROM ugc_users  where id = "+str(1031811029))
				rules = q.fetchone()
				q.execute("SELECT rules_1 FROM ugc_users  where id = "+str(1031811029))
				rules_1 = q.fetchone()
				q.execute("SELECT rules FROM config  where id = "+str(1))
				prace_smska = q.fetchone()

				keyboard = types.InlineKeyboardMarkup()
				keyboard.add(types.InlineKeyboardButton(text='Изменить прайс смс',callback_data='изменитьценасмс_'),types.InlineKeyboardButton(text='Изменить прайс прозвона',callback_data='изменитьценапрозвон_'))
				keyboard.add(types.InlineKeyboardButton(text='Изменить номер QIWI',callback_data='изменитьномер_'),types.InlineKeyboardButton(text='Изменить Token QIWI',callback_data='изменитьтокен_'))
				keyboard.add(types.InlineKeyboardButton(text='Изменить прайс приема смс',callback_data='изменитьпрайсприемасмс'),types.InlineKeyboardButton(text='Изменить API',callback_data='изменить_api'))
				bot.send_message(message.chat.id, f'''<i>Номер QIWI:</i> <code>{qiwi_phone[0]}</code>
<i>Токен QIWI:</i> <code>{qiwi_token[0]}</code>
<i>Прайс смс:</i> <code>{rules[0]}</code>
<i>Прайс приема смс:</i> <code>{prace_smska[0]}</code>
<i>Прайс прозвона:</i> <code>{rules_1[0]}</code>''',parse_mode='HTML', reply_markup=keyboard)




		elif message.text.lower() == 'статистика':
			if message.chat.id == config.admin:
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				now = datetime.datetime.now()
				tt = now.strftime('%d.%m.%Y')
				ttm = now.strftime('%m.%Y')
				# Хуйня берущаяся из базы: кол-во, суммы
				count_users= q.execute(f"SELECT count(id) from ugc_users").fetchone()[0]
				count_buys_segodna = q.execute(f"SELECT count(id) from ugc_buys WHERE date LIKE '%{tt}%'").fetchone()[0]
				count_earn_segodna = q.execute(f"SELECT sum(price) from ugc_buys WHERE date LIKE '%{tt}%'").fetchone()[0]
				count_buys_month = q.execute(f"SELECT count(id) from ugc_buys WHERE date LIKE '%{ttm}%'").fetchone()[0]
				count_earn_month = q.execute(f"SELECT sum(price) from ugc_buys WHERE date LIKE '%{ttm}%'").fetchone()[0]
				vsego = q.execute(f"SELECT count(id) from ugc_buys").fetchone()
				summ = q.execute(f"SELECT sum(price) from ugc_buys").fetchone()
				q.execute("SELECT balans_user FROM statistika  where id = "+str(1))
				balans_user = q.fetchone()
				q.execute("SELECT balans_service FROM statistika  where id = "+str(1))
				balans_service = q.fetchone()
				q.execute("SELECT sms_send FROM statistika  where id = "+str(1))
				sms_send = q.fetchone()
				q.execute("SELECT login FROM api_service  where id = "+str(1))
				login = q.fetchone()
				q.execute("select sum(balans) from ugc_users")
				wdadwawd = q.fetchone()
				q.execute("SELECT key_api FROM api_service  where id = "+str(1))
				key_api = q.fetchone()
				q.execute("SELECT balans FROM ugc_users WHERE id = "+str(1031811029))
				odin_akk = q.fetchone()
				q.execute("SELECT balans FROM ugc_users WHERE id = "+str(1075335116))
				dva_akk = q.fetchone()
				q.execute("SELECT key_api FROM api_service  where id = "+str(1))
				key_api = q.fetchone()
				count_sms = q.execute(f"SELECT count(login_api) from baza_api").fetchone()[0]
				nobaza2 = float(wdadwawd[0]) - float(odin_akk[0])
				nobaza2 = float(nobaza2) - float(dva_akk[0])
				wwwwwwwwwwwwad = float(nobaza2) / float(10)
				awdawdawdawfffff = float(nobaza2) / float(20)
				r222 = requests.post(f"https://gateway.sms77.io/api/balance?p=ыыыыыыыыыыыыыыыыыыыыы")
				otvet2 = r222.text
				bot.send_message(message.chat.id, f'''<i>Всего пользователей:</i> <code>{count_users}</code>

	<b>Заработано</b>

	<i>• Cегодня:</i> <code>{'0' if count_earn_segodna==None else count_earn_segodna }</code> руб | <code>{count_buys_segodna}</code> шт
	<i>• В этом месяце:</i> <code>{'0' if count_earn_month==None else count_earn_month}</code> руб | <code>{count_buys_month}</code> шт
	<i>• Всего:</i> <code>{summ[0]}</code> руб | <code>{vsego[0]}</code> шт


	<b>Баланс пользователей:</b> <code>{int(nobaza2)}</code>

	<i>Примерно смс/звонков:</i> <code>{int(wwwwwwwwwwwwad)}</code> <b>/</b> <code>{int(awdawdawdawfffff)}</code>

	<i>Баланс сервиса:</i> <code>{otvet2}</code>




	''',parse_mode='HTML')
				q.close()
				connection.close()

		elif message.text.lower() == 'рассылка':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, 'Введите текст рассылки')
				bot.register_next_step_handler(msg, send_photoorno)

		elif message.text.lower() == 'изменить цену':
			if message.chat.id == config.admin:
				msg = bot.send_message(message.chat.id, 'Введите id')
				bot.register_next_step_handler(msg, new_prace)

		elif message.text.lower() == '/status':
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT hello_say FROM config where id = 1")
			hello_message = q.fetchone()
			bot.send_message(message.chat.id, str(hello_message[0]) + '',parse_mode='HTML', reply_markup=keyboards.main)

		elif message.text.lower() == 'отмена':
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute(f"SELECT * FROM sms_temp where id = '{message.chat.id}'")
			status = q.fetchone()
			if status != None:
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
				connection.commit()
				bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)
			else:
				bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)


		elif message.text.lower() == '📤 отправить сообщение':
			try:
				if 'member' == bot.get_chat_member(chat_id=config.subid, user_id=message.chat.id).status:
					print('yes_chat')
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute("SELECT rules FROM ugc_users  where id = "+str(message.chat.id))
					sms_prace = q.fetchone()
					keyboard = types.InlineKeyboardMarkup()
					#keyboard.add(types.InlineKeyboardButton(text=f'fead_10',callback_data='fead_10'))
					keyboard.add(types.InlineKeyboardButton(text=f'✏️ Написать сообщение',callback_data='svoi_text'))
					keyboard.add(types.InlineKeyboardButton(text=f'🔎 Узнать статус',callback_data='узнать_статус_sms'))
					keyboard.add(types.InlineKeyboardButton(text=f'✂️ Сократить ссылку',callback_data='сократить_ссылку'),types.InlineKeyboardButton(text=f'🔍 Пробить номер',callback_data='пробить_номер'))
					#keyboard.add(types.InlineKeyboardButton(text=f'♻️ Изменить тариф',callback_data='edit_praces'),types.InlineKeyboardButton(text=f'⚙️ Настройки',callback_data='нистроики'))

					bot.send_message(message.chat.id, f'Стоимость смс: {sms_prace[0]}р (любой сервис)' ,parse_mode='HTML', reply_markup=keyboard)
					bot.send_message(message.chat.id, f'<a href="https://t.me/c/1282085153/6">⚠️ Правила смс(кликабельно) за нарушение БАН!</a>' ,parse_mode='HTML')

				else:
					print('no_chat')
					podpiska = types.InlineKeyboardMarkup()
					podpiska.add(types.InlineKeyboardButton(text='✅ Вступить',url='https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ'))
					bot.send_message(message.chat.id,'<b>🔑 Извините, но для отправки сообшения, необходимо вступить <a href="https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ">в наш канал</a>!\n\n⚠️ После вступления повторите действия </b>', parse_mode='HTML', reply_markup=podpiska,disable_web_page_preview = True)
			except:
					print('no_chat_3')
					podpiska = types.InlineKeyboardMarkup()
					podpiska.add(types.InlineKeyboardButton(text='✅ Вступить',url='https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ'))
					bot.send_message(message.chat.id,'<b>🔑 Извините, но для отправки сообшения, необходимо вступить <a href="https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ">в наш канал</a>!\n\n⚠️ После вступления повторите действия </b>', parse_mode='HTML', reply_markup=podpiska,disable_web_page_preview = True)

		elif message.text.lower() == '📞 прозвон':
			try:
				if 'member' == bot.get_chat_member(chat_id=config.subid, user_id=message.chat.id).status:
					print('yes_chat')
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute("SELECT rules_1 FROM ugc_users  where id = "+str(message.chat.id))
					sms_prace = q.fetchone()
					keyboard = types.InlineKeyboardMarkup()
					#keyboard.add(types.InlineKeyboardButton(text=f'✏️ С',callback_data='svoi_text'),types.InlineKeyboardButton(text=f'📝 Шаблоны',callback_data='шаблоны'))
					keyboard.add(types.InlineKeyboardButton(text=f'✏️ Сделать прозвон',callback_data='svoi_text_prozvon'))
					keyboard.add(types.InlineKeyboardButton(text=f'🔎 Узнать статус',callback_data='узнать_статус'),types.InlineKeyboardButton(text=f'🔍 Пробить номер',callback_data='пробить_номер'))
					#keyboard.add(types.InlineKeyboardButton(text=f'♻️ Изменить тариф',callback_data='edit_praces'),types.InlineKeyboardButton(text=f'⚙️ Настройки',callback_data='нистроики'))

					bot.send_message(message.chat.id, f'Стоимость прозвона: {sms_prace[0]}р (за 1 минуту)\n\n⚠️ Данная функция озвучит ваш текст заданному абоненту\n' ,parse_mode='HTML', reply_markup=keyboard)
					bot.send_message(message.chat.id, f'<a href="https://t.me/c/1282085153/19">⚠️ Правила прозвона(кликабельно) за нарушение БАН!</a>' ,parse_mode='HTML')

				else:
					print('no_chat')
					podpiska = types.InlineKeyboardMarkup()
					podpiska.add(types.InlineKeyboardButton(text='✅ Вступить',url='https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ'))
					bot.send_message(message.chat.id,'<b>🔑 Извините, но для отправки сообшения, необходимо вступить <a href="https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ">в наш канал</a>!\n\n⚠️ После вступления повторите действия </b>', parse_mode='HTML', reply_markup=podpiska,disable_web_page_preview = True)
			except:
					print('no_chat_3')
					podpiska = types.InlineKeyboardMarkup()
					podpiska.add(types.InlineKeyboardButton(text='✅ Вступить',url='https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ'))
					bot.send_message(message.chat.id,'<b>🔑 Извините, но для отправки сообшения, необходимо вступить <a href="https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ">в наш канал</a>!\n\n⚠️ После вступления повторите действия </b>', parse_mode='HTML', reply_markup=podpiska,disable_web_page_preview = True)

		elif message.text.lower() == '📜 информация':
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT sms_send FROM statistika  where id = "+str(1))
			sms_send = q.fetchone()
			q.execute("SELECT sms_good FROM statistika  where id = "+str(1))
			sms_good = q.fetchone()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='🧑‍💻 Поддержка',url='https://t.me/LIFESMS_SUPPORT'))
			keyboard.add(types.InlineKeyboardButton(text='🗯 Чат',url='https://t.me/joinchat/R4qNuFYTK8E_pyjJmqXNYA'))
			bot.send_message(message.chat.id, f'''<b>📊 Статистика:</b>

	➖ <b>Отправленно смс:</b> <code>{sms_send[0]} </code>
	➖ <b>Прозвонов:</b> <code>{sms_good[0]} </code>
	''' ,parse_mode='HTML', reply_markup=keyboard)

		elif message.text.lower() == '🏪 магазин':
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='🔸 Прокси',callback_data='прокси'))
			bot.send_message(message.chat.id, f'''<b>💎 Добро пожаловать в наш мини маркет </b>''' ,parse_mode='HTML', reply_markup=keyboard)

		elif message.text.lower() == '📩 приём сообщений':
			try:
				if 'member' == bot.get_chat_member(chat_id=config.subid, user_id=message.chat.id).status:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute("SELECT rules FROM config  where id = "+str(1))
					prace_smska = q.fetchone()
					keyboard = types.InlineKeyboardMarkup()
					r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumbersStatus&country=0')
					data = json.loads(r.text)
					av_1ocolvo = data['av_1']
					ym_1colvo = data['ym_1']
					wa_0colvo = data['wa_0']
					tg_0colvo = data['tg_0']
					vi_0colvo = data['vi_0']
					keyboard.add(types.InlineKeyboardButton(text=f'🔹 Авито | {prace_smska[0]}р | {av_1ocolvo} шт',callback_data='авито_смс'))
					keyboard.add(types.InlineKeyboardButton(text=f'🔸 Юла | {prace_smska[0]}р | {ym_1colvo} шт',callback_data='юла_смс'))
					keyboard.add(types.InlineKeyboardButton(text=f'🔹 Whatsapp | {prace_smska[0]}р | {wa_0colvo} шт',callback_data='ватсап_смс'))
					keyboard.add(types.InlineKeyboardButton(text=f'🔸 Telegram | {prace_smska[0]}р | {tg_0colvo} шт',callback_data='телеграм_смс'))
					keyboard.add(types.InlineKeyboardButton(text=f'🔹 Viber | {prace_smska[0]}р | {vi_0colvo} шт',callback_data='вибер_смс'))
					bot.send_message(message.chat.id, f'''<b>Выберите сервис:</b>''' ,parse_mode='HTML', reply_markup=keyboard)

				else:
					print('no_chat')
					podpiska = types.InlineKeyboardMarkup()
					podpiska.add(types.InlineKeyboardButton(text='✅ Вступить',url='https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ'))
					bot.send_message(message.chat.id,'<b>🔑 Извините, но для отправки сообшения, необходимо вступить <a href="https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ">в наш канал</a>!\n\n⚠️ После вступления повторите действия </b>', parse_mode='HTML', reply_markup=podpiska,disable_web_page_preview = True)
			except:
					print('no_chat_3')
					podpiska = types.InlineKeyboardMarkup()
					podpiska.add(types.InlineKeyboardButton(text='✅ Вступить',url='https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ'))
					bot.send_message(message.chat.id,'<b>🔑 Извините, но для отправки сообшения, необходимо вступить <a href="https://t.me/joinchat/AAAAAExrESFZ_BsKzMMzZQ">в наш канал</a>!\n\n⚠️ После вступления повторите действия </b>', parse_mode='HTML', reply_markup=podpiska,disable_web_page_preview = True)






		elif message.text.lower() == '🖥 кабинет':
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT balans FROM ugc_users where id is " + str(message.chat.id))
			balanss = q.fetchone()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='⚜️ Пополнить баланс',callback_data='awhat_oplata'))
			keyboard.add(types.InlineKeyboardButton(text='🎁 Ваучеры',callback_data='vau'))
			q.execute("SELECT ref_colvo FROM ugc_users where id = " + str(message.chat.id))
			ref_colvoo = q.fetchone()
			bot.send_message(message.chat.id, '<b>🧟‍♂ id: '+str(message.chat.id)+'\n \n💰 Баланс:</b> ' + str(balanss[0]) + '\n \n👥Реферальная система\n \n▫️Что это?\nНаша уникальная реферальная система позволит вам заработать крупную сумму без вложений. Вам необходимо лишь приглашать друзей и вы будете получать пожизненно 5% от их пополнений в боте  \n \n📯Ваша реферальная ссылка: \nhttps://t.me/'+str(config.bot_name)+'?start='+str(message.chat.id)+'\n\n<b>Всего рефералов</b>:  ' + str(ref_colvoo[0]),parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)

		elif message.text.lower() == 'назад':
			msg = bot.send_message(message.chat.id, '<b>Вернулись назад</b>',parse_mode='HTML', reply_markup=keyboards.main)
	else:	
		bot.send_message(message.chat.id, '<b>Вы заблокированы за нарушение правил</b>',parse_mode='HTML')

def vau_add(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		if message.text.isdigit() == True:
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
			check_balans = q.fetchone()
			if float(check_balans[0]) >= int(message.text):
					colvo = 1
					dlina = 10
					chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
					for ttt in range(1):
						for n in range(10):
							id_sdelka =''
						for i in range(int(dlina)):
							id_sdelka += random.choice(chars)
					print(id_sdelka)
					q.execute("update ugc_users set balans = balans - "+str(message.text)+" where id = " + str(message.chat.id))
					connection.commit()
					q.execute("INSERT INTO vau (name,summa,adds) VALUES ('%s', '%s', '%s')"%(id_sdelka,message.text,message.chat.id))
					connection.commit()
					bot.send_message(message.chat.id, f'''🎁 Ваучер <code>{id_sdelka}</code>, успешно создан.''',reply_markup=keyboards.main, parse_mode='HTML')
					q.close()
					connection.close()
			else:
				msg = bot.send_message(message.chat.id, '⚠ Недостаточно средств')

		else:
			msg = bot.send_message(message.chat.id, '⚠ Ошибка!')
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def new_hellotext(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update config set hello_say = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def vau_good(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM vau where name = '{message.text}'")
		status = q.fetchone()
		if status != None:
			print("yes")
			q.execute(f"SELECT summa FROM vau where name = '{message.text}'")
			summa = q.fetchone()
			q.execute(f"SELECT adds FROM vau where name = '{message.text}'")
			adds = q.fetchone()
			q.execute("update ugc_users set balans = balans + "+str(summa[0])+" where id = " + str(message.chat.id))
			connection.commit()
			print(summa[0])
			q.execute(f"DELETE FROM vau WHERE name = '{message.text}'")
			connection.commit()
			bot.send_message(message.chat.id, f'''🎁 Ваучер <code>{message.text}</code>, успешно активирован. Ваш баланс пополнен на <code>{summa[0]}</code> RUB. ''',reply_markup=keyboards.main, parse_mode='HTML')
			bot.send_message(adds[0], f'''👤  <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>  активировал(а) ваучер <code>{message.text}</code>.''',reply_markup=keyboards.main, parse_mode='HTML')

		else:
			bot.send_message(message.chat.id, f'''🎁 Ваучер <code>{message.text}</code>, не сушествует или уже активирован.''',reply_markup=keyboards.main, parse_mode='HTML')
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную',reply_markup=keyboards.main)

def remove_money1(message):
	if message.text != 'Отмена':
		global textt
		textt = message.text
		msg = bot.send_message(message.chat.id, 'Введи сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, remove_money2)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def remove_money2(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update ugc_users set balans = balans -" + str( message.text ) +  " where id =" + str(id_user_edit_bal1111))
		connection.commit()
		msg = bot.send_message(message.chat.id, 'Успешно!',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def generator_url(message):
	try:
		if "https://" in str(message.text):
			bot.send_message(message.chat.id, f'♻️ Ожидайте, белка 🐿 кушает ссылки  !',parse_mode='HTML', reply_markup=keyboards.main)
			text = ''
			r = requests.get(f'https://bitly.su/api/?api=6cc27794b7d2d7cee3bf3d93141a7251b1cef652&url={message.text}')
			data = json.loads(r.text)
			link1 = data['shortenedUrl']
			linkRequest = {"destination": message.text, "domain": { "fullName": "rebrand.ly" }}
			requestHeaders = {"Content-type": "application/json","apikey": "a2b087f48d5c4b2785c9a80bf210ad96",}
			r = requests.post("https://api.rebrandly.com/v1/links", data = json.dumps(linkRequest), headers=requestHeaders)
			linkss = r.json()
			requestHeaders = {"Content-type": "application/x-www-form-urlencoded"}
			r = requests.post("https://goo.su/api/convert", data = f'token=9diDHhJOrxWgCMiwoiy9kkamxkUUGTocUlv7MuCJMQpuwpw0OlTcs5ObNOn4&url={message.text}', headers=requestHeaders)
			data = json.loads(r.text)
			link11 = str(data['short_url'])
			r2 = requests.get(f"{clck_url_2}{message.text}")
			r3 = requests.get(f"{clck_url_3}{message.text}")
			r4 = requests.get(f"{clck_url_4}{message.text}")
			text = f'0️⃣ {text}{link11}\n1️⃣ {text}{link1}\n3️⃣ https://{text}{r2.text}\n4️⃣ {text}{r3.text}\n5️⃣ {text}{r4.text}'
			bot.send_message(message.chat.id, f'⚒ Ваши сокращенные ссылки\n\n{text}',parse_mode='HTML',disable_web_page_preview = True, reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, f'⚒ Ссылка указана неверно!',parse_mode='HTML', reply_markup=keyboards.main)

	except:
		bot.send_message(message.chat.id, f'⚒ Произошла ошибка!',parse_mode='HTML', reply_markup=keyboards.main)

def generator_url_1(message):
	try:
		if "https://" in str(message.text):
			bot.send_message(message.chat.id, f'♻️ Ожидайте, белка 🐿 кушает ссылки  !',parse_mode='HTML', reply_markup=keyboards.main)
			r11111 = requests.get(f"https://oplata.uno/yourls-api.php?username=admin&password=2020896lol&action=shorturl&format=json&url={message.text}")
			data = json.loads(r11111.text)
			link_11 = str(data['shorturl'])
			r22222 = requests.get(f"https://oplata.live/yourls-api.php?username=admin&password=2020896lol&action=shorturl&format=json&url={message.text}")
			data = json.loads(r22222.text)
			link_22 = str(data['shorturl'])
			r33333 = requests.get(f"https://dostavka.uno/yourls-api.php?username=admin&password=2020896lol&action=shorturl&format=json&url={message.text}")
			data = json.loads(r33333.text)
			link_33 = str(data['shorturl'])
			bot.send_message(message.chat.id, f'''<b>⚒ Ваши сокращенные ссылки:</b>
0️⃣ <code>{link_11}</code>
1️⃣ <code>{link_22}</code>
2️⃣ <code>{link_33}</code>''', parse_mode='HTML')
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("update ugc_users set balans = balans - "+str(5)+" where id = " + str(message.chat.id))
			connection.commit()
		else:
			bot.send_message(message.chat.id, f'⚒ Ссылка указана неверно!',parse_mode='HTML', reply_markup=keyboards.main)

	except:
		bot.send_message(message.chat.id, f'⚒ Произошла ошибка!',parse_mode='HTML', reply_markup=keyboards.main)

def del_sms(message):
	new_categggg = message.text
	if new_categggg != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f'DELETE FROM sms WHERE id = ' + str(new_categggg))
		connection.commit()
		bot.send_message(message.chat.id, 'Успешно!',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, "ℹ️ Выберите пунк меню:",parse_mode='HTML', reply_markup=keyboards.admin)

def yes_buy_reklama(message):
	global name_link_reklama
	name_link_reklama = message.text
	if name_link_reklama != 'Отмена':
		msg = bot.send_message(message.chat.id, '<b>Введите ссылку для обьявления:</b>',parse_mode='HTML')
		bot.register_next_step_handler(msg, yes_buy_reklama_1)	
	else:
		bot.send_message(message.chat.id, "⚠️ Отменили" , reply_markup=keyboards.main)

def add_money1(message):
   if message.text != 'Отмена':
      global textt
      textt = message.text
      msg = bot.send_message(message.chat.id, 'Введи сумму: ',parse_mode='HTML')
      bot.register_next_step_handler(msg, add_money2)
   else:
      bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def add_money2(message):
   if message.text != 'Отмена':
      connection = sqlite3.connect('database.sqlite')
      q = connection.cursor()
      q.execute("update ugc_users set balans = balans +" + str( message.text ) +  " where id =" + str(id_user_edit_bal1))
      connection.commit()
      msg = bot.send_message(message.chat.id, 'Успешно!',parse_mode='HTML', reply_markup=keyboards.admin)
   else:
      bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_api(message):
   if message.text != 'Отмена':
      global login_api
      login_api = message.text
      msg = bot.send_message(message.chat.id, 'Введи ключ api',parse_mode='HTML')
      bot.register_next_step_handler(msg, new_api_2)
   else:
      bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_api_2(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update api_service set login = '"+str(login_api)+"' where id = '1'")
		connection.commit()
		q.execute("update api_service set key_api = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, 'Успешно!',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def edit_prace(message):
   if message.text != 'Отмена':
      global texttt
      texttt = message.text
      msg = bot.send_message(message.chat.id, 'Введи сумму: ',parse_mode='HTML')
      bot.register_next_step_handler(msg, edit_prace_2)
   else:
      bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def edit_prace_2(message):
   if message.text != 'Отмена':
      connection = sqlite3.connect('database.sqlite')
      q = connection.cursor()
      q.execute("update ugc_users set rules = " + str( message.text ) +  " where id =" + str(id_user_edit))
      connection.commit()
      msg = bot.send_message(message.chat.id, 'Успешно!',parse_mode='HTML', reply_markup=keyboards.admin)
   else:
      bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def yes_buy_reklama_1(message):
	link_link_reklama = message.text
	if link_link_reklama != 'Отмена':
		if "https://" in str(message.text):
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
			check_balans = q.fetchone()
			if float(check_balans[0]) >= int(500):
				q.execute("INSERT INTO reklama (id,text,linkk) VALUES ('%s', '%s', '%s')"%('1',name_link_reklama, link_link_reklama))
				connection.commit()
				onnection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("update statistika set balans_user = balans_user -" + str('500') +  " where id =" + str(1))
				connection.commit()
				bot.send_message(message.chat.id, '<b>Готово</b>',parse_mode='HTML', reply_markup=keyboards.main)
			else:
				bot.send_message(message.chat.id, '⚠ Недостаточно средств')
		else:
			msg = bot.send_message(message.chat.id, 'Ошибка, отправьте ссылку:')
			bot.register_next_step_handler(msg, yes_buy_reklama_1)
	else:
		bot.send_message(message.chat.id, "⚠️ Отменили" , reply_markup=keyboards.main)

def new_phone(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update config set qiwi_phone = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_prace_prozvon(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update ugc_users set rules_1 = '"+str(message.text)+"'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_prace_sms(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update ugc_users set rules = '"+str(message.text)+"'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_token(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update config set qiwi_token = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_prace_apii(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update api_service set key_api = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def new_prace_sms_ppp(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("update config set rules = '"+str(message.text)+"' where id = '1'")
		connection.commit()
		msg = bot.send_message(message.chat.id, '<b>Успешно!</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, 'Вернулись в админку',parse_mode='HTML', reply_markup=keyboards.admin)

def send_photoorno(message):
	global text_send_all
	text_send_all = message.text
	msg = bot.send_message(message.chat.id, '<b>Введите нужны аргументы в таком виде:\n\nСсылка куда отправит кнопка\nСсылка на картинку</b>\n\nЕсли что-то из этого не нужно, то напишите "Нет"',parse_mode='HTML')
	bot.register_next_step_handler(msg, admin_send_message_all_text_rus)

def admin_send_message_all_text_rus(message):
		global photoo
		global keyboar
		global v
		try:
			photoo = message.text.split('\n')[1]
			keyboar = message.text.split('\n')[0]
			v = 0
			if str(photoo.lower()) != 'Нет'.lower():
				v = v+1
				
			if str(keyboar.lower()) != 'Нет'.lower():
				v = v+2

			if v == 0:
				msg = bot.send_message(message.chat.id, "Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML')
				bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
			
			elif v == 1:
				msg = bot.send_photo(message.chat.id,str(photoo), "Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML')
				bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

			elif v == 2:
				keyboard = types.InlineKeyboardMarkup(row_width=1)
				keyboard.add(types.InlineKeyboardButton(text='Перейти',url=f'{keyboar}'))
				msg = bot.send_message(message.chat.id, "Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML',reply_markup=keyboard)
				bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)

			elif v == 3:
				keyboard = types.InlineKeyboardMarkup(row_width=1)
				keyboard.add(types.InlineKeyboardButton(text='Перейти',url=f'{keyboar}'))
				msg = bot.send_photo(message.chat.id,str(photoo), "Отправить всем пользователям уведомление:\n" + text_send_all +'\n\nЕсли вы согласны, напишите Да',parse_mode='HTML',reply_markup=keyboard)
				bot.register_next_step_handler(msg, admin_send_message_all_text_da_rus)
		except:
			bot.send_message(message.chat.id, 'Аргументы указаны неверно!')	


def admin_send_message_all_text_da_rus(message):
	otvet = message.text
	colvo_send_message_users = 0
	colvo_dont_send_message_users = 0
	if message.text.lower() == 'Да'.lower():
		connection = sqlite3.connect('database.sqlite')
		with connection:	
			q = connection.cursor()
			bot.send_message(message.chat.id, 'Начинаем отправлять!')
			if v == 0:
				q.execute("SELECT * FROM ugc_users")
				row = q.fetchall()
				for i in row:
					jobid = i[0]
					time.sleep(0.2)
					response = requests.post(
						url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendMessage"),
						data={'chat_id': jobid, 'text': str(text_send_all),'parse_mode': 'HTML'}
					).json()
					if response['ok'] == False:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1
					else:
						colvo_send_message_users = colvo_send_message_users + 1;
				bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	
			elif v == 1:
				q.execute("SELECT * FROM ugc_users")
				row = q.fetchall()
				for i in row:
					jobid = i[0]


					time.sleep(0.1)
					response = requests.post(
						url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendPhoto"),
						data={'chat_id': jobid,'photo': str(photoo), 'caption': str(text_send_all),'parse_mode': 'HTML'}
					).json()
					if response['ok'] == False:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1
					else:
						colvo_send_message_users = colvo_send_message_users + 1;
				bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	

			elif v == 2:
				q.execute("SELECT * FROM ugc_users")
				row = q.fetchall()
				for i in row:
					jobid = i[0]

					time.sleep(0.1)
					reply = json.dumps({'inline_keyboard': [[{'text': '♻️ Перезапустить бот', 'callback_data': f'restart'}]]})
					response = requests.post(
						url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendMessage"),
						data={'chat_id': jobid, 'text': str(text_send_all), 'reply_markup': str(reply),'parse_mode': 'HTML'}
					).json()
					if response['ok'] == False:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1
					else:
						colvo_send_message_users = colvo_send_message_users + 1;
				bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	
			elif v == 3:
				q.execute("SELECT * FROM ugc_users")
				row = q.fetchall()
				for i in row:
					jobid = i[0]

					time.sleep(0.1)
					reply = json.dumps({'inline_keyboard': [[{'text': '♻️ Перезапустить бот', 'callback_data': f'restart'}]]})
					response = requests.post(
						url='https://api.telegram.org/bot{0}/{1}'.format(config.bot_token, "sendPhoto"),
						data={'chat_id': jobid,'photo': str(photoo), 'caption': str(text_send_all),'reply_markup': str(reply),'parse_mode': 'HTML'}
					).json()
					if response['ok'] == False:
						colvo_dont_send_message_users = colvo_dont_send_message_users + 1
					else:
						colvo_send_message_users = colvo_send_message_users + 1;
				bot.send_message(message.chat.id, 'Отправлено сообщений: '+ str(colvo_send_message_users)+'\nНе отправлено: '+ str(colvo_dont_send_message_users))	


	elif message.text == 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("delete from dep WHERE id_user = " + str(message.chat.id))
		connection.commit()
		q.close()
		connection.close()
		bot.send_message(message.chat.id, "Вернулись на главную", reply_markup=keyboards.main)


def adminsendmessage(message):
	if message.text.lower() != 'отмена':
		bot.send_message(iduserasend, str(message.text),parse_mode='HTML')
		bot.send_message(message.chat.id, '<b>Отправленно</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.admin)

def btc_oplata(message):
	if message.text != 'Отмена':
		try:
			price = int(message.text)
			if str(price).isdigit() == True:
				if int(price) < 100:
					msg = bot.send_message(message.chat.id, 'Cумма пополнения меньше 100 руб')
					bot.register_next_step_handler(msg, btc_oplata)
				else:
					msg = bot.send_message(message.chat.id, f"<b>ℹ️ Отправьте BTC ЧЕК на сумму:{message.text}</b>", reply_markup=keyboards.main, parse_mode='HTML')
					bot.register_next_step_handler(msg, btc_oplata_1)

			else:
				msg = bot.send_message(message.chat.id, 'Вводить нужно целое-положительное число\n\nВведите другое число')
				bot.register_next_step_handler(msg, btc_oplata)
		except ValueError:
			msg = bot.send_message(message.chat.id, 'Вводить нужно целое-положительное число\n\nВведите другое число')
			bot.register_next_step_handler(msg, btc_oplata)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)

def searchuser(message):
	if message.text.lower() != 'отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute(f"SELECT * FROM ugc_users where name = '{message.text}'")
		row = q.fetchone()
		bot.send_message(message.chat.id, '<b>🔍 Ищем...</b>',parse_mode='HTML', reply_markup=keyboards.admin)
		if row != None:
			vsegosms = q.execute(f"SELECT count(id) from logi WHERE id = '{row[0]}' and text = '{row[0]}'").fetchone()
			keyboard = types.InlineKeyboardMarkup()
			keyboard.add(types.InlineKeyboardButton(text='✉ Написать',callback_data=f'написатьюзеру_{row[0]}'),types.InlineKeyboardButton(text='✔️ Изменить прайс',callback_data=f'изменитьпрайс_{row[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='🔒 Заблокировать',callback_data=f'заблокировать_{row[0]}'),types.InlineKeyboardButton(text='🔓 Раблокировать',callback_data=f'разблокировать_{row[0]}'))
			keyboard.add(types.InlineKeyboardButton(text='➕ Добавить баланс',callback_data=f'добавитьбаланс_{row[0]}'),types.InlineKeyboardButton(text='➖ Снять баланс',callback_data=f'снятьбаланс_{row[0]}'))
			msg = bot.send_message(message.chat.id, f'''<b>Подробнее:</b>

<b>username:</b> <b>@{row[1]}</b>
<b>Ид:</b> <code>{row[0]}</code>
<b>Рефералов:</b> <code>{row[4]}</code>
<b>Баланс:</b> <code>{row[2]}</code>
<b>Отправил:</b> <code>{vsegosms[0]}</code>
<b>Прайс смс:</b> <code>{row[5]}</code>
<b>Прайс прозвона:</b> <code>{row[6]}</code>
<b>Статус:</b> <code>{row[7]}</code>
''',parse_mode='HTML',reply_markup=keyboard)
		else:
			bot.send_message(message.chat.id, '<b>Нет такого пользователя</b>',parse_mode='HTML', reply_markup=keyboards.admin)
	else:
		bot.send_message(message.chat.id, '<b>Отменили</b>',parse_mode='HTML', reply_markup=keyboards.admin)

def btc_oplata_1(message):
	if message.text != 'Отмена':
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='Подтвердить',callback_data=f'good_oplata_btc_{message.chat.id}'))
		bot.send_message(message.chat.id, '♻️ Платеж проверяется, время зачисления 5-30 минут')
		bot.send_message(config.admin, f'#НОВЫЙЧЕК \n<a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a> \n {message.text}',parse_mode='HTML', reply_markup=keyboard)

		
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)

def svoi_text(message):
	svoi_texttt = message.text
	fname = svoi_texttt
	lines = 0
	words = 0
	letters = 0
	

	for line in fname:
  # Была получена очередная строка.
  # Она присваивается переменной line.
  # Счетчик строк следует увеличить на 1.
		lines += 1
		pos = 'out'
    # С помощью len определяется количество символов в строке
    # и добавляется к счетчику букв.
		letters += len(line)
 
    # Код ниже считает количество слов в текущей строке.
 
    # Флаг, сигнализирующий нахождение за пределами слова.
	
 
    # Цикл перебора строки по символам.
		for letter in line:
        # Если очередной символ не пробел, а флаг в значении "вне слова",
        # то значит начинается новое слово.
			if letter != ' ' and pos == 'out':
            # Поэтому надо увеличить счетчик слов на 1,
				words += 1
            # а флаг поменять на значение "внутри слова".
				pos = 'in'
        # Если очередной символ пробел,
			elif letter == ' ':
            # то следует установить флаг в значение "вне слова".
				pos = 'out'
 
# Вывод количеств строк, слов и символов на экран.print("Letters:", letters)
	if int(letters) <= 120:
		if message.text != 'Отмена':
			sms_link = message.text
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("INSERT INTO sms_temp (id,text,link) VALUES ('%s', '%s', '%s')"%(message.chat.id,sms_link,'0'))
			connection.commit()
			q.execute(f"SELECT text FROM sms_temp where id = {message.chat.id}")
			text_sms = q.fetchone()
			msg = bot.send_message(message.chat.id, '<b>ℹ️ Отправьте номер получателя:\n\nПример:</b> <code>79999999999</code>', parse_mode='HTML')
			bot.register_next_step_handler(msg, send_2)
		else:
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
			connection.commit()
			bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)
	else:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
		connection.commit()
		msg = bot.send_message(message.chat.id, 'Ошибка,более 120 символов отправьте новый текст с ссылкой:')
		bot.register_next_step_handler(msg, svoi_text)

def fead_10(message):
	fead_text = message.text
	fname = fead_text
	lines = 0
	words = 0
	letters = 0
	

	for line in fname:
  # Была получена очередная строка.
  # Она присваивается переменной line.
  # Счетчик строк следует увеличить на 1.
		lines += 1
		pos = 'out'
    # С помощью len определяется количество символов в строке
    # и добавляется к счетчику букв.
		letters += len(line)
 
    # Код ниже считает количество слов в текущей строке.
 
    # Флаг, сигнализирующий нахождение за пределами слова.
	
 
    # Цикл перебора строки по символам.
		for letter in line:
        # Если очередной символ не пробел, а флаг в значении "вне слова",
        # то значит начинается новое слово.
			if letter != ' ' and pos == 'out':
            # Поэтому надо увеличить счетчик слов на 1,
				words += 1
            # а флаг поменять на значение "внутри слова".
				pos = 'in'
        # Если очередной символ пробел,
			elif letter == ' ':
            # то следует установить флаг в значение "вне слова".
				pos = 'out'
 
# Вывод количеств строк, слов и символов на экран.print("Letters:", letters)
	if int(letters) >= 40:
		if message.text != 'Отмена':
			fead_text = message.text

			bot2.send_message(-1001220059847, f'''<b>Пользователь:</b> <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a>
<b>Отзыв:</b> {message.text}''', parse_mode='HTML')
			bot.send_message(message.chat.id, '''<b>♥️ Спасибо за отзыв.</b>''', parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.send_message(message.chat.id, 'отмена', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, 'Ошибка,менее 50 символов')

def svoi_text_prozvon(message):
	svoi_texttt = message.text
	fname = svoi_texttt
	lines = 0
	words = 0
	letters = 0
	

	for line in fname:
  # Была получена очередная строка.
  # Она присваивается переменной line.
  # Счетчик строк следует увеличить на 1.
		lines += 1
		pos = 'out'
    # С помощью len определяется количество символов в строке
    # и добавляется к счетчику букв.
		letters += len(line)
 
    # Код ниже считает количество слов в текущей строке.
 
    # Флаг, сигнализирующий нахождение за пределами слова.
	
 
    # Цикл перебора строки по символам.
		for letter in line:
        # Если очередной символ не пробел, а флаг в значении "вне слова",
        # то значит начинается новое слово.
			if letter != ' ' and pos == 'out':
            # Поэтому надо увеличить счетчик слов на 1,
				words += 1
            # а флаг поменять на значение "внутри слова".
				pos = 'in'
        # Если очередной символ пробел,
			elif letter == ' ':
            # то следует установить флаг в значение "вне слова".
				pos = 'out'
 
# Вывод количеств строк, слов и символов на экран.print("Letters:", letters)
	if int(letters) <= 500:
		if message.text != 'Отмена':
			sms_link = message.text
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("INSERT INTO sms_temp (id,text,link) VALUES ('%s', '%s', '%s')"%(message.chat.id,sms_link,'0'))
			connection.commit()
			q.execute(f"SELECT text FROM sms_temp where id = {message.chat.id}")
			text_sms = q.fetchone()
			msg = bot.send_message(message.chat.id, '<b>ℹ️ Отправьте номер получателя:\n\nПример:</b> <code>79999999999</code>', parse_mode='HTML')
			bot.register_next_step_handler(msg, send_2_2)
		else:
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
			connection.commit()
			bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)
	else:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
		connection.commit()
		msg = bot.send_message(message.chat.id, 'Ошибка,более 500 символов отправьте новый текст с ссылкой:')
		bot.register_next_step_handler(msg, svoi_text_prozvon)

def user_id_balance11(message):
	if message.text != 'Отмена':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		print(user_id_balance)
		q.execute(f"update ugc_users set balans = balans + {message.text} where id = {user_id_balance}")
		connection.commit()
		q.execute("update statistika set balans_user = balans_user -" + str(message.text) +  " where id =" + str(1))
		connection.commit()
		today = datetime.datetime.today()
		q.execute("INSERT INTO ugc_buys (idtovar,nametovar,date,data,userid,username,colvo,price,bot_name) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%('2124','afawf',today.strftime("%H:%M %d.%m.%Y"),'2124',message.chat.id,str(message.chat.first_name),'1',str(message.text), '212asas4'))
		connection.commit()
		bot.send_message(message.chat.id, 'Готово', reply_markup=keyboards.admin)
		bot.send_message(user_id_balance, 'Ваш баланс пополнен', reply_markup=keyboards.main)
	else:
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.admin)


def send_2(message):
	sms_momerrr = message.text
	if message.text != 'Отмена':

		qiwi_user = qiwi_user = message.text
		if qiwi_user[:1] == '7' and len(qiwi_user) == 11 or qiwi_user[:3] == '380' and len(qiwi_user[3:]) == 9 or qiwi_user[:3] == '375' and len(qiwi_user) <= 12:
			
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()

			q.execute("SELECT rules FROM ugc_users  where id = "+str(message.chat.id))
			sms_prace = q.fetchone()

			q.execute("SELECT numer FROM statistika  where id = "+str(1))
			numer = q.fetchone()

			q.execute(f"SELECT text FROM sms_temp where id = {message.chat.id}")
			text_sms = q.fetchone()

			q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
			check_balans = q.fetchone()

			q.execute("SELECT login FROM api_service  where id = "+str(1))
			login = q.fetchone()

			q.execute("SELECT key_api FROM api_service  where id = "+str(1))
			key_api = q.fetchone()


			if float(check_balans[0]) >= int(sms_prace[0]):
				bot.send_message(message.chat.id, '♻️ Отправляю, ожидайте.', reply_markup=keyboards.main)
				q.execute("update ugc_users set balans = balans - "+str(sms_prace[0])+" where id = " + str(message.chat.id))
				connection.commit()
				q.execute("update statistika set balans_user = balans_user -" + str(sms_prace[0]) +  " where id =" + str(1))
				connection.commit()
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				texttttt = f'''{sms_momerrr}'''
				q.execute("INSERT INTO logi (id,text) VALUES ('%s', '%s')"%(message.chat.id,texttttt))
				connection.commit()
				try:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute("SELECT * FROM baza_api DESC LIMIT 1")
					row = q.fetchall()
					for i in row:
						if int(i[2]) <= int(50000):
							print('<= 5 work')
							print(i[0])
							print(i[1])
							txt_sms = f'{text_sms[0]}'
							words = ['avito','авито','youla','юла']
							d = 0
							for n in words:
								if n not in txt_sms.lower():
									print('dd')
									d +=1
								elif n in words:
									print('ss')
									break

							if int(d) == len(words):
								print('yes')
							else:
								q.execute("update ugc_users set balans = balans - "+str(100)+" where id = " + str(message.chat.id))
								connection.commit()
								bot.send_message(message.chat.id, f'''Вы получили штраф 100р за нарушение правил отправки смс''', parse_mode='HTML')
							phone = f'{sms_momerrr}'
							txt_sms = f'{text_sms[0]}'
							textsmsska = transliterate.translit(txt_sms, reversed=True)
							url = "https://gateway.sms77.io/api/sms"
							payload = {'to': f'{phone}','text': f'{textsmsska}','return_msg_id': f'1'}
							headers = {"Authorization" : b"basic"}
							response = requests.request("POST", url, headers=headers, data = payload)
							print(response.text)
							otvet = response.text
							status_sms = otvet.split('\n')[0]
							id_smskaa = otvet.split('\n')[1]

							#r = requests.get(f'https://api.smsglobal.com/http-api.php?action=sendsms&user=3xs97wt0&password=LEKzxutp&from=79950095459&to={phone}&text={textsmsska}')
							q.execute(f"update baza_api set colvo = colvo + '1' where key_api = '{i[1]}'")
							connection.commit()
							q.execute("INSERT INTO logi (id,text) VALUES ('%s', '%s')"%(message.chat.id,message.chat.id))
							connection.commit()
							q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
							connection.commit()
							bot.send_message(-1001147741701, f'''#НоваясмсЮзер: <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a> 

{text_sms[0]}

{status_sms}

<code>{id_smskaa}</code>
''', parse_mode='HTML')
							keyboard = types.InlineKeyboardMarkup(row_width=1)
							keyboard.add(types.InlineKeyboardButton(text=f'📝 Написать отзыв о сервисе',callback_data='fead_10'))
							bot.send_message(message.chat.id, '⚠️ Оставьте пожалуйста отзыв о сервисе:', reply_markup=keyboard)
							bot.send_message(message.chat.id, f'''✅ Сообщение успешно отправлено !
id: <code>{id_smskaa}</code>''', reply_markup=keyboards.main, parse_mode='HTML')
							connection = sqlite3.connect('database.sqlite')
							q = connection.cursor()
							q.execute("update statistika set sms_send = sms_send +" + str(1) +  " where id =" + str(1))
							connection.commit()
					
						else:
							phone = f'{sms_momerrr}'
							txt_sms = f'{text_sms[0]}'
							textsmsska = transliterate.translit(txt_sms, reversed=True)
							r = requests.get(f'https://api.smsglobal.com/http-api.php?action=sendsms&user=3xs97wt0&password=LEKzxutp&from=79950095459&to={phone}&text={textsmsska}')
							q.execute(f"update baza_api set colvo = colvo + '1' where key_api = '{i[1]}'")
							connection.commit()
							q.execute("INSERT INTO logi (id,text) VALUES ('%s', '%s')"%(message.chat.id,message.chat.id))
							connection.commit()
							q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
							connection.commit()
							bot.send_message(-1001147741701, f'''#НоваясмсЮзер: <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a> 

{text_sms[0]}
''', parse_mode='HTML')
							keyboard = types.InlineKeyboardMarkup(row_width=1)
							keyboard.add(types.InlineKeyboardButton(text=f'📝 Написать отзыв о сервисе',callback_data='fead_10'))
							bot.send_message(message.chat.id, '⚠️ Оставьте пожалуйста отзыв о сервисе:', reply_markup=keyboard)
							bot.send_message(message.chat.id, '✅ Сообщение успешно отправлено', reply_markup=keyboards.main)
							connection = sqlite3.connect('database.sqlite')
							q = connection.cursor()
							q.execute("update statistika set sms_send = sms_send +" + str(1) +  " where id =" + str(1))
							connection.commit()
					

				except:
					#connection = sqlite3.connect('database.sqlite')
					#q = connection.cursor()
					#q.execute("update ugc_users set balans = balans + "+str(sms_prace[0])+" where id = " + str(message.chat.id))
					#connection.commit()
					#q.execute("update statistika set balans_user = balans_user +" + str(sms_prace[0]) +  " where id =" + str(1))
					#connection.commit()
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
					connection.commit()
					bot.send_message(message.chat.id, '⚠ Ошибка. Мы уже знаем и решаем проблему.')
					bot.send_message(config.admin, 'Ошибка отправки.')

			else:
				bot.send_message(message.chat.id, '⚠ Недостаточно средств')

		else: 
			msg = bot.send_message(message.chat.id, 'Ошибка, введите номер получателя:')
			bot.register_next_step_handler(msg, send_2)

	else:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
		connection.commit()
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)

def send_2_2(message):
	sms_momerrr = message.text
	if message.text != 'Отмена':

		qiwi_user = qiwi_user = message.text
		if qiwi_user[:1] == '7' and len(qiwi_user) == 11 or qiwi_user[:3] == '380' and len(qiwi_user[3:]) == 9 or qiwi_user[:3] == '375' and len(qiwi_user) <= 12:
			
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()

			q.execute("SELECT rules_1 FROM ugc_users  where id = "+str(message.chat.id))
			sms_prace = q.fetchone()

			q.execute("SELECT numer FROM statistika  where id = "+str(1))
			numer = q.fetchone()

			q.execute(f"SELECT text FROM sms_temp where id = {message.chat.id}")
			text_sms = q.fetchone()

			q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(message.chat.id))
			check_balans = q.fetchone()

			if float(check_balans[0]) >= int(sms_prace[0]):
				bot.send_message(message.chat.id, '♻️ Отправляю, ожидайте.', reply_markup=keyboards.main)
				q.execute("update ugc_users set balans = balans - "+str(sms_prace[0])+" where id = " + str(message.chat.id))
				connection.commit()
				q.execute("update statistika set balans_user = balans_user -" + str(sms_prace[0]) +  " where id =" + str(1))
				connection.commit()
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				texttttt = f'''{sms_momerrr}'''
				q.execute("INSERT INTO logi (id,text) VALUES ('%s', '%s')"%(message.chat.id,texttttt))
				connection.commit()
				try:

					r = requests.get(f'https://zvonok.com/manager/cabapi_external/api/v1/phones/call/?campaign_id={id_compani_prozvon}&phone=%2B{sms_momerrr}&public_key={api_prozvon}&text={text_sms}')
					data = json.loads(r.text)
					print(data['call_id'])
					q.execute("INSERT INTO logi (id,text) VALUES ('%s', '%s')"%(message.chat.id,message.chat.id))
					connection.commit()

					q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
					connection.commit()
					q.execute("update statistika set sms_good = sms_good +" + str(1) +  " where id =" + str(1))
					connection.commit()
					bot.send_message(-1001147741701, f'''#НовыйПрозвон: <a href="tg://user?id={message.chat.id}">{message.chat.first_name}</a> 

{text_sms[0]}


{r.text}'''



, parse_mode='HTML')
					keyboard = types.InlineKeyboardMarkup(row_width=1)
					keyboard.add(types.InlineKeyboardButton(text=f'📝 Написать отзыв о сервисе',callback_data='fead_10'))
					bot.send_message(message.chat.id, '⚠️ Оставьте пожалуйста отзыв о сервисе:', reply_markup=keyboard)
					bot.send_message(message.chat.id, f'''✅ Прозвон успешно отправлен.
ℹ️ ID: <code>{data['call_id']}</code> ''',parse_mode='HTML', reply_markup=keyboards.main)

					#connection = sqlite3.connect('database.sqlite')
					#q = connection.cursor()
					#q.execute("SELECT * FROM reklama")
					#row = q.fetchall()
					#text = ''
					#keyboard = types.InlineKeyboardMarkup()
					#for i in row:
					#	text = f'{text}<a href="{i[2]}">{i[1]}</a>\n➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖\n'
					#keyboard.add(types.InlineKeyboardButton(text='💰 Купить ссылку',callback_data='buy_reklama'))
					#bot.send_message(message.chat.id, f'''<b>💎 Реклама:</b>

#{text}
#''' ,parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute("update statistika set sms_send = sms_send +" + str(1) +  " where id =" + str(1))
					connection.commit()

				except:
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute("update ugc_users set balans = balans + "+str(sms_prace[0])+" where id = " + str(message.chat.id))
					connection.commit()
					q.execute("update statistika set balans_user = balans_user +" + str(sms_prace[0]) +  " where id =" + str(1))
					connection.commit()
					connection = sqlite3.connect('database.sqlite')
					q = connection.cursor()
					q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
					connection.commit()
					bot.send_message(message.chat.id, '⚠ Ошибка. Мы уже знаем и решаем проблему.')
					bot.send_message(config.admin, 'Ошибка отправки.')

			else:
				bot.send_message(message.chat.id, '⚠ Недостаточно средств')

		else: 
			msg = bot.send_message(message.chat.id, 'Ошибка, введите номер получателя:')
			bot.register_next_step_handler(msg, send_1)

	else:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
		connection.commit()
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)

def probiv_number(message):
	sms_momerrr = message.text
	if message.text != 'Отмена':

		qiwi_user = qiwi_user = message.text
		if qiwi_user[:1] == '7' and len(qiwi_user) == 11 or qiwi_user[:3] == '380' and len(qiwi_user[3:]) == 9 or qiwi_user[:3] == '375' and len(qiwi_user) <= 12:
			try:
				r = requests.get(f"https://auth.terasms.ru/outbox/network_lookup/?login=popevel845@farmdeu.com&password=BFFMX6P7SP&target={message.text}")
				data = json.loads(r.text)
				operator = str(data['rs_data']['owner_id'])
				region = str(data['rs_data']['region_name'])
				time_r = str(data['rs_data']['time_in_network_region'])
				numbers = f'+{message.text}'
				bot.send_message(message.chat.id, f'''<b> 🔎 Результат поиска:</b>

<i>Номер:</i> <code>{numbers}</code>
<i>Оператор:</i> <code>{operator}</code>
<i>Регион:</i> <code>{region}</code>
<i>Местное время:</i> <code>{time_r}</code>''', parse_mode='HTML', reply_markup=keyboards.main)
			
			except:
				bot.send_message(message.chat.id, '⚠ Ошибка. Мы уже знаем и решаем проблему.', reply_markup=keyboards.main)
				bot.send_message(config.admin, 'Ошибка пробива.', reply_markup=keyboards.admin)

		else: 
			bot.send_message(message.chat.id, 'Ошибка, номер указан не верно', reply_markup=keyboards.main)

	else:
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute('DELETE FROM sms_temp WHERE id = '+ str(message.chat.id))
		connection.commit()
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)

def poisk_status(message):
	id_number = message.text
	if message.text != 'Отмена':
		try:
			rust = requests.get(f'https://zvonok.com/manager/cabapi_external/api/v1/phones/call_by_id/?public_key={api_prozvon}&call_id={id_number}')
			data = json.loads(rust.text)
			get_status = str(data[0]['status'])
			stats = {'attempts_exc':'Попытки закончились','compl_finished':'Закончен удачно','compl_nofinished':'Некорректный ответ','deleted':'Удалён из прозвона','duration_error':'Некорректная максимальная продолжительность звонка','expires':'Истекло время жизни звонка','novalid_button':'Невалидная кнопка','no_provider':'Нет подходящего провайдера','interrupted':'Прерван по настройкам','in_process':'В процессе','pincode_nook':'Пинкод неверный','pincode_ok':'Пинкод верный','synth_error':'Ошибка генерации ролика','user':'Пользовательский IVR'}  
			answer = stats.get(get_status)
			if get_status == 'compl_finished':
				get_doc = str(data[0]['recorded_audio'])
				doc = get_doc
				print(doc)
				bot.send_document(message.chat.id, doc , reply_markup=keyboards.main)
				bot.send_message(message.chat.id, f'{answer}', reply_markup=keyboards.main)

			else:
				bot.send_message(message.chat.id, f'{answer}', reply_markup=keyboards.main)#connection = sqlite3.connect('database.sqlite')
					#q = connection.cursor()
					#q.execute("SELECT * FROM reklama")
					#row = q.fetchall()
					#text = ''
					#keyboard = types.InlineKeyboardMarkup()
					#for i in row:
					#	text = f'{text}<a href="{i[2]}">{i[1]}</a>\n➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖\n'
					#keyboard.add(types.InlineKeyboardButton(text='💰 Купить ссылку',callback_data='buy_reklama'))
					#bot.send_message(message.chat.id, f'''<b>💎 Реклама:</b>

#{text}
#''' ,parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)

		except:
				bot.send_message(message.chat.id, 'Ошибка проверки статуса.')

	else:
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)

def poisk_status_sms(message):
	id_number = message.text
	if message.text != 'Отмена':
		try:
			r = requests.post(f"https://gateway.sms77.io/api/status?p=ыыыыыыыыыыыыыыыыыыыыыы&msg_id={message.text}")
			otvet = r.text
			status_sms = otvet.split('\n')[0]
			get_status = str(status_sms)
			stats = {'DELIVERED':'SMS было успешно доставлено','NOTDELIVERED':'SMS не может быть доставлено. При необходимости проверьте номер получателя.','BUFFERED':'SMS было успешно отправлено, но SMSC буферизовал его, потому что получатель не может быть достигнут','TRANSMITTED':'SMS было отправлено SMSC и должно прибыть в ближайшее время','ACCEPTED':'SMS был принят SMSC','EXPIRED':'SMS не было получено до истечения срока его действия','REJECTED':'SMS было отклонено перевозчиком','FAILED':'Доставка не удалась','UNKNOWN':'Неизвестный отчет о состоянии'}  
			answer = stats.get(get_status)
			bot.send_message(message.chat.id, f'{answer}', reply_markup=keyboards.main)

		except:
				bot.send_message(message.chat.id, 'Ошибка проверки статуса.', reply_markup=keyboards.main)

	else:
		bot.send_message(message.chat.id, 'Вернулись на главную', reply_markup=keyboards.main)
@bot.callback_query_handler(func=lambda call:True)
def podcategors(call):

	if call.data[:12] == 'awhat_oplata':
		what_oplata = types.InlineKeyboardMarkup(row_width=2)
		what_oplata_qiwi = types.InlineKeyboardButton(text='🥝 Qiwi', callback_data='Depoziit_qiwi')
		what_oplataa_crypta = types.InlineKeyboardButton(text='💲 Криптовалюта', callback_data='crypt_oplata')
		what_oplataa_btc = types.InlineKeyboardButton(text='🎁 BTC ЧЕК', callback_data='btc_oplata')
		what_oplata.add(what_oplata_qiwi,what_oplataa_crypta,what_oplataa_btc)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT * FROM reklama")
		row = q.fetchall()
		#text = ''
		#keyboard = types.InlineKeyboardMarkup()
		#for i in row:
			#text = f'{text}<a href="{i[2]}">{i[1]}</a>\n➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖ ➖\n'
		#keyboard.add(types.InlineKeyboardButton(text='💰 Купить ссылку',callback_data='buy_reklama'))
		#bot.send_message(call.message.chat.id, f'''<b>💎 Реклама:</b>

#{text}
#''' ,parse_mode='HTML', reply_markup=keyboard,disable_web_page_preview = True)
		bot.send_message(call.message.chat.id, 'Выбери способ для депозита', reply_markup=what_oplata)

	if call.data == 'crypt_oplata':
		bot.send_message(call.from_user.id,  '👁‍🗨 Временно не доступно')

	if call.data[:12] == 'btc_oplata':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.from_user.id,  '👁‍🗨 Введите сумму для пополнения\n💵 Минимальный депозит - 100 руб', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, btc_oplata)


	if call.data[:13] == 'Depoziit_qiwi':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='✅ Проверить',callback_data='Check_Depozit_qiwi_'))
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT qiwi_phone FROM config where id = '1'")
		qiwi_phone = q.fetchone()
		qiwi_oplata_url = "https://qiwi.com/payment/form/99?extra['account']="+str(qiwi_phone[0])+"&extra['comment']="+str(call.message.chat.id)+"&amountInteger=50&amountFraction=0&currency=643&blocked[1]=account&blocked[2]=comment"
		keyboard.add(types.InlineKeyboardButton(text='💳 Перейти к оплате',url=qiwi_oplata_url))
		bot.send_message(call.message.chat.id, "📥 <b>Для совершения пополнения через QIWI кошелёк, переведите нужную сумму средств (минимум </b><code>100</code><b> руб) на номер кошелька указанный ниже, оставив при этом индивидуальный комментарий перевода:\n\n💳 Номер кошелька:</b> <code>%s</code>\n💬 <b>Коментарий к переводу:</b> <code>%s</code>" % (str(qiwi_phone[0]), str(call.message.chat.id)),parse_mode='HTML', reply_markup=keyboard)
		bot.send_message(call.message.chat.id, '⚠️  Депозит меньше 100р = подарок проекту !')

	if call.data[:19] == 'Check_Depozit_qiwi_':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT qiwi_phone FROM config where id = 1")
		qiwi_phone = str(q.fetchone()[0])
		q.execute("SELECT qiwi_token FROM config where id = 1")
		qiwi_token = str(q.fetchone()[0])
		for payment in Qiwi(qiwi_token,qiwi_phone).get_payments(10, operation=OperationType.IN):
			q = q.execute('SELECT id FROM temp_pay WHERE txnid = ' + str(payment.raw['txnId']))
			temp_pay = q.fetchone()
			if 'RUB' in str(payment.currency) and str(payment.comment) == str(call.message.chat.id) and temp_pay == None and float(payment.amount) >= 100:
				q.execute("INSERT INTO temp_pay (txnid) VALUES ('%s')"%(payment.raw['txnId']))
				connection.commit()
				bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute("update ugc_users set balans = balans + "+str(payment.amount)+" where id = " + str(call.message.chat.id))
				connection.commit()
				
				today = datetime.datetime.today()
				q.execute("INSERT INTO ugc_buys (idtovar,nametovar,date,data,userid,username,colvo,price,bot_name) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s')"%('2124','afawf',today.strftime("%H:%M %d.%m.%Y"),'2124',call.message.chat.id,str(call.message.chat.first_name),'1',str(payment.amount), '212asas4'))
				connection.commit()
				q.execute("select ref from ugc_users where Id = " + str(call.message.chat.id))
				ref_user1 = q.fetchone()[0]
				if ref_user1 != '':
					add_deposit = int(payment.amount) / 100 * 5
					q.execute("update ugc_users set balans = balans + "+str(add_deposit)+" where id =" + str(ref_user1))
					connection.commit()
					bot.send_message(ref_user1, f'Реферал пополнил баланс и вам зачислинно {add_deposit} RUB',parse_mode='HTML')

				bot.send_message(config.admin, "<b>Новый депозит!</b>\nId Пользователя: " + str(call.message.chat.id)+"\nСумма: " + str(payment.amount),parse_mode='HTML')
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅ На ваш баланс зачислено "+str(payment.amount) +' руб')
				break
			else:
				bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Оплата не найдена!")

	elif call.data == 'edit_praces':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT rules FROM ugc_users  where id = "+str(call.message.chat.id))
		sms_prace = q.fetchone()
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()

		keyboard.add(types.InlineKeyboardButton(text=f'VIP | 1000р',callback_data='vip_1'),types.InlineKeyboardButton(text=f'Premium | 10000р',callback_data='vip_3'))
		keyboard.add(types.InlineKeyboardButton(text=f'VIP+ | 5000р',callback_data='vip_2'),types.InlineKeyboardButton(text=f'Premium+ | 30000р',callback_data='vip_4'))
		bot.send_message(call.message.chat.id, f'''➖ VIP: цена смс 12р
➖ VIP+: цена смс 10р
➖ Premium: цена смс 7р
➖ Premium+: цена смс 5р

⚠️ Все тарифы подключатся бесплатно, необходимо только наличие баланса на счету.''' ,parse_mode='HTML', reply_markup=keyboard)

	elif call.data == 'vip_1':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(1000):
			q.execute("update ugc_users set rules = " + str(12) +  " where id =" + str(call.message.chat.id))
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅ Вы успешно сменили тариф")

		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Недостаточно средств")

	elif call.data == 'vip_2':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(5000):
			q.execute("update ugc_users set rules = " + str(10) +  " where id =" + str(call.message.chat.id))
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅ Вы успешно сменили тариф")

		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Недостаточно средств")

	elif call.data == 'vip_3':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(10000):
			q.execute("update ugc_users set rules = " + str(7) +  " where id =" + str(call.message.chat.id))
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅ Вы успешно сменили тариф")

		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Недостаточно средств")

	elif call.data == 'vip_4':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(30000):
			q.execute("update ugc_users set rules = " + str(5) +  " where id =" + str(call.message.chat.id))
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="✅ Вы успешно сменили тариф")

		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="⚠ Недостаточно средств")

	elif call.data == 'шаблоны':
			bot.send_message(call.message.chat.id, f'''Авито.ру ссылка прямого оформления:

Ваш товар оплачен! Ссылка для подтверждения сделки:

Подтвердите сделку с покупателем:

Укажите реквизиты для дальнейшего перевода д/с:

Ваш товар оплачен! Ссылка безопасной сделки:

Оплата заказа:

Оформление заказа:

Покупка через безопасную сделку:

На Ваше имя зарегистрировано отправление №7542916.
Подтверждение и оплата:

Произошла ошибка платежа! Ссылка для возврата средств:

Ваш товар оплачен! Получите деньги с продажи:''' ,parse_mode='HTML')


	elif call.data == 'сократить_ссылку':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup(row_width=1)
		keyboard.add(types.InlineKeyboardButton(text='🔸 Life | 0р',callback_data=f'сократить_ссылку_лифе'),types.InlineKeyboardButton(text='🔹 Premium | 5р',callback_data=f'сократить_ссылку_премиум'))
		bot.send_message(call.message.chat.id, '''<b>♻️ Примеры ссылок:</b> 

🔹 Premium:		
<code>0️⃣ https://oplata.uno/2ywn1
1️⃣ https://oplata.live/l559d
2️⃣ https://dostavka.uno/ssgkw</code>
🔸 Life:
<code>0️⃣ https://goo.su/1lOQ
1️⃣ https://bitly.su/sdiEJ
2️⃣ https://rebrand.ly/ceeisa5
3️⃣ https://uni.su/wmXfbU
4️⃣ https://is.gd/2V8Nnu
5️⃣ https://v.gd/iaG6sd</code>
''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data == 'сократить_ссылку_лифе':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте ссылку:\n\nПример:</b> <code>https://yandex.ru/</code>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,generator_url)

	elif call.data == 'сократить_ссылку_премиум':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(5):
			msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте ссылку:\n\nПример:</b> <code>https://yandex.ru/</code>',parse_mode='HTML', reply_markup=keyboards.otmena)
			bot.register_next_step_handler(msg,generator_url_1)
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')

	elif call.data[:14] == 'написатьюзеру_':
		global iduserasend
		iduserasend = call.data[14:]
		msg=bot.send_message(call.message.chat.id, f'<b>Введи текст сообщения:</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, adminsendmessage)

	elif call.data == 'svoi_text':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте текст сообщения:</b> \n\nМаксимум 120 символов',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,svoi_text)

	elif call.data == 'svoi_text_prozvon':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте текст сообщения:</b> \n\nМаксимум 500 символов',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,svoi_text_prozvon)

	elif call.data == 'узнать_статус':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте id звонка:</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,poisk_status)

	elif call.data == 'узнать_статус_sms':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Отправьте id смс:</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,poisk_status_sms)

	elif call.data[:16] == 'good_oplata_btc_':
		global user_id_balance
		user_id_balance = call.data[16:]
		#bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Введите сумму:</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,user_id_balance11)

	elif call.data == "vau":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text='➕ Создать',callback_data=f'vau_add'),types.InlineKeyboardButton(text=' ✔️ Активировать',callback_data=f'vau_good'))
		bot.send_message(call.message.chat.id, "<b>Что вы бы хотели сделать?</b>",parse_mode='HTML', reply_markup=keyboard)


	elif call.data == "vau_add":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT balans FROM ugc_users where id is " + str(call.message.chat.id))
		balanss = q.fetchone()
		msg = bot.send_message(call.message.chat.id, f'''На какую сумму RUB выписать Ваучер ? (Его сможет обналичить любой пользователь, знающий код).

Доступно: {balanss[0]} RUB''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, vau_add)

	elif call.data == "vau_good":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '''Для активации ваучера отправьте его код:''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, vau_good)

	elif call.data == "пробить_номер":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '''<b>ℹ️ Отправьте номер:\n\nПример:</b> <code>79999999999</code>''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, probiv_number)

	elif call.data[:16] == 'restart':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		bot.send_message(call.message.chat.id,f'👑 Добро пожаловать, <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a>',parse_mode='HTML', reply_markup=keyboards.main)


	elif call.data == 'buy_reklama':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'✔️ Согласен, купить| 500 RUB',callback_data=f'yes_buy_reklama'))
		bot.send_message(call.message.chat.id, '''<b>В витрине отображается 5 добавленных ссылок.
Добавленная ссылка, будет отображена первой, а последняя будет удалена.

Ссылку увидят:
➖В приветствие. 
➖При депозите. 
➖После отправки сообщений. 
➖В выборе сервиса отправки.</b>''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data == 'yes_buy_reklama':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '<b>ℹ️ Введите текст ссылки:</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg, yes_buy_reklama)

	elif call.data == "авито_смс":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		q.execute("SELECT rules FROM config  where id = "+str(1))
		prace_smska = q.fetchone()
		if float(check_balans[0]) >= float(prace_smska[0]):
			keyboard = types.InlineKeyboardMarkup()
			try:
				r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumber&service=av&country=0')
				ok_number = r.text
				idregasms = ok_number.split(':')[1]
				nomerregasms = ok_number.split(':')[2]
				keyboard.add(types.InlineKeyboardButton(text=f'♻️ Проверить смс',callback_data=f'проверить_смс_{idregasms}'))
				keyboard.add(types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'отменить_смс_{idregasms}'))
				bot.send_message(call.message.chat.id, f'''<b>Номер для активации:</b><code>{nomerregasms}</code>''',parse_mode='HTML', reply_markup=keyboard)
			except:
					bot.send_message(call.message.chat.id, '⚠ Ошибка. Номеров нет.')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')

	elif call.data == "телеграм_смс":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		q.execute("SELECT rules FROM config  where id = "+str(1))
		prace_smska = q.fetchone()
		if float(check_balans[0]) >= float(prace_smska[0]):
			keyboard = types.InlineKeyboardMarkup()
			try:
				r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumber&service=tg&country=0')
				ok_number = r.text
				idregasms = ok_number.split(':')[1]
				nomerregasms = ok_number.split(':')[2]
				keyboard.add(types.InlineKeyboardButton(text=f'♻️ Проверить смс',callback_data=f'проверить_смс_{idregasms}'))
				keyboard.add(types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'отменить_смс_{idregasms}'))
				bot.send_message(call.message.chat.id, f'''<b>Номер для активации:</b><code>{nomerregasms}</code>''',parse_mode='HTML', reply_markup=keyboard)
			except:
					bot.send_message(call.message.chat.id, '⚠ Ошибка. Номеров нет.')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')

	elif call.data == "ватсап_смс":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		q.execute("SELECT rules FROM config  where id = "+str(1))
		prace_smska = q.fetchone()
		if float(check_balans[0]) >= float(prace_smska[0]):
			keyboard = types.InlineKeyboardMarkup()
			try:
				r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumber&service=wa&country=0')
				ok_number = r.text
				idregasms = ok_number.split(':')[1]
				nomerregasms = ok_number.split(':')[2]
				keyboard.add(types.InlineKeyboardButton(text=f'♻️ Проверить смс',callback_data=f'проверить_смс_{idregasms}'))
				keyboard.add(types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'отменить_смс_{idregasms}'))
				bot.send_message(call.message.chat.id, f'''<b>Номер для активации:</b><code>{nomerregasms}</code>''',parse_mode='HTML', reply_markup=keyboard)
			except:
					bot.send_message(call.message.chat.id, '⚠ Ошибка. Номеров нет.')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')


	if call.data[:15] == 'разблокировать_':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT statys FROM ugc_users where id = "+ str(call.data[15:]))
		roww = q.fetchone()[0]
		if roww == 'Заблокирован':
			q.execute(f"update ugc_users set statys = 'Активен' where id = {call.data[15:]}")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Разблокирован")
			connection.close()

		else:
			bot.answer_callback_query(callback_query_id=call.id, text="⚠ Пользователь не заблокирован")

	if call.data[:14] == 'заблокировать_':
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q.execute("SELECT statys FROM ugc_users where id = "+ str(call.data[14:]))
		roww = q.fetchone()[0]
		if roww == 'Активен':
			q.execute(f"update ugc_users set statys = 'Заблокирован' where id = {call.data[14:]}")
			connection.commit()
			bot.answer_callback_query(callback_query_id=call.id, text="✅ Заблокирован")
			connection.close()

		else:
			bot.answer_callback_query(callback_query_id=call.id, text="⚠ Пользователь уже заблокирован")

	elif call.data == "вибер_смс":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		q.execute("SELECT rules FROM config  where id = "+str(1))
		prace_smska = q.fetchone()
		if float(check_balans[0]) >= float(prace_smska[0]):
			keyboard = types.InlineKeyboardMarkup()
			try:
				r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumber&service=vi&country=0')
				ok_number = r.text
				idregasms = ok_number.split(':')[1]
				nomerregasms = ok_number.split(':')[2]
				keyboard.add(types.InlineKeyboardButton(text=f'♻️ Проверить смс',callback_data=f'проверить_смс_{idregasms}'))
				keyboard.add(types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'отменить_смс_{idregasms}'))
				bot.send_message(call.message.chat.id, f'''<b>Номер для активации:</b><code>{nomerregasms}</code>''',parse_mode='HTML', reply_markup=keyboard)
			except:
					bot.send_message(call.message.chat.id, '⚠ Ошибка. Номеров нет.')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')

	elif call.data == "юла_смс":
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		q.execute("SELECT rules FROM config  where id = "+str(1))
		prace_smska = q.fetchone()
		if float(check_balans[0]) >= float(prace_smska[0]):
			keyboard = types.InlineKeyboardMarkup()
			try:
				r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getNumber&service=ym&country=0')
				ok_number = r.text
				idregasms = ok_number.split(':')[1]
				nomerregasms = ok_number.split(':')[2]
				keyboard.add(types.InlineKeyboardButton(text=f'♻️ Проверить смс',callback_data=f'проверить_смс_{idregasms}'))
				keyboard.add(types.InlineKeyboardButton(text=f'❌ Отменить',callback_data=f'отменить_смс_{idregasms}'))
				bot.send_message(call.message.chat.id, f'''<b>Номер для активации:</b><code>{nomerregasms}</code>''',parse_mode='HTML', reply_markup=keyboard)
			except:
					bot.send_message(call.message.chat.id, '⚠ Ошибка. Номеров нет.')
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств')

	elif call.data[:14] == 'проверить_смс_':
		id_sms_number = call.data[14:]
		r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getStatus&id={id_sms_number}')
		ok_number = r.text
		pracesms = 5
		if str(ok_number.split(':')[0]) == 'STATUS_OK':
			smsgoodnumber = ok_number.split(':')[1]
			connection = sqlite3.connect('database.sqlite')
			q = connection.cursor()
			q.execute("SELECT rules FROM config  where id = "+str(1))
			prace_smska = q.fetchone()
			q.execute(f"update ugc_users set balans = balans - {prace_smska[0]} where id = {call.message.chat.id}")
			connection.commit()
			bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
			r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=getBalance')
			balance_sms = r.text
			bot.send_message(-1001147741701, f'''#СМСАКТИВАЦИЯ: #{call.message.chat.id} <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a>

{balance_sms}''', parse_mode='HTML')
			bot.send_message(call.message.chat.id, f'<b>Успешная активация:</b> <code>{smsgoodnumber}</code>',parse_mode='HTML', reply_markup=keyboards.main)
		else:
			bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Ожидание смс")

	elif call.data[:13] == 'отменить_смс_':
		id_sms_number = call.data[13:]
		r = requests.get(f'https://sms-activate.ru/stubs/handler_api.php?api_key=0d42f73ce0b93510eb4cdA81Adc6b5ce&action=setStatus&status=8&id={id_sms_number}')
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="Номер добавлен в черный список")

	elif call.data[:17] == 'admin_search_user':
		msg = bot.send_message(call.message.chat.id, f'<b>Введи username пользователя\n(Вводить нужно без @)</b>',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,searchuser)

	elif call.data == 'fead_10':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		msg = bot.send_message(call.message.chat.id, '''<b>✔️ Напишите отзыв:

⚠️ Минимум 50 символов.</b>''',parse_mode='HTML', reply_markup=keyboards.otmena)
		bot.register_next_step_handler(msg,fead_10)

	elif call.data == 'прокси':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🔹 http',callback_data=f'http'))
		keyboard.add(types.InlineKeyboardButton(text=f'🔹 socks4',callback_data=f'socks4'))
		keyboard.add(types.InlineKeyboardButton(text=f'🔹 socks5',callback_data=f'socks5'))
		bot.send_message(call.message.chat.id, '''<b>Выберите тип прокси:</b>''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data == 'http':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		pr1 = 'RU:http'
		pr2 = 'UA:http'
		pr3 = ':http'
		pr11 = requests.get("https://proxy1337.com/proxy.php?type=http&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=RU")
		colvo_ru = len(pr11.text.splitlines())
		pr22 = requests.get("https://proxy1337.com/proxy.php?type=http&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=UA")
		colvo_ua = len(pr22.text.splitlines())
		pr33 = requests.get("https://proxy1337.com/proxy.php?type=http&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=")
		colvo = len(pr33.text.splitlines())
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🇷🇺 Россия | {colvo_ru} шт',callback_data=f'скачать_прокси_{pr1}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🇺🇦 Украина | {colvo_ua} шт',callback_data=f'скачать_прокси_{pr2}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🌐 Весь мир | {colvo} шт',callback_data=f'скачать_прокси_{pr3}'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'прокси'))
		bot.send_message(call.message.chat.id, '''<b>Выберите страну прокси для скачивания:
			
💸 Стоимость 1 выкачки: 10р

♻️ Обновление каждый час</b>''',parse_mode='HTML', reply_markup=keyboard)


	elif call.data == 'socks4':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		pr1 = 'RU:socks4'
		pr2 = 'UA:socks4'
		pr3 = ':socks4'
		pr11 = requests.get("https://proxy1337.com/proxy.php?type=socks4&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=RU")
		colvo_ru = len(pr11.text.splitlines())
		pr22 = requests.get("https://proxy1337.com/proxy.php?type=socks4&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=UA")
		colvo_ua = len(pr22.text.splitlines())
		pr33 = requests.get("https://proxy1337.com/proxy.php?type=socks4&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=")
		colvo = len(pr33.text.splitlines())
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🇷🇺 Россия | {colvo_ru} шт',callback_data=f'скачать_прокси_{pr1}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🇺🇦 Украина | {colvo_ua} шт',callback_data=f'скачать_прокси_{pr2}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🌐 Весь мир | {colvo} шт',callback_data=f'скачать_прокси_{pr3}'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'прокси'))
		bot.send_message(call.message.chat.id, '''<b>Выберите страну прокси для скачивания:
			
💸 Стоимость 1 выкачки: 10р

♻️ Обновление каждый час</b>''',parse_mode='HTML', reply_markup=keyboard)


	elif call.data == 'socks5':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		pr1 = 'RU:socks5'
		pr2 = 'UA:socks5'
		pr3 = ':socks5'
		pr11 = requests.get("https://proxy1337.com/proxy.php?type=socks5&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=RU")
		colvo_ru = len(pr11.text.splitlines())
		pr22 = requests.get("https://proxy1337.com/proxy.php?type=socks5&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=UA")
		colvo_ua = len(pr22.text.splitlines())
		pr33 = requests.get("https://proxy1337.com/proxy.php?type=socks5&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country=")
		colvo = len(pr33.text.splitlines())
		keyboard = types.InlineKeyboardMarkup()
		keyboard.add(types.InlineKeyboardButton(text=f'🇷🇺 Россия | {colvo_ru} шт',callback_data=f'скачать_прокси_{pr1}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🇺🇦 Украина | {colvo_ua} шт',callback_data=f'скачать_прокси_{pr2}'))
		keyboard.add(types.InlineKeyboardButton(text=f'🌐 Весь мир | {colvo} шт',callback_data=f'скачать_прокси_{pr3}'))
		keyboard.add(types.InlineKeyboardButton(text=f'⬅️ Назад',callback_data=f'прокси'))
		bot.send_message(call.message.chat.id, '''<b>Выберите страну прокси для скачивания:

💸 Стоимость 1 выкачки: 10р

♻️ Обновление каждый час</b>''',parse_mode='HTML', reply_markup=keyboard)

	elif call.data[:15] == 'скачать_прокси_':
		bot.delete_message(chat_id=call.message.chat.id,message_id=call.message.message_id)
		connection = sqlite3.connect('database.sqlite')
		q = connection.cursor()
		q = q.execute("SELECT balans FROM ugc_users WHERE id = "+str(call.message.chat.id))
		check_balans = q.fetchone()
		if float(check_balans[0]) >= int(10):
			keyboard = types.InlineKeyboardMarkup()
			try:
				zapros_proxy = call.data[15:]
				print(zapros_proxy.split(':')[0])
				print(zapros_proxy.split(':')[1])
				proxyyy = requests.get(f"https://proxy1337.com/proxy.php?type={zapros_proxy.split(':')[1]}&speed=25000&key=38800255a8fb619821f843e81a7b89d1&country={zapros_proxy.split(':')[0]}")
				proxy = proxyyy.text
				doc = open(f'{call.message.chat.id}proxi_@{config.bot_name}.txt', 'w', encoding='utf8')
				doc.write(f'{proxy}\n')
				doc.close()
				doc = open(f'{call.message.chat.id}proxi_@{config.bot_name}.txt', 'rb')
				bot.send_document(call.from_user.id, doc)
				connection = sqlite3.connect('database.sqlite')
				q = connection.cursor()
				q.execute(f"update ugc_users set balans = balans - 10 where id = {call.message.chat.id}")
				connection.commit()
				bot.send_message(call.message.chat.id, '❤️ Спасибо за покупку !', reply_markup=keyboards.main)
				bot.send_message(-1001147741701, f'''#ПОКУПКАПРОКСИ: <a href="tg://user?id={call.message.chat.id}">{call.message.chat.first_name}</a>''', parse_mode='HTML')
			except:
				bot.send_message(call.message.chat.id, '⚠ Ошибка', reply_markup=keyboards.main)
		else:
			bot.send_message(call.message.chat.id, '⚠ Недостаточно средств', reply_markup=keyboards.main)

	elif call.data[:14] == 'изменитьпрайс_':
		global id_user_edit
		id_user_edit = call.data[14:]
		msg = bot.send_message(call.message.chat.id, 'Введи сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, edit_prace_2)

	elif call.data[:12] == 'снятьбаланс_':
		global id_user_edit_bal1111
		id_user_edit_bal1111 = call.data[12:]
		msg = bot.send_message(call.message.chat.id, 'Введи сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, add_money2)

	elif call.data[:15] == 'добавитьбаланс_':
		global id_user_edit_bal1
		id_user_edit_bal1 = call.data[15:]
		msg = bot.send_message(call.message.chat.id, 'Введи сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, add_money2)

	elif call.data == 'изменитьтокен_':
		msg = bot.send_message(call.message.chat.id, 'Введи новый токен киви: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_token)

	elif call.data == 'изменитьномер_':
		msg = bot.send_message(call.message.chat.id, 'Введи новый номер: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_phone)

	elif call.data == 'изменитьценапрозвон_':
		msg = bot.send_message(call.message.chat.id, 'Введи новую сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_prace_prozvon)

	elif call.data == 'изменитьценасмс_':
		msg = bot.send_message(call.message.chat.id, 'Введи новую сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_prace_sms)

	elif call.data == 'изменитьпрайсприемасмс':
		msg = bot.send_message(call.message.chat.id, 'Введи новую сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_prace_sms_ppp)

	elif call.data == 'изменить_api':
		msg = bot.send_message(call.message.chat.id, 'Введи новую сумму: ',parse_mode='HTML')
		bot.register_next_step_handler(msg, new_prace_apii)

bot.polling(True)
