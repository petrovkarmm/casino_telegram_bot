import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.types import ErrorEvent
from aiogram_dialog import setup_dialogs, DialogManager
from aiogram_dialog.api.exceptions import UnknownIntent, OutdatedIntent
from dotenv import load_dotenv, find_dotenv
from telegram_functions.casino_dialog.casino_dialog_router import casino_dialog_router
from telegram_functions.middlewares.balance_middleware import BalanceUpdater
from telegram_functions.main_menu_router import start_menu_router

load_dotenv(find_dotenv())

token = os.getenv("BOT_TOKEN")


async def bot_start():
    # main configuration
    bot = Bot(token=token)
    dp = Dispatcher()
    setup_dialogs(dp)

    async def error_unknown_intent_handler(
            event: ErrorEvent, dialog_manager: DialogManager
    ):
        if isinstance(event.exception, UnknownIntent) or isinstance(event.exception, OutdatedIntent):
            try:
                event_message_id = event.update.callback_query.message.message_id
                event_chat_id = event.update.callback_query.message.chat.id
                await bot.delete_message(
                    chat_id=event_chat_id, message_id=event_message_id
                )
            except AttributeError:
                print(f'Отбилась в закрытый диалог.')
            except Exception as exception:
                print(exception)

        else:
            return print(f"{event}")

    # error handler
    # dp.errors.register(error_unknown_intent_handler)

    # mw
    dp.message.middleware(BalanceUpdater())
    dp.callback_query.middleware(BalanceUpdater())

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
