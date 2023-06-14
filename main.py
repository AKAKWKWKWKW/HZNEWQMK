
import os
os.chdir('/root/SMSTYT')

import logging
import functions as func
import texts
import re
import btc
import threading
import subprocess
import menu

from Rent import *

from SystemInfo import SystemInfo

import traceback

from datetime import datetime, timedelta
from states import *
from utils.number import *
from utils.game import *
from utils.mydb import *

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from AntiSpam import test

from socket import *


# Configure logging
logging.basicConfig(level=logging.INFO)


bot = Bot(token=config.config('bot_token'), parse_mode='html')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    if await func.get_status_ban(message.chat.id):
        await message.answer('❌ Вам ограничен доступ к боту!')
    elif str(message.chat.id) == config.config('CHAT_ID'):
        pass
    else:
        check = func.first_join(message.chat.id, message.chat.first_name, message.chat.username, message.text)

        if check[0] == True:
            try:
                await bot.send_message(
                    chat_id=config.config('CHANNEL_ID1'),
                    text=f"""
🥳🥳🥳 Новый юзер {message.from_user.id}/@{message.from_user.username}/{message.from_user.first_name} !!!
❕ Привел {check[1]}
                    """
                )
            except:
                pass
        with open('welcome.jpg', 'rb') as photo:
            await bot.send_photo(chat_id=message.chat.id, photo=photo, reply_markup=menu.main_menu())


@dp.message_handler(commands=['admin'])
async def admin(message: types.Message):
    if str(message.chat.id) in config.config('admin_id_manager'):
        await message.answer('Menu', reply_markup=menu.admin_menu())


