import random
import sqlite3 as sql

from datetime import *

from aiogram.types import InputFile

from db_help import User
import time
from keyboards import *
import os
import sqlite3 as sq
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text
import keyboards
import requests
import json
import urllib.request
from aiogram.utils.exceptions import Throttled
import db_help
from datetime import datetime
import asyncio
import datetime
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import func
from glQiwiApi import QiwiP2PClient
from glQiwiApi.qiwi.clients.p2p.types import Bill
import os
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import ReplyKeyboardRemove
from db_help import add_balance, del_balance
from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

# ======

skin = 'Береты "Damascus"' #в кавычки вписать через название скина для вывода

TOKEN = ""
adminid = 1741514552#вписать айди админа
channel = '@end_soft' #в кавычки вписать канал бота

otzivi = -1001843513023
bot.username = 'end_soft'


qiwi = "89655953777"
sber = "<code>2202206201150625</code>"
spb = "wrfw"
yoo = "<code>4100118112602897</code>"
tink = "5536914093470312"


# ======

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())

class Sender(StatesGroup):
    photo = State()
    text = State()

class UserState(StatesGroup):
    suma = State()
    vivod = State()
    screen = State()
    pay = State()
    otziv = State()

# ======
class GoldState(StatesGroup):
    amount_plus = State()
    user_id_plus = State()
    amount_minus = State()
    user_id_minus = State()

class StateMachine(StatesGroup):
    del_gold = State()
    give_gold = State()

class CoinFlip(StatesGroup):
    stake = State()
    choice = State()

class PaymentStates(StatesGroup):
    amount = State()
    payment_system = State()
    screenshot = State()

class SetGoldRate(StatesGroup):
    set_gold_rate = State()

class NewPromoState(StatesGroup):
    name = State()
    limit = State()
    gold = State()

class PromoCode(StatesGroup):
    EnterPromo = State()


db = sq.connect('users.db')
sql = db.cursor()


from aiogram.utils.deep_linking import get_start_link


# ======






#f = open('golds.txt','r')
#pricegold = str(*f)
apiqiwihelp = ""
qiwi_p2p_client = QiwiP2PClient(shim_server_url="play.nanix.fun:80", secret_p2p=apiqiwihelp)#в кавычки вписать секретный киви p2p ключ купить можно @ms_shop_robot



sql.execute('''
    CREATE TABLE IF NOT EXISTS gold_transactions (
        user_id INTEGER,
        amount INTEGER,
        date TEXT
    )
''')

sql.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
        id TEXT PRIMARY KEY,
        cash INTEGER DEFAULT 0,
        
        payment_system TEXT,
        amount INTEGER,
        screenshot BLOB
    )
''')

sql.execute('''create table if not exists user (
    id TEXT,
    name TEXT,
    referrals BIGINT,
    cash INTEGER,
    gold BIGINT,
    referral_code TEXT
    )
''')

sql.execute('''create table if not exists promocodes(
    name TEXT,
    promo_limit TEXT,
    gold TEXT
    )
''')

sql.execute('''create table if not exists used_promocodes(
    user_id TEXT,
    promo_name TEXT
    )
''')

sql.execute('''CREATE TABLE IF NOT EXISTS config1(
    min_withdraw TEXT DEFAULT '50',
    min_deposit TEXT DEFAULT '50'
    )
