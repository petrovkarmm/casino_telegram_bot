import asyncio
from pprint import pprint

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCounter


async def first_window_start_data(dialog_manager: DialogManager, **_kwargs):
    return dialog_manager.start_data


async def balance_getter(dialog_manager: DialogManager, **kwargs):
    balance = dialog_manager.start_data['balance']
    coefficient = dialog_manager.dialog_data['coefficient']

    return {
        'balance': balance
    }


async def roulette_spin_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'roulette_spin': dialog_manager.dialog_data.get('roulette_spin', '⏳ Крутим...')
    }