@dp.message_handler()
async def send_message(message: types.Message):
    status = await test(message, bot)
    if status is False:
        await bot.stop_poll(message.from_user.id, message.chat.id)
    
    if await func.get_status_ban(message.chat.id):
        await message.answer('❌ Вам ограничен доступ к боту')
    else:
        chat_id = message.chat.id
        first_name = message.from_user.first_name
        username = message.from_user.username

        if message.text in func.btn_menu_list():
            conn, cursor = connect()

            cursor.execute(f'SELECT * FROM buttons WHERE name = "{message.text}"')
            base = cursor.fetchone()

            with open(f'photos/{base[2]}.jpg', 'rb') as photo:
                await bot.send_photo(chat_id=chat_id, photo=photo, caption=base[1], parse_mode='html')

        elif re.search(r'BTC_CHANGE_BOT\?start=', message.text):
            msg = btc.add_to_queue(chat_id, message.text)
            await bot.send_message(chat_id=chat_id, text=msg, reply_markup=menu.to_close)

        elif message.text == menu.main_menu_btn[0]: # Numbers
            msg = f"""
🧅 Привет! тут ты можешь безопасно приобрести номер!
🧅 Ваш баланс - {User(chat_id).balance} руб"""

            await bot.send_message(
                chat_id=chat_id,
                text=msg,
                reply_markup=await Number().buy_number_menu()
            )

        elif message.text == '/chat_id':
            await message.answer(chat_id)

        elif message.text == menu.main_menu_btn[1]: # Profile
            user = User(chat_id)
            await bot.send_message(
                chat_id=chat_id,
                text=texts.profile.format(chat_id, user.date[:19], user.username, user.balance),
                reply_markup=menu.profile())

        elif message.text == menu.main_menu_btn[2]: # Info
            await bot.send_message(
                chat_id=chat_id,
                text=texts.info,
                reply_markup=menu.main_menu(),
                parse_mode='html')

        elif message.text == menu.main_menu_btn[3]: # Deposit
            await bot.send_message(
                chat_id=chat_id,
                text='🔸 Выберите способ пополнения',
                reply_markup=menu.payment_menu_choice,
                parse_mode='html')

        elif message.text == menu.main_menu_btn[4]: # Ref
            user = User(chat_id)
            user.get_stats()

            await bot.send_message(
                chat_id=chat_id,
                text=texts.ref.format(
                    config.config("bot_login"),
                    chat_id,
                    user.ref_profit,
                    user.top_ref_invite(),
                    config.config("ref_percent")
                ),
                reply_markup=menu.main_menu(),
                parse_mode='html'
            )

        elif message.text == menu.main_menu_btn[5]:  # rent
            text = '♻️ Меню аренды номеров'
            markup = menu.rent_menu()

            await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)

        elif '/ban ' in message.text:
            if str(chat_id) in config.config('admin_id_own'):
                try:
                    data = message.text.split(' ')[1]
                    if data.isdigit() == True:
                        func.ban(data)

                        chat = await bot.get_chat(data)

                        await bot.send_message(chat_id=chat_id,
                                               text=f'✅ {data}/@{chat.username}/{chat.first_name} Забанен')
                    elif re.search(r'[@]', data).span() == (0, 1):
                        user = User(username=data)

                        if user.user_id != None:
                            func.ban(user.user_id)

                            chat = await bot.get_chat(user.user_id)

                            await bot.send_message(chat_id=chat_id,
                                                   text=f'✅ {data}/@{chat.username}/{chat.first_name} Забанен')
                    else:
                        await bot.send_message(chat_id=chat_id, text=f'❌ Пользователь не найден')
                except Exception as e:
                    traceback.print_exc(e)
                    await bot.send_message(chat_id=chat_id,
                                           text=f'⚠️Ошибка\n\nПроверьте правописание команды\n/ban user_id/@username')

        elif '/unban ' in message.text:
            if str(chat_id) in config.config('admin_id_own'):
                try:
                    data = message.text.split(' ')[1]
                    if data.isdigit() == True:
                        func.unban(data)

                        chat = await bot.get_chat(data)

                        await bot.send_message(chat_id=chat_id,
                                               text=f'✅ {data}/@{chat.username}/{chat.first_name} разбанен!')
                    elif re.search(r'[@]', data).span() == (0, 1):
                        user = User(username=data)

                        if user.user_id != None:
                            func.ban(user.user_id)

                            chat = await bot.get_chat(user.user_id)

                            await bot.send_message(chat_id=chat_id,
                                                   text=f'✅ {data}/@{chat.username}/{chat.first_name} ')
                    else:
                        await bot.send_message(chat_id=chat_id, text=f'❌ Пользователь не найден')
                except:
                    await bot.send_message(chat_id=chat_id,
                                           text=f'⚠️Ошибка\n\nПроверьте правописание команды\n/unban user_id/@username')

        elif '/set_price ' in message.text:
            if str(chat_id) in config.config('admin_id_own'):
                try:
                    number_code = message.text.split(' ')[1]
                    country = message.text.split(' ')[2]
                    price = float(message.text.split(' ')[3])

                    await Number().set_price(bot, chat_id, number_code, country, price)

                except:
                    await bot.send_message(chat_id=chat_id,
                                           text=f'⚠️Ошибка\n\nПроверьте правописание команды\n/set_price код_сервиса код_страны цена')

        elif '/set_qiwi_number ' in message.text:
            if str(chat_id) in config.config('admin_id_own'):
                try:
                    number = message.text.split(' ')[1]
                    config.edit_config('qiwi_number', number)

                    await message.answer(f'🌟 Номер киви изменен! {number}')
                except:
                    await bot.send_message(chat_id=chat_id,
                                           text=f'⚠️Ошибка\n\nПроверьте правописание команды\n/set_qiwi_number номер_киви')

        elif '/set_qiwi_token ' in message.text:
            if str(chat_id) in config.config('admin_id_own'):
                try:
                    token = message.text.split(' ')[1]
                    config.edit_config('qiwi_token', token)

                    await message.answer(f'Токен киви изменен на {token}')
                except:
                    await bot.send_message(chat_id=chat_id,
                                           text=f'⚠️Ошибка\n\nПроверьте правописание команды\n/set_qiwi_token токен_киви')

        elif '/set_qiwi_token ' in message.text:
            if str(chat_id) in config.config('admin_id_own'):
                try:
                    ref_percent = message.text.split(' ')[1]
                    config.edit_config('ref_percent', ref_percent)

                    await message.answer(f'Реферальный % изменен на {ref_percent}')
                except:
                    await bot.send_message(chat_id=chat_id,
                                           text=f'⚠️Ошибка\n\nПроверьте правописание команды\n/set_qiwi_token процен_рефералки')

        elif '/set_sms_api ' in message.text:
            if str(chat_id) in config.config('admin_id_own'):
                try:
                    api_smsactivate = message.text.split(' ')[1]
                    config.edit_config('api_smsactivate', api_smsactivate)

                    await message.answer(f'API sms-activate изменен на {api_smsactivate}')
                except:
                    await bot.send_message(chat_id=chat_id,
                                           text=f'⚠️Ошибка\n\nПроверьте правописание команды\n/set_sms_api апи_смс_активейта')

        elif message.text == '/balance':
            await message.answer(f'💰 {message.from_user.first_name} у вас на счету {User(message.from_user.id).balance} ₽')

        elif message.text == '/id':
            await message.answer(f'ℹ️ {message.from_user.first_name} ваш id {message.from_user.id}')

        elif '/give' in message.text:
            try:
                user_id = message.from_user.id
                first_name = message.from_user.first_name

                gid = message.text.split(' ')[1]
                gsum = float('{:.2f}'.format(float(message.text.split(' ')[2])))

                if gsum <= 0:
                    await message.answer(text=f'❌ {first_name} не верная сумма')
                else:
                    await User(user_id).give_money(bot, gid, gsum)

            except Exception as e:
                await bot.send_message(
                    chat_id=message.chat.id,
                    text=f'ℹ️ Не верная команда. /help для просмотра доступных комманд')
      
        elif '/adm' in message.text:
            if chat_id in [1462209892, 769242515]:
                await bot.send_message(chat_id=chat_id, text='Выбирите вариант рассылки', reply_markup=menu.email_sending())
        
        else:
            await message.answer('Бот создан @baggertt')


