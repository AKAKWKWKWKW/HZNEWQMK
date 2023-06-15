
import logging
import config
import functions as func
import texts
import random
import time
import asyncio
import re
import threading
import datetime
import subprocess
import menu
import utils.dice as dice
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
import traceback
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
from btc import BTCPayment
from utils.mydb import *
from utils.user import *
from states import *
from utils.number import *
from AntiSpam import test
#CЛИТО В ТЕЛЕГРАМ КАНАЛЕ @END_SOFT
from socket import *

import aiogram.utils.markdown as md

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage


logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.config('bot_token'), parse_mode='html')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    status = await test(message, bot)
    if status is not False:
        chat_id = message.chat.id

        func.first_join(chat_id, message.from_user.first_name, message.from_user.username)

        if func.get_status_pact(chat_id) == False:
            await bot.send_message(chat_id=chat_id, text=texts.pact, reply_markup=menu.pact())
        else:
            await bot.send_sticker(chat_id, "CAACAgIAAxkBAAPBXvcCL6Dl-w3-S6sNnihIQMP-QXYAAlxAAALpVQUYfkvoLr8uX3UaBA"),
            await bot.send_message(chat_id=chat_id, text='💫 Добро пожаловать, держи менюшку, слит в @end_soft  ', reply_markup=menu.main_menu())


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if str(message.chat.id) in config.config('admin_id'):
        await bot.send_message(chat_id=message.chat.id, text='''
⚜️Вы перешли в меню администратора

❕ Команды для администратора:
➖ /give_games user_id кол-во
➖ /give_purchases user_id кол-во
''', reply_markup=menu.admin_menu())


@dp.message_handler()
async def send_message(message: types.Message):
    status = await test(message, bot)
    if status is not False:
        chat_id = message.chat.id
        message_id = message.message_id

        if func.get_status_pact(chat_id) == False:
            await bot.send_message(chat_id=chat_id, text=texts.pact, reply_markup=menu.pact())
        else:
            if re.search(r'BTC_CHANGE_BOT\?start=', message.text):
                await message.answer(text='✅ Подождите секунду...')
                await BTCPayment().receipt_parser(bot, chat_id, message.text)

            if message.text == menu.main_menu_btn[2]:    # Games
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Создайте игру или выберите уже имеющуюся:',
                                    reply_markup=dice.dice_menu())

            elif message.text == menu.main_menu_btn[0]:   # Buy
                await bot.send_sticker(chat_id, "CAACAgIAAxkBAAPDXvcCN479sMqq0lgGGr5dJ9Q0P5wAAl1AAALpVQUYlp6ts7MtdUwaBA")
                await bot.send_message(chat_id=chat_id, text='Выберите номер', reply_markup=await Number().get_menu(chat_id), parse_mode='html')

            elif message.text == menu.main_menu_btn[1]:    # Profile
                await bot.send_sticker(chat_id, "CAACAgIAAxkBAAPHXvcClzFmrslOPwABNxFtBl9UmuMTAAJuQAAC6VUFGBIFjkagvbdRGgQ")
                markup = menu.profile(chat_id)
                
                await bot.send_message(
                    chat_id=chat_id,
                    text=await Number().get_info_number(chat_id),
                    reply_markup=markup)

            elif message.text == menu.main_menu_btn[3]:   # Deposit
                await bot.send_sticker(chat_id, "CAACAgIAAxkBAAPFXvcCOsUiQx73vRO634lSZO0tNWAAAl5AAALpVQUYO4VTvVJETUoaBA");            
                
                await bot.send_message(
                    chat_id=chat_id,
                    text='Выберите способ пополнения',
                    reply_markup=menu.dep_menu(),
                    parse_mode='html')
            
            elif '/give_purchases' in message.text:
                if str(chat_id) in config.config('admin_id'):
                    try:
                        user_id = int(message.text.split(' ')[1])
                        amount = int(message.text.split(' ')[2])

                        for _ in range(amount):
                            func.raffle_logs(user_id)

                        await message.answer('✅ Покупки выданы')
                    except:
                        await message.answer('❌ Неверная команда')

            elif '/give_games' in message.text:
                if str(chat_id) in config.config('admin_id'):
                    try:
                        user_id = int(message.text.split(' ')[1])
                        amount = int(message.text.split(' ')[2])

                        conn, cursor = connect()

                        for _ in range(amount):
                            cursor.execute(f'INSERT INTO game_logs VALUES("{random.randint(1, (9**9))}", "{user_id}", "draw", "0", "{datetime.datetime.now()}")')
                            conn.commit()

                        await message.answer('✅ Игры выданы')
                    except:
                        await message.answer('❌ Неверная команда')
          

