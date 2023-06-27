import sqlite3 as sql
from aiogram.utils.markdown import hlink
import time

def spisok():
    con = sql.connect("users.db")
    with con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM user")
        results = (cur.fetchall())
        return results
    con.commit()
    cur.close()




