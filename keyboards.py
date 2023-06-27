#[The keyboards file]

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app import adminid
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#======


def get_payment_systems_keyboard(payment_systems):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for system, requisites in payment_systems.items():
        button = InlineKeyboardButton(system, callback_data=f"payment_system:{system}")
        keyboard.add(button)
    return keyboard

payment_systems = {
    "Qiwi": "+79991234567",
    "Sber": "1234567890",
    "Spb": "qwerty",
    "Yoomey": "0987654321",
    "Tinkoff": "asdfgh",
}

support = f'tg://user?id={adminid}'



def markup_main():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("💲 Пополнить баланс"), KeyboardButton("📤 Вывести"), KeyboardButton("🙎🏼‍♂ Профиль"))
    markup.row(KeyboardButton("🧳 Кейсы"), KeyboardButton("🎮 Мини игры"))
    markup.row(KeyboardButton("🔢 Калькулятор"))

    markup.row(KeyboardButton("ℹ️ Информация"), KeyboardButton("📝 Отзывы"), KeyboardButton("🛠 Поддержка"))




    return markup

def exitmenu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("🔙Назад"))


    return markup

def exitmenu1():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton("Назад"))
    return keyboard
    

    
def games_key():
	"Function of return main markup"
	"Cancel markup"
	markup = InlineKeyboardMarkup(row_width=1)
	markup.row(InlineKeyboardButton(text="🪙 Орел и Решка", callback_data="coin_flip"))


	return markup

def otzivi_key():
  "Function of return main markup"
  "Cancel markup"
  markup = InlineKeyboardMarkup(row_width=1)
  markup.row(InlineKeyboardButton(text="Перейти", url="https://t.me/end_soft"))

  return markup



def aadmin(user_id):
  "Function of return main markup"
  "Cancel markup"
  markup = InlineKeyboardMarkup(row_width=1)
  markup.row(InlineKeyboardButton(text="Выдать голду", callback_data="start"))
  markup.row(InlineKeyboardButton(text="Снять голду", callback_data="super"))
  markup.row(InlineKeyboardButton(text="Статистика", callback_data="pro"))
  markup.row(InlineKeyboardButton(text="Рассылка", callback_data="mail"))
  markup.row(InlineKeyboardButton(text="Изменить курс", callback_data="rate"))
  markup.row(InlineKeyboardButton(text="Бэкап система", callback_data="backup"))
  markup.row(InlineKeyboardButton(text="Получить базу данных", callback_data="database"))
  markup.row(InlineKeyboardButton(text="Пополнения", callback_data="buygolda"))
  markup.row(InlineKeyboardButton(text="Настройка промокодов", callback_data="promo_setting"))
  markup.row(InlineKeyboardButton(text="Изменить мин. вывод", callback_data="minvivod_setting"))
  markup.row(InlineKeyboardButton(text="Изменить мин пополнение", callback_data="mindep_setting"))






  return markup

def promo_menu(user_id):
  "Function of return main markup"
  "Cancel markup"
  markup = InlineKeyboardMarkup(row_width=1)
  markup.row(InlineKeyboardButton(text="Посмотреть промокоды", callback_data="seepromo"))
  markup.row(InlineKeyboardButton(text="Удалить промокод", callback_data="delpromo"))
  markup.row(InlineKeyboardButton(text="Создать промокод", callback_data="newpromo"))





  return markup



def profile():
	"Function of return main markup"
	"Cancel markup"
	markup = InlineKeyboardMarkup(row_width=1)
	markup.row(InlineKeyboardButton(text="🎁 Активировать промокод", callback_data="promo"))




	return markup

def profilekey():
	"Function of return main markup"
	"Cancel markup"
	markup = InlineKeyboardMarkup(row_width=1)
	markup.row(InlineKeyboardButton(text="❌", callback_data="exitprofile"))


	return markup

def vivod():
	"Function of return main markup"
	"Cancel markup"
	markup = InlineKeyboardMarkup(row_width=1)
	markup.row(InlineKeyboardButton(text="✅", callback_data="a_"))


	return markup

def clients():

	markup = InlineKeyboardMarkup(row_width=1)
	markup.row(InlineKeyboardButton(text="Контакты", callback_data="contacts"))
	markup.row(InlineKeyboardButton(text='Условия использования', url='https://telegra.ph/Usloviya-ispolzovaniya-01-29'))
	markup.row(InlineKeyboardButton(text='Политика конфиденциальности', url='https://telegra.ph/Politika-konfidencialnosti-01-29-8'))
	markup.row(InlineKeyboardButton(text="❌", callback_data="exitc"))

	return markup

def supportMenu():

	markup = InlineKeyboardMarkup(row_width=1)
	markup.row(InlineKeyboardButton (text='Написать в поддержку', url=support))

	return markup

def payment_services():

    markup = InlineKeyboardMarkup(row_width=1)
    markup = InlineKeyboardMarkup(row_width=1)
    markup.row(InlineKeyboardButton(text='Qiwi', callback_data='payment_qiwi'))
    markup.row(InlineKeyboardButton(text='Tinkoff', callback_data='payment_tinkoff'))
    markup.row(InlineKeyboardButton(text='Sberbank', callback_data='payment_sberbank'))

    return markup




#=====
