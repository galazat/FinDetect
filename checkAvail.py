import requests

def get_status(url):
    try:
        print ('Попытка подключения...')
        response = requests.head(url, timeout=5)
        status_code = response.status_code
        reason = response.reason
        response_time = response.elapsed.total_seconds()
    except requests.exceptions.ConnectionError:
         status_code = '000'
         reason = 'Сайт не доступен'
         response_time = 'нет ответа'
    website_status = (status_code, reason,  response_time)
    return website_status


names = ['www.insanelymac']
top_level_domain = 'com'
protocol = 'https'

for name in names:
    site = '{}://{}.{}'.format(protocol, name, top_level_domain)
    website_status = get_status(site)
    print (site)
    print ( 'Код:', website_status[0], '| Статус:', website_status[1], '| Время ответа:',website_status[2])
    print ("")
    if website_status[2] > 1.5:
        print ('Угроза ddos')
        
# недоступный сайт: https://www.thepythoncode.com/article/extracting-domain-name-information-in-python
# заюзать whois
# пощупать Nagios
