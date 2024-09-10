import json
import requests
import datetime as dt


def cyrillic_to_latin(text):
    cyrillic = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    latin = "abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA"
    trantab = str.maketrans(cyrillic, latin)
    return text.translate(trantab)


def send_sms(params):
    url = "https://smspro.nikita.kg/api/message"
    transaction_id = params['transaction_id']
    name = params['name']
    date = params['date']
    sale_sum = params['sale_sum']
    coupon_code = params['coupon_code']
    discount = params['discount']
    phone = params['phone']

    message = cyrillic_to_latin(
        f"{name}, благодарим за покупку {date} на {sale_sum}сомов! Ваш купон {coupon_code} на {discount} скидку на Игрушки уже с вами! ИДЕАЛЬНЫЕ ПОДАРКИ В БАЛАПАН!")
    print(message)
    xml_payload = """<?xml version="1.0" encoding="UTF-8"?>
    <message>
        <login>muratusakg</login>
        <pwd>Amiran</pwd>
        <id>{transaction_id}</id>
        <sender>Balapan Osh</sender>
        <text>{message}</text>
        <phones>
            <phone>{phone}</phone>
        </phones>
        <test>0</test>
    </message>
    """.format(
        transaction_id=transaction_id,
        message=message,
        phone=params['phone'],
    )

    print(xml_payload)
    headers = {
        'Content-Type': 'application/xml',
    }

    response = requests.post(url, headers=headers, data=xml_payload)

    if response.status_code == 200:
        print("Request successful. Response:")
        print(response.text)
    else:
        print("Request failed. Status Code:", response.status_code)
        print("Response:", response.text)


if __name__ == '__main__':
    # current second minute hour
    transaction_id = dt.datetime.now().strftime("%S%M%H%d%m%Y")[2:]
    params = {
        'transaction_id': transaction_id,
        'name': 'Тургунбай Алдакулов',
        'date': '22.12.2023',
        'sale_sum': '1000',
        'coupon_code': '0747',
        'discount': '20',
        'phone': '996770815300'
    }
    send_sms(params)
