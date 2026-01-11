import asyncio
import pytest

from app.telegram.client import get_client


pytest.skip(
    "Login test je ruční utilita, ne automatický test",
    allow_module_level=True,
)


async def main():
    client = get_client()
    await client.start()
    print("OK – Telegram client přihlášen")


if __name__ == "__main__":
    asyncio.run(main())
