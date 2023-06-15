from aiogram import types
from utils.mydb import *
import functions as func
import config
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
main_menu_btn = [
    '🍭 Купить',
    '🧜🏻 Профиль',
    '🎲 Игры',
    '💸 Пополнить'

]
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
admin_sending_btn = [
    '✅ Начать',
    '🕑 Отложить',
    '❌ Отменить'
]
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
to_close = types.InlineKeyboardMarkup(row_width=3)
to_close.add(
    types.InlineKeyboardButton(text='Скрыть', callback_data='to_close')
)


def admin_sending():
    markup = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    markup.add(
        admin_sending_btn[0],
        admin_sending_btn[1],
        admin_sending_btn[2],
    )

    return markup


def profile(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=3)
    markup.add(
        types.InlineKeyboardButton(text='🎲 Игры', callback_data='games'),
        types.InlineKeyboardButton(text='💸 Пополнить', callback_data='deposit'),
    )
    markup.add(
        types.InlineKeyboardButton(text='ВВЕСТИ ПРОМОКОД', callback_data='enter_promo')
    )
    if func.check_condition_url_chat(chat_id):
        markup.add(
            types.InlineKeyboardButton(text='Поддержка', url='t.me/wavesupp'),
            types.InlineKeyboardButton(text='Новости', url='t.me/wave_novosti'),
            types.InlineKeyboardButton(text='Чат', url=config.config('chat_url'))
        )
    else:
        markup.add(
            types.InlineKeyboardButton(text='Поддержка', url='t.me/wavesupp'),
            types.InlineKeyboardButton(text='Новости', url='t.me/wave_novosti'),
        )

    return markup


def dep_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='🔹 QIWI ', callback_data='qiwi'),
        types.InlineKeyboardButton(text='🔹 BANKER', callback_data='banker'),
    )

    return markup


def admin_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton(text='Изменить баланс', callback_data='give_balance'),
        types.InlineKeyboardButton(text='Рассылка', callback_data='email_sending'),
        types.InlineKeyboardButton(text='Информация', callback_data='admin_info'),
        types.InlineKeyboardButton(text='Розыгрыш', callback_data='admin_raffle'),
        types.InlineKeyboardButton(text='ПРОМОКОДЫ', callback_data='admin_promocodes'),
    )

    return markup


def email_sending():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='Рассылка(только текст)', callback_data='email_sending_text'),
        types.InlineKeyboardButton(text='Рассылка(текст + фото)', callback_data='email_sending_photo')
    )

    return markup


def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        main_menu_btn[0],   # Buy
        main_menu_btn[1],   # Profile
        # main_menu_btn[3],   # Games
        # main_menu_btn[4],   # Deposit

    )

    return markup


def payment_menu(url):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='🔹 Перейти к оплате 🔹', url=url),
    )

    return markup


def get_code_menu(code, price, number_code):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='🌀 Получить код', callback_data=f'get_code:{code}:{number_code}'),
        types.InlineKeyboardButton(text='🚫 Отменить', callback_data=f'number_cancel:{price}:{code}:{number_code}'),
    )

    return markup


def good_code(code):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='✅ Подтвердить получение кода', callback_data=f'good_code:{code}'),
    )

    return markup


def raffle_confirm():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='✅ Я участвую', callback_data=f'raffle_confirm'),
    )

    return markup


def raffle_up():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='🔄 Обновить', callback_data=f'raffle_up'),
    )

    return markup


def pact():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='✅ Я согласен', callback_data=f'accept_pact'),
    )

    return markup


def admin_promocodes():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton(text='СОЗДАТЬ', callback_data=f'admin_create_promo'),
        types.InlineKeyboardButton(text='СПИСОК', callback_data=f'admin_list_promo'),
    )

    return markup