''')

db.commit()

# Получаем количество записей в таблице config1
sql.execute('SELECT COUNT(*) FROM config1')
count = sql.fetchone()[0]

# Если таблица пуста, то создаем строку с значениями по умолчанию
if count == 0:
    sql.execute("INSERT INTO config1 (min_withdraw, min_deposit) VALUES ('50', '50')")
    db.commit()



@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    sql.execute('SELECT * FROM profiles WHERE id=?', (message.from_user.id,))
    profile = sql.fetchone()

    if profile is None:

        sql.execute('INSERT INTO profiles (id, cash) VALUES (?, 0)', (message.from_user.id,))
        db.commit()

        sql.execute('SELECT * FROM profiles WHERE id=?', (message.from_user.id,))
        profile = sql.fetchone()

    print(message.text[7:])

    if db_help.check_user(message.from_user.id) == None:
        db_help.register_user(message.chat.id, message.from_user.first_name)
        await bot.send_message(adminid, f"🔔 Новый пользователь!\n\n🛠 ID [{message.chat.id} - {message.from_user.first_name}]")
        await message.answer(f'✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>', reply_markup=keyboards.markup_main())
    else:
        await message.answer(f'✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>', reply_markup=keyboards.markup_main())

@dp.callback_query_handler(text='minvivod_setting')
async def min_withdraw_setting(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    # Получаем текущие значения из базы данных и отправляем пользователю
    min_withdraw = sql.execute("SELECT min_withdraw FROM config1").fetchone()[0]
    await bot.send_message(call.from_user.id, f"Текущее минимальное количество для вывода: {min_withdraw}\nВведите новое значение:")

    # Добавляем состояние в хранилище состояний пользователя
    await state.set_state('setting_min_withdraw')

@dp.callback_query_handler(text='mindep_setting')
async def min_deposit_setting(call: CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(call.id)
    # Получаем текущие значения из базы данных и отправляем пользователю
    min_deposit = sql.execute("SELECT min_deposit FROM config1").fetchone()[0]
    await bot.send_message(call.from_user.id, f"Текущее минимальное пополнение: {min_deposit}\nВведите новое значение:")

    # Добавляем состояние в хранилище состояний пользователя
    await state.set_state('setting_min_deposit')

@dp.message_handler(state='setting_min_withdraw')
async def set_min_withdraw(message: Message, state: FSMContext):
    # Получаем введенное пользователем значение
    min_withdraw = message.text

    # Сохраняем значение в базе данных
    sql.execute("UPDATE config1 SET min_withdraw = ?", (min_withdraw,))
    db.commit()

    # Очищаем состояние пользователя
    await state.finish()

    # Отправляем сообщение об успешном изменении
    await bot.send_message(message.from_user.id, f"Минимальное количество для вывода установлено на {min_withdraw}")

@dp.message_handler(state='setting_min_deposit')
async def set_min_deposit(message: Message, state: FSMContext):
    # Получаем введенное пользователем значение
    min_deposit = message.text

    # Сохраняем значение в базе данных
    sql.execute("UPDATE config1 SET min_deposit = ?", (min_deposit,))
    db.commit()

    # Очищаем состояние пользователя
    await state.finish()

    # Отправляем сообщение об успешном изменении
    await bot.send_message(message.from_user.id, f"Минимальное пополнение установлено на {min_deposit}")

@dp.message_handler(text='🔢 Калькулятор')
async def get_profile(message: types.Message,  state: FSMContext):
    price_gold = float(db_help.goldsc()[1])
    await message.answer("<b>Введите количество голды, которую хотите купить и я вам скажу сколько это будет стоить:</b>", reply_markup=keyboards.exitmenu())
    await state.set_state("gold_amount")

@dp.message_handler(state="gold_amount")
async def calculate_gold_price(message: types.Message, state: FSMContext):
    if message.text == "🔙Назад":
        # Обработка нажатия кнопки "Назад"
        await state.finish()
        await message.answer("Вы вернулись в главное меню.", reply_markup=keyboards.markup_main())
        return

    gold_amount = message.text
    price_gold = float(db_help.goldsc()[1])
    if not str.isdigit(gold_amount):
        await message.answer("<b>Введите пожалуйста число</b>", reply_markup=keyboards.exitmenu())
        return
    else:
        gold_amount = float(gold_amount)
        total_price = gold_amount * price_gold
        await message.answer(f"<b>{gold_amount} голды будет стоить {total_price} рублей.</b>", reply_markup=keyboards.markup_main())
    await state.finish()


@dp.message_handler(text='🎮 Мини игры')
async def games(message: types.Message):
    def games_key():
        # функция вернуть клавиатуру
        markup = InlineKeyboardMarkup(row_width=1)
        markup.row(InlineKeyboardButton(text="🪙 Орел и Решка", callback_data="coin_flip"))
        return markup

    text = 'Здесь вы можете посмотреть и сыграть в наши мини-игры!'
    await message.answer(text, reply_markup=games_key())
    
@dp.callback_query_handler(lambda c: c.data == 'coin_flip')
async def coin_flip(callback_query: types.CallbackQuery, state: FSMContext):
    user_info = db_help.check_user(callback_query.from_user.id)
    if user_info:
        if callback_query.message.text == "🔙Назад":
            # Обработка нажатия кнопки "Назад"
            await message.answer("Вы вернулись в главное меню.", reply_markup=keyboards.markup_main())
            return
        
        text = 'Введите сумму, которую хотите поставить:'
        await callback_query.message.answer(text, reply_markup=keyboards.exitmenu())
                 
        await CoinFlip.stake.set()
    else:
        await callback_query.answer('Для начала зарегистрируйтесь /start')

@dp.message_handler(state=CoinFlip.stake)
async def get_stake(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    
    if message.text == "🔙Назад":
        # Обработка нажатия кнопки "Назад"
        await state.finish()
        await message.answer("Вы вернулись в главное меню.", reply_markup=keyboards.markup_main())
        return
    
    if message.text.isdigit():
        stake = int(message.text)
        # Получаем данные пользователя из базы данных
        user_data = sql.execute(f"SELECT cash FROM user WHERE id = '{user_id}'").fetchone()
        user_cash = user_data[0]

        if stake > user_cash:
            await message.answer("Ставка превышает ваш баланс.")
            return

        await state.update_data(stake=stake)
        text = 'Выберите орел или решка:'
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton(text='Орел', callback_data='heads'),
            InlineKeyboardButton(text='Решка', callback_data='tails')
        )
        await message.answer(text, reply_markup=markup)
        await CoinFlip.choice.set()
    else:
        text = 'Некорректная ставка, введите сумму числом'
        await message.answer(text)

@dp.callback_query_handler(state=CoinFlip.choice)
async def get_choice(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    stake = data.get('stake')
    if callback_query.data == 'heads':
        coin = random.choices(['heads', 'tails'], weights=(3, 7), k=1)[0] # изменен вес на (3, 7)
        if coin == 'heads':
            winnings = stake * 2
            text = f'Вы выиграли {winnings}!\nРезультат: орел'
            db_help.add_balance(callback_query.from_user.id, winnings)
        else:
            text = f'Вы проиграли {stake} :( \nРезультат: решка'
            db_help.del_balance(callback_query.from_user.id, stake)
    elif callback_query.data == 'tails':
        coin = random.choices(['heads', 'tails'], weights=(7, 3), k=1)[0] # изменен вес на (7, 3)
        if coin == 'tails':
            winnings = stake * 2
            text = f'Вы выиграли {winnings}!\nРезультат: решка'
            db_help.add_balance(callback_query.from_user.id, winnings)
        else:
            text = f'Вы проиграли {stake} :( \nРезультат: орел'
            db_help.del_balance(callback_query.from_user.id, stake)
    else:
        text = 'Некорректный выбор'
    await callback_query.message.answer(text, reply_markup=keyboards.markup_main())
    await state.finish()


@dp.message_handler(text='🔙Назад', state='*')
async def go_back(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, '<b>Вы вернулись назад</b>', reply_markup=keyboards.markup_main())


@dp.message_handler(text='ℹ️ Информация')
async def info(message: types.Message):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('💭 Чат', url="https://t.me/end_soft")
    btn2 = InlineKeyboardButton('📊 Канал', url="https://t.me/end_soft")
    btn3 = InlineKeyboardButton('📉 Курс', callback_data='course')
    btn4 = InlineKeyboardButton('Топ дня', callback_data='top_day')
    btn5 = InlineKeyboardButton('Топ недели', callback_data='top_week')
    btn6 = InlineKeyboardButton('Топ месяца', callback_data='top_month')
    markup.row(btn2)
    markup.row(btn3)
    markup.row(btn4, btn5, btn6)
    await message.answer('Выберите нужный пункт:', reply_markup=markup)


@dp.callback_query_handler(text='course')
async def top_week(callback_query: types.CallbackQuery):


    # Формируем текст сообщения с топ-5 транзакций
    pricegold = float(db_help.goldsc()[1])
    ponprice = pricegold * 100

    # Отправляем сообщение с топ-5 транзакций и всплывающим уведомлением
    await bot.answer_callback_query(callback_query.id, text=f'🥇 Курс голды на данный момент - {ponprice} рублей за 100 голды', show_alert=True)
    

@dp.callback_query_handler(text='top_day')
async def top_day(callback_query: types.CallbackQuery):
    # Получаем список 5 самых крупных транзакций за последние 24 часа
    sql.execute('''
                SELECT user_id, amount
                FROM gold_transactions
                WHERE date >= datetime('now', '-1 day')
                ORDER BY amount DESC
                LIMIT 5
                ''')
    top_transactions = sql.fetchall()

    # Формируем текст сообщения с топ-5 транзакций
    message_text = 'Топ-5 крупнейших покупок за последние 24 часа:\n\n'
    for i, transaction in enumerate(top_transactions, start=1):
        message_text += f'{i}. {transaction[1]:.2f} голды\n'

    # Отправляем сообщение с топ-5 транзакций и всплывающим уведомлением
    await bot.answer_callback_query(callback_query.id, text=f'{message_text}', show_alert=True)

@dp.callback_query_handler(text='top_week')
async def top_week(callback_query: types.CallbackQuery):
    # Получаем список 5 самых крупных транзакций за последнюю неделю
    sql.execute('''
                SELECT user_id, amount
                FROM gold_transactions
                WHERE date >= datetime('now', '-7 days')
                ORDER BY amount DESC
                LIMIT 5
                ''')
    top_transactions = sql.fetchall()

    # Формируем текст сообщения с топ-5 транзакций
    message_text = 'Топ-5 крупнейших покупок за последнюю неделю:\n\n'
    for i, transaction in enumerate(top_transactions, start=1):
        message_text += f'{i}. {transaction[1]:.2f} голды\n'

    # Отправляем сообщение с топ-5 транзакций и всплывающим уведомлением
    await bot.answer_callback_query(callback_query.id, text=f'{message_text}', show_alert=True)
    
@dp.callback_query_handler(text='top_month')
async def top_month(callback_query: types.CallbackQuery):
    # Получаем список 5 самых крупных транзакций за последний месяц
    sql.execute('''
                SELECT user_id, amount
                FROM gold_transactions
                WHERE date >= datetime('now', '-30 days')
                ORDER BY amount DESC
                LIMIT 5
                ''')
    top_transactions = sql.fetchall()

    # Формируем текст сообщения с топ-5 транзакций
    message_text = 'Топ-5 крупнейших покупок за последний месяц:\n\n'
    for i, transaction in enumerate(top_transactions, start=1):
        message_text += f'{i}. {transaction[1]:.2f} голды\n'

    # Отправляем сообщение с топ-5 транзакций и всплывающим уведомлением
    await bot.answer_callback_query(callback_query.id, text=f'{message_text}', show_alert=True)

@dp.message_handler(text='💲 Пополнить баланс')
async def test(message: types.Message):
    cash = sql.execute("SELECT cash FROM user WHERE id == '{key}'".format(key=message.from_user.id)).fetchone()
    user = User(message.from_user.id)
    await message.answer(f"⬇️⬇️⬇️", reply_markup=keyboards.exitmenu())

    await bot.send_message(message.from_user.id, "Выберите платежную систему:", reply_markup=get_payment_systems_keyboard())

@dp.message_handler(text='🙎🏼‍♂ Профиль')
async def get_profile(message: types.Message):
    user = User(message.from_user.id)
    await message.answer(f"<b>⚙️ Профиль\n\nID - {message.from_user.id}\nБаланс (голда) - {user.cash}</b>", reply_markup=keyboards.profile())

@dp.message_handler(text='🧳 Кейсы')
async def case_menu(message: types.Message):
    user = User(message.from_user.id)
    await message.answer(f"<b>Баланс (голда) - {user.cash}</b>")
    markup = InlineKeyboardMarkup(row_width=2)
    novice_case_button = InlineKeyboardButton('🧳 Кейс "Новичок"', callback_data='novice_case')
    master_case_button = InlineKeyboardButton('🧳 Кейс "Master"', callback_data='master_case')
    markup.add(master_case_button)
    await message.answer('Выберите кейсы:', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data in ['novice_case', 'master_case'])
async def process_case(callback_query: types.CallbackQuery):
    user = User(callback_query.from_user.id)
    case = {}
    if callback_query.data == 'novice_case':
        case['title'] = 'Новичок'
        case['items'] = [
            {'name': 'Awm Dragon', 'price': 35},
            {'name': 'Akr Carbon', 'price': 20},
            {'name': 'Glock', 'price': 10},
            {'name': 'M4', 'price': 10},
        ]
        case['price'] = 20
    else:
        case['title'] = 'Master'
        case['items'] = [
            {'name': 'USP Ray', 'price': 10},
            {'name': 'FAMAS Anger ST', 'price': 12},
            {'name': 'UMP4 White Carbon', 'price': 15},
            {'name': 'USP Purple Camo', 'price': 15},
            {'name': 'MP7 Winter Sport', 'price': 20},
            {'name': 'SM Arctic', 'price': 23},
            {'name': 'AKR12 Carbon', 'price': 25},
            {'name': 'AWM Gear', 'price': 27},
            {'name': 'M4 Lizard', 'price': 30},
            {'name': 'P350 Neon', 'price': 50},
        ]
        case['price'] = 20
    items_text = '\n'.join([f"{i+1}. {item['name']} - {item['price']}G" for i, item in enumerate(case['items'])])
    await callback_query.message.edit_text(f"🧳 Кейс «{case['title']}»\nСодержание кейса:\n{items_text}\n💲 Стоимость: {case['price']} руб.")
    markup = InlineKeyboardMarkup(row_width=2)
    back_button = InlineKeyboardButton('🔙 Назад', callback_data='back')
    buy_button = InlineKeyboardButton('💲 Купить', callback_data=f'buy_case_{callback_query.data}')
    markup.add(back_button, buy_button)
    await callback_query.message.reply('Выберите действие:', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data in ['back'])
async def cancel_case(callback_query: types.CallbackQuery):
    markup = InlineKeyboardMarkup(row_width=2)
    novice_case_button = InlineKeyboardButton('🧳 Кейс "Новичок"', callback_data='novice_case')
    master_case_button = InlineKeyboardButton('🧳 Кейс "Master"', callback_data='master_case')
    markup.add(master_case_button)
    await callback_query.message.edit_text('Выберите кейсы:', reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data.startswith('buy_case_'))
async def buy_case(callback_query: types.CallbackQuery):
    case_type = callback_query.data.split('_')[-1]
    user = User(callback_query.from_user.id)
    case = {}
    if case_type == 'novice_case':
        case['title'] = 'Новичок'
        case['items'] = [
            {'name': 'Awm Dragon', 'price': 35},
            {'name': 'Akr Carbon', 'price': 20},
            {'name': 'Glock', 'price': 10},
            {'name': 'M4', 'price': 10},
        ]
        case['price'] = 20
    else:
        case['title'] = 'Master'
        case['items'] = [
            {'name': 'USP Ray', 'price': 10},
            {'name': 'FAMAS Anger ST', 'price': 12},
            {'name': 'UMP4 White Carbon', 'price': 15},
            {'name': 'USP Purple Camo', 'price': 15},
            {'name': 'MP7 Winter Sport', 'price': 20},
            {'name': 'SM Arctic', 'price': 23},
            {'name': 'AKR12 Carbon', 'price': 25},
            {'name': 'AWM Gear', 'price': 27},
            {'name': 'M4 Lizard', 'price': 30},
            {'name': 'P350 Neon', 'price': 50},
        ]
        case['price'] = 20
    if user.cash >= case['price']:
        item = random.choice(case['items'])
        del_balance(callback_query.from_user.id, case['price'])
        add_balance(callback_query.from_user.id, item['price'])
        await callback_query.message.reply(f"🎉 Поздравляем, вы выиграли {item['name']} за {item['price']}!")
        await callback_query.answer()
    else:
        await callback_query.message.reply('❌ Недостаточно средств на балансе.')
        await callback_query.answer()

@dp.message_handler(text='💲 Купить')
async def buy_gold(message: types.Message):
    user = User(message.from_user.id)
    price_gold = float(db_help.goldsc()[1])
    await message.answer(f"<b>Введите кол-во голды для покупки\n\nВаш баланс - {user.cash} голды/{db_help.check_user(message.from_user.id)[4]} рублей\n\nКурс голды - {price_gold} рублей за 1 голду</b>", reply_markup=keyboards.exitmenu())
    await UserState.suma.set()
    
    
@dp.message_handler(text='📤 Вывести')
async def withdraw_gold(message: types.Message):
    user = User(message.from_user.id)
    await message.answer(f"<b>Введите кол-во голды для вывода\n\nВаш баланс - {user.cash} голды/{db_help.check_user(message.from_user.id)[4]} рублей</b>", reply_markup=keyboards.exitmenu())
    await UserState.vivod.set()

@dp.message_handler(text='📝 Отзывы')
async def withdraw_gold(message: types.Message):
    await message.answer("<b>⬇️ Наши отзывы</b>", reply_markup=keyboards.otzivi_key())
    

@dp.message_handler(text="🛠 Поддержка")
async def support_handler(message: types.Message):
	await test(await message.answer(f"✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>", reply_markup=keyboards.supportMenu()))

back_markup = types.InlineKeyboardMarkup()
back_markup.add(types.InlineKeyboardButton(text="❌", callback_data="back"))

#@dp.callback_query_handler(text="back", state="*")
#async def go_to_main_menu(call: types.CallbackQuery, state: FSMContext):
 #   user = User(call.from_user.id)
 #   await call.message.edit_text(f'✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>', reply_markup=keyboards.markup_main())
 #   await state.finish()

@dp.callback_query_handler(text="exit")
async def test(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f'✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>', reply_markup=keyboards.markup_main())

@dp.message_handler(content_types=["photo"], state=UserState.screen)
async def golda(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.photo[-1].download("screen.jpg")
    photo = InputFile("screen.jpg")
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(InlineKeyboardButton(text="✅", callback_data=f"a_{message.from_user.id}"))
    await bot.send_photo(chat_id=adminid, photo=photo, caption= f'Вывод голды {data["golds"]} голды\n\nID Пользователя - {data["ids"]}', reply_markup=markup)
    await message.answer('<b>Ожидайте вывод, вам придет уведомление❤️</b>', reply_markup=keyboards.markup_main())
    await state.finish()
@dp.callback_query_handler(text_startswith="a_")
async def test(call: types.CallbackQuery):
    ids = call.data.split('_')[1]
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(InlineKeyboardButton(text="Оставить отзыв", callback_data="otziiv"))
    await bot.send_message(ids, f"✅ Администратор подтвердил вывод голды. Оставьте отзыв нажав на кнопку ниже", reply_markup=markup)
    await bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@dp.callback_query_handler(text="otziiv")
async def test(call: types.CallbackQuery):
    await bot.edit_message_text(chat_id=call.message.chat.id, 
                                message_id=call.message.message_id, 
                                text="Напишите текст отзыва", 
                                reply_markup=None)
    await UserState.otziv.set()

	

@dp.callback_query_handler(text="golds")
async def test(call: types.CallbackQuery):
    pricegold = float(db_help.goldsc()[1])
    ponprice = pricegold * 100
    await call.message.edit_text(f"<b>🥇 Курс голды на данный момент - {ponprice} рублей за 100 голды</b>", reply_markup=keyboards.exitmenu())


# функция для получения номера заказа из файла
def get_order_number():
    if os.path.exists('orders.txt'): # проверяем существование файла
        with open('orders.txt', 'r') as f:
            order_number = int(f.read())
    else: # если файла нет, начинаем нумерацию с 1
        order_number = 1
    return order_number

# функция для сохранения номера заказа в файл
def save_order_number(order_number):
    with open('orders.txt', 'w') as f:
        f.write(str(order_number))

@dp.message_handler(state=UserState.otziv)
async def get_otziv(message: types.Message, state: FSMContext):
    data = await state.get_data()
    order_number = get_order_number() # генерируем уникальный номер отзыва
    otziv_text = f"{message.from_user.first_name}: {message.text}" # получаем текст отзыва
    otziv_date = message.date.strftime('%d.%m.%Y') # получаем дату отзыва в нужном формате
    otziv_message = f"Отзыв №{order_number} ⭐️⭐️⭐️⭐️⭐️\n\n{otziv_text}\n\nВывел {otziv_date}" # формируем текст сообщения
    await bot.send_message(otzivi, otziv_message) # отправляем сообщение в канал otzivi
    await message.reply('Спасибо за отзыв!', reply_markup=keyboards.markup_main()) # отвечаем пользователю
    order_number += 1
    save_order_number(order_number)
    await state.finish() # завершаем состояние FSMContext



def get_payment_systems_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("Qiwi", callback_data="payment_system:qiwi"),
        types.InlineKeyboardButton("Sber", callback_data="payment_system:sber"),
        types.InlineKeyboardButton("Tinkoff", callback_data="payment_system:tink"),
    )
    return keyboard

qiwi = "89655953777"
sber = "<code>2202206201150625</code>"
spb = "wrfw"
yoo = "<code>4100118112602897</code>"
tink = "5536914093470312"

@dp.callback_query_handler(lambda c: c.data.startswith('payment_system'))
async def process_payment_system(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.data == "🔙Назад":
        # Обработка нажатия кнопки "Назад"
        await bot.send_message(callback_query.from_user.id, "Вы вернулись в главное меню.", reply_markup=keyboards.markup_main())
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        await state.finish()

        return

    payment_system = callback_query.data.split(':')[1]

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Вы выбрали платежную систему: {payment_system}", reply_markup=keyboards.exitmenu())

    await state.update_data(payment_system=payment_system)

    if payment_system == "qiwi":
        await bot.send_message(callback_query.from_user.id, f"<b>Ссылка для оплаты Qiwi:</b> {qiwi}")
    if payment_system == "sber":
        await bot.send_message(callback_query.from_user.id, f"<b>Номер карты для оплаты СберБанк:</b> <code>{sber}</code>", reply_markup=keyboards.exitmenu())
    if payment_system == "yoomey":
        await bot.send_message(callback_query.from_user.id, f"<b>Номер счета YooMoney  для оплаты:</b> <code>{yoo}</code>", reply_markup=keyboards.exitmenu())

    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.send_message(callback_query.from_user.id, "<b>Введите сумму пополнения:</b>", reply_markup=keyboards.exitmenu())
    await PaymentStates.amount.set()

@dp.message_handler(state=PaymentStates.amount)
async def process_amount(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await bot.send_message(message.from_user.id, "Пожалуйста, введите числовое значение.")
        return

    amount = int(message.text)
    if message.text == "🔙Назад":
        # Обработка нажатия кнопки "Назад"
        await message.answer("Вы вернулись в главное меню.", reply_markup=keyboards.markup_main())
        await bot.delete_message(message.chat.id, message.message_id)
        await state.finish()

        return
    # Retrieve the minimum deposit value from the database
    min_deposit = sql.execute("SELECT min_deposit FROM config1").fetchone()[0]

    # Check if the deposit amount is less than the minimum deposit value
    if amount < int(min_deposit):
        await state.finish()
        await bot.send_message(message.from_user.id, f"Минимальная сумма пополнения {min_deposit} рублей.", reply_markup=keyboards.markup_main())
        return

    await state.update_data(amount=amount)
    pricegolda = float(db_help.goldsc()[1])
    goldamount = amount / pricegolda

    await bot.send_message(message.from_user.id, f"<b>За {amount} рублей, вы получите {goldamount} голды</b>")
    await bot.send_message(message.from_user.id, f"""<b>🐻: Теперь отправь деньги на отправленные выше реквизиты:
💰 Сумма: {amount} ₽

📸 Отправь сюда в чат скриншот чека:</b>""")
    await PaymentStates.screenshot.set()


@dp.message_handler(state=UserState.suma)
async def get_username(message: types.Message, state: FSMContext):
    if message.text.isdigit() == True:
        pricegolda = float(db_help.goldsc()[1])
        balnce = float(message.text)//pricegolda
        if balnce >= 50:
            balnce = float(message.text)*pricegolda
            if db_help.check_user(message.from_user.id)[4] >= balnce:
                await state.finish()
                db_help.del_gold(message.from_user.id, balnce)
                db_help.add_balance(message.from_user.id, message.text)
                await bot.send_message(message.from_user.id, f"✅ <b>Вы купили {message.text} голды! За {balnce} рублей</b>")
                await bot.send_message(adminid, f"🔔 <b>{message.from_user.id} - {message.from_user.first_name} купил - {message.text} G по курсу - {float(db_help.goldsc()[1])}, на {balnce}</b>")
            else:
                await state.finish()
                await bot.send_message(message.from_user.id, f"❗️ <b>У вас недостаточно денег!</b>", reply_markup=keyboards.exitmenu())
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, f"❗️ <b>У вас недостаточно денег!\n\nМинимальная сумма покупки - 50 рублей</b>")
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, f"❗️ <b>Введите число!</b>")


@dp.message_handler(content_types=types.ContentType.PHOTO, state=PaymentStates.screenshot)
async def process_screenshot(message: types.Message, state: FSMContext):

    await state.update_data(screenshot=message.photo[-1].file_id)

    data = await state.get_data()
    payment_system = data.get('payment_system')
    amount = data.get('amount')
    screenshot = data.get('screenshot')


    sql.execute('UPDATE profiles SET payment_system=?, amount=?, screenshot=? WHERE id=?',
                   (payment_system, amount, screenshot, message.from_user.id))
    db.commit()


    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Принять", callback_data=f"accept:{message.from_user.id}"),
        InlineKeyboardButton("Отклонить", callback_data=f"reject:{message.from_user.id}")
    )

    admin_id = 6190927801 # админ айди
    await bot.send_message(adminid, "<b>Пришла новая заявка на пополнение💵</b>")


    await state.finish()

    await bot.send_message(message.from_user.id, "Ваша заявка принята и будет обработана администратором.", reply_markup=keyboards.markup_main())



@dp.callback_query_handler(lambda c: c.data.startswith('accept:') or c.data.startswith('reject:'))
async def process_application(callback_query: types.CallbackQuery):
    action, user_id = callback_query.data.split(':')
    user_id = int(user_id)
    user = User(callback_query.from_user.id)

    if action == 'accept':
        sql.execute('SELECT * FROM profiles WHERE id=?', (user_id,))
        application = sql.fetchone()

        sql.execute('SELECT * FROM user WHERE id=?', (user_id,))
        app = sql.fetchone()

        balance = application[3]

        print(f'{user_id} пополнил {balance}')

        # Обновляем баланс пользователя
        sql.execute('UPDATE profiles SET cash=? WHERE id=?', (0, user_id))
        sql.execute('UPDATE profiles SET amount=? WHERE id=?', (0, user_id))

        db.commit()

        pricegolda = float(db_help.goldsc()[1])
        balanceplus = balance / pricegolda 
        db_help.add_balance(user_id, balanceplus)
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        sql.execute('''
                    INSERT INTO gold_transactions (user_id, amount, date)
                    VALUES (?, ?, ?)
                    ''', (user_id, balanceplus, now))
        db.commit()

        # Отправляем сообщение администратору с информацией о новом пополнении
        await bot.send_message(user_id, f"<b>Ваша заявка на пополнение на {application[3]} рублей принята🤑.</b>")
    elif action == 'reject':
        sql.execute('UPDATE profiles SET cash=? WHERE id=?', (0, user_id))
        sql.execute('UPDATE profiles SET amount=? WHERE id=?', (0, user_id))

        await bot.send_message(user_id, "Ваша заявка на пополнение отклонена😭.")

    db.commit()
    await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(commands=['balance'])
async def cmd_balance(message: types.Message):
    sql.execute('SELECT * FROM profiles WHERE id=?', (message.from_user.id,))
    profile = sql.fetchone()
    user = User(message.from_user.id) 

    if profile is not None:
        await message.reply(f"Ваш текущий баланс: {user.cash}")
    else:
        await message.reply("Профиль пользователя не найден.")

    db.commit()




@dp.message_handler(state=UserState.vivod)
async def get_username(message: types.Message, state: FSMContext):
    min_vivod = sql.execute("SELECT min_withdraw FROM config1").fetchone()[0]
    if message.text == "🔙Назад":
        # Обработка нажатия кнопки "Назад"
        await state.finish()
        await message.answer("Вы вернулись в главное меню.", reply_markup=keyboards.markup_main())
        await bot.delete_message(callback_query.message.chat.id, callback_query.message.message_id)
        return


    if message.text.isdigit() == True:
        if int(db_help.check_user(message.from_user.id)[3]) >= int(message.text):
            if int(message.text) >= int(min_vivod):
                photo = InputFile("example.jpg")
                gold = float(message.text)+float(message.text)*float(0.25)
                db_help.del_balance(message.from_user.id, message.text)
                await bot.send_photo(chat_id=message.chat.id, photo=photo, caption=f'<b>Выставьте скин {skin} за {gold} голды\nЗатем отправьте скриншот скина на рынке. (как в прикрепленном изображении)</b>', reply_markup=ReplyKeyboardRemove())
                await state.update_data(ids=message.from_user.id, golds=gold)
                await state.update_data(golds=gold) # сохраняем данные golds в состоянии FSMContext
                await UserState.screen.set()
            else:
                await state.finish()
                await bot.send_message(message.from_user.id, f"❗️ <b>Минимальная сумма для вывода - {min_vivod} G!</b>", reply_markup=keyboards.exitmenu())
        else:
            await state.finish()
            await bot.send_message(message.from_user.id, f"❗️ <b>У вас недостаточно голды!</b>", reply_markup=keyboards.exitmenu())
    else:
        await state.finish()
        await bot.send_message(message.from_user.id, f"❗️ <b>Введите число!</b>", reply_markup=keyboards.exitmenu())

@dp.message_handler(commands=["a"])
async def admin_panel(message: types.Message):
    if message.from_user.id==adminid:
        markup = keyboards.aadmin(message.from_user.id)
        await bot.send_message(chat_id=message.chat.id, text="Админ панель", reply_markup=markup)


@dp.callback_query_handler(lambda c: c.data == 'buygolda')
async def process_buygolda(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    # Получаем все заявки из базы данных
    sql.execute('SELECT * FROM profiles WHERE payment_system IS NOT NULL AND amount IS NOT NULL AND screenshot IS NOT NULL')
    rows = sql.fetchall()

    non_zero_rows = []  # Создаем список для ненулевых заявок

    # Фильтруем заявки с ненулевой суммой пополнения
    for row in rows:
        if row[3] != 0:
            non_zero_rows.append(row)

    if len(non_zero_rows) == 0:
        # Если заявок нет, выводим сообщение об этом
        await bot.send_message(callback_query.from_user.id, "На данный момент заявок на пополнение нет.")
    else:
        # Если заявки есть, выводим их все
        for row in non_zero_rows:
            user_id = row[0]
            payment_system = row[2]
            amount = row[3]
            screenshot_file_id = row[4]

            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                InlineKeyboardButton("Принять", callback_data=f"accept:{user_id}"),
                InlineKeyboardButton("Отклонить", callback_data=f"reject:{user_id}")
            )

            await bot.send_photo(callback_query.from_user.id, screenshot_file_id,
                                 caption=f"Платежная система: {payment_system}\nСумма пополнения: {amount}",
                                 reply_markup=keyboard)

@dp.callback_query_handler(lambda c: c.data == 'promo_setting')
async def process_callback_promo_setting(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    markup = keyboards.promo_menu(user_id)
    await bot.send_message(user_id, "Выберите действие", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == 'super')
async def add_gold(callback_query: CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Введите количество голды, которое нужно снять:")
    await GoldState.amount_minus.set()

@dp.message_handler(state=GoldState.amount_minus)
async def get_user_id(message: Message, state: FSMContext):
    amount = message.text
    await state.update_data(amount=amount)
    await message.answer("Введите id пользователя:")
    await GoldState.user_id_minus.set()

@dp.message_handler(state=GoldState.user_id_minus)
async def process_gold(message: Message, state: FSMContext):
    user_id = message.text
    amount = (await state.get_data())['amount']
    if message.text.isdigit():
        if amount.isdigit():
            db_help.del_balance(user_id, amount)
            await message.answer(f"У пользователя {user_id} успешно снято {amount} голды.")
            await state.finish()

        else:
            await message.answer("Введите количество голды в виде числа.")
    else:
        await message.answer("Вы ввели неправильный id пользователя.")
        await state.finish()



@dp.callback_query_handler(lambda c: c.data == 'start')
async def del_gold(callback_query: CallbackQuery):
    await callback_query.answer()
    await bot.send_message(callback_query.from_user.id, "Введите количество голды, которое нужно выдать:")
    await GoldState.amount_plus.set()

@dp.message_handler(state=GoldState.amount_plus)
async def get_user_id(message: Message, state: FSMContext):
    amount = message.text
    await state.update_data(amount=amount)
    await message.answer("Введите id пользователя:")
    await GoldState.user_id_plus.set()

@dp.message_handler(state=GoldState.user_id_plus)
async def process_gold(message: Message, state: FSMContext):
    user_id = message.text
    amount = (await state.get_data())['amount']
    if message.text.isdigit():
        if amount.isdigit():
            db_help.add_balance(user_id, amount)
            await message.answer(f"У пользователя {user_id} успешно добавлено {amount} голды.")
            await state.finish()
        else:
            await message.answer("Введите количество голды в виде числа.")
    else:
        await message.answer("Вы ввели неправильный id пользователя.")
        await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'database')
async def command_start(message: types.Message):
    await bot.send_document(chat_id=adminid, document = open('users.db', 'rb'), caption = f'   BACKUP от {datetime.datetime.now()}')

@dp.callback_query_handler(lambda c: c.data == 'backup')
async def command_start(message: types.Message):
     await backup()
     await message.answer('Бекап система включена')


@dp.message_handler(commands=["dbg"])
async def command_start(message: types.Message):
    db_help.dbgolds()

@dp.callback_query_handler(lambda callback_query: callback_query.data == 'rate')
async def change_rate(callback_query: types.CallbackQuery, state: FSMContext):
    if callback_query.from_user.id == adminid:
        await bot.answer_callback_query(callback_query.id)
        await bot.send_message(callback_query.from_user.id, "Введите новый курс золота:")
        await SetGoldRate.set_gold_rate.set()  # Set the state to input the new gold rate
    else:
        await bot.answer_callback_query(callback_query.id, text="У вас нет прав для выполнения этой команды")


@dp.message_handler(state=SetGoldRate.set_gold_rate)
async def set_gold_rate(message: types.Message, state: FSMContext):
    if message.from_user.id == adminid:
        cours = message.text.strip()

        # Преобразуем строку с курсом золота в числовое значение
        gold_rate = float(cours)
        
        db_help.golds(gold_rate)  # Update the gold rate in the database
        await message.answer(f'Курс золота успешно изменен')
        await bot.send_message(adminid, f'Новый курс золота: {gold_rate}')  # Send confirmation message to admin
        await state.finish()
    else:
        await message.answer("У вас нет прав для выполнения этой команды")	

@dp.callback_query_handler(lambda c: c.data == 'back', state='*')
async def back(callback_query: types.CallbackQuery, state: FSMContext):
    # Отменяем текущее состояние
    await callback_query.message.answer('Отмена рассылки.')
    await state.finish()


# функция для обработки нажатия кнопки "Рассылка"
@dp.callback_query_handler(lambda c: c.data == 'mail')
async def send_message(callback_query: types.CallbackQuery):
    # создание клавиатуры с выбором "с картинкой" или "без картинки"
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(text="С картинкой", callback_data="photo"), InlineKeyboardButton(text="Без картинки", callback_data="text"))
    markup.row(InlineKeyboardButton(text="Назад", callback_data="back"))
    # отправка сообщения с выбором
    await bot.send_message(callback_query.from_user.id, "Выберите тип рассылки:", reply_markup=markup)
    # переход к состоянию выбора типа рассылки
    await Sender.photo.set()

# функция для обработки нажатия кнопки "С картинкой" или "Без картинки" в состоянии выбора типа рассылки
@dp.callback_query_handler(lambda c: c.data in ['photo', 'text'], state=Sender.photo)
async def send_message_type(callback_query: types.CallbackQuery, state: FSMContext):
    # получение выбранного типа рассылки
    message_type = "с картинкой" if callback_query.data == 'photo' else "без картинки"
    # сохранение выбранного типа рассылки в контексте пользователя
    await state.update_data(message_type=message_type)
    # отправка сообщения с просьбой отправить картинку, если выбран тип рассылки "с картинкой"
    if callback_query.data == 'photo':
        await bot.send_message(callback_query.from_user.id, "Отправьте картинку для рассылки:")
        # переход к состоянию отправки картинки
        await Sender.photo.set()
    # отправка сообщения с просьбой отправить текст, если выбран тип рассылки "без картинки"
    elif callback_query.data == 'text':
        await bot.send_message(callback_query.from_user.id, "Введите текст рассылки:")
        # переход к состоянию отправки текста
        await Sender.text.set()

@dp.message_handler(content_types=['photo'], state=Sender.photo)
async def check_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        file_id = message.photo[-1].file_id
        await bot.send_message(message.from_user.id, "Введите текст рассылки:")
        # сохранение идентификатора фото в контексте пользователя
        data['file_id'] = file_id
        await state.set_data(data)
        # переход к состоянию отправки текста
    await Sender.text.set()



# функция для обработки отправки текста в состоянии отправки текста
@dp.message_handler(content_types=['text'], state=Sender.text)
async def send_message_text(message: types.Message, state: FSMContext):
    # получение выбранного типа рассылки и идентификатора фото (если есть) из контекста пользователя
    await bot.send_message(message.from_user.id, f"<b>Рассылка запущена</b>")

    data = await state.get_data()
    message_type = data.get('message_type')
    file_id = data.get('file_id', None)
    # получение списка всех пользователей
    users = sql.execute("select id from user").fetchall()
    receive_users = 0 # переменная для хранения количества пользователей, которые получили рассылку
    block_users = 0 # переменная для хранения количества пользователей, которые не получили рассылку
    # отправка сообщения со статистикой рассылки
    async def send_result():
        await bot.send_message(message.from_user.id, f"*Рассылка завершена*\nСообщение получили: *{receive_users}*\nСообщение не получили: *{block_users}*", parse_mode='Markdown')
    # отправка сообщений с картинкой и текстом для всех пользователей
    for user in users:
        try:
            # отправка сообщения с картинкой
            if file_id:
                await bot.send_photo(user[0], file_id, caption=message.text)
            # отправка сообщения без картинки
            else:
                await bot.send_message(user[0], message.text)
            # увеличение счетчика получивших рассылку пользователей
            receive_users += 1
        except:
            # увеличение счетчика не получивших рассылку пользователей
            block_users += 1
        # задержка отправки следующего сообщения, чтобы не превышать лимиты Telegram API
        await asyncio.sleep(1)
    # отправка сообщения со статистикой рассылки
    asyncio.create_task(send_result())
    # переход к состоянию без состояния
    await state.finish()

# функция для обработки нажатия кнопки "Статистика"
@dp.callback_query_handler(lambda c: c.data == 'pro')
async def send_statistics(callback_query: types.CallbackQuery):
    # получение количества пользователей в базе данных
    user_count = db_help.get_user_count()
    # отправка сообщения со статистикой
    await bot.send_message(callback_query.from_user.id, f"Количество пользователей в боте: {user_count}")


# ======

async def my_function():

    await bot.send_document(chat_id=adminid, document = open('users.db', 'rb'), caption = f'🔔 BACKUP от {datetime.datetime.now()}')

async def schedule_function():
    while True:
        now = datetime.datetime.now()
        if now.hour == 0 and now.minute == 0 and now.second == 0:
            # Запуск функции в 12:00:00
            asyncio.ensure_future(my_function())
        await asyncio.sleep(1)


@dp.callback_query_handler(lambda c: c.data == 'reff')
async def process_reff_callback(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    referals = db_help.get_referrals(user_id)[2]
    referral_link = f"https://t.me/{bot.username}?start={user_id}"
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton(text=f"👥 Рефералы: {referals}", callback_data="dummy"))
    markup.add(InlineKeyboardButton(text="❌", callback_data="exit"))
    await bot.send_message(
        callback_query.from_user.id,
        text="🏆 Реферальная система\n\n"
             "📤 Отправьте ссылку ниже вашим друзьям. Если Ваш друг зарегистрируется по ссылке и купит у нас голду, то вы получите процент с его покупок!"
             "\n\n👇Ваша ссылка для приглашения👇"
             f"\n<code>{referral_link}</code>",
        reply_markup=markup,
    )

@dp.callback_query_handler(lambda c: c.data == 'buygolda')
async def process_buygolda(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)

    # Получаем все заявки из базы данных
    sql.execute('SELECT * FROM profiles WHERE payment_system IS NOT NULL AND amount IS NOT NULL AND screenshot IS NOT NULL')
    rows = sql.fetchall()

    if len(rows) == 0:
        # Если заявок нет, выводим сообщение об этом
        await bot.send_message(callback_query.from_user.id, "На данный момент заявок на пополнение нет.")
    else:
        # Если заявки есть, выводим их все
        for row in rows:
            user_id = row[0]
            payment_system = row[2]
            amount = row[3]
            screenshot_file_id = row[4]

            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                InlineKeyboardButton("Принять", callback_data=f"accept:{user_id}"),
                InlineKeyboardButton("Отклонить", callback_data=f"reject:{user_id}")
            )

            await bot.send_photo(callback_query.from_user.id, screenshot_file_id,
                                 caption=f"Платежная система: {payment_system}\nСумма пополнения: {amount}",
                                 reply_markup=keyboard)

    # Возвращаем пользователя на главную страницу
    await bot.send_message(callback_query.from_user.id, "Главное меню", reply_markup=aadmin(callback_query.from_user.id))

@dp.callback_query_handler(text="exit")
async def test(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text(f'✅ <b>Спасибо что выбрали нас!❤️ \n\n❗️ Подпишись на наш телеграмм канал, там публикуются новости, конкурсы - {channel}</b>', reply_markup=keyboards.markup_main())

async def handle_newpromo_command(message: types.Message):
    # Запрос названия промокода
    await message.answer("Введите название промокода:")
    await NewPromoState.name.set()

@dp.message_handler(state=NewPromoState.name)
async def handle_newpromo_name(message: types.Message, state: FSMContext):
    # Сохраняем название промокода
    promo_name = message.text
    await state.update_data(name=promo_name)
    
    # Запрос лимита промокода
    await message.answer("Введите лимит промокода (количество использований):")
    await NewPromoState.limit.set()

@dp.message_handler(state=NewPromoState.limit)
async def handle_newpromo_limit(message: types.Message, state: FSMContext):
    # Сохраняем лимит промокода
    promo_limit = int(message.text)
    await state.update_data(limit=promo_limit)
    
    # Запрос количества голды за промокод
    await message.answer("Введите количество голды, которое будет выдано за промокод:")
    await NewPromoState.gold.set()

@dp.message_handler(state=NewPromoState.gold)
async def handle_newpromo_gold(message: types.Message, state: FSMContext):
    # Сохраняем количество голды за промокод
    promo_gold = int(message.text)
    await state.update_data(gold=promo_gold)
    
    # Записываем информацию в базу данных
    data = await state.get_data()
    promo_name = data.get('name')
    promo_limit = data.get('limit')
    promo_gold = data.get('gold')
    
    sql.execute("INSERT INTO promocodes (name, promo_limit, gold) VALUES (?, ?, ?)",
                (promo_name, promo_limit, promo_gold))
    db.commit()
    
    # Отправляем подтверждение и возвращаемся в основное меню
    await message.answer(f"Промокод {promo_name} успешно создан! Лимит: {promo_limit}, голды: {promo_gold}.")
    await state.finish()

@dp.callback_query_handler(lambda c: c.data == 'seepromo')
async def process_callback_see_promo(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    promocodes = sql.execute("SELECT name, promo_limit, gold FROM promocodes").fetchall()
    if not promocodes:
        await bot.send_message(user_id, "Нет доступных промокодов")
    else:
        for promo in promocodes:
            await bot.send_message(user_id, f"Промокод: {promo[0]}\nЛимит использований: {promo[1]}\nЗолото: {promo[2]}")

@dp.callback_query_handler(lambda c: c.data == 'delpromo')
async def process_callback_del_promo(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    promocodes = sql.execute("SELECT name FROM promocodes").fetchall()
    if not promocodes:
        await bot.send_message(user_id, "Нет доступных промокодов")
    else:
        markup = InlineKeyboardMarkup()
        for promo in promocodes:
            markup.row(InlineKeyboardButton(text=promo[0], callback_data=f"deletepromo_{promo[0]}"))
        await bot.send_message(user_id, "Выберите промокод для удаления", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data.startswith('deletepromo_'))
async def process_callback_delete_promo(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    promo_name = callback_query.data.split('_')[1]
    sql.execute("DELETE FROM promocodes WHERE name=?", (promo_name,))
    await bot.send_message(user_id, f"Промокод {promo_name} успешно удален")

@dp.callback_query_handler(text="newpromo")
async def newpromo_callback_handler(callback_query: types.CallbackQuery):
    # Переходим в состояние создания нового промокода
    await callback_query.answer()
    await handle_newpromo_command(callback_query.message)

@dp.callback_query_handler(lambda c: c.data == 'promo')
async def process_callback_promo(callback_query: types.CallbackQuery):
    await callback_query.answer()
    user_id = callback_query.from_user.id
    await bot.send_message(user_id, "Введите промокод")
    await PromoCode.EnterPromo.set()

@dp.message_handler(state=PromoCode.EnterPromo)
async def process_enter_promo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    promo_code = message.text
    promo = sql.execute("SELECT * FROM promocodes WHERE name=?", (promo_code,)).fetchone()
    if not promo:
        await message.reply("Промокод не найден")
        await state.finish()
        return
    elif promo[1] == '0':
        await message.reply("Промокод уже был активирован или закончился лимит использований")
    else:
        used_promos = sql.execute("SELECT * FROM used_promocodes WHERE user_id=? AND promo_name=?", (user_id, promo_code)).fetchall()
        if used_promos:
            await message.reply("Вы уже активировали этот промокод")
        else:
            gold = int(promo[2])
            db_help.add_balance(user_id, gold)
            sql.execute("UPDATE promocodes SET promo_limit=promo_limit-1 WHERE name=?", (promo_code,))
            sql.execute("INSERT INTO used_promocodes(user_id, promo_name) VALUES (?, ?)", (user_id, promo_code))
            db.commit()
            await message.reply(f"Промокод успешно активирован! Вам начислено {gold} золота")
    await state.finish()


async def backup():
    asyncio.create_task(schedule_function())

def setup():
    "Setup function"

    print('[BOT] Started')
    executor.start_polling(dp, skip_updates=True)



# ======


if __name__ == "__main__":
    setup()
