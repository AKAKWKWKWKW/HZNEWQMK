import requests
import json

import config

from aiogram import types
from datetime import datetime
from utils.mydb import *
from utils.user import User


sms_text = """
🖥 Сервис: %s
☎️ Номер: %s
⏳ Дата сообщения: %s
⌛️ Дата окончания аренды: %s

👤 От: %s
📩 Сообщение: %s
"""


class Rent:
    @staticmethod
    def create_table():
        conn, cursor = connect()

        try:
            cursor.execute("""CREATE TABLE rent_numbers (service text, 
                                                    countries_and_prices text, 
                                                    name text) """)

            cursor.execute("INSERT INTO rent_numbers VALUES('%s', '%s', '%s')" % (
                'wa', '0:Россия:10:30:130:beeline,tele2;2:Казахстан:10:30:130:beeline,tele2', 'Whatsapp'))
            conn.commit()
        except:
            pass

        try:
            cursor.execute("""CREATE TABLE active_rent (user_id text, 
                                                        rent_id text, 
                                                        end_date text,
                                                        number text,
                                                        price text,
                                                        service text, 
                                                        country text, 
                                                        buy_date text) """)
        except:
            pass

        try:
            cursor.execute("""CREATE TABLE logs_rent (user_id text, 
                                                      rent_id text, 
                                                      end_date text,
                                                      number text,
                                                      price text,
                                                      service text, 
                                                      country text, 
                                                      buy_date text) """)
        except:
            pass

        try:
            cursor.execute("""CREATE TABLE logs_sms (rent_id text, 
                                                      phone_from text, 
                                                      text text,
                                                      sms_id text,
                                                      date text)""")
        except:
            pass

        try:
            cursor.execute("""CREATE TABLE temp_sms (rent_id text, 
                                                      phone_from text, 
                                                      text text,
                                                      sms_id text,
                                                      date text,
                                                      temp_id text)""")
        except:
            pass

    def get_menu_services(self):
        markup = types.InlineKeyboardMarkup(row_width=2)

        numbers = self.get_list_numbers()

        # for i in numbers:
        #     markup.add(types.InlineKeyboardButton(text=i[2],
        #                                           callback_data='rent_service:%s' % (i[0])))

        x1 = 0
        x2 = 1
        try:
            for i in range(len(numbers)):
                markup.add(
                    types.InlineKeyboardButton(text=numbers[x1][2], callback_data='rent_service:%s' % (numbers[x1][0])),
                    types.InlineKeyboardButton(text=numbers[x2][2], callback_data='rent_service:%s' % (numbers[x2][0])),
                )

                x1 += 2
                x2 += 2
        except Exception as e:
            try:
                markup.add(
                    types.InlineKeyboardButton(text=numbers[x1][2], callback_data='rent_service:%s' % (numbers[x1][0])),
                )
            except:
                pass

        markup.add(types.InlineKeyboardButton(text='🔙', callback_data='rent_back'))

        return markup

    def get_menu_countries(self, service):
        markup = types.InlineKeyboardMarkup(row_width=2)

        number = self.get_service_info(service)

        for i in number[1].split(';'):
            markup.add(types.InlineKeyboardButton(text=i.split(':')[1],
                                                  callback_data='rent_country:%s:%s' % (service, i.split(':')[0])))

        markup.add(types.InlineKeyboardButton(text='🔙', callback_data='rent_number'))
        return markup

    def get_menu_time(self, service, country):
        markup = types.InlineKeyboardMarkup(row_width=2)

        number = self.get_service_info(service)

        for i in number[1].split(';'):
            i = i.split(':')
            if i[0] == country:
                markup.add(types.InlineKeyboardButton(text='🕐 4 час | %sр' % i[2],
                                                      callback_data='rent_time:%s:%s:4' % (
                                                      service, i[0])),

                           types.InlineKeyboardButton(text='🕓 24 часа | %sр' % i[3],
                                                      callback_data='rent_time:%s:%s:24' % (
                                                      service, i[0])),

                           types.InlineKeyboardButton(text='🕗 7 дней | %sр' % i[4],
                                                      callback_data='rent_time:%s:%s:168' % (
                                                      service, i[0])),
                           )
                markup.add(types.InlineKeyboardButton(text='🔙', callback_data='rent_service:%s' % (service)),)
                break

        return markup

    def get_service_info(self, service):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM rent_numbers WHERE service = "%s"' % service)
        number = cursor.fetchone()

        self.service_code = number[0]
        self.countries_and_prices = number[1]
        self.service_name = number[2]

        if number:
            return number[0], number[1], number[2]

    @staticmethod
    def get_list_numbers():
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM rent_numbers')
        numbers = cursor.fetchall()

        return numbers

    async def get_operators(self, service, country_code):
        self.get_service_info(service)

        operators = None

        for i in self.countries_and_prices.split(';'):
            i = i.split(':')
            if i[0] == country_code:
                operators = i[5].split(',')
                break

        return operators

    async def rent_number(self, bot, user_id, price, service, country, rent_time):
        try:
            user = User(user_id)
            operators = await self.get_operators(service, country)

            print(operators)

            chat_id = None
            text = None
            status = None

            for i in operators:

                operator = i

                if user.balance >= float(price):
                    print(config.config('api_smsactivate'), service, rent_time, operator, country, config.config('webhook_url'))

                    url = 'https://sms-activate.ru/stubs/handler_api.php?' \
                          'api_key=%s&' \
                          'action=getRentNumber&' \
                          'service=%s&' \
                          'rent_time=%s&' \
                          'operator=%s&' \
                          'country=%s&' \
                          'url=https://%s/webhook' % (config.config('api_smsactivate'),
                                                      service, rent_time, operator, country,
                                                      config.config('webhook_url'))

                    resp = requests.get(url)
                    resp = json.loads(resp.text)

                    status = resp['status']

                    if status == 'success':
                        user.update_balance(-float(price))

                        rent_id = resp['phone']['id']
                        end_date = resp['phone']['endDate']
                        number = resp['phone']['number']
                        buy_date = datetime.now()

                        self.write_logs(user_id, rent_id, end_date, number, price, service, country, buy_date)

                        self.get_service_info(service)

                        await bot.send_message(
                            chat_id=user_id,
                            text="""
❕ Вы успешно арендовали номер: +%s
🖥 Сервис: %s
⌛️ Дата окончания: %s
        """ % (number, self.service_name, end_date)
                        )

                        break
                    elif status == 'error':
                        try:
                            text = f'⚠️⚠️⚠️ Ошибка в аренде номеров: \n{resp}'

                            await bot.send_message(
                                chat_id=config.config('CHANNEL_ID2'),
                                text=text
                            )
                        except:
                            pass
                        
                        try:
                            error = resp['message']
                
                            if error == 'ACCOUNT_INACTIVE':
                                chat_id = user_id
                                text = ''
                            elif error == 'NO_BALANCE':
                                chat_id = config.config('admin_id_own').split(':')[0]
                                text = '⚠️⚠ Ошибка в аренде номеров: закончисля баланс на сайте'
                            elif error == 'BAD_SERVICE':
                                chat_id = config.config('admin_id_own').split(':')[0]
                                text = '⚠️⚠️⚠️ Ошибка в аренде номеров: неверный сервис, пиши @baggertt'
                            else:
                                chat_id = user_id
                                text = '🔺 Не обнаружено свободных номеров!'

                        except:
                            error = resp['msg']

                            chat_id = chat_id
                            text = error

            if status == 'error':
                try:
                    await bot.send_message(
                        chat_id=chat_id,
                        text=text
                    )
                except:
                    print('error msg rent rent')
        except Exception as e:
            chat_id = config.config('admin_id_own').split(':')[0]
            text = f'⚠️⚠️⚠️⚠️⚠️ Ошибка в аренде номеров: все пошло по пи%#е, пиши @baggertt\n{e}'

            await bot.send_message(
                chat_id=chat_id,
                text=text
            )


    @staticmethod
    def write_logs(user_id, rent_id, end_date, number, price, service, country, buy_date):
        conn, cursor = connect()

        cursor.execute('INSERT INTO active_rent VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (user_id,
                                                                                                            rent_id,
                                                                                                            end_date,
                                                                                                            number,
                                                                                                            price,
                                                                                                            service,
                                                                                                            country,
                                                                                                            buy_date))
        conn.commit()

        cursor.execute('INSERT INTO logs_rent VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")' % (user_id,
                                                                                                          rent_id,
                                                                                                          end_date,
                                                                                                          number,
                                                                                                          price,
                                                                                                          service,
                                                                                                          country,
                                                                                                          buy_date))
        conn.commit()

    def get_info_rent_number(self, rent_id):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM logs_rent WHERE rent_id = "%s"' % rent_id)
        info = cursor.fetchone()

        self.user_id = info[0]
        self.rent_id = info[1]
        self.end_date = info[2]
        self.number = info[3]
        self.price = info[4]
        self.service_code = info[5]
        self.country_code = info[6]
        self.buy_date = info[7]

        return info

    def get_country_name(self, service, country_code):
        print(country_code)
        self.get_service_info(service)

        for i in self.countries_and_prices.split(';'):
            i = i.split(':')
            if i[0] == country_code:
                self.country_name = i[1]

                return self.country_name

    def get_price(self, service, country_code, time):
        self.get_service_info(service)

        for i in self.countries_and_prices.split(';'):
            i = i.split(':')
            if i[0] == country_code:
                if int(time) == 4:
                    return float(i[2])
                elif int(time) == 24:
                    return float(i[3])
                elif int(time) == 168:
                    return float(i[4])

    def get_menu_my_rent_number(self, user_id):
        numbers = self.get_active_rent_number_user(user_id)

        markup = types.InlineKeyboardMarkup(row_width=2)

        for i in numbers:
            markup.add(types.InlineKeyboardButton(text=i[3],
                                                  callback_data='my_rent:%s' % i[1]))

        markup.add(types.InlineKeyboardButton(text='« Назад', callback_data='rent_back'), )

        return markup

    def get_info_for_rent_number(self, rent_id):

        self.get_info_rent_number(rent_id)
        self.get_country_name(self.service_code, self.country_code)
        self.get_service_info(self.service_code)

        all_message = self.get_all_message(rent_id)

        msg = ''
        number = 0
        for i in all_message:
            number += 1
            msg += '%s. \nОТ: %s\n ДАТА: %s\n СМС: %s\n\n' % (number, i[0], i[3], i[1])

        text = """
🖥 Сервис: %s
🏳️ Страна: %s
☎️ Номер: %s
⏳ Дата аренды: %s
⌛️ Дата окончания аренды: %s

📩 Сообщения: 
%s
        """ % (self.service_name, self.country_name, self.number, self.buy_date, self.end_date, msg)

        return text

    @staticmethod
    def get_all_message(rent_id):
        url = 'https://sms-activate.ru/stubs/handler_api.php?api_key=%s&action=getRentStatus&id=%s' % (config.config('api_smsactivate'), rent_id)
        resp = requests.get(url)

        resp = json.loads(resp.text)

        logs_sms = []

        if resp['status'] == 'success':
            for i in range(int(resp['quantity'])):
                data = resp['values'][str(i)]
                logs_sms.append([data['phoneFrom'],
                                data['text'],
                                data['service'],
                                data['date']])

        return logs_sms

    @staticmethod
    def get_active_rent_number_user(user_id):
        conn, cursor = connect()

        cursor.execute(f'SELECT * FROM active_rent WHERE user_id = "%s"' % user_id)
        numbers = cursor.fetchall()

        base = []

        for i in numbers:
            if datetime.fromisoformat(i[2]) < datetime.now():
                cursor.execute(f'DELETE FROM active_rent WHERE rent_id = "%s"' % i[1])
                conn.commit()
            else:
                base.append(i)

        return base

    @staticmethod
    def admin_get_rent():
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

        markup = types.InlineKeyboardMarkup(row_width=2)

        for i in base:
            markup.add(
                types.InlineKeyboardButton(text='%s | +%s' % (User(i[0]).username, i[3]), callback_data='rent_del:%s' % i[1])
            )

        return markup

    async def del_rent(self, rent_id, bot):
        self.get_info_rent_number(rent_id)

        conn, cursor = connect()

        cursor.execute(f'DELETE FROM active_rent WHERE rent_id = "%s"' % rent_id)
        conn.commit()

        url = 'https://sms-activate.ru/stubs/handler_api.php?api_key=%s&action=setRentStatus&id=%s&status=2' % (
            config.config('api_smsactivate'), rent_id)
        resp = requests.get(url)

        await bot.send_message(self.user_id, '⚠️ Аренда с номером +%s отменена, так как за 10 минут поступило 0 смс, на баланс начислено +%s рублей' % (self.number, self.price))
        User(self.user_id).update_balance(self.price)





Rent().create_table()