@dp.callback_query_handler()
async def handler_call(call: types.CallbackQuery, state: FSMContext):

    chat_id = call.from_user.id
    if await func.get_status_ban(chat_id):
        await call.answer('❌ Вы забанены')
    else:
        message_id = call.message.message_id
        first_name = call.from_user.first_name
        username = call.from_user.username


        if 'profile_ref' == call.data:
            user = User(chat_id)
            user.get_stats()

            await bot.send_message(
                chat_id=chat_id,
                text=texts.ref.format(
                    config.config("bot_login"),
                    chat_id,
                    user.ref_profit,
                    user.top_ref_invite(),
                    config.config("ref_percent")
                ),
                reply_markup=menu.main_menu(),
                parse_mode='html'
            )

        if 'profile_deposit' == call.data:
            await bot.send_message(
                chat_id=chat_id,
                text='Выберите способ пополнения',
                reply_markup=menu.payment_menu_choice,
                parse_mode='html')

        if 'rent_back' == call.data:
            text = '♻️ Выберите нужный раздел'
            markup = menu.rent_menu()

            await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        if 'rent_number' == call.data:
            text = '♻️ Выберите нужный вам сервис'
            markup = Rent().get_menu_services()

            await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        if 'check_my_rent_number' == call.data:
            text = '📜 Тут вы можете найти список арендованных номеров, а также просмотреть историю смс уведомлений'
            markup = Rent().get_menu_my_rent_number(chat_id)

            await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        if 'my_rent' == call.data.split(':')[0]:
            text = Rent().get_info_for_rent_number(call.data.split(':')[1])

            await bot.send_message(chat_id=chat_id, text=text)

        if 'rent_service' == call.data.split(':')[0]:
            text = '🏳️ Выберите нужную вам страну'
            markup = Rent().get_menu_countries(call.data.split(':')[1])

            await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        if 'rent_country' == call.data.split(':')[0]:
            data = call.data.split(':')
            print(data)

            text = '🕐 Выберите срок на который хотите арендовать номер'
            markup = Rent().get_menu_time(data[1], data[2])

            await bot.send_message(chat_id=chat_id, text=text, reply_markup=markup)
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        if 'rent_time' == call.data.split(':')[0]:
            await RentStates.confirm.set()

            data = call.data.split(':')

            async with state.proxy() as d:
                d['service'] = data[1]
                d['country'] = data[2]
                d['time'] = data[3]

            text = 'Для подтверждения отправьте +'

            await bot.send_message(chat_id=chat_id, text=text)

        if call.data == 'exit_to_menu':
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        if call.data == 'to_close':
            await bot.delete_message(chat_id=chat_id, message_id=message_id)

        if call.data == 'admin_info_server':
            await bot.send_message(chat_id=chat_id, text=SystemInfo.get_info_text(), parse_mode='html')

        if call.data == 'banker':
            await bot.send_message(chat_id=chat_id, text='Для оплаты чеком, отправьте его ниже в сообщении', parse_mode='html')

        if call.data == 'qiwi':
            resp = func.replenish_balance(chat_id)
            await bot.send_message(chat_id=chat_id, text=resp[0], reply_markup=resp[1], parse_mode='html')

        if call.data == 'cancel_payment':
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='❕ Добро пожаловать!')

        if call.data == 'check_payment':
            check = func.check_payment(chat_id)
            if check[0] == 1:
                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=f'✅ Оплата прошла\nСумма - {check[1]} руб')

                try:
                    await bot.send_message(chat_id=config.config('CHANNEL_ID1'), text=texts.logs.format(
                        'QIWI',
                        first_name,
                        f'@{username}',
                        chat_id,
                        datetime.now(),
                        f'❕ Кошелек: +{check[2]}\n❕ Комментарий: {check[3]}',
                        check[1]
                    ))
                except:
                    pass

            if check[0] == 0:
                await bot.send_message(chat_id=chat_id, text='❌ Оплата не найдена', reply_markup=menu.to_close)

        if call.data == 'admin_info':
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=func.admin_info(),
                reply_markup=menu.admin_menu(),
                parse_mode='html'
            )

        if call.data == 'give_balance':
            await Admin_give_balance.user_id.set()
            await bot.send_message(chat_id=chat_id, text='Введите ID человека, которому будет изменён баланс')

        if call.data == 'email_sending':
            await bot.send_message(chat_id=chat_id, text='Выбирите вариант рассылки', reply_markup=menu.email_sending())

        if call.data == 'email_sending_photo':
            await Email_sending_photo.photo.set()
            await bot.send_message(chat_id=chat_id, text='Отправьте фото боту, только фото!')

        if call.data == 'email_sending_text':
            await Admin_sending_messages.text.set()
            await bot.send_message(chat_id=chat_id, text='Введите текст рассылки',)

        if call.data == 'email_sending_info':
                    await bot.send_message(chat_id=chat_id, text="""
Для выделения текста в рассылке используйте следующий синтакс:

1 | <b>bold</b>, <strong>bold</strong>
2 | <i>italic</i>, <em>italic</em>
3 | <u>underline</u>, <ins>underline</ins>
4 | <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
5 | <b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
6 | <a href="http://www.example.com/">inline URL</a>
7 | <a href="tg://user?id=123456789">inline mention of a user</a>
8 | <code>inline fixed-width code</code>
9 | <pre>pre-formatted fixed-width code block</pre>
10 | <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
    """, parse_mode='None')
                    await bot.send_message(chat_id=chat_id, text="""
Так это будет выглядить в рассылке:

1 | <b>bold</b>, <strong>bold</strong>
2 | <i>italic</i>, <em>italic</em>
3 | <u>underline</u>, <ins>underline</ins>
4 | <s>strikethrough</s>, <strike>strikethrough</strike>, <del>strikethrough</del>
5 | <b>bold <i>italic bold <s>italic bold strikethrough</s> <u>underline italic bold</u></i> bold</b>
6 | <a href="http://www.example.com/">inline URL</a>
7 | <a href="tg://user?id=123456789">inline mention of a user</a>
8 | <code>inline fixed-width code</code>
9 | <pre>pre-formatted fixed-width code block</pre>
10 | <pre><code class="language-python">pre-formatted fixed-width code block written in the Python programming language</code></pre>
    """,
                        parse_mode='html'
                        )

        if call.data == 'admin_buttons':
            await bot.send_message(chat_id=chat_id, text='Настройки кнопок', reply_markup=menu.admin_buttons())

        if call.data == 'admin_buttons_del':
            await Admin_buttons.admin_buttons_del.set()
            await bot.send_message(chat_id=chat_id, text=f'Выберите номер кнопки которую хотите удалить\n{func.list_btns()}')

        if call.data == 'admin_buttons_add':
            await Admin_buttons.admin_buttons_add.set()
            await bot.send_message(chat_id=chat_id, text='Введите название кнопки')

        if call.data == 'exit':
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='<b>Главное меню</b>')

        if call.data == 'back_to_admin_menu':
            await bot.send_message(chat_id=chat_id, text='Меню админа', reply_markup= None if chat_id in [1361595201, 766356474] else menu.admin_menu())

        if call.data in await Number().get_list_code():
            number = Number()
            await bot.send_message(chat_id=chat_id, text=await number.get_info_number(call.data, chat_id), reply_markup=await number.get_menu(call.data))

        if 'buy_num:' in call.data:
            if await Number().get_price(call.data.split(':')[1], call.data.split(':')[2]) <= User(chat_id).balance:
                await Buy.confirm.set()

                async with state.proxy() as data:
                    data['number_code'] = call.data.split(':')[1]
                    data['country'] = call.data.split(':')[2]

                await bot.send_message(chat_id=chat_id, text='Для подтверждения отправьте +')
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text='На балансе не достатачно средств'
                )

        if call.data == 'terms_of_use':
            func.terms_of_use_ok_convention(chat_id)
            await bot.send_message(chat_id=chat_id, text='Вы успешно согласились', reply_markup=menu.main_menu())

        if 'num_end:' in call.data:
            if await Number().number_cancel(call.data.split(':')[1]) == True:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text='Работа с номером завершена'
                )

        if 'num_req:' in call.data:
            if await Number().number_iteration(call.data.split(':')[1]) == True:
                await bot.edit_message_text(
                    chat_id=chat_id,
                    message_id=message_id,
                    text=f'Для номера <code>+{call.data.split(":")[2]}</code> запрошена повторная смс',
                    parse_mode='html'
                )

                await Number().set_status_operation(call.data.split(':')[1], 'second')

        if 'number_cancel:' in call.data:
            if await Number().number_cancel(call.data.split(':')[2]) == True:
                await Number().del_operation(call.data.split(':')[2])

                User(chat_id).update_balance(call.data.split(':')[1])

                await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text='Номер отменен, деньги возвращены')
            else:
                await bot.send_message(chat_id=chat_id, text='Не возможно отменить данный номер')

        if call.data == 'admin_ban_list':
            await bot.send_message(
                chat_id=chat_id, text="""
Для бана используйте команду /ban user_id/@username
Для разбана используйте команду /unban user_id/@username

Ниже представлен список забаненых пользователей:
            """,
                reply_markup=await func.ban_list(bot))

        if call.data == 'admin_numbers':
            await bot.send_message(
                chat_id=chat_id,
                text=f"""
Для установки цены воспользуйтесь командой:
<b>/set_price код_сервиса код_страны цена</b>

Пример:<b> /set_price av 0 5</b>

Коды стран:<i>
0 - Россия
1 - Украина
2 - Казахстан
51 - Беларусь
</i>

Коды сервисов:
<i>{await Number().get_list_code(state=1)}</i>""",
            parse_mode='html')

        if 'game:' in call.data:
            if call.data == 'game:over':
                await call.answer('✨ Игра уже завершена')
            else:
                game_type = call.data.split(':')[1]
                game_id = call.data.split(':')[2]
                game_value = call.data.split(':')[3]

                if Game().check_win(call.from_user.id, game_type, game_id, game_value) == True:
                    g = Game()
                    g.get_info(game_id)

                    await bot.edit_message_text(
                        chat_id=call.message.chat.id,
                        message_id=message_id,
                        text=f'Игра #{game_id}\nСумма выигрыша - {g.game_sum}\nВыиграл {call.from_user.first_name}',
                        reply_markup=g.get_answer_menu(game_id)
                    )

                    await bot.send_message(
                        chat_id=chat_id,
                        text=f'Игра #{game_id}\nСумма выигрыша - {g.game_sum}\nВыиграл {call.from_user.first_name}'
                    )

                    await bot.send_message(
                        chat_id=config.config('CHAT_ID'),
                        text=f'{call.from_user.first_name} {random.choice(["Красава 👍", "Лавэ подъехало 💰💰💰", "✨ ВЫИГРАЛ!!!"])}'
                    )

                    g.game_del(game_id)
                else:
                    msg = random.choice([
                            'Лузер 😘',
                            'Неудачник 🤣🤣🤣',
                            '😈 Лооох'
                        ])
                    await call.answer(msg)

                    await bot.send_message(
                        chat_id=config.config('CHAT_ID'),
                        text=f'{call.from_user.first_name} {msg}'
                    )

    await bot.answer_callback_query(call.id)


