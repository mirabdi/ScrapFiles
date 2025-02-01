
from utils.common import write_to_json, read_json, calculate_time

stores = {
    "57c09c3d3ce7d59d048b46ca": {
        "name": "Балапан Ош №1",
        "city": "Osh",
    },
    "608931190bd70c702d0dbf6c": {
        "name": "Балапашка №2",
        "city": "Osh",
    },
    "6187a2f023e410447a333bd0": {
        "name": "Балапан Анар №4",
        "city": "Osh",
    },
    "6534e92e6b78a2722e0a1b13": {
        "name": "Балапан Фрунзенский №7",
        "city": "Osh",
    },
    "61fcfbe56fd83334d906684b": {
        "name": "Балапан Масалиева №5",
        "city": "Osh",
    },
    "60a1ffac0bd70c60721c5c99": {
        "name": "Балапан ЖА",
        "city": "Ja",
    },
    "637b680b51c3772c3270c50c": {
        "name": "Балапан Узген №6",
        "city": "Uzgen",
    },
    "667a67de8d522538ee0ba760": {
        "name": "OFF PRICE",
        "city": "Osh",
    },
    "smm": {
        "name": "smm",
        "city": "Osh",
    },
    "617be0fd23e410238456d59f": {
        "name": "Основной склад",
        "city": "Osh",
    },
    "66bf4c1c56115d41810faa97": {
        "name": "NestHome",
        "city": "Osh",
    }
}

