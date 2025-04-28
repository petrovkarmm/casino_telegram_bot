import asyncio

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs

from settings import bot_token
from start_menu.casino_dialog.casino_dialog_router import casino_dialog_router
from start_menu.start_menu_router import start_menu_router


async def bot_start():
    # main configuration
    bot = Bot(token=bot_token)
    dp = Dispatcher()
    setup_dialogs(dp)

    # handlers routers
    dp.include_router(start_menu_router)

    # dialog routers
    dp.include_router(casino_dialog_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(bot_start())
    except Exception as e:
        print(e)
