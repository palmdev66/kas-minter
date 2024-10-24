import socks
import asyncio
import os
import random

from telethon import TelegramClient
from config import api_id, api_hash, proxy as proxy_toggle

async def run(ticker, mint_count, gas):
    if proxy_toggle is True:
        proxy = await get_proxy()
    else:
        proxy = None
    sessions = await get_sessions()

    for session in sessions:
        await account_run(ticker, mint_count, session, proxy, gas)

async def get_sessions():
    sessions = []

    files = os.listdir("sessions")
    files = [f for f in files if os.path.isfile(os.path.join("sessions", f))]

    for file in files:
        session_name = "sessions/" + file.replace(".session", "")
        sessions.append(session_name)

    return sessions


async def get_proxy():
    with open('proxies.txt', 'r') as file:
        proxies = file.readlines()

    proxies = [proxy.strip() for proxy in proxies]
    random_proxy = random.choice(proxies)

    ipport, loginpass = random_proxy.split('@')
    login, password = loginpass.split(':')
    ip, port = ipport.split(':')

    proxy = (socks.SOCKS5, ip, port, login, password)

    return proxy

async def account_run(ticker, mint_count, session_name, proxy, gas):
    client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)
    await client.connect()
    me = await client.get_me()
    full_name = me.first_name + (' ' + me.last_name if me.last_name else '')

    print(f"[{full_name}] Logged in")

    for i in range(1, 10):
        bot_username = f'kspr_{i}_bot'
        print(f"[{full_name}] Minting at @{bot_username}..")

        await client.send_message(bot_username, '/mint')
        await asyncio.sleep(0.5)
        await client.send_message(bot_username, str(ticker))
        await asyncio.sleep(0.5)
        await client.send_message(bot_username, str(mint_count))
        await asyncio.sleep(0.5)
        await client.send_message(bot_username, str(gas))
        await asyncio.sleep(0.5)
        messages = await client.get_messages(bot_username)
        await messages[0].click(text='✅ Confirm')
        print(f"[{full_name}] Minting started!")

if __name__ == '__main__':
    count = 0
    ticker = input("Название тикера: ")
    while count < 20 or count > 100:
        count = int(input("Количество минтов от 20 до 100: "))
    gas = input("Выберите газ\n\n1. Low\n2. Medium\n3. High\n\nЛибо введите свое значение: ")
    if gas == "1":
        gas = "Low"
    elif gas == "2":
        gas = "Medium"
    elif gas == "3":
        gas = "High"
    asyncio.run(run(ticker, count, gas))