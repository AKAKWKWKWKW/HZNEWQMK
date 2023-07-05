# -*- coding: utf-8 -*-

import requests
import random
import time


def send_request(typee, phone=None, text=None, sms_id=None):
	login = 'iamdver'
	password = '123123zz'
	proxies = {
              "http"  : 'http://KnpXY9Ei:GtiKkenb@91.236.121.28:46071',
              "https" : 'https://KnpXY9Ei:GtiKkenb@91.236.121.28:46071'
            }
	if typee == 'balance':
		data = {'login': login, 'password':password}
		sda = requests.get('http://api.smsfeedback.ru/messages/v2/balance/', params=data, proxies=proxies)
		print(sda.text)

	elif typee == 'names':
		data = {'login': login, 'password':password}
		sda = requests.get('http://api.smsfeedback.ru/messages/v2/senders/', params=data, proxies=proxies)
	
	elif typee == 'send_sms':
		data = {'login': login,
		'password':password,
		'phone': phone,
		'text': text
		}
		sda = requests.get('http://api.smsfeedback.ru/messages/v2/send/', params=data, proxies=proxies)

	elif typee == 'check_sms':
		data = {'login': login,
		'password':password,
		'id': sms_id
		}
		sda = requests.get('http://api.smsfeedback.ru/messages/v2/status/', params=data, proxies=proxies)

	return sda.text