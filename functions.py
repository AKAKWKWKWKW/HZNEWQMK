from utils.mydb import *
from utils.user import User

from aiogram import types

import datetime
import random
import texts
import menu
import config
import requests
import json
import time


buy_dict = {}

class Buy:
    def __init__(self, user_id):
        self.user_id = user_id
        self.product_code = None


def first_join(user_id, first_name, username, code):
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
    row = cursor.fetchall()
    who_invite = code[7:]

    if who_invite == '':
        who_invite = 0
    
    if len(row) == 0:
        sql = f'INSERT INTO users VALUES (%s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, (user_id, first_name, f"@{username}", '0', who_invite, datetime.datetime.now(), 'no'))
        conn.commit()

        return True, who_invite
        
    return False, 0


def check_in_bd(user_id):
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
    row = cursor.fetchall()

    if len(row) == 0:
        return False
    else:
        return True


def replenish_balance(user_id):
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM check_payment WHERE user_id = "{user_id}"')
    row = cursor.fetchall()
    
    if len(row) > 0:
        code = row[0][1]
    else:
        code = random.randint(1111, 9999)

        cursor.execute(f'INSERT INTO check_payment VALUES ("{user_id}", "{code}", "0")')
        conn.commit()

    msg = texts.replenish_balance.format(
        number=config.config("qiwi_number"),
        code=code,
    )
    url =  f'https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={config.config("qiwi_number")}&amountFraction=0&extra%5B%27comment%27%5D={code}&currency=643&&blocked[0]=account&&blocked[1]=comment'

    markup = menu.payment_menu(url)

    return msg, markup


def check_payment(user_id):
    try:
        conn, cursor = connect()
    
        session = requests.Session()
        session.headers['authorization'] = 'Bearer ' + config.config("qiwi_token")
        parameters = {'rows': '10'}
        h = session.get(
            'https://edge.qiwi.com/payment-history/v1/persons/{}/payments'.format(config.config("qiwi_number")),
            params=parameters)
        req = json.loads(h.text)

        cursor.execute(f'SELECT * FROM check_payment WHERE user_id = {user_id}')
        result = cursor.fetchone()
        comment = result[1]

        for i in range(len(req['data'])):
            if comment in str(req['data'][i]['comment']):
                if str(req['data'][i]['sum']['currency']) == '643':
                    User(user_id).update_balance(req["data"][i]["sum"]["amount"])
                    User(user_id).give_ref_reward(req["data"][i]["sum"]["amount"])

                    cursor.execute(f'DELETE FROM check_payment WHERE user_id = "{user_id}"')
                    conn.commit()

                    rub = req["data"][i]["sum"]["amount"]

                    try:
                        cursor.execute(f'INSERT INTO deposit_logs VALUES ("{user_id}", "qiwi", "{rub}", "{datetime.datetime.now()}")')
                        conn.commit()
                    except:
                        pass

                    return 1, req["data"][i]["sum"]["amount"], req["data"][i]["personId"], req['data'][i]['comment']

                    
    except Exception as e:
        print(e)

    return 0, 0


def admin_info():
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM users')
    row = cursor.fetchall()
    
    d = datetime.timedelta(days=1)
    h = datetime.timedelta(hours=1)
    date = datetime.datetime.now()

    amount_user_all = 0
    amount_user_day = 0
    amount_user_hour = 0

    for i in row:
        amount_user_all += 1

        if date - datetime.datetime.fromisoformat(i[5]) <= d:
            amount_user_day += 1
        if date - datetime.datetime.fromisoformat(i[5]) <= h:
            amount_user_hour += 1

    cursor.execute(f'SELECT * FROM deposit_logs')
    row = cursor.fetchall()

    qiwi = 0
    all_qiwi = 0
    banker = 0
    all_banker = 0

    for i in row:
        if i[1] == 'qiwi':
            if date - datetime.datetime.fromisoformat(i[3]) <= d:
                qiwi += i[2]

            all_qiwi += i[2]

        elif i[1] == 'banker':
            if date - datetime.datetime.fromisoformat(i[3]) <= d:
                banker += i[2]

            all_banker += i[2]


    msg = f"""
❕ Информаци о пользователях:

❕ За все время - <b>{amount_user_all}</b>
❕ За день - <b>{amount_user_day}</b>
❕ За час - <b>{amount_user_hour}</b>

❕ Пополнений за 24 часа
❕ QIWI: <b>{qiwi} ₽</b>
❕ BANKER: <b>{banker} ₽</b>

⚠️ Ниже приведены данные за все время
❕ Пополнения QIWI: <b>{all_qiwi} ₽</b>
❕ Пополнения BANKER: <b>{all_banker} ₽</b>
"""

    return msg


