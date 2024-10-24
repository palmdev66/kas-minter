import socks
import asyncio
import os
import random

from telethon import TelegramClient
from config import api_id, api_hash, proxy as proxy_toggle

async def run():
    if proxy_toggle is True:
        proxy = await get_proxy()
    else:
        proxy = None

    sessions = await get_sessions()

    for session in sessions:
        await account_run(session, proxy)

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

async def account_run(session_name, proxy):
    client = TelegramClient(session_name, api_id, api_hash, proxy=proxy)
    await client.connect()
    me = await client.get_me()
    full_name = me.first_name + (' ' + me.last_name if me.last_name else '')

    print(f"[{full_name}] Logged in")

    for i in range(1, 10):
        bot_username = f'kspr_{i}_bot'
        print(f"[{full_name}] Cancelling at @{bot_username}..")

        messages = await client.get_messages(bot_username)
        if "Minting Progress" in messages[0].message:
            await messages[0].click(0)
        print(f"[{full_name}] Cancelled!\n\n")

if __name__ == '__main__':
    asyncio.run(run())