import logging
import os
from aiogram import Bot, Dispatcher, types, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3

logging.basicConfig(level=logging.INFO)

bot_token = ""
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect('profiles.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS profiles (
        user_id INTEGER PRIMARY KEY,
        balance INTEGER DEFAULT 0,
        payment_system TEXT,
        amount INTEGER,
        screenshot BLOB
    )
''')
conn.commit()


class PaymentStates(StatesGroup):
    amount = State()
    payment_system = State()
    screenshot = State()


@dp.message_handler(Command('start'))
async def cmd_start(message: types.Message):
    
    cursor.execute('SELECT * FROM profiles WHERE user_id=?', (message.from_user.id,))
    profile = cursor.fetchone()

    if profile is None:
      
        cursor.execute('INSERT INTO profiles (user_id, balance) VALUES (?, 0)', (message.from_user.id,))
        conn.commit()
 
        cursor.execute('SELECT * FROM profiles WHERE user_id=?', (message.from_user.id,))
        profile = cursor.fetchone()

   
    await message.reply(f"Ваш баланс: {profile[1]}")
    await message.reply("Выберите платежную систему:", reply_markup=get_payment_systems_keyboard())


def get_payment_systems_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("Qiwi", callback_data="payment_system:qiwi"),
        types.InlineKeyboardButton("Sber", callback_data="payment_system:sber"),
        types.InlineKeyboardButton("Spb", callback_data="payment_system:spb"),
        types.InlineKeyboardButton("Yoomey", callback_data="payment_system:yoomey"),
        types.InlineKeyboardButton("Tinkoff", callback_data="payment_system:tinkoff"),
    )
    return keyboard


@dp.callback_query_handler(lambda c: c.data.startswith('payment_system'))
async def process_payment_system(callback_query: types.CallbackQuery, state: FSMContext):
    payment_system = callback_query.data.split(':')[1]

    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(callback_query.from_user.id, f"Вы выбрали платежную систему: {payment_system}")

    await state.update_data(payment_system=payment_system)
   
    await bot.send_message(callback_query.from_user.id, "Введите сумму пополнения:")
    await PaymentStates.amount.set()


@dp.message_handler(state=PaymentStates.amount)
async def process_amount(message: types.Message, state: FSMContext):
    amount = int(message.text)

    await state.update_data(amount=amount)

    await bot.send_message(message.from_user.id, "Пришлите скриншот платежа:")
    await PaymentStates.screenshot.set()

@dp.message_handler(content_types=types.ContentType.PHOTO, state=PaymentStates.screenshot)
async def process_screenshot(message: types.Message, state: FSMContext):
 
    await state.update_data(screenshot=message.photo[-1].file_id)

    data = await state.get_data()
    payment_system = data.get('payment_system')
    amount = data.get('amount')
    screenshot = data.get('screenshot')

   
    cursor.execute('UPDATE profiles SET payment_system=?, amount=?, screenshot=? WHERE user_id=?',
                   (payment_system, amount, screenshot, message.from_user.id))
    conn.commit()

   
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Принять", callback_data=f"accept:{message.from_user.id}"),
        InlineKeyboardButton("Отклонить", callback_data=f"reject:{message.from_user.id}")
    )


    admin_id = 756597038  # админ айди
    await bot.send_photo(admin_id, screenshot,
                         caption=f"Платежная система: {payment_system}\nСумма пополнения: {amount}",
                         reply_markup=keyboard)

   
    await state.finish()

    await bot.send_message(message.from_user.id, "Ваша заявка принята и будет обработана администратором.")


@dp.callback_query_handler(lambda c: c.data.startswith('accept:') or c.data.startswith('reject:'))
async def process_application(callback_query: types.CallbackQuery):
    action, user_id = callback_query.data.split(':')
    user_id = int(user_id)

    if action == 'accept':
        cursor.execute('SELECT * FROM profiles WHERE user_id=?', (user_id,))
        application = cursor.fetchone()
        balance = application[1] + application[3]
        cursor.execute('UPDATE profiles SET balance=? WHERE user_id=?', (balance, user_id))
        conn.commit()

        await bot.send_message(user_id, f"Ваша заявка на пополнение суммы {application[3]} принята.")
        await bot.send_message(user_id, f"Ваш текущий баланс: {balance}")
    elif action == 'reject':
        await bot.send_message(user_id, "Ваша заявка на пополнение отклонена.")

    conn.commit()

    await bot.answer_callback_query(callback_query.id)

@dp.message_handler(commands=['balance'])
async def cmd_balance(message: types.Message):
    cursor.execute('SELECT * FROM profiles WHERE user_id=?', (message.from_user.id,))
    profile = cursor.fetchone()

    if profile is not None:
        balance = profile[1]
        await message.reply(f"Ваш текущий баланс: {balance}")
    else:
        await message.reply("Профиль пользователя не найден.")



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
