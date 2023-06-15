from utils.mydb import *
from utils.user import User
from aiogram import types
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
import datetime
import random
import menu
import config
import requests
import json
import time

#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
def first_join(user_id, first_name, login):
    if check_user_in_bd(user_id) == False:
        conn, cursor = connect()
        
        sql = f'INSERT INTO users VALUES(%s, %s, %s, %s, %s)'

        cursor.execute(sql, (user_id, first_name, login, datetime.datetime.now(), "0"))
        conn.commit()
    else:
        pass

#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
def check_user_in_bd(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM users WHERE user_id = "{user_id}"')
    check = cursor.fetchall()

    if len(check) > 0:
        return True
    else:
        return False
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT

def deposit_qiwi(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM check_payment WHERE user_id = {user_id}')
    check = cursor.fetchall()
    if len(check) > 0:
        code = check[0][1]
        date = float(check[0][2])
    else:
        code = random.randint(11111, 99999)
        date = time.time()

        cursor.execute(f'INSERT INTO check_payment VALUES ("{user_id}", "{code}", "{date}")')
        conn.commit()


    url =  f'https://qiwi.com/payment/form/99?extra%5B%27account%27%5D={config.config("qiwi_number")}&amountFraction=0&extra%5B%27comment%27%5D={code}&currency=643&&blocked[0]=account&&blocked[1]=comment'

    markup = menu.payment_menu(url)

    return code, date, markup


def check_payment(user_id):
    conn, cursor = connect()

    try:
        session = requests.Session()
        session.headers['authorization'] = 'Bearer ' + config.config('qiwi_token')
        parameters = {'rows': '10'}
        h = session.get(
            'https://edge.qiwi.com/payment-history/v1/persons/{}/payments'.format(config.config("qiwi_token")),
            params=parameters)
        req = json.loads(h.text)

        cursor.execute(f'SELECT * FROM check_payment WHERE user_id = {user_id}')
        result = cursor.fetchone()

        comment = result[1]
        for i in range(len(req['data'])):
            if comment in str(req['data'][i]['comment']):
                if str(req['data'][i]['sum']['currency']) == '643':
                    deposit = float(req["data"][i]["sum"]["amount"])

                    User(user_id).update_balance(deposit)

                    cursor.execute(f'DELETE FROM check_payment WHERE user_id = "{user_id}"')
                    conn.commit()

                    return True
    except:
        pass

    return False


def admin_info():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM users')
    row = cursor.fetchone()

    current_time = str(datetime.datetime.now())

    amount_user_all = 0
    amount_user_day = 0
    amount_user_hour = 0

    while row is not None:
        amount_user_all += 1
        if row[3][:-15:] == current_time[:-15:]:
            amount_user_day += 1
        if row[3][:-13:] == current_time[:-13:]:
            amount_user_hour += 1

        row = cursor.fetchone()

    msg = '❕ Информаци:\n\n' \
          f'❕ За все время - {amount_user_all}\n' \
          f'❕ За день - {amount_user_day}\n' \
          f'❕ За час - {amount_user_hour}'

    return msg


def add_raffle(bank, amount_players, game_time, amount_dice_games):
    conn, cursor = connect()

    code = f'raffle_{random.randint(11111, 99999)}'

    cursor.execute(f'INSERT INTO raffle_list VALUES ("{bank}", "{amount_players}", "{time.time() + (float(game_time) * 60)}", "{code}", "{amount_dice_games}")')
    conn.commit()

    cursor.execute(f'CREATE TABLE {code} (user_id TEXT)')
    conn.commit()

    return True


def raffle_logs(user_id):
    conn, cursor = connect()

    cursor.execute(f'INSERT INTO raffle_logs VALUES ("{user_id}")')
    conn.commit()


def check_raffle():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM raffle_list')
    row = cursor.fetchall()

    if len(row) == 0:
        return False
    else:
        return True


def check_raffle_condition(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM raffle_list')
    row = cursor.fetchone()

    condition = int(row[1])
    condition2 = int(row[4])

    cursor.execute(f'SELECT * FROM raffle_logs WHERE user_id = "{user_id}"')
    stats = cursor.fetchall()

    cursor.execute(f'SELECT * FROM game_logs WHERE user_id = "{user_id}"')
    games = cursor.fetchall()

    amount_games = len(games)

    if condition <= len(stats):
        if condition2 <= amount_games:
            return True

    return False


def check_condition_url_chat(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM raffle_logs WHERE user_id = "{user_id}"')
    stats = cursor.fetchall()

    if len(stats) >= int(config.config('amount_buys_for_url')):
        return True
    else:
        return False



def check_user_in_raffle(user_id):
    conn, cursor = connect()

    code = get_code_raffle()

    cursor.execute(f'SELECT * FROM {code} WHERE user_id = "{user_id}"')
    row = cursor.fetchall()

    if len(row) == 0:
        return False
    else:
        return True


def get_code_raffle():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM raffle_list')
    row = cursor.fetchall()

    return row[0][3]


def raffle_confirm(user_id):
    conn, cursor = connect()

    code = get_code_raffle()

    cursor.execute(f'INSERT INTO {code} VALUES ("{user_id}")')
    conn.commit()

    return True


def get_raffle_info():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM raffle_list')
    row = cursor.fetchall()

    code = get_code_raffle()

    cursor.execute(f'SELECT * FROM {code}')
    amount_users = cursor.fetchall()

    return row[0][0], row[0][1], row[0][2], len(amount_users), int(100 / len(amount_users)), row[0][4]


def check_time_raffle():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM raffle_list')
    row = cursor.fetchall()

    if float(row[0][2]) <= time.time():
        return True
    else:
        return False


def raffle_start():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM raffle_list')
    info = cursor.fetchall()

    code = get_code_raffle()

    cursor.execute(f'DELETE FROM raffle_list WHERE id = "{info[0][3]}"')
    conn.commit()

    cursor.execute(f'SELECT * FROM {code}')
    row = cursor.fetchall()

    win = row[random.randint(0, len(row) - 1)][0]

    User(win).update_balance(info[0][0])

    cursor.execute(f'DROP TABLE {code}')
    conn.commit()

    return win, row


def get_users_list():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM users')
    users = cursor.fetchall()

    return users


def get_payments_history():
    session = requests.Session()
    session.headers['authorization'] = 'Bearer ' + config.config('qiwi_token')

    parameters = {'rows': '10'}

    h = session.get(
        'https://edge.qiwi.com/payment-history/v1/persons/{}/payments'.format(config.config("qiwi_number")),
        params=parameters
    )

    req = json.loads(h.text)

    return req['data']


def get_list_payments_code():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM check_payment')
    check_payment = cursor.fetchall()

    return check_payment


def del_purchase_ticket(user_id):
    conn, cursor = connect()

    cursor.execute(f'DELETE FROM check_payment WHERE user_id = "{user_id}"')
    conn.commit()


def get_status_pact(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM pact WHERE user_id = "{user_id}"')
    pact = cursor.fetchall()

    if len(pact) == 0:
        cursor.execute(f'INSERT INTO pact VALUES ("{user_id}", "no")')
        conn.commit()

        return False
    else:
        if pact[0][1] == "no":
            return False
        else:
            return True


def accept_pact(user_id):
    conn, cursor = connect()

    cursor.execute(f'UPDATE pact SET status = "yes" WHERE user_id = "{user_id}"')
    conn.commit()


def add_sending(info):
    conn, cursor = connect()

    cursor.execute(f'INSERT INTO sending VALUES ("{info["type_sending"]}", "{info["text"]}", "{info["photo"]}", "{info["date"]}")')
    conn.commit()


def sending_check():
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM sending')
    row = cursor.fetchall()

    for i in row:
        if datetime.datetime.strptime(i[3], '%Y-%m-%d %H:%M') <= datetime.datetime.now():
            cursor.execute(f'DELETE FROM sending WHERE photo = "{i[2]}"')
            conn.commit()

            return i

    return False


def create_promo(name, percent, life_time):
    conn, cursor = connect()
    
    time_code = life_time[-1:]
    if time_code == 'd':
        life_time = int(life_time[:-1]) * 60 * 60
    elif time_code == 'm':
        life_time = int(life_time[:-1]) * 60
    elif time_code == 's':
        life_time = int(life_time[:-1])
    else:
        return False 

    create_date = time.time()
    end_date = create_date + life_time

    sql = 'INSERT INTO promo_list VALUES (%s, %s, %s, %s)'
    cursor.execute(sql, (name, percent, create_date, end_date))
    conn.commit()

    return True


def get_promo_list_menu():
    conn, cursor = connect()

    cursor.execute('SELECT * FROM promo_list')
    promocodes = cursor.fetchall()

    markup = types.InlineKeyboardMarkup(row_width=1)

    for promo in promocodes:
        status = '✅' if promo[3] > float(time.time()) else '❌'
        markup.add(
            types.InlineKeyboardButton(text=f'{status} | {promo[0]} | {promo[1]} | {time.ctime(promo[2])}', callback_data=f'promo_list:{status}:{promo[0]}:{promo[1]}:{int(promo[2])}:{int(promo[3])}')
        )

    return markup


async def enter_promo(bot, chat_id, promo_name):
    conn, cursor = connect()

    sql = 'SELECT * FROM promo_list WHERE promo = %s'
    cursor.execute(sql, (promo_name, ))
    promo = cursor.fetchone()

    if promo is not None:
        cursor.execute(f'DELETE FROM active_promo WHERE user_id = "{chat_id}"')
        conn.commit()

        sql = 'INSERT INTO active_promo VALUES (%s, %s, %s, %s)'
        cursor.execute(sql, (chat_id, promo_name, int(time.time()), int(promo[3])))
        conn.commit()

        await bot.send_message(chat_id=chat_id, text=f'✅ Вы активировали промокод и получили скидку {promo[1]} %')
    else:
        await bot.send_message(chat_id=chat_id, text='❌ Промокод не найден')


def get_current_discount(chat_id):
    conn, cursor = connect()
    
    sql = 'SELECT * FROM active_promo WHERE user_id = %s'
    cursor.execute(sql, (chat_id, ))
    check = cursor.fetchone()

    if check is not None:
        sql = 'SELECT * FROM promo_list WHERE promo = %s'
        cursor.execute(sql, (check[1], ))
        promo = cursor.fetchone()
        
        if promo is not None:
            discount = promo[1]
        else:
            discount = 0
    else:
        discount = 0

    return discount