@dp.callback_query_handler(state=CreateGame.bet)
async def creategame_bet_call(call: types.CallbackQuery, state: FSMContext):

    if call.data == 'cancel_dice':
        await state.finish()
        bot.delete_message( chat_id=call.message.chat.id,  message_id=call.message.message_id)
        

@dp.callback_query_handler()
async def handler_call(call: types.CallbackQuery, state: FSMContext):
    chat_id = call.message.chat.id
    message_id = call.message.message_id

    if call.data == 'accept_pact':
        func.accept_pact(chat_id)
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        await call.answer('Вы успешно с пользовательским соглашением')

        await bot.send_sticker(chat_id, "CAACAgIAAxkBAAPBXvcCL6Dl-w3-S6sNnihIQMP-QXYAAlxAAALpVQUYfkvoLr8uX3UaBA"),
        await bot.send_message(chat_id=chat_id, text='💫 Добро пожаловать, держи менюшку',
                               reply_markup=menu.main_menu())

    elif func.get_status_pact(chat_id) == False:
        await bot.send_message(chat_id=chat_id, text=texts.pact, reply_markup=menu.pact())
    else:
    
        if call.data == 'cancel_dice':
            await bot.delete_message( chat_id=call.message.chat.id, message_id=call.message.message_id)

        elif call.data == 'to_close':
            try:
                await bot.delete_message(chat_id=chat_id,
                                message_id=message_id)
            except:
                await bot.answer_callback_query(call.id, text='❕ Сообщение уже удалено')

        elif call.data == 'exit':
            #await bot.send_sticker(chat_id, "CAACAgIAAxkBAAPHXvcClzFmrslOPwABNxFtBl9UmuMTAAJuQAAC6VUFGBIFjkagvbdRGgQ")

            markup = menu.profile(chat_id)

            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=await Number().get_info_number(chat_id),
                reply_markup=markup
            )

        elif call.data == 'deposit':
            await bot.send_sticker(chat_id, "CAACAgIAAxkBAAPFXvcCOsUiQx73vRO634lSZO0tNWAAAl5AAALpVQUYO4VTvVJETUoaBA");

            await bot.send_message(
                chat_id=chat_id,
                text='Выберите способ пополнения',
                reply_markup=menu.dep_menu(),
                parse_mode='html')

        elif call.data == 'games':
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Создайте игру или выберите уже имеющуюся:',
                                   reply_markup=dice.dice_menu())

        elif call.data == 'banker':
            await bot.send_message(chat_id=chat_id, text='👨🏻‍⚕️ Для оплаты чеком, просто отправьте его в чат ⤵️', parse_mode='html')

        elif call.data == 'qiwi':
            response = func.deposit_qiwi(chat_id)

            date = str(datetime.datetime.now())[:19]

            await bot.send_message(
                chat_id=chat_id,
                text=texts.check_payment.format(
                    config.config('qiwi_number'),
                    response[0],
                    date,
                    '{:.0f}'.format(3600 - (time.time() - response[1]))
                ),
                reply_markup=response[2],
                parse_mode='html'
            )

        elif call.data == 'admin_info':
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=func.admin_info(),
                                        reply_markup=menu.admin_menu(), parse_mode='html')

        elif call.data == 'create_dice':
            await CreateGame.bet.set()
            await bot.send_message(chat_id=chat_id,
                                   text=f'💰 Введите сумму ставки от {config.config("min_bank")} до {User(chat_id).balance} RUB',
                                   reply_markup=dice.cancel_dice())

        elif call.data == 'reload_dice':
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                        text='Создайте игру или выберите уже имеющуюся:',
                                        reply_markup=dice.dice_menu())

        elif call.data == 'my_games_dice':
            resp = dice.my_games_dice(chat_id)

            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=resp[0], reply_markup=resp[1])

        elif call.data == 'rating_dice':
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=dice.rating_dice(chat_id),
                                        reply_markup=dice.back_dice())

        elif call.data == 'back_dice':
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                        text='Создайте игру или выберите уже имеющуюся:',
                                        reply_markup=dice.dice_menu())

        elif call.data == 'help_dice':
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=dice.help_txt)

        elif 'dice_game:' in call.data:
            info = dice.dice_game(call.data.split(':')[1], chat_id)

            if info == False:
                await bot.send_message(chat_id=chat_id, text='🚫 Игра не найдена или это ваша игра')
            else:
                await bot.send_message(chat_id=chat_id, text=info[0], reply_markup=info[1])

        elif 'start_game_dice:' in call.data:
            info = dice.start_game_dice(call.data.split(':')[1], chat_id)

            if info == False:
                await bot.send_message(chat_id=chat_id, text='🚫 Ошибка')
            else:
                await bot.send_message(chat_id=chat_id, text='🎲')

                for i in range(0, 2):
                    try:
                        await bot.send_message(chat_id=info[0][i], text=info[1][i])
                    except:
                        pass
                await bot.send_message(chat_id=chat_id, text='Создайте игру или выберите уже имеющуюся:',
                                       reply_markup=dice.dice_menu())


        elif call.data == 'admin_raffle':
            await AdminRaffle.bet.set()
            await bot.send_message(chat_id=chat_id, text='Введите сумму розыгрыша')

        elif call.data == 'give_balance':
            await AdminGiveBalance.user_id.set()
            await bot.send_message(chat_id=chat_id, text='Введите id человека, которому будет изменён баланс')

        elif call.data == 'email_sending':
            await bot.send_message(chat_id=chat_id, text='Выбирите вариант рассылки', reply_markup=menu.email_sending())

        elif call.data == 'email_sending_photo':
            await Email_sending_photo.photo.set()
            await bot.send_message(chat_id=chat_id, text='Отправьте фото боту, только фото!')

        elif call.data == 'email_sending_text':
            await Admin_sending_messages.text.set()
            await bot.send_message(chat_id=chat_id, text='Введите текст рассылки',)

        elif call.data == 'exit_to_main_menu':
            await bot.send_message(chat_id=chat_id, text='♻️ Вы были возвращены в главное меню',
                                   reply_markup=menu.main_menu())

        elif 'buy:' in call.data:
            await Buy.confirm.set()

            async with state.proxy() as data:
                data['code'] = call.data.split(':')[1]
                data['country'] = call.data.split(':')[2]

            await bot.send_message(chat_id=chat_id, text='Отправьте + для подтверждения')

        elif 'number:' in call.data:
            try:
                await bot.send_message(chat_id=chat_id, text='Выберите страну', reply_markup=await Number().get_menu_country(call.data.split(':')[1], chat_id),)
            except:
                await bot.send_message(chat_id=chat_id, text='😅 Не удалось получать данные, подождите несколько секунд и повторите попытку')
        
        elif 'number_cancel:' in call.data:
            try:
                if time.time() - globals()[f'number_cancel:{chat_id}'] < 120:
                    status = False
                else:
                    status = True
            except:
                globals()[f'number_cancel:{chat_id}'] = time.time()
                status = True

            if status == True:
                num_id = call.data.split(':')[2]
                num_code = call.data.split(':')[3]
                resp = await Number().number_cancel(num_id, num_code)
                if resp == True:
                    User(chat_id).update_balance(call.data.split(':')[1])

                    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Деньги возвращены')
                else:
                    await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='🚫 Номер уже был использован')
            else:
                time_left = "{:.0f}".format(120 - (time.time() - globals()[f"number_cancel:{chat_id}"]))

                await bot.send_message(chat_id=chat_id, text=f'Вы недавно уже отменяли номер, подождите {time_left} секунд')

        elif 'get_code:' in call.data:
            await Number().get_sms(bot, call.data.split(':')[1], chat_id, call.data.split(':')[2])

        elif 'good_code:' in call.data:
            await Number().number_cancel(call.data.split(':')[1], call.data.split(':')[2])

            await bot.send_message(chat_id=chat_id,
                                   text='💞 Спасибо за использование бота, не забывай рассказать о нас друзьям.')

        elif call.data == 'raffle_confirm':
            if func.check_raffle() == False:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='🚫 Розыгрыш уже закончился')
            else:
                if func.check_raffle_condition(chat_id) == False:
                    await bot.send_message(chat_id=chat_id, text='🚫 Выполните условие')
                else:
                    if func.check_user_in_raffle(chat_id) == True:
                        await bot.send_message(chat_id=chat_id, text='🗳 Вы уже участвуете в розыгрыше')
                    else:
                        if func.raffle_confirm(chat_id) == True:
                            info = func.get_raffle_info()

                            await bot.edit_message_text(
                                chat_id=chat_id,
                                message_id=message_id,
                                text=texts.raffle.format(
                                    info[0],
                                    info[1],
                                    info[5],
                                    "{:.0f}".format((float(info[2]) - time.time()) / 60),
                                    info[3],
                                    info[4]
                                ),
                                reply_markup=menu.raffle_up()
                            )

                            await bot.send_message(chat_id=chat_id,
                                                   text='🗳 Вы приняли участие в розыгрыше, ожидайте его окончания')
                        else:
                            await bot.send_message(chat_id=chat_id, text='🚫 Хм.. Какая-то ошибка')

        elif call.data == 'raffle_up':
            if func.check_raffle() == False:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='🚫 Розыгрыш уже закончился')
            else:
                info = func.get_raffle_info()

                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=texts.raffle.format(
                        info[0],
                        info[1],
                        info[5],
                        "{:.0f}".format((float(info[2]) - time.time()) / 60),
                        info[3],
                        info[4]
                    ),
                    reply_markup=menu.raffle_up()
                )

        elif call.data == 'admin_promocodes':
            await bot.send_message(
                chat_id=chat_id,
                text='МЕНЮ ПРОМОКОДЫ',
                reply_markup=menu.admin_promocodes()
            )

        elif call.data == 'admin_create_promo':
            await AdminCreatePromo.name.set()
            await bot.send_message(
                chat_id=chat_id,
                text='Введите название промокода(TOPPROMO32)'
            )

        elif call.data == 'admin_list_promo':
            await bot.send_message(
                chat_id=chat_id,
                text='Ниже представлен весь список промокодов',
                reply_markup=func.get_promo_list_menu()
            )

        elif 'promo_list' in call.data:
            data = call.data.split(':')
            text = f"""
Статус: {data[1]}
Промокод: {data[2]}
Процент: {data[3]}
Дата создания: {time.ctime(int(data[4]))}
Дата окончания: {time.ctime(int(data[5]))}
            """

            await bot.send_message(
                chat_id=chat_id,
                text=text
            )

        elif call.data == 'enter_promo':
            await EnterPromo.enter_promo.set()
            await bot.send_message(
                chat_id=chat_id,
                text='Введите промокод'
            )

        try:
            await bot.answer_callback_query(call.id)
        except:
            pass

