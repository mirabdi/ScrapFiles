# config.py

COMMON_URL = "https://web.cloudshop.ru/proxy/"

URLS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",
    "http://127.0.0.1:8003",
    "https://balapan.herokuapp.com",
    "http://192.168.0.101:8000",
    "https://cloudshop-855e74fca5e5.herokuapp.com"
]
SERVER_MODE = 4

BASE_URL = URLS[SERVER_MODE]




COMMON_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Cookie": "connect.sid=s%3ACCbsN_yXDmHY5-xoiF_rrt1soQ8DcjYU.oca9fsL0wQPzj0IV6MNEx9YcVDUnIosvGndwg2rqWT8; _ga=GA1.2.542887636.1724217881; _gid=GA1.2.1595331544.1724217881; _dc_gtm_UA-59354684-1=1; _ym_uid=17242178815680849; _ym_d=1724217881; _ym_isad=2; _ga_BQMWMKX4HT=GS1.2.1724217881.1.0.1724217881.60.0.0; carrotquest_session=71gemiz3q7un97wth19swg3bkx8luvbu; carrotquest_session_started=1; carrotquest_device_guid=245a30b4-e6d7-4234-996c-4e653b55bd6c; carrotquest_realtime_services_transport=wss; ls.auth=true; company_id=57c09c3b3ce7d59d048b46c9; carrotquest_uid=374621182109944238; carrotquest_auth_token=user.374621182109944238.25978-ccb24a76cf1dc17d8b27697209.50a147af9b5c00121e4cae2a3c6dd8086f88530d9b847efb; carrotquest_realtime_services_key=",
    "Host": "web.cloudshop.ru",
    "Referer": "https://web.cloudshop.ru",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "Key": "null",
    "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"99\", \"Google Chrome\";v=\"127\", \"Chromium\";v=\"127\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\""
}


# COMMON_HEADERS = {
#     "Accept": "application/json, text/plain, */*",
#     "Accept-Encoding": "gzip, deflate, br, zstd",
#     "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
#     "Connection": "keep-alive",
#     "Content-Length": "297",
#     "Content-Type": "application/json;charset=UTF-8",
#     "Cookie": "_ga=GA1.2.1039414880.1703580179; _ym_uid=1703580181588918438; carrotquest_device_guid=afd99a2a-7b51-4d96-ad58-9e9acd87ac1b; _ga=GA1.3.1039414880.1703580179; _ga_BQMWMKX4HT=GS1.3.1707787592.7.1.1707787619.33.0.0; _ym_d=1720252065; company_id=66bddcb6ef3d842b8d5f93f7; connect.sid=s%3AMY2NMqj8nP7GTnJ8puT6eDdPJrgjD4oN.O3TBRT3zhdLmHn7j9CaH%2Bo4FvzCRHtOO%2Bij6ldsXON4; ls.auth=true; carrotquest_uid=1788970626120158197; carrotquest_auth_token=user.1788970626120158197.25978-ccb24a76cf1dc17d8b27697209.2d9d59b00132f59170b5646aee20327514a30808f0eb43b7; _gid=GA1.2.2038183748.1725684541; _ym_isad=1; carrotquest_realtime_services_transport=wss; carrotquest_hide_all_unread_popups=true; _dc_gtm_UA-59354684-1=1; _ga_BQMWMKX4HT=GS1.2.1725749148.36.1.1725750149.60.0.0; carrotquest_session=068zre9oagkym11c3g4l3caefsu619v5; carrotquest_session_started=1",
#     "Host": "web.cloudshop.ru",
#     "Origin": "https://web.cloudshop.ru",
#     "Referer": "https://web.cloudshop.ru/card/clients/m/clients/add",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
#     "Key": "null",
#     "Sec-Ch-Ua": "\"Chromium\";v=\"128\", \"Not;A=Brand\";v=\"24\", \"Microsoft Edge\";v=\"128\"",
#     "Sec-Ch-Ua-Mobile": "?0",
#     "Sec-Ch-Ua-Platform": "\"Windows\""
# }
