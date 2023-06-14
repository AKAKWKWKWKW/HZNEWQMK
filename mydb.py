import mysql.connector


def connect():

    conn = mysql.connector.connect(
        host='185.241.54.82',
        user='root',
        password='MOJ50YX13d56',
        database='numberbot'
    )

    cursor = conn.cursor()

    return conn, cursor


def connect_to_raffle():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='raffle'
    )

    cursor = conn.cursor()

    try:
        cursor.execute(f'CREATE TABLE logs (user_id TEXT, value INT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE list (bank TEXT, condition TEXT, time TEXT, id TEXT)')
        conn.commit()
    except:
        pass

    return conn, cursor


conn, cursor = connect()

def create_tables():
    try:
        cursor.execute(f'CREATE TABLE users (user_id TEXT, first_name TEXT, username TEXT, balance DECIMAL(10, 2), who_invite TEXT, date TEXT, terms_of_use TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE check_payment (user_id TEXT, code TEXT, referral_code TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE sending (type TEXT, text TEXT, photo TEXT, date TEXT)')
        conn.commit()
    except:
        pass
    
    try:
        cursor.execute(f'CREATE TABLE list (type TEXT, text TEXT, photo TEXT, date TEXT)')
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
        cursor.execute(f'CREATE TABLE buttons (name TEXT, info TEXT, photo TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE deposit_logs (user_id TEXT, type TEXT, sum DECIMAL(10, 2), date TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE ban_list (user_id TEXT)')
        conn.commit()
    except:
        pass
    
    try:
        cursor.execute(f'CREATE TABLE stats (user_id TEXT, ref_profit DECIMAL(10, 2), amount_ref INT, number_purchases_good INT, number_purchases_bad INT, deposit DECIMAL(10, 2))')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE numbers (code TEXT, name TEXT, country1 TEXT, country2 TEXT, country3 TEXT, country4 TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE wait_list_number (user_id TEXT, operation_ID TEXT, number TEXT, number_code TEXT, country TEXT, status TEXT, purchase_time DOUBLE, price DECIMAL(10, 2))')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE ref_log (user_id TEXT, all_profit DECIMAL(10, 2))')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE ban (user_id TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE message_list (msg TEXT)')
        conn.commit()
    except:
        pass
    
    try:
        cursor.execute(f'CREATE TABLE games (id TEXT, sum DECIMAL(10, 2), answer TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE game_logs (id TEXT, sum DECIMAL(10, 2), answer TEXT, win TEXT)')
        conn.commit()
    except:
        pass

    try:
        cursor.execute(f'CREATE TABLE number_logs (user_id TEXT, operation_id TEXT, number TEXT, status TEXT, price TEXT, date Text)')
        conn.commit()
    except:
        pass


create_tables()