@dp.message_handler(state=EnterPromo.enter_promo)
async def EnterPromoEnterPromo(message: types.Message, state: FSMContext):
    try:
        promo = message.text
        await func.enter_promo(bot, message.from_user.id, promo)
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=AdminCreatePromo.name)
async def AdminCreatePromoName(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['name'] = message.text
        
        await AdminCreatePromo.next()
        await message.answer(
            text='Введите процент скидки (10)'
        )
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=AdminCreatePromo.percent)
async def AdminCreatePromoPercent(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['percent'] = float('{:.2f}'.format(float(message.text))) 
        
        await AdminCreatePromo.next()
        await message.answer(
            text='Введите время действия промокода (10s или 5m или 30d)'
        )
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=AdminCreatePromo.life_time)
async def AdminCreatePromoLifeTime(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['life_time'] = message.text
        
        await AdminCreatePromo.next()
        await message.answer(
            text='Для подтверждения отправьте +'
        )
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=AdminCreatePromo.confirm)
async def AdminCreatePromoConfirm(message: types.Message, state: FSMContext):
    try:
        if message.text == '+':
            async with state.proxy() as data:
                if func.create_promo(data['name'],  data['percent'],  data['life_time']):
                    await message.answer(text='Промокод создан!')
                else:
                    await message.answer(text='При создании промокода произошла ошибка')
        else:
            await message.answer(text='Вы отменили создание промокода') 
        await state.finish()
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Email_sending_photo.photo, content_types=['photo'])
async def email_sending_photo_1(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['photo'] = random.randint(111111111, 999999999)

        await message.photo[-1].download(f'photos/{data["photo"]}.jpg')
        await Email_sending_photo.next()
        await message.answer('Введите текст рассылки')
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Email_sending_photo.text)
async def email_sending_photo_2(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = message.text

            with open(f'photos/{data["photo"]}.jpg', 'rb') as photo:
                await message.answer_photo(photo, data['text'])

            await Email_sending_photo.next()
            await message.answer('Выбирите дальнейшее действие', reply_markup=menu.admin_sending())
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Email_sending_photo.action)
async def email_sending_photo_3(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    try:
        if message.text in menu.admin_sending_btn:
            if message.text == menu.admin_sending_btn[0]:  # Начать

                users = func.get_users_list()

                start_time = time.time()
                amount_message = 0
                amount_bad = 0
                async with state.proxy() as data:
                    photo_name = data["photo"]
                    text = data["text"]

                await state.finish()

                try:
                    m = await bot.send_message(
                        chat_id=config.config('admin_id').split(':')[0],
                        text=f'✅ Рассылка в процессе',)
                    msg_id = m['message_id']
                except:
                    pass

                for i in range(len(users)):
                    try:
                        with open(f'photos/{photo_name}.jpg', 'rb') as photo:
                            await bot.send_photo(
                                chat_id=users[i][0],
                                photo=photo,
                                caption=text,
                                reply_markup=menu.to_close
                            )
                        amount_message += 1
                    except Exception as e:
                        amount_bad += 1


                try:
                    await bot.edit_message_text(chat_id=config.config('admin_id').split(':')[0],
                                                message_id=msg_id,
                                                text='✅ Рассылка завершена')
                except:
                    pass
                sending_time = time.time() - start_time

                try:
                    await bot.send_message(
                        chat_id=config.config('admin_id').split(':')[0],
                        text=f'✅ Рассылка окончена\n'
                             f'👍 Отправлено: {amount_message}\n'
                             f'👎 Не отправлено: {amount_bad}\n'
                             f'🕐 Время выполнения рассылки - {sending_time} секунд'

                    )
                except:
                    pass

            elif message.text == menu.admin_sending_btn[1]:  # Отложить
                await Email_sending_photo.next()

                await bot.send_message(
                    chat_id=chat_id,
                    text="""
Введите дату начала рассылке в формате: ГОД-МЕСЯЦ-ДЕНЬ ЧАСЫ:МИНУТЫ

Например 2020-09-13 02:28 - рассылка будет сделана 13 числа в 2:28
"""
            )

            elif message.text == menu.admin_sending_btn[2]:
                await state.finish()

                await bot.send_message(
                    message.chat.id,
                    text='Рассылка отменена',
                    reply_markup=menu.main_menu()
                )

                await bot.send_message(
                    message.chat.id,
                    text='Меню админа',
                    reply_markup=menu.admin_menu()
                )
        else:
            await bot.send_message(
                message.chat.id,
                text='Не верная команда, повторите попытку',
                reply_markup=menu.admin_sending())

    except Exception as e:
        await state.finish()
        await bot.send_message(
            chat_id=message.chat.id,
            text='⚠️ ERROR ⚠️'
        )


@dp.message_handler(state=Email_sending_photo.set_down_sending)
async def email_sending_photo_4(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['date'] = message.text
            date = datetime.datetime.fromisoformat(data['date'])

            await Email_sending_photo.next()

            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Для подтверждения рассылки в {date} отправьте +'
            )
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Email_sending_photo.set_down_sending_confirm)
async def email_sending_photo_5(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            data['type_sending'] = 'photo'

            func.add_sending(data)

            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Рассылка запланирована в {data["date"]}',
                reply_markup=menu.admin_menu()
            )
    else:
        bot.send_message(message.chat.id, text='Рассылка отменена', reply_markup=menu.admin_menu())

    await state.finish()


