from connect import connect
from send_api import get_balance, get_balance2,get_balance_sputnik, get_balance_notisend, get_balance_smsfeedback, get_balance_getsms, get_balance_payok
from datetime import datetime


start = '''<b>💌 Филя:Sender - твой проводник в сфере отправки смс сообщений</b>

<b>Главное меню ⤵️</b>
'''


def select_audio(infa):
	text = f'''<b>✅ Аудио успешно выбрано!

📢 Введите номер телефона, на который вы хотите заказать звонок (только цифрами, например 79680330567).

💰 Стоимость розыгрыша - <code>{infa[6]}</code> рублей</b>'''
	return text

def api_text(userid, api,token, time):
	if str(api) == '0':
		token = 'Не доступно'
		time = 'None'
	if str(api) == '1':
		if str(time) == 'Навсегда':
			time = 'Навсегда'
		else:
			time = datetime.strptime(time, "%Y-%m-%d")

	text = f'''<b>⚜️ Подключение своих проектов

💡 API - это протокол взаимодействия между вашим ПО и нашим сервисом. Помогает автоматизировать процесс отправки SMS сообщений

🔑 Ваш API Token: <code>{token}</code>
⏳ Подписка до: <code>{time}</code>

{'❗️ Для получения доступа, необходима подписка' if str(api) == '0' else ''}
</b>'''

	return text

def shurl_infa(url_id):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_short_link where url_id = "{url_id}"')
	row = q.fetchone()
	text = f'''<b>ℹ️ Информация по сокращенной ссылке:

🔗 Длинная ссылка: <code>{row[1]}</code>
⚡️ Сокращенная ссылка: <code>{row[2]}</code>
⏳ Дата создания: <code>{row[6]}</code>

👁 Кол-во переходов: <code>{row[5]}</code></b>
	'''
	return text


def profile(userid):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_users where userid = "{userid}"')
	row = q.fetchone()
	q.execute(f'SELECT COUNT(id) FROM ugc_sms where userid = "{userid}" and status = "send"')
	success = q.fetchone()
	q.execute(f'SELECT COUNT(id) FROM ugc_sms where userid = "{userid}" and status = "nosend"')
	bad = q.fetchone()
	q.execute(f'SELECT COUNT(id) FROM ugc_sms where userid = "{userid}"')
	rowww = q.fetchone()
	text = f'''<b>👋 Привет, <a href="tg://user?id={userid}">счастливчик</a>

🆔 ID: <code>{userid}</code>
🌏 Имя отправителя: {row[13]}
💌 Отправлено смс: {rowww[0]}


💰 Баланс: {"%.2f" % float(row[2])}₽
</b>

'''
	return text


def free_thread():
	text = '''<b>🔥 Понижение стоимости звонка 🔥</b>

Хочешь понизить цену отправки звонка?
Добавь "<code>FilyaCallsBot</code>" в Свой ник телеграмма (имя/фамилия)

<i>Пока Ваш ник содержит эту "фразу", цена отправки снижена на 5 рублей</i>
	'''
	return text


def infa_voice(db_id):
	connection,q = connect()
	q.execute(f'SELECT * FROM ugc_sms where id = "{db_id}"')
	row = q.fetchone()
	price = row[5]
	text = f'''<b>✅ СМС отправлено ({row[3]})

⚡️ Текст сообщения: <code>{row[4]}</code>
🗓 Дата отправки: {row[5]}
💰 Стоимость: {row[7]} руб
</b>'''
	return text


def stata():
	try:
		connection,q = connect()
		q.execute(f'SELECT COUNT(userid) FROM ugc_users')
		count_userd = q.fetchone()[0]
		text = f'''<b>📊 Статистика

👤‍ Пользователей: {count_userd}
</b>'''
		return text
	except:
		pass


