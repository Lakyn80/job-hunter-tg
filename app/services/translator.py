import os
import httpx

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

if not DEEPSEEK_API_KEY:
    raise RuntimeError("Chybí DEEPSEEK_API_KEY v .env")

API_URL = "https://api.deepseek.com/chat/completions"


async def translate_to_cs(text: str) -> str:
    if not text.strip():
        return ""

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "system",
                "content": "Jsi překladač. Přelož text do češtiny. Neodpovídej ničím jiným než překladem."
            },
            {
                "role": "user",
                "content": text
            }
        ],
        "temperature": 0.2,
    }

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        data = resp.json()

    return data["choices"][0]["message"]["content"].strip()
