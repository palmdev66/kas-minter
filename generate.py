import asyncio
from telethon import TelegramClient
from config import api_id, api_hash

async def main():
    while True:
        phone_number = input("\n\n----\n\nPhone number: ")
        phone_number = phone_number.replace("+", "")
        client = TelegramClient(f"sessions/{phone_number}", api_id, api_hash)
        await client.start(phone=phone_number)
        print(f"Generated session: /sessions/{phone_number}.session")

if __name__ == '__main__':
    asyncio.run(main())