from aiogram import types
from utils.user import User
from utils.mydb import *

# import sqlite3
import random
import datetime
import config


my_games_txt = """
🎲 Мои игры в кости: {}

💖 Выигрыш: {} RUB
💔 Проигрыш: {} RUB
📊 Профит: {} RUB

Данные приведены за все время
"""

raiting_txt = """
📊 ТОП 3 игроков:

🥇 1 место - {} RUB
🥈 2 место - {} RUB
🥉 3 место - {} RUB

🏆 Ваше место в рейтинге: {} из {} ({} RUB)

Данные приведены за всё время.
Рейтинг обновляется каждые несколько минут.
"""

help_txt = """
🧑🏻‍💻 По вопросам/предложениям/багам, вы можете написать @wavesupp
"""


dice_game_info_txt = """
🎲 Кости #{}
💰 Ставка: {} RUB

🎲🎲🎲 Бросьте кости...
"""


dice_game_result_txt = """
🎲 Кости #{}
💰 Банк: {} RUB

🌝 Ваш результат: {}
🌚 Результат соперника: {}

{}
"""


class Game():

    def __init__(self, code):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM games WHERE id = "{code}"')
        info = cursor.fetchall()

        if len(info) == 0:
            self.status = False
        else:
            self.status = True

            self.id_game = info[0][0]
            self.user_id = info[0][1]
            self.bet = float(info[0][2])

    def del_game(self):
        conn, cursor = connect()

        cursor.execute(f'DELETE FROM games WHERE id = "{self.id_game}"')
        conn.commit()


def dice_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='🗳 Создать игру', callback_data='create_dice'),
        types.InlineKeyboardButton(text='🔁 Обновить', callback_data='reload_dice'),
    )

    markup = get_games_menu(markup)

    markup.add(
        types.InlineKeyboardButton(text='📊 Мои игры', callback_data='my_games_dice'),
        types.InlineKeyboardButton(text='🏆 Рейтинг', callback_data='rating_dice'),
        types.InlineKeyboardButton(text='ᐊ Назад', callback_data='exit'),
    )

    return markup


def get_games_menu(markup):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM games')
    games = cursor.fetchall()

    for i in games:
        markup.add(types.InlineKeyboardButton(text=f'🎲 Игра #{i[0]} | {i[2]} RUB', callback_data=f'dice_game:{i[0]}'))

    return markup


def cancel_dice():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='🚫 Отменить', callback_data='cancel_dice')
    )

    return markup


def back_dice():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='ᐊ Назад', callback_data='back_dice')
    )

    return markup


def create_game(user_id, bet):
    conn, cursor = connect()

    cursor.execute(f'INSERT INTO games VALUES("{random.randint(111111, 999999)}", "{user_id}", "{bet}")')
    conn.commit()


