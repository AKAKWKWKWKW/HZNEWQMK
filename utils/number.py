from utils.mydb import *
from utils.user import *
from aiogram import types

import config
import requests
import json
import time
import asyncio
# import sqlite3
import texts
import menu
import functions as func


class Number():

    def __init__(self):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM numbers')
        self.numbers = cursor.fetchall()


    async def get_list_code(self, state=0):
        if state == 0:
            code_list = []

            for i in self.numbers:
                code_list.append(i[0])
        elif state == 1:
            code_list = ''

            for i in self.numbers:
                code_list += f'{i[0]} - {i[1]}\n'

        return code_list


    async def request_info_from_smshub(self, country):
        with open(f'docs/country_{country.split(":")[0]}.txt', 'r', encoding='UTF-8') as txt:
            return json.loads(txt.read())
    

    async def request_info_from_smsactivate(self, country):
        with open(f'docs/countrySMSACTIVATE_{country.split(":")[0]}.txt', 'r', encoding='UTF-8') as txt:
            return json.loads(txt.read())


    async def get_info_number(self, user_id):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM game_logs WHERE user_id = "{user_id}"')
        games = cursor.fetchall()

        amount_games = len(games)

        user = User(user_id)

        msg = texts.info.format(
            user.balance,
            user_id,
            user.get_purchase_count(),
            amount_games,
            func.get_current_discount(user_id)
        )

        return msg


    async def get_country_name(self, country_code):
        base = {
            '0': '🇷🇺 Россия',
            '1': '🇺🇦 Украина',
            '2': '🇰🇿 Казахстан',
            '51': '🇧🇾 Беларусь',
            '15': '🇵🇱 Польшу',
            '32': '🇷🇴 Румыния 32',
        }

        return base.get(country_code)


    async def get_menu(self, user_id):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM numbers')
        __service = cursor.fetchall()

        markup = types.InlineKeyboardMarkup(row_width=2)

        x1 = 0
        x2 = 1
        
        discount = func.get_current_discount(user_id)

        try:
            for i in range(len(__service)):
                price1 = f'{__service[x1][2].split(":")[1]} ₽' if discount == 0 else f'{float(__service[x1][2].split(":")[1]) - float(__service[x1][2].split(":")[1]) / 100 * discount} ₽ | Скидка {discount} %'
                price2 = f'{__service[x2][2].split(":")[1]} ₽' if discount == 0 else f'{float(__service[x2][2].split(":")[1]) - float(__service[x2][2].split(":")[1]) / 100 * discount} ₽ | Скидка {discount} %'
                
                markup.add(
                    types.InlineKeyboardButton(text=f'🔹  {__service[x1][1]} | {price1}',
                                               callback_data=f'number:{__service[x1][0]}'),
                    types.InlineKeyboardButton(text=f'🔹  {__service[x2][1]} | {price2}',
                                               callback_data=f'number:{__service[x2][0]}')
                )

                x1 += 2
                x2 += 2
        except Exception as e:
            try:
                price1 = f'{__service[x1][2].split(":")[1]} ₽' if discount == 0 else f'{float(__service[x1][2].split(":")[1]) - float(__service[x1][2].split(":")[1]) / 100 * discount} ₽ | Скидка {discount} %'
                markup.add(
                    types.InlineKeyboardButton(text=f'🔹  {__service[x1][1]} | {price1}',
                                               callback_data=f'number:{__service[x1][0]}')
                )
            except:
                return markup

        return markup


    async def get_menu_country(self, number_code, user_id):
        base = await self.get_country_amount_price(number_code)

        discount = func.get_current_discount(user_id)

        markup = types.InlineKeyboardMarkup(row_width=2)
        for i in base:
            price = f'{i[2]}' if discount == 0 else f'{float(i[2]) - float(i[2]) / 100 * discount} ₽ | Скидка {discount} %'
            markup.add(
                types.InlineKeyboardButton(text=f'{await self.get_country_name(i[0])} | {i[1]} | {price}',
                                           callback_data=f'buy:{number_code}:{i[0]}')
            )

        return markup

    
    async def get_country_amount_price(self, number_code):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM numbers WHERE code = "{number_code}"')
        __service = cursor.fetchone()

        base = []
        
        for i in range(2, len(__service) - 1):
            if __service[i] != '0':
                if number_code == 'ym':
                    amount = await self.request_info_from_smsactivate(__service[i].split(':')[0])
                    amount = int(amount[f'{number_code}_0'])
                else:
                    amount = await self.request_info_from_smshub(__service[i].split(':')[0])
                    amount = int(amount[f'{number_code}_0'])

                base.append([__service[i].split(':')[0] ,amount, __service[i].split(':')[1]])

        return base



    async def get_price(self, number_code, country):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM numbers WHERE code = "{number_code}"')
        __service = cursor.fetchone()

        for i in range(2, len(__service) - 1):
            if __service[i].split(':')[0] == str(country):
                return float(__service[i].split(':')[1])


    async def get_number(self, number_code, country):
        #if number_code == 'ym':
            #url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.config("api_smsactivate")}&action=getNumber&service={number_code}&forward=0&operator=any&ref=0&country={country}'
       #else:
        url = f'https://smshub.org/stubs/handler_api.php?api_key={config.config("api_smshub")}&action=getNumber&service={number_code}&forward=0&operator=any&ref=0&country={country}'
        
        response = requests.post(url)
        response = response.text

        try:
            self.status = response.split(':')[0]
            self.operation_ID = response.split(':')[1]
            self.number = response.split(':')[2]
        except:
            pass

        return self.status


    async def buy_number(self, bot, user_id, number_code, country):
        self.country = country

        user = User(user_id)

        price = await self.get_price(number_code, self.country)
        price = float(price) - (float(price) / 100 * float(func.get_current_discount(user_id)))

        if user.balance >= price:
            self.status = await self.get_number(number_code, self.country)
        else:
            await bot.send_message(chat_id=user_id, text='🚫 Пора пополнить кошелек')

            return

        if str(self.status) == 'ACCESS_NUMBER':
            if number_code == 'ym':
                url2 = f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.config("api_smsactivate")}&action=setStatus&status=1&id={self.operation_ID}'
            else:
                url2 = f'https://smshub.org/stubs/handler_api.php?api_key={config.config("api_smshub")}&action=setStatus&status=1&id={self.operation_ID}'
            response2 = requests.post(url2)

            User(user_id).update_balance(-price)

            await bot.send_message(
                chat_id=user_id,
                text=f'Ваш номер: {self.number}',
                reply_markup=menu.get_code_menu(self.operation_ID, price, number_code)
            )

        elif str(self.status) == 'NO_NUMBERS':
            await bot.send_message(
                chat_id=user_id,
                text=f'🚫 Номеров нет в наличии, попробуйте позже'
            )


    async def get_service_name(self, number_code):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM numbers WHERE code = "{number_code}"')
        __service = cursor.fetchone()

        return __service[1]


    async def get_menu_number_cancel(self, operation_ID, price):
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton(text='❌ Отменить', callback_data=f'number_cancel:{price}:{operation_ID}')
        )

        return markup


    async def get_sms(self, bot, operation_ID, chat_id, number_code):
        if number_code == 'ym':
            url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.config("api_smsactivate")}&action=getStatus&id={operation_ID}'
        else:
            url = f'https://smshub.org/stubs/handler_api.php?api_key={config.config("api_smshub")}&action=getStatus&id={operation_ID}'

        response = requests.post(url)
        response = response.text

        sms = 0
        status = 0

        try:
            status = response.split(':')[0]
            sms = response.split(':')[1]
        except:
            pass

        if str(status) == 'STATUS_OK':
            await bot.send_message(chat_id=chat_id, text=f'🎉 Ваш код: {sms}',
                                   reply_markup=menu.good_code(operation_ID))

            try:
                func.raffle_logs(chat_id)
            except: pass

        else:
            await bot.send_message(chat_id=chat_id, text='Подождите, смс еще не пришло')


    async def set_status_operation(self, operation_ID, status):
        conn, cursor = connect()

        cursor.execute(f'UPDATE wait_list_number SET status = "{status}" WHERE operation_ID = "{operation_ID}"')
        conn.commit()


    async def del_operation(self, operation_ID):
        conn, cursor = connect()

        cursor.execute(f'DELETE FROM wait_list_number WHERE operation_ID = "{operation_ID}"')
        conn.commit()


    async def get_data_operation(self, operation_ID):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM wait_list_number WHERE operation_ID = "{operation_ID}"')
        operation = cursor.fetchone()

        self.user_id = operation[0]
        self.operation_ID = operation[1]
        self.number = operation[2]
        self.number_code = operation[3]
        self.country = operation[4]
        self.status = operation[5]
        self.purchase_time = operation[6]
        self.price = operation[7]


    async def get_buy_num_menu(self, operation_ID, number):
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton(text='✅ Завершить заказ', callback_data=f'num_end:{operation_ID}'),
            types.InlineKeyboardButton(text='🔂 Запросить еще смс', callback_data=f'num_req:{operation_ID}:{number}')
        )

        return markup


    async def number_cancel(self, operation_ID, number_code):
        if number_code == 'ym':
            url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.config("api_smsactivate")}&action=setStatus&status=8&id={operation_ID}'
        else:
            url = f'https://smshub.org/stubs/handler_api.php?api_key={config.config("api_smshub")}&action=setStatus&status=8&id={operation_ID}'
        
        response = requests.post(url)

        if response.text == 'BAD_STATUS':
            return False
        elif response.text == 'ACCESS_CANCEL':
            return True


    async def number_iteration(self, operation_ID):
        url = f'https://sms-activate.ru/stubs/handler_api.php?api_key={config.config("api_smsactivate")}&action=setStatus&status=3&id={operation_ID}'
        response = requests.post(url)

        return True

    async def buy_number_menu(self):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM numbers')
        numbers = cursor.fetchall()

        markup = types.InlineKeyboardMarkup(row_width=2)

        x1 = 0
        x2 = 1
        try:
            for i in range(len(numbers)):
                markup.add(
                    types.InlineKeyboardButton(text=f'{numbers[x1][1]} | {numbers[x1][2].split(":")[1]} ₽',
                                               callback_data=f'{numbers[x1][0]}'),
                    types.InlineKeyboardButton(text=f'{numbers[x2][1]} | {numbers[x2][2].split(":")[1]} ₽',
                                               callback_data=f'{numbers[x2][0]}'),
                )
                x1 += 2
                x2 += 2
        except Exception as e:
            try:
                markup.add(
                    types.InlineKeyboardButton(text=f'{numbers[x1][1]} | {numbers[x1][2].split(":")[1]} ₽',
                                               callback_data=f'{numbers[x1][0]}'))
            except:
                return markup

        markup.add(
            types.InlineKeyboardButton(text='Выйти', callback_data='exit_to_menu')
        )

        return markup


    async def set_price(self, bot, chat_id, number_code, country, price):

        for i in self.numbers:
            if i[0] == number_code:
                for j in range(2, len(i)-1):
                    if i[j].split(':')[0] == country:
                        conn, cursor = connect()

                        cursor.execute(f'UPDATE numbers SET country{j-1} = "{country}:{price}" WHERE code = "{number_code}"')
                        conn.commit()

                        await bot.send_message(chat_id=chat_id, text=f'Вы изменили цену на {price} ₽')

                        return

        await bot.send_message(chat_id=chat_id, text='Сервис не найден')


    async def get_country_number(self, number_code):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM numbers WHERE code = "{number_code}"')
        number = cursor.fetchone()

        country_list = []


        for i in range(2, len(number) - 1):
            print(i)
            if number[i] != '0':
                country_list.append(number[i].split(':')[0])

        return country_list