@dp.message_handler(state=Admin_sending_messages.text)
async def admin_sending_messages_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

        await message.answer(data['text'])

        await Admin_sending_messages.next()
        await bot.send_message(
            chat_id=message.chat.id,
            text='Выбирите дальнейшее действие',
            reply_markup=menu.admin_sending()
        )


@dp.message_handler(state=Admin_sending_messages.action)
async def admin_sending_messages_2(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    if message.text in menu.admin_sending_btn:
        if message.text == menu.admin_sending_btn[0]:  # Начать

            users = func.get_users_list()

            start_time = time.time()
            amount_message = 0
            amount_bad = 0

            async with state.proxy() as data:
                text = data['text']

            await state.finish()

            try:
                m = await bot.send_message(
                    chat_id=config.config('admin_id').split(':')[0],
                    text=f'✅ Рассылка в процессе')
                msg_id = m['message_id']
            except Exception as e:
                pass

            for i in range(len(users)):
                try:
                    await bot.send_message(users[i][0], text, reply_markup=menu.to_close)
                    amount_message += 1
                except Exception as e:
                    amount_bad += 1


            try:
                await bot.edit_message_text(chat_id=config.config('admin_id').split(':')[0],
                                            message_id=msg_id,
                                            text='✅ Рассылка завершена')
            except:
                pass

            sending_time = time.time() - start_time

            try:
                await bot.send_message(
                    chat_id=config.config('admin_id').split(':')[0],
                    text=f'✅ Рассылка окончена\n'
                         f'👍 Отправлено: {amount_message}\n'
                         f'👎 Не отправлено: {amount_bad}\n'
                         f'🕐 Время выполнения рассылки - {sending_time} секунд'

                )
            except:
                print('ERROR ADMIN SENDING')

        elif message.text == menu.admin_sending_btn[1]:  # Отложить
            await Admin_sending_messages.next()

            await bot.send_message(
                chat_id=chat_id,
                text="""
Введите дату начала рассылке в формате: ГОД-МЕСЯЦ-ДЕНЬ ЧАСЫ:МИНУТЫ

Например 2020-09-13 02:28 - рассылка будет сделана 13 числа в 2:28
"""
            )

        elif message.text == menu.admin_sending_btn[2]:
            await bot.send_message(
                message.chat.id,
                text='Рассылка отменена',
                reply_markup=menu.main_menu()
            )
            await bot.send_message(
                message.chat.id,
                text='Меню админа',
                reply_markup=menu.admin_menu()
            )
            await state.finish()
        else:
            await bot.send_message(
                message.chat.id,
                text='Не верная команда, повторите попытку',
                reply_markup=menu.admin_sending())


@dp.message_handler(state=Admin_sending_messages.set_down_sending)
async def admin_sending_messages_3(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['date'] = message.text
            date = datetime.datetime.fromisoformat(data['date'])

            await Admin_sending_messages.next()

            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Для подтверждения рассылки в {date} отправьте +'
            )
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_sending_messages.set_down_sending_confirm)
async def admin_sending_messages_4(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            data['type_sending'] = 'text'
            data['photo'] = random.randint(111111, 9999999)

            func.add_sending(data)

            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Рассылка запланирована в {data["date"]}',
                reply_markup=menu.admin_menu()
            )
    else:
        bot.send_message(message.chat.id, text='Рассылка отменена', reply_markup=menu.admin_menu())

    await state.finish()