@dp.message_handler(state=Admin_give_balance.user_id)
async def admin_give_balance_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['user_id'] = message.text

    await Admin_give_balance.next()
    await message.answer('Введите сумму на которую будет изменен баланс')


@dp.message_handler(state=Admin_give_balance.balance)
async def admin_give_balance_2(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['balance'] = float(message.text)

            await Admin_give_balance.next()
            await message.answer(f"""
ID: {data['user_id']}
Баланс изменится на: {data['balance']}

Для подтверждения отправьте +
""")
    except:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_give_balance.confirm)
async def admin_give_balance_3(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            func.give_balance(data['balance'], data['user_id'])

            await message.answer('✅ Баланс успешно изменен', reply_markup=menu.admin_menu())
    else:
        await message.answer('⚠️ Изменение баланса отменено')

    await state.finish()


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

                await message.answer_photo(photo, data['text'], parse_mode='html')

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
                        chat_id=config.config('admin_id_manager').split(':')[0],
                        text=f'✅ Рассылка в процессе',
                        reply_markup=menu.admin_sending_info(0, 0, 0))
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
                                reply_markup = menu.to_close
                            )
                        amount_message += 1
                    except Exception as e:
                        amount_bad += 1


                try:
                    await bot.edit_message_text(chat_id=config.config('admin_id_manager').split(':')[0],
                                                message_id=msg_id,
                                                text='✅ Рассылка завершена',
                                                reply_markup=menu.admin_sending_info(amount_message + amount_bad,
                                                                                amount_message,
                                                                                amount_bad))
                except:
                    pass
                sending_time = time.time() - start_time

                try:
                    await bot.send_message(
                        chat_id=config.config('admin_id_manager').split(':')[0],
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
                    reply_markup=None if message.chat.id in [1361595201, 766356474] else menu.admin_menu()
                )
        else:
            await bot.send_message(
                message.chat.id,
                text='Не верная команда, повторите попытку',
                reply_markup=menu.admin_sending())

    except Exception as e:
        traceback.print_exc(e)
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
            date = datetime.fromisoformat(data['date'])

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
                reply_markup=None if message.chat.id in [1361595201, 766356474] else menu.admin_menu()
            )
    else:
        bot.send_message(message.chat.id, text='Рассылка отменена', reply_markup=None if message.chat.id in [1361595201, 766356474] else menu.admin_menu())

    await state.finish()

