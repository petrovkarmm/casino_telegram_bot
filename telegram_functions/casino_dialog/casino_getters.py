from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import ManagedCounter


async def balance_getter(dialog_manager: DialogManager, **kwargs):
    balance = dialog_manager.middleware_data.get('balance', 0)

    return {
        'balance': balance
    }


async def roulette_spin_getter(dialog_manager: DialogManager, **kwargs):
    return {
        'roulette_spin': dialog_manager.dialog_data.get('roulette_spin', '⏳ Крутим...'),
    }
