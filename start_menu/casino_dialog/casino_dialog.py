from aiogram import F
from aiogram.methods import Close
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Row
from aiogram_dialog.widgets.text import Format

from start_menu.casino_dialog.casino_dialog_states import CasinoDialog
from start_menu.casino_dialog.casino_getters import first_window_start_data
from start_menu.casino_dialog.casino_on_click_functions import close_dialog, choose_set

casino_menu_window = Window(
    Format(
        text='🎰 Ваш текущий баланс: {balance}\n\n'
             'Выберите игру 🎲'
    ),
    SwitchTo(id='roulette', text=Format('🎯 Рулетка'), state=CasinoDialog.roulette),
    Button(id='close_dialog', text=Format('❌ Закрыть'), on_click=close_dialog),
    getter=first_window_start_data,
    state=CasinoDialog.casino_main_menu,
)

roulette_menu_window = Window(
    Format(
        text=(
            '🎡 РУЛЕТКА 🎡\n\n'
            '⬛⬛🟥🟥🟥⬛⬛\n'
            '⬛🟥🟩🟩🟩🟥⬛\n'
            '🟥🟩⬛⚪️⬛🟩🟥\n'
            '🟥🟩⚪️🟥⚪️🟩🟥\n'
            '🟥🟩⬛⚪️⬛🟩🟥\n'
            '⬛🟥🟩🟩🟩🟥⬛\n'
            '⬛⬛🟥🟥🟥⬛⬛\n\n'
            '💬 Сделайте вашу ставку!\n\n'
            'Испытайте удачу! 🍀'
        ),
        when=~F["dialog_data"]["current_rate"]
    ),
    Format(
        text=(
            '🎡 РУЛЕТКА 🎡\n\n'
            '⬛⬛🟥🟥🟥⬛⬛\n'
            '⬛🟥🟩🟩🟩🟥⬛\n'
            '🟥🟩⬛⚪️⬛🟩🟥\n'
            '🟥🟩⚪️🟥⚪️🟩🟥\n'
            '🟥🟩⬛⚪️⬛🟩🟥\n'
            '⬛🟥🟩🟩🟩🟥⬛\n'
            '⬛⬛🟥🟥🟥⬛⬛\n\n'
            '💬 Ваша ставка {dialog_data[current_rate]}.\n\n'
            'Крутите рулетку! 🎲'
        ),
        when=F["dialog_data"]["current_rate"]
    ),
    SwitchTo(id='roulette_choose_bet', text=Format('⚡️ Сделать ставку'), when=~F["dialog_data"]["current_rate"],
             state=CasinoDialog.roulette_choose_bet),
    Button(id='spin_roulette', text=Format('😈 Прокрутить рулетку'), when=F["dialog_data"]["current_rate"]),
    Row(
        Back(id='back', text=Format('🔙 Назад')),
        Button(id='close_dialog', text=Format('❌ Закрыть'), on_click=close_dialog),
    ),
    state=CasinoDialog.roulette,
)

roulette_choose_bet_window = Window(
    Format(
        text='🎰 Ваш текущий баланс: {balance}\n\n'
             'Выберите ставку: '
    ),
    Group(
        Button(id='bet_black', text=Format('⬛ Черное'), on_click=choose_set),
        Button(id='bet_red', text=Format('🟥 Красное'), on_click=choose_set),
        Button(id='bet_green', text=Format('🟩 Зеленое (джекпот)'), on_click=choose_set),
        Button(id='bet_even', text=Format('➗ Четное'), on_click=choose_set),
        Button(id='bet_odd', text=Format('➖ Нечетное'), on_click=choose_set),
        Button(id='bet_small', text=Format('🔢 Меньше 18'), on_click=choose_set),
        Button(id='bet_big', text=Format('🔢 Больше 18'), on_click=choose_set),
        width=2  # чтобы кнопки шли по 2 в ряд красиво
    ),
    Row(
        Back(id='back', text=Format('🔙 Назад')),
        Button(id='close_dialog', text=Format('❌ Закрыть'), on_click=close_dialog),
    ),
    getter=first_window_start_data,
    state=CasinoDialog.roulette_choose_bet,
)

roulette_set_bet_window = Window(
    Format(
        text='🎰 Ваш текущий баланс: {balance}\n'
             'Выберите сумму ставки: '
    ),
    getter=first_window_start_data,
    state=CasinoDialog.roulette_set_bet,
)

casino_dialog = Dialog(
    casino_menu_window,
    roulette_menu_window,
    roulette_choose_bet_window,
    roulette_set_bet_window
)