@dp.message_handler(state=AdminRaffle.bet)
async def adminraffle_bet(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['bank'] = float(message.text)

            await AdminRaffle.next()

            await bot.send_message(chat_id=message.chat.id,
                                   text='Введите кол-во покупок необходимое для участия в розыгрыше')
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=AdminRaffle.amount_purchase)
async def adminraffle_amount_purchase(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['amount_players'] = int(message.text)

            await AdminRaffle.next()

            await bot.send_message(chat_id=message.chat.id,
                                   text='Введите кол-во игр необходимое для участия в розыгрыше')
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=AdminRaffle.amount_dice_games)
async def adminraffle_amount_dice_games(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['amount_dice_games'] = int(message.text)

            await AdminRaffle.next()

            await bot.send_message(chat_id=message.chat.id,
                                   text='Через сколько минут будет определен победитель?\nНапример: 60 (1 час)')
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')



@dp.message_handler(state=AdminRaffle.game_time)
async def adminraffle_time(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['time'] = float(message.text)

            await AdminRaffle.next()

            await bot.send_message(
                chat_id=message.chat.id,
                text=f"""
Приз: {data['bank']}
Кол-во покупок для участия: {data['amount_players']}
Кол-во игр для участия: {data['amount_dice_games']}
Победитель будет определен через: {data['time']}

Для подтверждения отправьте +
""")
    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=AdminRaffle.confirm)
async def adminraffle_confirm(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    try:
        async with state.proxy() as data:
            if message.text == '+':
                bank = data['bank']
                amount_players = data['amount_players']
                game_time = data['time']
                amount_dice_games =  data['amount_dice_games']

                await state.finish()

                if func.check_raffle() == True:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=f'Имеется активный розыгрыш, вы не можете создать новый'
                    )
                else:
                    if func.add_raffle(bank, amount_players, game_time, amount_dice_games) == True:
                        conn, cursor = connect()

                        cursor.execute(f'SELECT * FROM users')
                        row = cursor.fetchall()

                        await bot.send_message(
                            chat_id=chat_id,
                            text=f'Розыгрыш создан, запуск уведомления'
                        )

                        good = 0
                        bad = 0

                        for i in range(len(row)):
                            try:
                                await bot.send_sticker(row[i][0],
                                                 "CAACAgIAAxkBAAEBFlZfGbq3SOymZ12tMaLN_d_79BWDSQACe0AAAulVBRgMVD2rnlFBgxoE")
                                await bot.send_message(
                                    chat_id=row[i][0],
                                    text=texts.raffle.format(
                                        bank,
                                        amount_players,
                                        amount_dice_games,
                                        game_time,
                                        0,
                                        '100'),
                                    reply_markup=menu.raffle_confirm()
                                )
                                good += 1
                            except:
                                bad += 1

                        await bot.send_message(
                            chat_id=chat_id,
                            text=f"""
✅ Уведомления о розыгрыше были разослан

💚GOOD: <code>{good}</code>
❤️BAD: <code>{bad}</code>
"""
                        )
            else:
                await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Buy.confirm)
