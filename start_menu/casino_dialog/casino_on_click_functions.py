import asyncio
import random
from pprint import pprint

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, BaseDialogManager, ShowMode
from aiogram_dialog.widgets.kbd import Button, ManagedCounter
from aiogram.exceptions import TelegramRetryAfter
from start_menu.casino_dialog.casino_data import BET_TYPES, wheel
from start_menu.casino_dialog.casino_dialog_states import CasinoDialog
from start_menu.casino_dialog.utils import parse_bet_slug, is_bet_winning


async def close_dialog(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    try:
        await dialog_manager.done()
    except Exception as e:
        print(e)
        pass


async def spin_roulette(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    dialog_manager.dialog_data["roulette_spin"] = "⏳ Крутим..."
    dialog_manager.dialog_data["spinning"] = True
    await dialog_manager.switch_to(CasinoDialog.roulette_spin)
    await check_roulette_spin(dialog_manager)


async def check_roulette_spin(dialog_manager: DialogManager):
    spins = 30
    start_index = random.randint(0, len(wheel) - 1)

    for i in range(spins):
        current_index = (start_index + i) % len(wheel)
        view = []
        for j in range(7):
            wheel_index = (current_index + j) % len(wheel)
            number, color = wheel[wheel_index]
            if j == 0:
                view.append(f'👉{color}{number}')
            else:
                view.append(f'{color}{number}')
        display = ' | '.join(view)
        await dialog_manager.update({'roulette_spin': display})
        await asyncio.sleep(0.07)

    final_index = (start_index + spins - 1) % len(wheel)
    result_number_str, result_color = wheel[final_index]
    result_number = int(result_number_str)

    dialog_data = dialog_manager.dialog_data
    bet_id = dialog_data.get("bet_id")
    potential_gain = dialog_data.get("potential_gain", 0)

    win = is_bet_winning(bet_id, result_number, result_color)

    view = []
    for j in range(7):
        wheel_index = (final_index + j) % len(wheel)
        number, color = wheel[wheel_index]
        if j == 0:
            view.append(f'✅{color}{number}')
        else:
            view.append(f'{color}{number}')
    display = ' | '.join(view)

    await dialog_manager.update({'roulette_spin': display})
    await asyncio.sleep(3.0)

    # Теперь добавляем текст результата
    color_name = {'🔴': 'красное', '⚫': 'черное', '🟩': 'зеленое'}[result_color]
    result_line = f'\n\n🎯 Результат: {result_color}{result_number} — {color_name.upper()}!'

    if win:
        result_line += f'\n\n💰 Вы выиграли {potential_gain} монет!'
    else:
        result_line += '\n\n😢 Вы проиграли... Повезет в следующий раз!'

    dialog_manager.dialog_data['spinning'] = False
    await dialog_manager.update({'roulette_spin': display + result_line})


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
    dialog_manager.dialog_data['bet_id'] = bet_id

    await dialog_manager.switch_to(
        CasinoDialog.roulette_set_bet
    )


async def set_bet_none(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data['current_bet'] = None
    await dialog_manager.switch_to(
        CasinoDialog.roulette_choose_bet
    )


async def set_bet_sum_none(
        callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
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
