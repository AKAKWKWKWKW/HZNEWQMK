import re
import socks
import time
import config
import requests
import mysql.connector
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.functions.contacts import ResolveUsernameRequest
from telethon.tl.functions.channels import GetMessagesRequest
from telethon.tl.functions.messages import GetHistoryRequest, ReadHistoryRequest
from telethon import TelegramClient, events, sync
import telethon.sync
from telethon.tl.types import PeerUser, PeerChat, PeerChannel
import telebot
import sqlite3

api_id = 988074
api_hash = 'a5ec8b7b6dbeedc2514ca7e4ba200c13'


client = TelegramClient('btc_pay', api_id, api_hash)
client.start()
bot_token = config.token

from connect import connect
def get_user_infa(userid):
	answer = telebot.TeleBot(config.token).get_chat(userid)
	return f'<a href="tg://user?id={userid}">{answer.first_name}</a> ({userid})'


def main():
	connection,q = connect()
	global i
	q.execute(f"SELECT * FROM ugc_buys where id != 'del' and wallet = 'banker'")
	info = q.fetchall()
	infoo = info
	for i in infoo:
		if i != None and i[1] != 'del':
			print('NEW_CHECK')
			time.sleep(1)
			client.send_message('BTC_CHANGE_BOT', f'/start {i[0]}')
			time.sleep(5)
			answer = check()
			if 'Вы получили' in str(answer) and 'RUB' in str(answer):
				summa_plus_balance = str(answer).split('BTC (')[1].split(' RUB')[0].replace(',','.').replace(' ','')
				q.execute(f"update ugc_users set balance = balance + '{summa_plus_balance}' where userid = '{i[1]}'")
				connection.commit()
				q.execute(f"update ugc_buys set summa = '{summa_plus_balance}' where id = '{i[0]}'")
				connection.commit()
				q.execute(f"update ugc_buys set id = 'del' where id = '{i[0]}'")
				connection.commit()
				try:
					telebot.TeleBot(config.token).send_message(i[1],f'''<b>🔥 Баланс пополнен на {summa_plus_balance}₽</b>''',parse_mode='HTML')
					telebot.TeleBot(config.token).send_message('-763339921', f'''<b>Пользователь: {get_user_infa(i[1])}\nПополнил баланс на {summa_plus_balance}₽\nСистема: BTC Banker</b>''',parse_mode='HTML')
				except:
					pass
			elif 'Упс, кажется, данный чек успел обналичить кто-то другой 😟' in str(answer):
				try:
					bot = telebot.TeleBot(bot_token).send_message(i[1], 'Ошибка в чеке')
				except:
					pass
				q.execute(f'DELETE FROM ugc_buys WHERE id = "{i[0]}"')
				connection.commit()
			else:
				try:
					bot = telebot.TeleBot(bot_token).send_message(i[1], 'Ошибка в чеке')
				except:
					pass
				q.execute(f'DELETE FROM ugc_buys WHERE id = "{i[0]}"')
				connection.commit()

def check():
	channel_username='BTC_CHANGE_BOT'
	channel_entity=client.get_entity(channel_username)
	posts = client(GetHistoryRequest(peer=channel_entity,limit=1,offset_date=None,offset_id=0,max_id=0,min_id=0,add_offset=0,hash=0))
	mesages = posts.messages
	for i in mesages:
		answer = i.message
		return answer

while True:
	time.sleep(2)
	main()

client.run_until_disconnected()