def my_games_dice(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM game_logs WHERE user_id = "{user_id}"')
    games = cursor.fetchall()

    amount_games = len(games)

    win_money = 0
    lose_money = 0
    markup = types.InlineKeyboardMarkup(row_width=2)

    if len(games) < int(config.config('range_game_list')):
        amount = len(games)
    else:
        amount = int(config.config('range_game_list'))

    btn_num = 0
    for i in range(len(games)-1, 0, -1):
        btn_num += 1

        if games[i][2] == 'win':
            win_money += float(games[i][3])


            if btn_num <= amount:
                markup.add(types.InlineKeyboardButton(text=f'{games[i][3]} RUB | ✅ Победа', callback_data=f'gamelog'))

        elif games[i][2] == 'lose':
            lose_money += float(games[i][3])

            if btn_num <= amount:
                markup.add(types.InlineKeyboardButton(text=f'{games[i][3]} RUB | 🔴 Проигрыш', callback_data=f'gamelog'))
    
    profit_money = win_money - lose_money
    profit_money = '{:.2f}'.format(profit_money)

    win_money = '{:.2f}'.format(win_money)
    lose_money = '{:.2f}'.format(lose_money)

    msg = my_games_txt.format(
        amount_games,
        win_money,
        lose_money,
        profit_money,
    )
    
    markup.add(types.InlineKeyboardButton(text=f'ᐊ Назад', callback_data=f'games'))
    
    return msg, markup


def rating_dice(user_id):
    conn, cursor = connect()

    cursor.execute(f'SELECT * FROM stats WHERE user_id = "{user_id}"')
    user = cursor.fetchall()

    if len(user) == 0:
        cursor.execute(f'INSERT INTO stats VALUES("{user_id}", "0")')
        conn.commit()

        user_money = 0
    else:
        user_money = user[0][1]

    cursor.execute(f'SELECT * FROM stats')
    games = cursor.fetchall()

    games = sorted(games, key=lambda money: float(money[1]), reverse=True)


    size_top = len(games)
    user_top = 0

    for i in games:
        user_top += 1

        if i[0] == str(user_id):
            break

    msg = raiting_txt.format(
        '{:.2f}'.format(games[0][1]),
        '{:.2f}'.format(games[1][1]),
        '{:.2f}'.format(games[2][1]),
        user_top,
        size_top,
        user_money
    )

    return msg


def dice_game(code, user_id):
    game = Game(code)

    if game.status == False or str(user_id) == game.user_id:
        return False
    else:
        msg = dice_game_info_txt.format(
            game.id_game,
            game.bet,
        )

        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(text='🎲 Кости', callback_data=f'start_game_dice:{game.id_game}')
        )

        return msg, markup


def start_game_dice(code, user_id):
    game = Game(code)
    user = User(user_id)

    if game.status != False and game.bet <= user.balance:
        user.update_balance(-game.bet)
        user = User(user_id)

        game.del_game()

        user1 = random.randint(1, 6)
        user2 = random.randint(1, 6)

        if user1 == user2:
            if user1 == 1:
                user1 += 1
            elif user1 == 6:
                user1 -= 1

        win_money = ((game.bet * 2) / 100) * (100 - float(config.config('percent')))


        if user1 > user2:
            user.update_balance(win_money)

            dice_write_game_log(game.id_game, user_id, 'win', win_money)
            dice_write_game_log(game.id_game, game.user_id, 'lose', win_money)

            status1 = '✅✅✅ Поздравляем с победой!'
            status2 = '🔴🔴🔴 Вы проиграли!'
        elif user1 < user2:
            User(game.user_id).update_balance(win_money)

            dice_write_game_log(game.id_game, game.user_id, 'win', win_money)
            dice_write_game_log(game.id_game, user_id, 'lose', win_money)

            status1 = '🔴🔴🔴 Вы проиграли!'
            status2 = '✅✅✅ Поздравляем с победой!'
        else:
            user.update_balance(game.bet)
            User(game.user_id).update_balance(game.bet)

            dice_write_game_log(game.id_game, game.user_id, 'draw', win_money)
            dice_write_game_log(game.id_game, user_id, 'draw', win_money)

            status1 = '🔵🔵🔵 Ничья!'
            status2 = '🔵🔵🔵 Ничья!'

        msg1 = dice_game_result_txt.format(
            game.id_game,
            '{:.2f}'.format(float(win_money)),
            user1,
            user2,
            status1
        )

        msg2 = dice_game_result_txt.format(
            game.id_game,
            '{:.2f}'.format(float(win_money)),
            user2,
            user1,
            status2
        )

        return [user_id, game.user_id], [msg1, msg2]
    return False


def dice_write_game_log(id, user_id, status, bet):
    conn, cursor = connect()

    cursor.execute(f'INSERT INTO game_logs VALUES("{id}", "{user_id}", "{status}", "{bet}", "{datetime.datetime.now()}")')
    conn.commit()

    cursor.execute(f'SELECT * FROM stats WHERE user_id = "{user_id}"')
    stats = cursor.fetchall()

    if len(stats) == 0:
        cursor.execute(f'INSERT INTO stats VALUES("{user_id}", "0")')
        conn.commit()
    else:
        cursor.execute(f'UPDATE stats SET money = {float(stats[0][1]) + float(bet)} WHERE user_id = "{user_id}"')
        conn.commit()
