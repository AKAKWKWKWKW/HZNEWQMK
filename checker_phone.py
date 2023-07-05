import json
import telebot
from telebot import types,apihelper
import time
import requests
import config
import notisend
from connect import connect
from sms77api.Sms77api import Sms77api
from sms77api.classes.Journal import JournalType
import smsfeedback

client = Sms77api("iJ4J3aKniNrn801NXrLNvTYl6hTz57DJIICl6UzBdBUBvM79clbcdJsuPbtIPaf9")
bot = telebot.TeleBot(config.token)


def get_user_infa(userid):
	answer = bot.get_chat(userid)
	return f'<a href="tg://user?id={userid}">{answer.first_name}</a> ({userid})'

def get_spisok():
	connection,q = connect()
	q.execute(f'SELECT id,userid,price,id_site,phone,text,service_send,date_send,api,name FROM ugc_sms where status = "check" and api = "0"')
	infa_user = q.fetchall()
	for i in infa_user:
		time.sleep(2)
		if i[6] not in ['mainsms', 'sms77']:
			q.execute(f"update ugc_sms set status = 'nosend' where id = '{i[0]}'")
			connection.commit()
		else:
			print(i[6])

			if i[6] == 'notisend':
				try:
					answer = checker_notisend(i[3])
					if answer == 'delivered':
						q.execute(f"update ugc_sms set status = 'send' where id = '{i[0]}'")
						connection.commit()
						q.execute(f"update ugc_sms set answer = '{answer}' where id = '{i[0]}'")
						connection.commit()
						bot.send_message(i[1], f'''<b>SMS Доставлено

Номер: {i[4]}
Дата: {i[7]}

Текст: {i[5]}''', parse_mode='HTML')
						if str(i[8]) == 'true':
							bot.send_message('-511487521', f'<b>Пользователь {get_user_infa(i[1])}\n\nНомер: {i[4]}\nТекст: {i[5]}\nСтатус: {answer}\nДата: {i[7]}</b>', parse_mode='HTML')
						else:
							bot.send_message('-1001502210606', f'<b>Пользователь {get_user_infa(i[1])}\n\nНомер: {i[4]}\nТекст: {i[5]}\nСтатус: {answer}\nДата: {i[7]}</b>', parse_mode='HTML')

					elif str(answer) in ['canceled', 'non-delivered', 'overdue']:
						q.execute(f"update ugc_users set balance = balance + '{int(i[2])/2}' where userid = '{i[1]}'")
						connection.commit()
						q.execute(f"update ugc_sms set status = 'nosend' where id = '{i[0]}'")
						connection.commit()
						q.execute(f"update ugc_sms set answer = '{answer}' where id = '{i[0]}'")
						connection.commit()
						bot.send_message(i[1], f'<b>❎ Не получилось отправить сообщение\n\nВернули на баланс {int(i[2])/2}₽</b>', parse_mode='HTML')
						if str(i[8]) == 'true':
							bot.send_message('-511487521', f'<b>Пользователь {get_user_infa(i[1])}\n\nНомер: {i[4]}\nТекст: {i[5]}\nСтатус: {answer}</b>', parse_mode='HTML')
						else:
							bot.send_message('-1001502210606', f'<b>Пользователь {get_user_infa(i[1])}\n\nНомер: {i[4]}\nТекст: {i[5]}\nСтатус: {answer}</b>', parse_mode='HTML')
					else:
						q.execute(f"update ugc_sms set status = 'nosend' where id = '{i[0]}'")
						connection.commit()
				except:
					q.execute(f"update ugc_sms set status = 'nosend' where id = '{i[0]}'")
					connection.commit()

			elif i[6] == 'sms77':
				answer = checker(i[3])
				print(answer)
				if answer == 'DELIVERED':
					q.execute(f"update ugc_sms set status = 'send' where id = '{i[0]}'")
					connection.commit()
					q.execute(f"update ugc_sms set answer = '{answer}' where id = '{i[0]}'")
					connection.commit()
					bot.send_message(i[1], f'''<b>SMS Доставлено

Номер: {i[4]}
Дата: {i[7]}

Текст: {i[5]}</b>''', parse_mode='HTML')
					bot.send_message('-1001502210606', f'<b>Пользователь {get_user_infa(i[1])}\n\nНомер: {i[4]}\nТекст: {i[5]}\nСтатус: {answer}\nОтправитель: {i[9]}</b>', parse_mode='HTML')

				elif answer == 'NOTDELIVERED':
					q.execute(f"update ugc_users set balance = balance + '15' where userid = '{i[1]}'")
					connection.commit()
					q.execute(f"update ugc_sms set status = 'nosend' where id = '{i[0]}'")
					connection.commit()
					q.execute(f"update ugc_sms set answer = '{answer}' where id = '{i[0]}'")
					connection.commit()
					bot.send_message(i[1], f'<b>❎ Не получилось отправить сообщение\n\nВернули на баланс 15₽</b>', parse_mode='HTML')
					bot.send_message('-1001502210606', f'<b>Пользователь {get_user_infa(i[1])}\n\nНомер: {i[4]}\nТекст: {i[5]}\nСтатус: {answer}\nОтправитель: {i[9]}</b>', parse_mode='HTML')
				else:
					pass

def checker_smsfeed(phoneid):
	asdsda = str(smsfeedback.send_request(typee='check_sms',sms_id=str(phoneid))).split(';')
	print(asdsda)
	if asdsda[0] not in ['delivery error', 'smsc reject', 'incorrect id', 'invalid mobile phone', 'spam detected', 'not enough balance']:
		return asdsda[1]
	else:
		return 'delivery error'


def checker_notisend(phoneid):
	try:
		sms = notisend.SMS()
		asdsad = sms.statusSMS(str(phoneid))
		return asdsad['messages'][f'{phoneid}']
	except:
		return 'sadds' 

def checker(phoneid):
	try:
		asdas = client.journal(typ = JournalType.OUTBOUND, params = { 'id': phoneid})
		return asdas[0]['dlr']
	except:
		return 'NOTDELIVERED'


def checkerrr(phoneid):
	print(phoneid)
	payload = {"id_sms": [str(phoneid)]}
		
	headers = {
		'Authorization': 'Bearer UgAGWW9dWS_YSqHns',
		'Content-Type': 'application/json',
	}

	response = requests.request("POST", 'https://im.smsclub.mobi/sms/status?', headers=headers, json=payload).json()
	return response['success_request']['info'][str(phoneid)]

def checkerr(phoneid):
	print(phoneid)
	payload = {"id_sms": [str(phoneid)]}
		
	headers = {
		'Content-Type': 'application/json',
	}

	response = requests.get(f'https://esputnik.com/api/v1/message/status?ids={phoneid}', auth=('d', 'f') , headers=headers).json()
	return response['results']['status']
	

while True:
	get_spisok()