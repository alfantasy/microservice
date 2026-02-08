import asyncio
import os
import httpx
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Device Manager Test")

# Ссылка на ваше приложение (нужно будет добавить в Environment Variables на Render)
# Например: https://my-app.onrender.com
APP_URL = os.getenv("RENDER_EXTERNAL_URL")

@app.get("/")
async def root():
    return {
        "status": "online",
        "port": 59000,
        "note": "Backward compatibility test for PC/Android"
    }

@app.on_event("startup")
async def startup_event():
    # Запускаем фоновую задачу "не засыпать"
    asyncio.create_task(keep_alive())

async def keep_alive():
    """Функция для пинга самого себя, чтобы сервер не уходил в спячку"""
    if not APP_URL:
        print("Внимание: RENDER_EXTERNAL_URL не задан. Авто-пинг невозможен.")
        return

    async with httpx.AsyncClient() as client:
        while True:
            await asyncio.sleep(300)  # Пауза 5 минут (300 секунд)
            try:
                # Пингуем главную страницу
                response = await client.get(APP_URL)
                print(f"Self-ping status: {response.status_code}")
            except Exception as e:
                print(f"Self-ping failed: {e}")

if __name__ == "__main__":
    # Фиксируем порт 59000
    uvicorn.run(app, host="0.0.0.0", port=59000)
