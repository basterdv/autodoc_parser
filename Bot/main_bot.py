import asyncio
import logging
from aiogram import Bot, Dispatcher
import os
from dotenv import load_dotenv
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram import Router
from Handlers import input_data

load_dotenv()
router = Router()
token = os.getenv('API_KEY')

# Объект бота
bot = Bot(token=token)


async def main():
    # Включаем логирование, чтобы не пропустить важные сообщения
    # logging.basicConfig(level=logging.INFO)
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    # Диспетчер
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(input_data.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