emps = {
    "meridina": {
        "versions": ["Меридина", "меридина", "МЕРИДИНА", "меридин", "меридинаа"],
    },
    "nurzhan": {
        "versions": ["Нуржан", "нуржан", "НУРЖАН", "нуржанн"],
    },
    "tanzilya": {
        "versions": ["Танзиля", "танзиля", "ТАНЗИЛЯ", "танзиляа", "Танзилья", ],
    },
    "kyzburak": {
        "versions": ["Кызбурак стажер", "Кызбурак", "кызбурак", "КЫЗБУРАК", "кызбуракк"],
    },
    "gulsana": {
        "versions": ["Гулсана", "гулсана", "ГУЛСАНА", "гулсанаа"],
    },
    "gulnur": {
        "versions": ["Гулнур Б1", "Гулнур", "гулнур", "Гулнур стажер", "гулнурр"],
    },
    "kamilla": {
        "versions": ["Камилла стажер", "Камилла", "камилла", "Камилла стажер Б1", "камила", "Камила"],
    },
    "kanymgul": {
        "versions": ["Канымгул стажер Б1", "Канымгул", "Канымгул стажер", "канымгул"]
    },
    "elvira": {
        "versions": ["Эльвира стажер Б1", "Эльвира", "Эльвира стажер", "эльвира"],
    },
    "aiperi": {
        "versions": ["Айпери стажер Б1", "Айпери", "Айпери стажер", "айпери"],
    },
    "alsu": {
        "versions": ["Алсу стажер Б1", "Алсу", "АЛСУ", "Алсуу", "алсу"],
    },
    "zuura": {
        "versions": ["Зуура стажер Б4", "Зуура", "зуура", "ЗУУРА", "зура"],
    },
    "fatima": {
        "versions": ["Фатима стажер", "Фатима", "фатима", "ФАТИМА", "фатиима"],
    },
    "kelsinay": {
        "versions": ["Келсинай стажер", "Келсинай", "келсинай", "КЕЛСИНАЙ", "келсинайй"],
    },
    "alisa": {
        "versions": ["Алиса", "алиса", "АЛИСА", "алис", "алисаа"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "akzhibek": {
        "versions": ["Акжибек", "акжибек", "АКЖИБЕК", "акжибекк"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "akdaana": {
        "versions": ["Акдаана", "акдаана", "АКДААНА", "акдана", "АКДАНА", "Акдана"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "munara": {
        "versions": ["Мунара", "мунара", "МУНАРА"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "aidana": {
        "versions": ["Айдана", "айдана", "АЙДАНА", "айдвна", "fqlfyf"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "perishte": {
        "versions": ["Периште", "периште", "ПЕРИШТЕ"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "nuriza": {
        "versions": ["Нуриза", "нуриза", "НУРИЗА"],
        "store_id": "667a67de8d522538ee0ba760",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "uulkan": {
        "versions": ["Уулкан", "уулкан", "УУЛКАН", "улкан", "УУЛКАн", "УУлкан"],
        "store_id": "608931190bd70c702d0dbf6c",
        "store_name": "Балапашка №2",
        "city": "Osh"
    },
    "begimai": {
        "versions": ["Бегимай", "бегимай", "БЕГИМАЙ"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "symbat": {
        "versions": ["Сымбат", "сымбат", "СЫМБАТ", "сымибат"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "meerimai": {
        "versions": ["Мээримай", "мээримай", "МЭЭРИМАЙ", "ммэримай"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "akmaanai": {
        "versions": ["Акмаанай", "акмаанай", "АКМААНАЙ"],
        "store_id": "667a67de8d522538ee0ba760",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "aigul": {
        "versions": ["Айгүл", "айгул", "АЙГҮЛ", "Айгул", "айгүл", "АЙГУЛ", "айгуль"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "gulnaz": {
        "versions": ["Гүлназ", "гулназ", "ГҮЛНАЗ", "гүлназ", "Гүлназ", "ГУЛНАЗ", "Гулназ"],
        "store_id": "608931190bd70c702d0dbf6c",
        "store_name": "Балапашка №2",
        "city": "Osh"
    },
    "anar": {
        "versions": ["Анар", "анар", "АНАР"],
        "store_id": "608931190bd70c702d0dbf6c",
        "store_name": "Балапашка №2",
        "city": "Osh"
    },
    "dinara": {
        "versions": ["Динара", "динара", "ДИНАРА"],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    },
    "tansuluu": {
        "versions": ["Тансулуу", "тансулуу", "ТАНСУЛУУ", "тансулу", "тансулууу", "Тансулууу"],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    },
    "begimai_2": {
        "versions": ["Бема", "бема", "БЕМА", "Бегимай 2"],
        "store_id": "6534e92e6b78a2722e0a1b13",
        "store_name": "Балапан Фрунзенский №7",
        "city": "Osh"
    },
    "aizat": {
        "versions": ["Айзат", "айзат", "АЙЗАТ"],
        "store_id": "6534e92e6b78a2722e0a1b13",
        "store_name": "Балапан Фрунзенский №7",
        "city": "Osh"
    },
    "asida": {
        "versions": ["Асида", "асида", "АСИДА"],
        "store_id": "61fcfbe56fd83334d906684b",
        "store_name": "Балапан Масалиева №5",
        "city": "Osh"
    },
    "diana": {
        "versions": ["Диана", "диана", "ДИАНА", "дияна"],
        "store_id": "61fcfbe56fd83334d906684b",
        "store_name": "Балапан Масалиева №5",
        "city": "Osh"
    },
    "nurkyz": {
        "versions": ["Нуркыз", "нуркыз", "НУРКЫЗ", "нурыз"],
        "store_id": "61fcfbe56fd83334d906684b",
        "store_name": "Балапан Масалиева №5",
        "city": "Osh"
    },
    "aigerim": {
        "versions": ["Айгерим", "айгерим", "АЙГЕРИМ", "агерим"],
        "store_id": "667a67de8d522538ee0ba760",
        "store_name": "OFF PRICE",
        "city": "Osh"
    },
    "saida": {
        "versions": ["Саида", "саида", "САИДА"],
        "store_id": "667a67de8d522538ee0ba760",
        "store_name": "OFF PRICE",
        "city": "Osh"
    },
    "elnura": {
        "versions": ["Элнура", "элнура", "ЭЛНУРА", "эльнура"],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    },
    "aidana_jal": {
        "versions": ["Айдана", "айдана", "АЙДАНА", "Айдвна", "айданаа"],
        "store_id": "60a1ffac0bd70c60721c5c99",
        "store_name": "Балапан ЖА",
        "city": "Ja"
    },
    "shano": {
        "versions": ["Шано", "шано", "ШАНО", "шона"],
        "store_id": "60a1ffac0bd70c60721c5c99",
        "store_name": "Балапан ЖА",
        "city": "Ja"
    },
    "gulshan": {
        "versions": ["Гулшан", "гулшан", "ГУЛШАН"],
        "store_id": "60a1ffac0bd70c60721c5c99",
        "store_name": "Балапан ЖА",
        "city": "Ja"
    },
    "akmaral": {
        "versions": ["Акмарал", "акмарал", "АКМАРАЛ", "Марал", "марал", "csqvsr"],
        "store_id": "60a1ffac0bd70c60721c5c99",
        "store_name": "Балапан ЖА",
        "city": "Ja"
    },
    "guliza": {
        "versions": ["Гулиза", "гулиза", "ГУЛИЗА", "Гулиз", "гулиз", "гули", "гул", "гулимза"],
        "store_id": "637b680b51c3772c3270c50c",
        "store_name": "Балапан Узген №6",
        "city": "Uzgen"
    },
    "kanykei": {
        "versions": ["Каныкей", "каныкей", "КАНЫКЕЙ", "кани", "кании", "каныыы", "Канииии", "Каниии", "каниии", "канекей", "КАНЫКЕй"],
        "store_id": "637b680b51c3772c3270c50c",
        "store_name": "Балапан Узген №6",
        "city": "Uzgen"
    },
    "elzada": {
        "versions": ["Элзада", "элзада", "ЭЛЗАДА", "эльзада", "Эльзада", "ЭЛЬЗАДА", "эдьзада"],
        "store_id": "667a67de8d522538ee0ba760",
        "store_name": "OFF PRICE",
        "city": "Osh"
    },
    "aizhan": {
        "versions": ["Айжан", "айжан", "АЙЖАН", "fqfy"],
        "store_id": "60a1ffac0bd70c60721c5c99",
        "store_name": "Балапан ЖА",
        "city": "Ja"
    },
    "nadira": {
        "versions": ["Надира", "надира", "НАДИРА", "Нади", "нади", "НАДИ", "нАДИ", "надди", "надиии", "надии", "НАДИРа", "НАДИра"],
        "store_id": "637b680b51c3772c3270c50c",
        "store_name": "Балапан Узген №6",
        "city": "Uzgen"
    },
    "syimyk": {
        "versions": ["Сыимык", "сыимык", "СЫИМЫК", "сыймык", "Сыймык", "СЫЙМЫК", "csqvsr", "cыймык"],
        "store_id": "60a1ffac0bd70c60721c5c99",
        "store_name": "Балапан ЖА",
        "city": "Ja"
    },
    "alfina": {
        "versions": ["Альфина", "альфина", "АЛЬФИНА", "альфия", "альфинаонлайн"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "kunduz": {
        "versions": ["Кундуз", "кундуз", "КУНДУЗ"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "aizirek": {
        "versions": ["Айзирек", "айзирек", "АЙЗИРЕК"],
        "store_id": "57c09c3d3ce7d59d048b46ca",
        "store_name": "Балапан Ош №1",
        "city": "Osh"
    },
    "ayana": {
        "versions": ["Аяна", "аяна", "АЯНА", "fzyf", "аян"],
        "store_id": "60a1ffac0bd70c60721c5c99",
        "store_name": "Балапан ЖА",
        "city": "Ja"
    },
    "bermet": {
        "versions": ["Бермет", "бермет", "БЕРМЕТ", "берметт"],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    },
    "meerim": {
        "versions": ["Мээрим", "мээрим", "МЭЭРИМ", "ммэрим", "Меерим", "меерим", "МЕЕРИМ", "мееримм"],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    },
    "miraida": {
        "versions": ["Мираида", "мираида", "МИРАЙДА", "мирайд", "мирайдаа"],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    },
    "adelya": {
        "versions": ["Аделя", "аделя", "АДЕЛЯ", "аделяа"],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    },
    "gulida": {
        "versions": ["Гулида", "гулида", "ГУЛИДА", "гулид", "гулидаа"],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    },
    "hadicha": {
        "versions": ["Хадича", "хадича", "ХАДИЧА", "хадич", "хадичаа", 'Хатижа', 'хатижа', 'ХАТИЖА', 'хатижаа', 'хадиче'],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    },
    "aliza": {
        "versions": ["Ализа", "ализа", "АЛИЗА", "ализ", "ализаа"],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    },
    "tologon": {
        "versions": ["Тологон", "тологон", "ТОЛОГОН", "тологонн"],
        "store_id": "6187a2f023e410447a333bd0",
        "store_name": "Балапан Анар №4",
        "city": "Osh"
    }
}



def handle_sale(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    store = thing['from']['_id']
    client = thing['to']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    response = {
        'style': 'sales',
        'number': number,
        'cloudshop_id': cloudshop_id,
        'store': store,
        'date': date,
        'created': created,
        'client': client,
        'sum': round(thing['sum'], 2),
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = -item['qty']
        sum = item['sum']
        sub = item['sub']
        price = item['price']
        discount_sum = item['discount_sum']
        discount_percent = item['discount_percent']
        if thing['type'] == 'inventory':
            product = {
                'cloudshop_id': cloudshop_id,
                'quantity': quantity,
                'sum': abs(sum),
                'sub': abs(sub),
                'price': abs(price),
                'discount_sum': discount_sum,
                'discount_percent': discount_percent,
            }
        else:
            product = {
                'cloudshop_id': cloudshop_id,
                'quantity': abs(quantity),
                'sum': abs(sum),
                'sub': abs(sub),
                'price': abs(price),
                'discount_sum': discount_sum,
                'discount_percent': discount_percent,
            }
        products.append(product)
    response['positions'] = products
    return response


def handle_return_sale(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    store = thing['to']['_id']
    client = thing['from']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    response = {
        'style': 'return_sales',
        'number': number,
        'cloudshop_id': cloudshop_id,
        'store': store,
        'date': date,
        'created': created,
        'client': client,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = item['qty']
        sum = item['sum']
        sub = item['sub']
        price = item['price']
        discount_sum = item['discount_sum']
        discount_percent = item['discount_percent']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'sum': abs(sum),
            'sub': abs(sub),
            'price': abs(price),
            'discount_sum': discount_sum,
            'discount_percent': discount_percent,
        }
        products.append(product)
    response['positions'] = products
    return response


def handle_purchase(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    store = thing['to']['_id']
    supplier = thing['from']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    response = {
        'style': 'purchases',
        'number': number,
        'cloudshop_id': cloudshop_id,
        'store': store,
        'supplier': supplier,
        'date': date,
        'created': created,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = item['qty']
        sum = item['sum']
        sub = item['sub']
        price = item['price']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'sum': abs(sum),
            'sub': abs(sub),
            'price': abs(price),
        }
        products.append(product)
    response['positions'] = products
    return response


def handle_return_purchase(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    store = thing['from']['_id']
    supplier = thing['to']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    response = {
        'style': 'return_purchases',
        'number': number,
        'cloudshop_id': cloudshop_id,
        'store': store,
        'supplier': supplier,
        'date': date,
        'created': created,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = -item['qty']
        sum = item['sum']
        sub = item['sub']
        price = item['price']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'sum': abs(sum),
            'sub': abs(sub),
            'price': abs(price),
        }
        products.append(product)
    response['positions'] = products
    return response


def handle_movement(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    to_store = thing['to']['_id']
    from_store = thing['from']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    response = {
        'style': 'movements',
        'number': number,
        'cloudshop_id': cloudshop_id,
        'from_store': from_store,
        'to_store': to_store,
        'date': date,
        'created': created,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = item['qty']
        sum = item['sum']
        sub = item['sub']
        price = item['price']
        discount_sum = item['discount_sum']
        discount_percent = item['discount_percent']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'price': abs(price),
        }
        products.append(product)
    response['positions'] = products
    return response


def handle_change(thing):
    number = thing['number']
    cloudshop_id = thing['_id']
    store = thing['from']['_id']
    date = calculate_time(thing['date'])
    created = calculate_time(thing['created'])
    sub_style = thing.get('sub_type', 'correction')
    response = {
        'style': 'changes',
        'sub_style': sub_style,
        'number': number,
        'cloudshop_id': cloudshop_id,
        'store': store,
        'date': date,
        'created': created,
    }
    products = []
    for item in thing['products']:
        cloudshop_id = item['_id']
        quantity = item['qty']
        price = item['price']
        product = {
            'cloudshop_id': cloudshop_id,
            'quantity': abs(quantity),
            'price': abs(price),
        }
        products.append(product)
    response['positions'] = products
    return response


def handle(thing):
    response = thing
    print(thing['products'] is list)
    return response
