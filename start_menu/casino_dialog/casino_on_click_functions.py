from pprint import pprint

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedCounter

from start_menu.casino_dialog.casino_data import BET_TYPES
from start_menu.casino_dialog.casino_dialog_states import CasinoDialog
from start_menu.casino_dialog.utils import parse_bet_slug


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
    bet_id = callback.data
    bet_info = BET_TYPES.get(bet_id)

    if not bet_info:
        await callback.answer("Ошибка выбора ставки", show_alert=True)
        return

    dialog_manager.dialog_data['title'] = bet_info.get('title')
    dialog_manager.dialog_data['coefficient'] = bet_info.get('coefficient')
    dialog_manager.dialog_data['current_bet'] = None

    await dialog_manager.switch_to(
        CasinoDialog.roulette_set_bet
    )


async def set_bet_none(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['current_bet'] = None


async def set_bet_clicked(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    bet_slug = callback.data
    bet = parse_bet_slug(bet_slug)

    current_bet = dialog_manager.dialog_data['current_bet']
    current_balance = dialog_manager.start_data['balance']
    coefficient = dialog_manager.dialog_data['coefficient']

    if current_bet:
        future_bet = bet + current_bet
        potential_gain = future_bet * coefficient
    else:
        future_bet = bet
        potential_gain = bet * coefficient

    if future_bet > current_balance:
        await callback.answer(
            text='Недостаточно денег на балансе.'
        )
    elif future_bet < 0:
        await callback.answer(
            text='Ставка не может быть меньше 0.'
        )
    else:
        dialog_manager.dialog_data['current_bet'] = future_bet
        dialog_manager.dialog_data['potential_gain'] = potential_gain