def give_balance(balance, user_id):
    conn, cursor = connect()
    
    cursor.execute(f'UPDATE users SET balance = "{balance}" WHERE user_id = "{user_id}"')
    conn.commit()


def get_users_list():
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM users')
    users = cursor.fetchall()

    return users


def add_sending(info):
    conn, cursor = connect()

    cursor.execute(f'INSERT INTO sending VALUES ("{info["type_sending"]}", "{info["text"]}", "{info["photo"]}", "{info["date"]}")')
    conn.commit()


def sending_check():
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM sending')
    row = cursor.fetchall()

    for i in row:
        if datetime.datetime.fromisoformat(i[3]) <= datetime.datetime.now():
            cursor.execute(f'DELETE FROM sending WHERE photo = "{i[2]}"')
            conn.commit()

            return i

    return False


def list_btns():
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM buttons')
    list_btn = cursor.fetchall()

    msg = ''

    for i in range(len(list_btn)):
        msg += f'№ {i} | {list_btn[i][0]}\n'

    return msg


def admin_del_btn(value):
    conn, cursor = connect()
    
    cursor.execute(f'SELECT * FROM buttons')
    list_btn = cursor.fetchall()

    name = list_btn[int(value)][0]

    cursor.execute(f'DELETE FROM buttons WHERE name = "{name}"')
    conn.commit()


def admin_add_btn(name, info, photo):
    conn, cursor = connect()
    
    cursor.execute(f'INSERT INTO buttons VALUES ("{name}", "{info}", "{photo}")')
    conn.commit()


def btn_menu_list():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM buttons')
    base = cursor.fetchall()
    
    btn_list = []

    for i in base:
        btn_list.append(i[0])

    return btn_list


def terms_of_use_ok_convention(user_id):
    conn, cursor = connect()

    cursor.execute(f'UPDATE users SET terms_of_use = "yes" WHERE user_id = "{user_id}"')
    conn.commit()


async def get_status_ban(user_id):
    conn, cursor = connect()
    cursor.execute(f'SELECT * FROM ban WHERE user_id = "{user_id}"')

    check = cursor.fetchall()

    if len(check) == 0:
        return False
    else:
        return True


async def ban_list(bot):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM ban')
    base = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=2)

    for i in base:
        try:
            chat = await bot.get_chat(i[0])

            markup.add(
                types.InlineKeyboardButton(text=f'👤 {i[0]}/@{chat.username}/{chat.first_name}', callback_data='ban_user'),
            )
        except: pass

    return  markup


def ban(user_id):
    conn, cursor = connect()

    cursor.execute(f'INSERT INTO ban VALUES ("{user_id}")')
    conn.commit()


def unban(user_id):
    conn, cursor = connect()

    cursor.execute(f'DELETE FROM ban WHERE user_id = "{user_id}"')
    conn.commit()


def btc_chat():
    response = requests.get(
        'https://blockchain.info/ticker',
    )

    response.json()['RUB']['15m']

    msg = f"""
BTC/RUB - {response.json()['RUB']['15m']} ₽
BTC/USD - {response.json()['USD']['15m']} $
    """

    return msg
