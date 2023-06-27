import sqlite3
import random
import hashlib
from typing import List
db = sqlite3.connect('users.db')
sql = db.cursor()

db1 = sqlite3.connect('config.db')
sql1 = db1.cursor()

idgolds = 1


db.commit()


def check_user(ids):
    sql.execute('''create table if not exists user (
    id TEXT,
    name TEXT,
    referals BIGINT,
    cash INTEGER,
    gold BIGINT
    referral_code TEXT

    )''')
    info = sql.execute(f'''select * from user where id = "{ids}"''')
    user_info = info.fetchone()
    if user_info:
        return user_info
    else:
        return None

def register_user(ids, name):
    sql.execute('''create table if not exists user (
        id TEXT,
        name TEXT,
        referrals BIGINT,
        cash INTEGER,
        gold BIGINT,
        referral_code TEXT
    )''')
    sql.execute(f"insert into user values ('{ids}', '{name}', '{0}', '{0}', '{0}', '{0}')")
    return db.commit()

def get_user_count():
    sql.execute("select count(*) from user")
    count = sql.fetchall()[0][0]
    return count

# Функция получения рефералов пользователя
def get_referrals(user_id: int):
    sql.execute('SELECT * FROM user WHERE id=?', (user_id,))
    user = sql.fetchone()

    # Проверяем, что пользователь существует
    if user is not None:
        return user[2]
    else:
        return None

# Функция получения реферрального кода пользователя
def get_referral_code(user_id: int):
    sql.execute('SELECT * FROM user WHERE id=?', (user_id,))
    user = sql.fetchone()

    # Проверяем, что пользователь существует
    if user is not None:
        return user[5]
    else:
        return None

def add_gold(ids, suma):
    sql.execute('''create table if not exists user (
    id TEXT,
    name TEXT,
    referals BIGINT,
    cash INTEGER,
    gold BIGINT
    referral_code TEXT
    )''')
    sql.execute(f"UPDATE user SET gold={int(check_user(ids)[4])+int(suma)} WHERE id={ids}")
    db.commit()  # сохраняем изменения в базе данных

def del_gold(ids, suma):
    sql.execute('''create table if not exists user (
    id TEXT,
    name TEXT,
    referals BIGINT,
    cash INTEGER,
    gold BIGINT
    referral_code TEXT
    )''')
    sql.execute(f"UPDATE user SET gold={int(check_user(ids)[4])-int(suma)} WHERE id={ids}")
    return db.commit()

def golds(gold_rate):
    sql1.execute('''create table if not exists user (
    id TEXT,
    name TEXT,
    referals BIGINT,
    cash INTEGER,
    gold BIGINT,
    referral_code TEXT
    )''')
    sql1.execute("UPDATE user SET golds=? WHERE id=?", (gold_rate, idgolds))
    return db1.commit()


def goldsc():
    sql1.execute('''create table if not exists user (
    id TEXT,
    name TEXT,
    referals BIGINT,
    cash INTEGER,
    gold BIGINT
    referral_code TEXT
    )''')
    info = sql1.execute(f'''select * from user where id = "{idgolds}"''')
    return info.fetchone()

def dbgolds():
    sql1.execute('''create table if not exists user (
    id TEXT,
    name TEXT,
    referals BIGINT,
    cash INTEGER,
    gold BIGINT
    referral_code TEXT
    )''')
    sql1.execute(f"insert into user values ('{1}', '{0}', '{0}', '{0}', '{0}')")
    return db1.commit()

def del_balance(ids, suma):
    sql.execute('''create table if not exists user (
    id TEXT,
    name TEXT,
    referals BIGINT,
    cash INTEGER,
    gold BIGINT
    referral_code TEXT
    )''')
    sql.execute(f"UPDATE user SET cash={int(check_user(ids)[3])-int(suma)} WHERE id={ids}")
    return db.commit()

def add_balance(ids, suma):
    sql.execute('''create table if not exists user (
    id TEXT,
    name TEXT,
    referals BIGINT,
    cash INTEGER,
    gold BIGINT
    referral_code TEXT
    )''')
    sql.execute(f"UPDATE user SET cash={int(check_user(ids)[3])+int(suma)} WHERE id={ids}")
    return db.commit()

class User():
    def __init__(self, id):
        self.sql_path = 'users.db'
        conn = sqlite3.connect(self.sql_path)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM user WHERE id = ?', [id])
        user = cursor.fetchone()

        self.id = user[0]
        self.name = user[1]
        self.referals = user[2]
        self.cash = user[3]
        self.gold = user[4]