import time
from json.decoder import JSONDecodeError

import pytest
import allure
import json
import requests
import uuid
import random
from hamcrest import *
# from jsonschema import validate
from allure_commons.types import AttachmentType
from hamcrest import *
from datetime import datetime, timedelta
from _configs.urls import URLs
from pytest import mark as m
from requests_toolbelt import MultipartEncoder
from websocket import create_connection


def my_request(method: str, url: str, payload):
    """Выполнить запрос.
       Прикрепить status_code и body
       Вернуть code и body"""

    ws_connect()
    pytest.last_message_id = uid()
    payload['id'] = pytest.last_message_id
    payload = json.dumps(payload)

    files = {'payload': (None, payload)}
    boundary = '----WebKitFormBoundaryytJKpNE9EfrP1bfJ'
    m = MultipartEncoder(fields=files, boundary=boundary)

    response = requests.request(
        method,
        url,
        headers={"Content-Type": m.content_type},
        data=m)

    allure.attach(str(response.request.body.fields['payload'][1]), name='Request body', attachment_type=AttachmentType.JSON)
    allure.attach("[" + response.request.method + "] " + response.url,
                  name='Response status : ' + str(response.status_code) + ' ' + response.reason,
                  attachment_type=AttachmentType.TEXT)
    allure.attach(response.text, name='Response body', attachment_type=AttachmentType.JSON)

    if pytest.my_log:
        print("\n\n" + datetime.now().strftime('%H:%M:%S.%f')[:-3] + " HTTP ----->: " + response.request.method)
        print(url)
        if response.request.body:
            print("body:")
            print(json.dumps(json.loads(str(response.request.body.fields['payload'][1])), sort_keys=True, indent=4))

        print("\n" + datetime.now().strftime('%H:%M:%S.%f')[:-3] + " HTTP <-----:")
        print("code: " + str(response.status_code))
        print("body:")

        try:
            print(json.dumps(json.loads(response.text), sort_keys=True, indent=4))
        except JSONDecodeError:
            print(response.text)

        print("\n")

    return response


# def get_json_schema_from_file(file_name):
#     BASE_PATH = "/Users/pletnev/GitHub/RuBike/"
#     with open(BASE_PATH + file_name, 'r') as f:
#         schema_data = f.read()
#     return json.loads(schema_data)


# def assert_valid_schema(data, schema_file):
#     """ Checks whether the given data matches the schema """
#     return validate(data, schema_file)


def assert_response(response, status_code, matcher):
    assert_that(response.status_code, equal_to(status_code))

    try:
        response_body = json.loads(response.text)
    except ValueError:
        response_body = response.text

    assert_that(response_body, matcher)


# def assert_response_schema(response, status_code, schema_file):
#     assert_that(response.status_code, equal_to(status_code))
#
#     try:
#         response_body = json.loads(response.text)
#         return validate(response_body, schema_file)
#     except ValueError:
#         print("ValueError")


def uid():
    return str(uuid.uuid4())


def ts():
    return int(round(time.time() * 1000))


class MyRandom:

    @staticmethod
    def phone():
        phone = ''.join([random.choice(list('123456789')) for x in range(random.randint(7, 7))])
        def_code = ['900', '901', '902']
        return '7' + str(random.choice(def_code)) + phone

    @staticmethod
    def incorrect_phone():
        phone = ''.join([random.choice(list('123456789')) for x in range(random.randint(7, 7))])
        return phone

    @staticmethod
    def short_phone():
        phone = ''.join([random.choice(list('123456789')) for x in range(random.randint(9, 9))])
        return '7'+phone

    @staticmethod
    def int_number(randint=2):
        phone = ''.join([random.choice(list('123456789')) for x in range(random.randint(randint, randint))])
        return int(phone)

    @staticmethod
    def long_phone():
        phone = ''.join([random.choice(list('123456789')) for x in range(random.randint(11, 11))])
        return '7'+phone

    @staticmethod
    def ru_string(long):
        return ''.join([random.choice(list('йцукенгшщзхъэждлорпавыфячсмитьбю')) for x in range(random.randint(long, long))])

    @staticmethod
    def en_string(long):
        return ''.join([random.choice(list('qwertyuioplkjhgfdsazxcvbnm')) for x in range(random.randint(long, long))])

    @staticmethod
    def symbol(long):
        return ''.join([random.choice(list('!"№;%:?*()_+=`~;:><')) for x in range(random.randint(long, long))])

    @staticmethod
    def ru_message(randint=1):
        return MyRandom.ru_string(MyRandom.int_number(randint)) + MyRandom.symbol(randint) + ' ' + MyRandom.ru_string(MyRandom.int_number(randint)) + MyRandom.symbol(randint) + ' ' + MyRandom.ru_string(MyRandom.int_number(randint)) + MyRandom.symbol(randint)


def get_reply():
    ws = ws_connect()
    ws.settimeout(3.0)
    mess = ws.recv()
    mess = json.loads(str(mess))
    mess_to_return = []

    if pytest.my_log:
        print("\nWSS <-----:")
        print(json.dumps(mess, sort_keys=True, indent=4))

    allure.attach(str(mess), name='Response body', attachment_type=AttachmentType.JSON)

    for m in mess:
        if m['replyToSender'] == pytest.session_id:
            if m['replyToMessage'] == pytest.last_message_id:
                if 'keyboard' in m:
                    mess_to_return.append({"id": m['id'], "text": m['text'], "buttons": m['keyboard']['buttons']})
                else:
                    mess_to_return.append({"id": m['id'], "text": m['text']})

    if len(mess_to_return) == 1:
        mess_to_return = mess_to_return[0]

    return mess_to_return


def ws_connect():
    if pytest.ws_connect is None or pytest.ws_connect.connected == False:
        pytest.ws_connect = create_connection(URLs.wss_widget+"/"+pytest.service_id+"/"+pytest.session_id+"/ws/"+pytest.ws_session_id)
    return pytest.ws_connect
