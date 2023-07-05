import requests
import json
from sms77api.Sms77api import Sms77api
import config
import random
import notisend
import smsfeedback
from connect import connect

client = Sms77api("iJ4J3aKniNrn801NXrLNvTYl6hTz57DJIICl6UzBdBUBvM79clbcdJsuPbtIPaf9")


def passwordd():
	chars = 'abcdefghijklnopqrstuvwxyz'
	for n in range(1):
		password =''
		for i in range(random.randint(3,6)):
			password += random.choice(chars)
		return password

def sending_sms(userid, phone, textsmsska, service_send, name='extra', test='ddd'):
	if service_send == 'sms77':
		if test == 'ddd':
			res = client.sms(to=phone, text=textsmsska.encode("utf-8"),
			params = {'return_msg_id': True,'json': True,'debug': False,'unicode': True, 'details': True, 'utf8': True, 'from': name})
			return res
		else:
			res = client.sms(to=phone, text=textsmsska.encode("utf-8"),
			params = {'return_msg_id': True,'json': True,'debug': True,'unicode': True, 'details': True, 'utf8': True, 'from': name})
			return res

	elif service_send == 'getsms':
		data = {
		  "key" : config.get_sms_token,
		  "number" : phone,
		  "sender_name" : name,
		  "message": textsmsska
		}

		req = requests.post('https://sender.getsms.shop/send', data=data).json()

		if str(req['ok']) == 'True':
			return req['ok']
		else:
			return 'false'


	elif service_send == 'mainsms':
		connection,q = connect()
		q.execute(f'SELECT balance,price,price_svoi,sender FROM ugc_users where userid = "{userid}"')
		infa_user = q.fetchone()
		sender_name = str(infa_user[3]).replace(' ', '').replace('\n', '')

		sms = notisend.SMS()
		asddsa = sms.sendSMS(phone,textsmsska, sender_name)


		if asddsa['status'] == 'success':
			return asddsa
		else:
			return 'false'



	elif service_send == 'turbo':
		connection,q = connect()
		q.execute(f'SELECT balance,price,price_svoi,sender FROM ugc_users where userid = "{userid}"')
		infa_user = q.fetchone()
		sender_name = str(infa_user[3]).replace(' ', '').replace('\n', '')
		response = requests.get(f'https://api.turbosms.ua/message/send.json?recipients[0]={phone}&sms[sender]={sender_name}&sms[text]={textsmsska}&token=e1761ebb883e8f40fc637ab88c164420996c3d22').json()
		# print(userid, phone, textsmsska, service_send, sender_name, test)
		print(response)
		if response['response_status'] == 'SUCCESS_MESSAGE_ACCEPTED' or response['response_status'] == 'SUCCESS_MESSAGE_SENT':
			return response
		else:
			return 'false'


	elif service_send == 'esputnik':
		headers = {"content-type": "application/json"}

		sfsd = {
		  "from" : 'marketing',
		  "text" : textsmsska,
		  "phoneNumbers" : [f'+{phone}'],
		}

		response = requests.post('https://esputnik.com/api/v1/message/sms', data=json.dumps(sfsd), auth=('f', 'd') , headers=headers).json()
		return response

	elif service_send == 'notisend':
		project='filya_sender'      # Имя проекта
		api_key='d'    # API-ключ
		sms = notisend.SMS(project, api_key)
		asddsa = sms.sendSMS(phone,textsmsska)
		return asddsa

	elif service_send == 'smsfeedback':
		send_sms = str(smsfeedback.send_request('send_sms', phone = str(phone), text=str(textsmsska))).split(';')
		return send_sms[1]

	else:
		payload = {'phone': [f'{phone}'],
		'message': f'{textsmsska}',
		'src_addr': 'RUSMS',}
		
		headers = {
			'Authorization': 'Bearer UgAGWW9S_YSqHns',
			'Content-Type': 'application/json',
		}

		response = requests.request("POST", 'https://im.smsclub.mobi/sms/send?', headers=headers, json=payload).json()
		return response

def get_balance():
	res = client.balance()
	return res

def get_balance_getsms():
	res = requests.get(f'https://sender.getsms.shop/balance?key={config.get_sms_token}').json()
	return res['balance']

def get_balance_payok():
	payload={'API_ID': '2928',
		'API_KEY': '830B0E3779C748C17F313310AE459531-5A3F7C01F3D962519FCB2FC21E42B423-EEE337BEA35C05AE9A28233A108F7E33'}
	res = requests.post('https://payok.io/api/balance', data=payload).json()
	print(str(res).encode('utf-8'))
	return res['balance']

def get_balance2():
	url = "https://api.turbosms.ua/user/balance.json"

	payload={'token': 'd'}

	response = requests.request("POST", url, data=payload).json()
	return response['response_result']['balance']


def get_balance_sputnik():
	headers = {
		'Content-Type': 'application/json',
	}

	response = requests.get('https://esputnik.com/api/v1/balance', auth=('log', 'pass') , headers=headers).json()
	return response['currentBalance']


def get_balance_smsfeedback():
	get_balance = str(smsfeedback.send_request('balance')).split(';')
	return get_balance[1]


def get_balance_notisend():
	project='filya_sender'      # Имя проекта
	api_key='d'    # API-ключ
	sms = notisend.SMS(project, api_key)
	return sms.getBalance()['balance']