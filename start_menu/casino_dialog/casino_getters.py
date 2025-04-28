from pprint import pprint

from aiogram_dialog import DialogManager


async def first_window_start_data(dialog_manager: DialogManager, **_kwargs):
    return dialog_manager.start_data