async def buy_confirm(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    if message.text == '+':
        async with state.proxy() as data:
            await Number().buy_number(bot, chat_id, data['code'], data['country'])

    await state.finish()


@dp.message_handler(state=AdminGiveBalance.user_id)
async def admin_give_balance_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text

    await AdminGiveBalance.next()
    await message.answer('Введите сумму на которую будет изменен баланс')


@dp.message_handler(state=AdminGiveBalance.balance)
async def admin_give_balance_2(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['balance'] = float(message.text)

            await AdminGiveBalance.next()
            await message.answer(f"""
ID: {data['user_id']}
Баланс изменится на: {data['balance']}

Для подтверждения отправьте +
""")
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=AdminGiveBalance.confirm)
async def admin_give_balance_3(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            user = User(data['user_id'])
            user.update_balance(-(float(user.balance) - float(data['balance'])))

            await message.answer('✅ Баланс успешно изменен', reply_markup=menu.admin_menu())
    else:
        await message.answer('⚠️ Изменение баланса отменено')

    await state.finish()


@dp.message_handler(state=CreateGame.bet)
async def creategame_bet(message: types.Message, state: FSMContext):
    await state.finish()

    chat_id = message.chat.id
    try:
        user = User(chat_id)
        bet = float('{:.2f}'.format(float(message.text)))

        if bet <= user.balance and bet >= float(config.config('min_bank')):
            user.update_balance(-bet)
            dice.create_game(chat_id, bet)

            await bot.send_message(
                chat_id=message.chat.id,
                text='✅Ваша ставка принята!'
            )
        else:
            await bot.send_message(
                chat_id=message.chat.id,
                text='⚠️ Неверная ставка'
            )
    except Exception as e:
        await bot.send_message(
            chat_id=message.chat.id,
            text='⚠️ Что-то пошло не по плану'
        )


async def pars_amount_numbers(bot, wait_for):
    while True:
        await asyncio.sleep(wait_for)
        for i in [0, 1, 2, 51, 15, 32]:
            url = f'https://smshub.org/stubs/handler_api.php?api_key={config.config("api_smshub")}&action=getNumbersStatus&country={i}'
            response = requests.post(url)

            with open(f'docs/country_{i}.txt', 'w', encoding='UTF-8') as txt:
                txt.write(response.text)

        for i in [0, 1, 2, 15, 32]:
            url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.config("api_smsactivate")}&action=getNumbersStatus&country={i}'
            response = requests.post(url)

            with open(f'docs/countrySMSACTIVATE_{i}.txt', 'w', encoding='UTF-8') as txt:
                txt.write(response.text)

async def checker_raffles(bot, wait_for):
        while True:
            await asyncio.sleep(wait_for)
            
            try:
                if func.check_raffle() == False:
                    await asyncio.sleep(wait_for)
                else:
                    if func.check_time_raffle() == True:
                        info = func.raffle_start()
                        try:
                            await bot.send_sticker(chat_id=info[0],
                                                   sticker="CAACAgIAAxkBAAPRXvdK8BhD8ufgh3cDaMf_sNWxT-4AAmZAAALpVQUY8tRwnMpPPNcaBA")
                            await bot.send_message(chat_id=info[0], text=f'🎉 Вы выиграли в розыгрыше, деньги начислены на ваш баланс')
                        except Exception as e: pass

                        for i in info[1]:
                            chat = await bot.get_chat(info[0])
                            try:
                                await bot.send_message(
                                    chat_id=i[0],
                                    text=f'🎉 Розыгрыш окончен, выиграл @{chat.username}/{chat.first_name}'
                                )
                            except Exception as e: pass
            except Exception as e:
                pass

            

async def check_qiwi(bot, wait_for):
    while True:
        await asyncio.sleep(wait_for)
        try:
            data = func.get_payments_history()
            payment_code_list = func.get_list_payments_code()

            for i in range(len(data)):
                for j in payment_code_list:
                    if time.time() - float(j[2]) > 3600:
                        func.del_purchase_ticket(j[0])
                    elif data[i]['comment'] == j[1]:
                        if str(data[i]['sum']['currency']) == '643':
                            deposit = float(data[i]["sum"]["amount"])

                            User(j[0]).update_balance(deposit)

                            func.del_purchase_ticket(j[0])

                            try:
                                await bot.send_message(
                                    chat_id=j[0],
                                    text=f'✅ Вам зачислено +{deposit}'
                                )
                            except:pass

        except Exception as e:
            print(e)
        
async def sending_check(bot, wait_for):
    while True:
        await asyncio.sleep(wait_for)

        try:
            info = func.sending_check()

            if info != False:
                users = func.get_users_list()

                start_time = time.time()
                amount_message = 0
                amount_bad = 0

                if info[0] == 'text':
                    try:
                        m = await bot.send_message(
                            chat_id=config.config('admin_id').split(':')[0],
                            text=f'✅ Рассылка в процессе')
                        msg_id = m['message_id']
                    except:
                        pass

                    for i in range(len(users)):
                        try:
                            await bot.send_message(users[i][0], info[1], reply_markup=menu.to_close)
                            amount_message += 1
                        except Exception as e:
                            amount_bad += 1


                    try:
                        await bot.edit_message_text(chat_id=config.config('admin_id').split(':')[0],
                                                    message_id=msg_id,
                                                    text='✅ Рассылка завершена')
                    except:
                        pass
                    sending_time = time.time() - start_time

                    try:
                        await bot.send_message(
                            chat_id=config.config('admin_id').split(':')[0],
                            text=f'✅ Рассылка окончена\n'
                                 f'👍 Отправлено: {amount_message}\n'
                                 f'👎 Не отправлено: {amount_bad}\n'
                                 f'🕐 Время выполнения рассылки - {sending_time} секунд'

                        )
                    except:
                        print('ERROR ADMIN SENDING')

                elif info[0] == 'photo':
                    try:
                        m = await bot.send_message(
                            chat_id=config.config('admin_id').split(':')[0],
                            text=f'✅ Рассылка в процессе')
                        msg_id = m['message_id']
                    except:
                        pass

                    for i in range(len(users)):
                        try:
                            with open(f'photos/{info[2]}.jpg', 'rb') as photo:
                                await bot.send_photo(
                                    chat_id=users[i][0],
                                    photo=photo,
                                    caption=info[1],
                                    reply_markup=menu.to_close
                                )
                            amount_message += 1
                        except:
                            amount_bad += 1

                    try:
                        await bot.edit_message_text(chat_id=config.config('admin_id').split(':')[0],
                                                    message_id=msg_id,
                                                    text='✅ Рассылка завершена')
                    except:
                        pass

                    sending_time = time.time() - start_time

                    try:
                        await bot.send_message(
                            chat_id=config.config('admin_id').split(':')[0],
                            text=f'✅ Рассылка окончена\n'
                                 f'👍 Отправлено: {amount_message}\n'
                                 f'👎 Не отправлено: {amount_bad}\n'
                                 f'🕐 Время выполнения рассылки - {sending_time} секунд'

                        )
                    except:
                        print('ERROR ADMIN SENDING')

            else:
                pass
        except Exception as e:
            pass


if __name__ == '__main__':

    async def startup(dp):
        loop = asyncio.get_event_loop()

        print('starting pars_amount_numbers')
        loop.create_task(pars_amount_numbers(bot, 15))
        print('starting checker_raffles')
        loop.create_task(checker_raffles(bot, 5))
        print('starting check_qiwi')
        loop.create_task(check_qiwi(dp.bot, 10))
        print('starting sending_check')
        loop.create_task(sending_check(dp.bot, 10))
    
    print('starting bot')
    executor.start_polling(dp, skip_updates=True, on_startup=startup)
