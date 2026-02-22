# config.py

COMMON_URL = "https://web.cloudshop.ru/proxy/"

URLS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8001",
    "http://127.0.0.1:8002",    
    "http://127.0.0.1:8003",
    "https://balapan.herokuapp.com",
    "http://172.30.1.44:8000",
    "http://192.168.0.103:8000",
    "https://cloudshop-855e74fca5e5.herokuapp.com"
]   
SERVER_MODE = 4
BASE_URL = URLS[SERVER_MODE]
COMMON_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
    "Connection": "keep-alive",
    "Cookie": "_ga=GA1.2.1039414880.1703580179; _ym_uid=1703580181588918438; _ym_d=1736644519; __stripe_mid=5b5d7f5c-201b-4cda-9aa9-43cde86ec8bb61a05c; _ga_BQMWMKX4HT=GS1.2.1738407257.47.0.1738407257.60.0.0; carrotquest_device_guid=c80bc75c-e06a-40af-acad-a400668e7277; connect.sid=s%3AXl4UYNRafGaqqUdsr-dxVNaqfOK7dLkU.o8h01ZMx85Pe6IFgBgJyOm9jBSpMn68e%2F0wyPhpbL3w; ls.auth=true; company_id=57c09c3b3ce7d59d048b46c9; carrotquest_session=hu1ag1z12moz41nstzoc3dcytalf8qxz; carrotquest_session_started=1; carrotquest_realtime_services_transport=wss; carrotquest_uid=374621182109944238; carrotquest_auth_token=user.374621182109944238.25978-ccb24a76cf1dc17d8b27697209.5d88499b35db234293b29015dd8bf2f15da1439954847890; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3NjM2OTYzNTQsImlhdCI6MTc2MzY5Mjc1NCwianRpIjoiMGZmN2Y2NmNkOTE4NDE0MGI5NGFhNWI2NTcyMTdhN2QiLCJhY3QiOiJ3ZWJfdXNlciIsInJvbGVzIjpbInVzZXIuJGFwcF9pZDoyNTk3OC4kdXNlcl9pZDoyNTk3OCIsInVzZXIuJGFwcF9pZDoyNTk3OC4kdXNlcl9pZDoyMTA5Nzg2MzcyNjcwNzUzNjQ0IiwidXNlci4kYXBwX2lkOjI1OTc4LiR1c2VyX2lkOjIxMDk4Mjc4MTI2MDM5ODg3NjYiLCJ1c2VyLiRhcHBfaWQ6MjU5NzguJHVzZXJfaWQ6MjExMDA3OTQ1MTkzNjA2NjAyMiIsInVzZXIuJGFwcF9pZDoyNTk3OC4kdXNlcl9pZDoyMTEwMDA2NDA2OTk5NDQ0MzA0IiwidXNlci4kYXBwX2lkOjI1OTc4LiR1c2VyX2lkOjIxMTA0NDU4Njk2Mzg2MTczMzciLCJ1c2VyLiRhcHBfaWQ6MjU5NzguJHVzZXJfaWQ6MjEwOTg2NjU3Mzk4NzU4MDM2MiIsInVzZXIuJGFwcF9pZDoyNTk3OC4kdXNlcl9pZDoyMTA5OTk5ODQ2NzgwODMyMDQ3IiwidXNlci4kYXBwX2lkOjI1OTc4LiR1c2VyX2lkOjIxMDk4MjY4NzgxOTY5NDI5NzQiLCJ1c2VyLiRhcHBfaWQ6MjU5NzguJHVzZXJfaWQ6MjExMDQzNTYxMDY4MTQxMTcyMSIsInVzZXIuJGFwcF9pZDoyNTk3OC4kdXNlcl9pZDoyMTA5Njg4OTIxMDYyMzc3NjA1Il0sImFwcF9pZCI6MjU5NzgsInVzZXJfaWQiOjM3NDYyMTE4MjEwOTk0NDIzOH0.mtK5YDM8lOs1o19knFvJfqg-38EBUIBai7ms5g6d2cE",
    "Host": "web.cloudshop.ru",
    "Referer": "https://web.cloudshop.ru/card/supplier",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36 Edg/142.0.0.0",
    "Key": "null",
    "Sec-Ch-Ua": "\"Chromium\";v=\"142\", \"Microsoft Edge\";v=\"142\", \"Not_A Brand\";v=\"99\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\""
}




