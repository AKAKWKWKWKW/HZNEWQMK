from telethon import TelegramClient
import re
import datetime
import time
import asyncio
import requests
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
from utils.mydb import *
from utils.user import User
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
api_id = 2152647
api_hash = '5fd09f7a92d896c677280284c2ba1cce'
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
client = TelegramClient(session="sms", api_id=api_id, api_hash=api_hash, app_version="10 P (28)",
                        device_model="Iphone", system_version='6.12.0')
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
client.start()

class BTCPayment():
    def __init__(self):
        self.banker = 'BTC_CHANGE_BOT'
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    def curs(self):
        response = requests.get(
            'https://blockchain.info/ticker',
        ) 
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
        return float(response.json()['RUB']['15m'])

#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    async def deposit_logs(self, user_id, types, amount):
        conn, cursor = connect()

        cursor.execute(f'INSERT INTO deposit_logs VALUES ("{user_id}", "{types}", "{amount}", "{datetime.datetime.now()}")')
        conn.commit()

#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
    async def receipt_parser(self, bot, user_id: int, cheque: str):
        code = re.findall(r'c_\S+', cheque)[0]
        if 'BTC_CHANGE_BOT' in cheque:
            await self.banker_btc(bot, user_id, code)

    async def banker_btc(self, bot, user_id: int, cheque: str):
        await client.send_message(self.banker, f'/start {cheque}')
        msg_bot = await self.get_last_message_banker()

        if 'Вы получили' in msg_bot:
            btc = msg_bot.replace('(', '').replace(')', '').split(' ')
            amount = round(float(btc[2]) * self.curs())
            User(user_id).update_balance(amount)

            await self.deposit_logs(user_id, 'banker', amount)
            await bot.send_message(chat_id=user_id, text=f'Получено + {amount} RUB')
            await bot.send_message(chat_id=1167426018,
                            text=f'<b>♻️ Пришло пополнение Banker!</b>\n\n'
                                 f'<b>🧑🏻‍🔧 От:</b> @{User(user_id).username} | {user_id}\n\n'
                                 f'<b>💰 Сумма:</b> {amount} RUB')

        else:
            await bot.send_message(chat_id=user_id, text=msg_bot)

    async def get_last_message_banker(self) -> str:
        while True:
            message = (await client.get_messages(self.banker, limit=1))[0]
            if message.message.startswith("Приветствую,"):
                await asyncio.sleep(0.5)
                continue
            if message.from_id is not None:
                me = await client.get_me()
                if message.from_id.user_id == me.id:
                    await asyncio.sleep(0.5)
                    continue
            else:
                return message.message

