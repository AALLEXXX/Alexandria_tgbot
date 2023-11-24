from aiogram import Dispatcher
from create_bot import bot
import asyncio
from aiogram.fsm.storage.memory import MemoryStorage
import logging
from handlers.main_handlers import main_router
from handlers.msg_handlers import msg_router

async def main() -> None:
    """Entry point
    """
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_routers(
        main_router,
        msg_router
    )
    try:
        logging.basicConfig(level=logging.INFO)
        await dp.start_polling(bot)
    except Exception as _ex:
        print(_ex)


if __name__ == '__main__':
    asyncio.run(main())
