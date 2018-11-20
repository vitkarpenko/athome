import os
import random
import telnetlib
from time import sleep

import vk_api

ROUTER_LOGIN = os.getenv('ROUTER_LOGIN').encode()
ROUTER_PASSWORD = os.getenv('ROUTER_PASSWORD').encode()

VK_LOGIN = os.getenv('VK_LOGIN')
VK_PASSWORD = os.getenv('VK_PASSWORD')

MOM_VK_ID = 187_822_398

NAMES_TO_MAC_AND_CUTIES = {
    'vitaly': ('f4:f5:db:c8:09:b1', ['Виталик']),
    'veva': (
        'f0:76:6f:a2:38:ef',
        [
            'Биба',
            'Капуста',
            'Суслик',
            'Капуста',
            'Батутик',
            'Ушастик',
            'Припузинка',
            'Сплюшка',
            'Тутурушка',
            'Вева',
            'Верочка',
        ],
    ),
}


def telnet_login():
    telnet = telnetlib.Telnet('192.168.1.1')
    telnet.read_until(b'Login:')
    telnet.write(ROUTER_LOGIN + b"\n")
    telnet.read_until(b'Password:')
    telnet.write(ROUTER_PASSWORD + b"\n")
    return telnet


def vk_login():
    vk_session = vk_api.VkApi(VK_LOGIN, VK_PASSWORD)
    vk_session.auth()
    return vk_session.get_api()


def show_associations(telnet):
    telnet.write(b"show associations\n")
    sleep(1)
    return telnet.read_very_eager().decode()


def send_notification(vk, name, old_state, new_state):
    cutie = random.choice(NAMES_TO_MAC_AND_CUTIES[name][1])

    if old_state == new_state:
        return

    if old_state == False and new_state == True:
        message = f'{cutie} вернулся домой :)'
    elif old_state == True and new_state == False:
        message = f'{cutie} куда-то попёрся...'
    elif old_state == None:
        message = f'{cutie} дома.' if new_state else f'{cutie} где-то шлындает.'
    vk.messages.send(message=message, user_id=MOM_VK_ID)


def main():
    vk = vk_login()
    telnet = telnet_login()
    athome = {name: None for name in NAMES_TO_MAC_AND_CUTIES}
    while True:
        associations = show_associations(telnet)
        for name in NAMES_TO_MAC_AND_CUTIES:
            old_state = athome[name]
            new_state = NAMES_TO_MAC_AND_CUTIES[name][0] in associations
            send_notification(vk, name, old_state, new_state)
            athome[name] = new_state
        sleep(5)


if __name__ == "__main__":
    main()
