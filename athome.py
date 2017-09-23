import os
import time

import requests


HEADERS = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36',
}

DATA = {
    'username': os.environ['ATHOME_LOGIN'],
    'password': os.environ['ATHOME_PASSWORD'],
    'submit.htm?login.htm': 'Send'
}


def auth(session, headers, data):
    response = session.post('http://192.168.0.1/login.cgi', headers=headers, data=data)
    return response


while True:
    try:
        with requests.Session() as s:
            auth(s, headers=HEADERS, data=DATA)
    except requests.exceptions.ConnectionError:
        continue
    else:
        break

response = s.get('http://192.168.0.1/wlstatbl.htm')
print(response.text)