def admin_stata():
	connection,q = connect()
	q.execute(f'SELECT COUNT(userid) FROM ugc_users')
	count_users = q.fetchone()[0]
	q.execute(f'SELECT COUNT(id),SUM(summa) FROM ugc_buys where wallet = "qiwi" and buy LIKE "%buy%" or wallet = "banker"')
	statistika = q.fetchone()
	q.execute(f'SELECT COUNT(id),SUM(price) FROM ugc_sms where status = "send"')
	count_call = q.fetchone()

	q.execute(f'SELECT COUNT(id),SUM(price) FROM ugc_vk_chats where status = "1"')
	vk_infa = q.fetchone()
	q.execute(f'SELECT COUNT(id),SUM(price) FROM ugc_vk_chats')
	vk_infa_all = q.fetchone()

	q.execute(f'SELECT COUNT(id),SUM(summa) FROM ugc_buys where wallet = "btc" or wallet = "usdt" or wallet = "tron"')
	qiwi_infa = q.fetchone()
	q.execute(f'SELECT COUNT(id),SUM(summa) FROM ugc_buys where wallet = "payok"')
	banker_infa = q.fetchone()
	text = f'''<b>📊 Статистика проекта:

[ Основное ]
Всего пользователей: {count_users}

[ Деньги ]
Всего пополнений: {statistika[0]} ({statistika[1]}₽)
Отправлено смс: {count_call[0]} ({"%.2f" % count_call[1]}₽)
Отправлено ВК: {vk_infa[0]} ({vk_infa[1]}₽)
ВК запросов: {vk_infa_all[0]} ({vk_infa_all[1]}₽)

Пополнений Cryptobot: {qiwi_infa[0]} ({"%.2f" % qiwi_infa[1]}₽)
Пополнений PayOk: {banker_infa[0]} ({"%.2f" % banker_infa[1]}₽)

[ Балансы ]
GETSms: <code>{get_balance_getsms()}₽</code>
PayOk: <code>{get_balance_payok()}₽</code>

</b>'''
	return text




def check_info(phone, price):
	text = f'''<b>💡 Так, проверка данных:

📞 Номер: {phone}
🎙 Звук: прикреплен к сообщению
💰 Стоимость: {price} руб

👉 Для отправки звонка, введи: <code>Да</code></b>'''
	return text




text_my_text = '''💡 Синтез речи - способ преобразование твоего текста в голос

👫 На выбор есть два голоса:
Мужской и женский

🔗 Примеры находятся в прикрепленных файлах


ℹ️ Минимум 5 символов, максимум - 150

'''



def get_infa_send(phone, text, price):
	text_send = f'''<b>*️⃣  Проверка информации:

⚡️ Номер: <code>{phone}</code>
💌 Текст сообщения: <code>{text}</code>

💰 Стоимость отправки сообщения: {price}₽
</b>
	'''

	return text_send

def get_infa_send_svoi(phone, text, price, name):
	
	text_send = f'''<b>*️⃣  Проверка информации:

✍️ Отправитель: <code>{name}</code>
⚡️ Номер: <code>{phone}</code>
💌 Текст сообщения: <code>{text}</code>

💰 Стоимость отправки сообщения: {price}₽
</b>
	'''

	return text_send


rules = '''<b>Пользовательское Соглашение
Используя бота, Вы соглашаетесь с условиями данного соглашения.</b>

Пользователь обязуется:
- не передавать в пользование свою учетную запись и/или логин и пароль своей учетной записи третьим лицам
- не регистрировать учетную запись от имени или вместо другого лица за исключением случаев, предусмотренных законодательством РФ
- не размещать материалы рекламного, эротического, порнографического или оскорбительного характера, а также иную информацию, размещение которой запрещено или противоречит нормам действующего законодательства РФ

Администрация имеет право:
- без уведомления пользователей создавать, изменять и отменять правила
- ограничивать доступ пользователям без объяснения причин
- отказывать в технической поддержке без объяснения причин
- предоставить всю доступную информацию о Пользователе уполномоченным на то органам государственной власти в случаях, установленных законом


Данное Соглашение вступает в силу при любом использовании данного проекта.
Соглашение действует бессрочно.
Администрация оставляет за собой право в одностороннем порядке изменять данное соглашение по своему усмотрению.
Администрация не оповещает пользователей об изменении в Соглашении.


<b>Все интересующие вопросы задаются @FilyaAdmin</b>
'''