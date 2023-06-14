# -*- coding: utf-8 -*-
from flask import Flask, request
from utils.mydb import *
import random


class WebHook:

    def run(self):
        app = Flask(__name__)

        @app.route("/", methods=['GET', 'POST'])
        def test():
            return '/'

        @app.route("/webhook", methods=['GET', 'POST'])
        def index():
            data = request.json

            rent_id = data['rentId']
            phone_from = data['sms']['phoneFrom']
            sms_text = data['sms']['text']
            sms_date = data['sms']['date']
            sms_id = data['sms']['smsId']

            self.logs_sms(rent_id, phone_from, sms_text, sms_id, sms_date)
            return 'info'

        app.run(port=5678)

    @staticmethod
    def logs_sms(rent_id, phone_from, sms_text, sms_id, sms_date):
        conn, cursor = connect()

        cursor.execute('INSERT INTO logs_sms VALUES ("%s", "%s", "%s", "%s", "%s")' % (rent_id,
                                                                                       phone_from,
                                                                                       sms_text,
                                                                                       sms_id,
                                                                                       sms_date))
        conn.commit()

        cursor.execute('INSERT INTO temp_sms VALUES ("%s", "%s", "%s", "%s", "%s", "%s")' % (
            rent_id, phone_from, sms_text, sms_id, sms_date, random.randint(0, 999999999)))
        conn.commit()


WebHook().run()

