import mysql.connector


def connect():
    conn = mysql.connector.connect(
        host='95.181.172.107 ',
        user='root',
        password='8laus3J5DYqU',
        database='numberbot'
    )

    cursor = conn.cursor()

    return conn, cursor


def create_tables():
    conn, cursor = connect()

    try:
        cursor.execute(f'CREATE TABLE users (user_id TEXT, name TEXT, login TEXT, date TEXT, balance DECIMAL(10, 2))')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE check_payment (user_id TEXT, code TEXT, date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE raffle_list (bank DECIMAL(10, 2), amount_players INT, time TEXT, id TEXT, amount_dice_games TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE raffle_logs (user_id TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE numbers (code TEXT, name TEXT, country1 TEXT, country2 TEXT, country3 TEXT, country4 TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE game_logs (id TEXT, user_id TEXT, status TEXT, bet DECIMAL(10, 2), date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE games (id TEXT, user_id TEXT, bet DECIMAL(10, 2))')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE stats (user_id TEXT, money DECIMAL(10, 2))')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE btc_list (user_id TEXT, code TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE payouts (user_id TEXT, sum TEXT, btc_check TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE payouts_step_0 (user_id TEXT, code TEXT, time TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE deposit_logs (user_id TEXT, type TEXT, sum DECIMAL(10, 2), date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE pact (user_id TEXT, status TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE sending (type TEXT, text TEXT, photo TEXT, date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE active_promo (user_id TEXT, promo TEXT, activation_date INT, end_date INT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE promo_list (promo TEXT, percent FLOAT, create_date INT, end_date INT)')
        conn.commit()
    except:
        pass

create_tables()
