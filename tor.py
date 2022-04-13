
import requests

proxy = {
    'http': 'socks5://127.0.0.1:9050',
    'https': 'socks5://127.0.0.1:9050'
}

url = ""

r = requests.get(url, proxies=proxy)