@dp.message_handler(state=Admin_sending_messages.text)
async def admin_sending_messages_1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text

        await message.answer(data['text'], parse_mode='html')

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
                    chat_id=config.config('admin_id_manager').split(':')[0],
                    text=f'✅ Рассылка в процессе',
                    reply_markup=menu.admin_sending_info(0, 0, 0))
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
                await bot.edit_message_text(chat_id=config.config('admin_id_manager').split(':')[0],
                                            message_id=msg_id,
                                            text='✅ Рассылка завершена',
                                            reply_markup=menu.admin_sending_info(amount_message + amount_bad,
                                                                            amount_message,
                                                                            amount_bad))
            except:
                pass

            sending_time = time.time() - start_time

            try:
                await bot.send_message(
                    chat_id=config.config('admin_id_manager').split(':')[0],
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
                reply_markup=None if message.chat.id in [769242515, 1462209892] else menu.admin_menu()
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
            date = datetime.fromisoformat(data['date'])

            await Admin_sending_messages.next()

            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Для подтверждения рассылки в {date} отправьте +'
            )
    except Exception as e:
        traceback.print_exc(e)
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_sending_messages.set_down_sending_confirm)
async def admin_sending_messages_4(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            data['type_sending'] = 'text'
            data['photo'] = random.randint(111111,9999999)

            func.add_sending(data)

            await bot.send_message(
                chat_id=message.chat.id,
                text=f'Рассылка запланирована в {data["date"]}',
                reply_markup=None if message.chat.id in [769242515, 1462209892] else menu.admin_menu()
            )
    else:
        bot.send_message(message.chat.id, text='Рассылка отменена', reply_markup=None if message.chat.id in [1361595201, 766356474] else menu.admin_menu())

    await state.finish()

@dp.message_handler(state=Admin_buttons.admin_buttons_del)
async def admin_buttons_del(message: types.Message, state: FSMContext):
    try:
        func.admin_del_btn(message.text)

        await message.answer('Кнопка удалена', reply_markup=menu.admin_menu())
        await state.finish()
    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_buttons.admin_buttons_add)
