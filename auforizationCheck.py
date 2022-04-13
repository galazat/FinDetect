import requests
from lxml import html, etree

URL_LOG = "https://online.akbars.ru/"
URL_MAIN = "https://www.akbars.ru/"

СardNumber = "4000793475525012"
Cvc2 = "456"
ExpMonth = "04"
ExpYear = "24"

s = requests.Session()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": "https://www.akbars.ru/",
    "Connection": "close",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}

result = requests.get(URL_MAIN, headers=headers)
print(result)
print(result.status_code)
print(result.reason)
print(result.elapsed.total_seconds())

print(result.headers)

#tree = html.fromstring(result.text)
#authURL = list(set(tree.xpath("//input[@name='authURL']/@value")))
#print(tree)

# headers = {
#     "Content-Length": "77",
#     "Sec-Ch-Ua": '"(Not(A:Brand";v="8", "Chromium";v="98"',
#     "Sec-Ch-Ua-Mobile": "?0",
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
#     "Content-Type": "application/json",
#     "Accept": "application/json, text/plain, */*",
#     "Sessiontoken": "null",
#     "Devicetoken": "null",
#     "Sec-Ch-Ua-Platform": '"Windows"',
#     "Origin": "https://online.akbars.ru",
#     "Sec-Fetch-Site": "same-site",
#     "Sec-Fetch-Mode": "cors",
#     "Sec-Fetch-Dest": "empty",
#     "Referer": "https://online.akbars.ru/",
#     "Accept-Encoding": "gzip, deflate",
#     "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
#     "Connection": "close"
# }

data = {
    "CardNumber": "4000793475525012",
    "Cvc2": "456",
    "ExpMonth": "04",
    "ExpYear": "24"
}

r1 = requests.get(URL_LOG, headers=result.headers)

print(r1)






# ПРИМЕР
#
#POST /AkbarsOnlineAuth/LoginInit HTTP/1.1
#Host: bankok.akbars.ru
#Cookie: _gcl_au=1.1.877179205.1637316138; iap.uid=87131818d1df45ee8fa0d50346ec272a; tmr_lvid=f73c8c3aef002cd254ed491ef58e5e44; tmr_lvidTS=1626287045868; _ym_uid=1626287046499142041; _ym_d=1637316139; _fbp=fb.1.1637316139054.1757935939; selectedCity=93b3df57-4c89-44df-ac42-96f05e9cd3b9; _gid=GA1.2.1013615373.1642497772; _ga_8YHHBELFH7=GS1.1.1642589429.7.0.1642589429.0; _ga=GA1.1.1903738750.1637316138; _ym_isad=2; tmr_reqNum=57
#Content-Length: 77
#Sec-Ch-Ua: " Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"
#Accept: application/json, text/plain, */*
#Content-Type: application/json;charset=UTF-8
#Sec-Ch-Ua-Mobile: ?0
#User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36
#Sec-Ch-Ua-Platform: "Windows"
#Origin: https://online.akbars.ru
#Sec-Fetch-Site: same-site
#Sec-Fetch-Mode: cors
#Sec-Fetch-Dest: empty
#Referer: https://online.akbars.ru/
#Accept-Encoding: gzip, deflate
#Accept-Language: ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7
#Connection: close
#
#{"Login":"dsvffd","Password":"POqix7FzXvBA3pWYWjXEUng01VE=","SaveLogin":true}