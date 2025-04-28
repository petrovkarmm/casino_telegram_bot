from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def close_dialog(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    try:
        await dialog_manager.done()
    except Exception as e:
        print(e)
        pass


async def choose_set(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    print(callback.data)