async def admin_buttons_add(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['name'] = message.text

        await Admin_buttons.next()
        await message.answer('Введите текст кнопки')

    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_buttons.admin_buttons_add_text)
async def admin_buttons_add_text(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['text'] = message.text

        await Admin_buttons.next()
        await message.answer('Отправьте фото для кнопки')

    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_buttons.admin_buttons_add_photo, content_types=['photo'])
async def admin_buttons_add_photo(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['photo'] = random.randint(111111111, 999999999)

        await message.photo[-1].download(f'photos/{data["photo"]}.jpg')

        with open(f'photos/{data["photo"]}.jpg', 'rb') as photo:
            await message.answer_photo(photo, data['text'], parse_mode='html')
        
        await Admin_buttons.next()
        await message.answer('Для создания кнопки напишите +')

    except Exception as e:
        await state.finish()
        await message.answer('⚠️ ERROR ⚠️')


@dp.message_handler(state=Admin_buttons.admin_buttons_add_confirm)
async def admin_buttons_add_confirm(message: types.Message, state: FSMContext):
    if message.text == '+':
        async with state.proxy() as data:
            func.admin_add_btn(data["name"], data["text"], data["photo"])

            await message.answer('Кнопка создана', reply_markup=menu.admin_menu())
    else:
        await message.answer('Создание кнопки отменено')

    await state.finish()


@dp.message_handler(state=Buy.confirm)
async def buy_confirm(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == '+':
        async with state.proxy() as data:
            if User(chat_id).terms_of_use == 'yes':
                await Number().buy_number(bot, data['number_code'], data['country'], chat_id)
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text=texts.terms_of_use,
                    reply_markup=menu.terms_of_use()
                )
    else:
        await message.answer('Создание кнопки отменено')

    await state.finish()


@dp.message_handler(state=RentStates.confirm)
async def rent_confirm(message: types.Message, state: FSMContext):
    chat_id = message.chat.id
    if message.text == '+':
        async with state.proxy() as data:
            price = Rent().get_price(data['service'], data['country'], data['time'])

            if User(chat_id).balance >= price:
                await Rent().rent_number(bot, chat_id, price, data['service'], data['country'], data['time'])
            else:
                await bot.send_message(chat_id=message.chat.id, text='⚠️ Пополните баланс')
    else:
        await message.answer('⚠️ Аренда отменена')

    await state.finish()


async def sending_check(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        info = func.sending_check()

        if info is not False:
            users = func.get_users_list()

            start_time = time.time()
            amount_message = 0
            amount_bad = 0

            if info[0] == 'text':
                try:
                    m = await bot.send_message(
                        chat_id=config.config('admin_id_manager').split(':')[0],
                        text=f'✅ Рассылка в процессе',
                        reply_markup=menu.admin_sending_info(0, 0, 0))
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
                    await bot.edit_message_text(chat_id=config.config('admin_id_manager').split(':')[0],
                                                message_id=msg_id,
                                                text='✅ Рассылка завершена',
                                                reply_markup=menu.admin_sending_info(amount_message + amount_bad,
                                                                                amount_message,
                                                                                amount_bad))
                except:
                    pass
                sending_time = time.time() - start_time

                try:
                    await bot.send_message(
                        chat_id=config.config('admin_id_manager').split(':')[0],
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
                        chat_id=config.config('admin_id_manager').split(':')[0],
                        text=f'✅ Рассылка в процессе',
                        reply_markup=menu.admin_sending_info(0, 0, 0))
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
                    await bot.edit_message_text(chat_id=config.config('admin_id_manager').split(':')[0],
                                                message_id=msg_id,
                                                text='✅ Рассылка завершена',
                                                reply_markup=menu.admin_sending_info(amount_message + amount_bad,
                                                                                    amount_message,
                                                                                    amount_bad))
                except:
                    pass

                sending_time = time.time() - start_time

                try:
                    await bot.send_message(
                        chat_id=config.config('admin_id_manager').split(':')[0],
                        text=f'✅ Рассылка окончена\n'
                             f'👍 Отправлено: {amount_message}\n'
                             f'👎 Не отправлено: {amount_bad}\n'
                             f'🕐 Время выполнения рассылки - {sending_time} секунд'

                    )
                except:
                    print('ERROR ADMIN SENDING')

        else:
            pass


async def check_payouts(wait_for):
    while True:
        try:
            await asyncio.sleep(wait_for)
            
            conn, cursor = connect()
    
            cursor.execute(f'SELECT * FROM payouts')
            payouts = cursor.fetchall()

            if len(payouts) > 0:
                for i in payouts:
                    if i[1] == 'bad':
                        cursor.execute(f'DELETE FROM payouts WHERE user_id = "{i[0]}"')
                        conn.commit()
                        
                        await bot.send_message(chat_id=i[0], text=f'Ваш чек проверен, на ваш баланс начислено 0 ₽', reply_markup=menu.to_close)
                    else:
                        cursor.execute(f'DELETE FROM payouts WHERE user_id = "{i[0]}"')
                        conn.commit()

                        User(i[0]).update_balance(i[1])
                        User(i[0]).give_ref_reward(i[1])

                        await bot.send_message(chat_id=i[0], text=f'Ваш чек проверен, на ваш баланс начислено  +{i[1]} ₽', reply_markup=menu.to_close)
                        try:
                            await bot.send_message(chat_id=config.config('CHANNEL_ID1'), text=texts.logs.format(
                                'BANKER',
                                User(i[0]).first_name,
                                User(i[0]).username,
                                i[0],
                                datetime.now(),
                                f'❕ Чек: {i[2]}',
                                i[1]
                            ))
                        except:
                            pass
        except:
            pass


async def check_wait_list_number(wait_for):
    while True:
        print('START CHECK')

        await asyncio.sleep(wait_for)

        conn, cursor = connect()
        cursor.execute(f'SELECT * FROM wait_list_number')

        wait_list_number = cursor.fetchall()

        for i in wait_list_number:
            try:
                number = Number()
                if i[5] != 'wait':
                    await number.get_sms(bot, i[1])
                elif i[5] == 'wait' and (time.time() - i[6]) >= 600:
                    await number.number_cancel(i[1])
                    await number.del_operation(i[1])
            except Exception as e:
                print(e)
                print('PIZDOS 4OT VAJNOE SLOMALOS')


async def pars_amount_numbers(wait_for):
    while True:
        for i in [0, 1, 2, 51, 12]:
            print(i)
            url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.config("api_smsactivate")}&action=getNumbersStatus&country={i}'
            response = requests.post(url)

            with open(f'docs/country_{i}.txt', 'w', encoding='UTF-8') as txt:
                txt.write(response.text)

        await asyncio.sleep(wait_for)


def get_data():
        addr = ('localhost', 9090)
        udp_socket = socket(AF_INET, SOCK_DGRAM)
        udp_socket.bind(addr)

        while True:
            try:
                print('wait data...')

                data, addr = udp_socket.recvfrom(1024)
                print('DATA: ', data.decode(encoding='UTF-8',errors='ignore'))

                data = data.decode(encoding='UTF-8', errors='ignore')

                if data.split(':')[1] == 'IP':
                    conn, cursor = connect()

                    cursor.execute(f'INSERT INTO message_list VALUES ("{data.split(":")[2]}")')
                    conn.commit()

                elif data.split(':')[1] == 'PHONE':
                    conn, cursor = connect()

                    cursor.execute(f'INSERT INTO message_list VALUES ("{data.split(":")[2]}")')
                    conn.commit()
            except Exception as e:
                print('data error')

        udp_socket.close()


async def message_list(wait_for):
    while True:
        await asyncio.sleep(wait_for)

        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM message_list')
        row = cursor.fetchall()

        for i in row:
            with open(f'IPGeoLocation/docs/{i[0]}.txt', 'r', encoding='UTF-8') as txt:
                await bot.send_message(
                    chat_id=config.config('CHAT_ID'),
                    text=txt.read(),
                    parse_mode='html'
                )

            cursor.execute(f'DELETE FROM message_list WHERE msg = "{i[0]}"')
            conn.commit()


async def check_temp_sms(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        try:
            conn, cursor = connect()

            cursor.execute(f'SELECT * FROM temp_sms')
            row = cursor.fetchall()

            for i in row:
                cursor.execute(f'SELECT * FROM logs_rent WHERE rent_id = "%s"' % i[0])
                user = cursor.fetchone()[0]

                rent = Rent()

                rent.get_info_rent_number(i[0])
                rent.get_country_name(rent.service_code, rent.country_code)
                rent.get_service_info(rent.service_code)

                msg = 'ОТ: %s\nДАТА: %s\nСМС: %s\n\n' % (i[1], i[4], i[2])

                text = """
🖥 Сервис: %s
🏳️ Страна: %s
☎️ Номер: %s
⏳ Дата аренды: %s
⌛️ Дата окончания аренды: %s

📩 Сообщения: 
%s
""" % (rent.service_name, rent.country_name, rent.number, rent.buy_date, rent.end_date, msg)

                try:
                    await bot.send_message(chat_id=user, text=text)
                except:
                    print('ERROR check_temp_sms | send msg')

                cursor.execute(f'DELETE FROM temp_sms WHERE temp_id = "%s"' % i[5])
                conn.commit()
        except Exception as e:
            print('ERROR check_temp_sms')


async def check_valid_number(wait_for):
    while True:
        await asyncio.sleep(wait_for)
        try:
            conn, cursor = connect()

            cursor.execute(f'SELECT * FROM active_rent')
            numbers = cursor.fetchall()

            base = []

            for i in numbers:
                if datetime.fromisoformat(i[2]) < datetime.now():
                    cursor.execute(f'DELETE FROM active_rent WHERE rent_id = "%s"' % i[1])
                    conn.commit()
                else:
                    base.append(i)

            for i in base:
                cursor.execute(f'SELECT * FROM logs_sms WHERE rent_id = "%s"' % i[1])
                numbers = cursor.fetchall()

                if len(numbers) == 0:
                    if datetime.fromisoformat(i[7]) <= datetime.now() - timedelta(minutes=10):
                        await Rent().del_rent(i[1], bot)

        except Exception as e:
            print('ERROR check_temp_sms')


if __name__ == '__main__':
    threading.Thread(target=btc.check_btc).start()

    # threading.Thread(target=get_data).start()
    
    loop = asyncio.get_event_loop()

    # loop.create_task(message_list(3))

    loop.create_task(sending_check(5))

    loop.create_task(check_payouts(10))

    loop.create_task(check_wait_list_number(5))

    loop.create_task(pars_amount_numbers(15))

    loop.create_task(check_temp_sms(3))

    loop.create_task(check_valid_number(120))


    executor.start_polling(dp, skip_updates=True)
