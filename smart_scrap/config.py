COMMON_URL = "https://web.cloudshop.ru/proxy/"

URLS = ["http://127.0.0.1:8000", "http://127.0.0.1:8001",
        "http://127.0.0.1:8002", "http://127.0.0.1:8003", "https://balapan.herokuapp.com", "https://cloudshop-855e74fca5e5.herokuapp.com"]
SERVER_MODE = 0

BASE_URL = URLS[SERVER_MODE]

COMMON_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9,ru;q=0.8,kk;q=0.7',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.2.450600340.1695317847; _ym_uid=1695317848264839686; _ym_d=1695317848; company_id=57c09c3b3ce7d59d048b46c9; carrotquest_device_guid=f7092372-16e0-4368-a14c-8c12e0b83ada; _gid=GA1.2.1613118061.1707974525; _ym_isad=1; carrotquest_realtime_services_transport=wss; connect.sid=s%3AkOXOe-0j9OCCNK4byEGQd1u3cak-seUS.UQob31SKyeWJJqEiEmIykxxFkNSrwMAeTVfhrQMc8bQ; carrotquest_session=kxgkf89gzdgcle3engccntnpb4ymmtin; carrotquest_session_started=1; ls.auth=true; carrotquest_uid=1641479624259013120; carrotquest_auth_token=user.1641479624259013120.25978-ccb24a76cf1dc17d8b27697209.5375aa88c76d04de455c4395b66c53fbcd6e7dd799e73be9; carrotquest_jwt_access=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdHQiOiJhY2Nlc3MiLCJleHAiOjE3MDc5NzgzNDgsImlhdCI6MTcwNzk3NDc0OCwianRpIjoiMzlhODY0MTAxYTgwNDgxMThkYmIyOWNjMmI5YzA2NmMiLCJhY3QiOiJ3ZWJfdXNlciIsImN0cyI6MTcwNzk3NDc0OCwicm9sZXMiOlsidXNlci4kYXBwX2lkOjI1OTc4LiR1c2VyX2lkOjE2NDE0Nzk2MjQyNTkwMTMxMjAiXSwiYXBwX2lkIjoyNTk3OCwidXNlcl9pZCI6MTY0MTQ3OTYyNDI1OTAxMzEyMH0.uQcjVGgpVsMirLVwuYnetsoRd_MJ4h6netnwIpySX3o; _dc_gtm_UA-59354684-1=1; _ga_BQMWMKX4HT=GS1.2.1707974524.167.1.1707974804.60.0.0',
    'Host': 'web.cloudshop.ru',
    'If-None-Match': 'W/"1239-kBn7BT9pCSbK4XzxZa9Moezg/bw"',
    'Referer': 'https://web.cloudshop.ru/card/catalog/list',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'key': 'null',
    'sec-ch-ua': '"Not A(Brand";v="99", "Google Chrome";v="121", "Chromium";v="121"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


# COMMON_HEADERS = {
#     "Accept": "application/json, text/plain, */*",
#     "Accept-Encoding": "gzip, deflate, br",
#     "Accept-Language": "en-US,en;q=0.9,ru;q=0.8,kk;q=0.7",
#     "Connection": "keep-alive",
#     "Cookie": "carrotquest_device_guid=4d739ebd-ac37-4966-9a01-639ee29cf01b; _ym_uid=1687568728177002426; _ym_d=1687568728; carrotquest_uid=374621182109944238; carrotquest_auth_token=user.374621182109944238.25978-ccb24a76cf1dc17d8b27697209.5815c6a485b8b173cecb09b4767e5b9f90165c0b5cca9075; connect.sid=s%3AEgvmZ3Ww4lMSHtjL_edSDRT7si6FVp9a.IACKssciYCJRSLpCn911uaYDP4dIYns%2FfHmae77Cw7M; _ga=GA1.2.1351731221.1691602588; ls.auth=true; company_id=57c09c3b3ce7d59d048b46c9; _gid=GA1.2.113564974.1692685161; _dc_gtm_UA-59354684-1=1",
#     "Host": "web.cloudshop.ru",
#     "Referer": "https://web.cloudshop.ru/",
#     "Sec-Fetch-Dest": "empty",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Site": "same-origin",
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
#     "key": "null",
#     "sec-ch-ua": "\"Chromium\";v=\"116\", \"Not)A;Brand\";v=\"24\", \"Google Chrome\";v=\"116\"",
#     "sec-ch-ua-mobile": "?0",
#     "sec-ch-ua-platform": "\"Linux\""
# }