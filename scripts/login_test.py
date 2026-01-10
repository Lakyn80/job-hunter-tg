# -*- coding: utf-8 -*-

import asyncio
from app.telegram.client import get_client

async def main():
    client = get_client()
    await client.start()
    me = await client.get_me()
    print(f'Přihlášen jako: {me.first_name} (@{me.username})')
    await client.disconnect()

asyncio.run(main())
