from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.jobs import router as jobs_router
from app.api.jobs_translate import router as jobs_translate_router
from app.telegram.client import connect_client, disconnect_client
from app.db.init_db import init_db

app = FastAPI(title="Job Hunter API")

app.include_router(health_router)
app.include_router(jobs_router)
app.include_router(jobs_translate_router)


@app.on_event("startup")
async def on_startup():
    print("🗄️ Inicializuji databázi")
    init_db()
    print("✅ Databáze připravena")

    print("🚀 FastAPI startup – spouštím Telegram klienta")
    await connect_client()
    print("✅ connect_client() dokončen")


@app.on_event("shutdown")
async def on_shutdown():
    print("🛑 FastAPI shutdown – odpojuji Telegram klienta")
    await disconnect_client()
