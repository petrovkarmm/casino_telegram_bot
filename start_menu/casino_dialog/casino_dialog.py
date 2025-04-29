from aiogram import F
from aiogram.methods import Close
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, SwitchTo, Back, Group, Row, Counter
from aiogram_dialog.widgets.text import Format, Const

from start_menu.casino_dialog.casino_dialog_states import CasinoDialog
from start_menu.casino_dialog.casino_getters import first_window_start_data, balance_getter, roulette_spin_getter
from start_menu.casino_dialog.casino_on_click_functions import close_dialog, choose_set, set_bet_clicked, set_bet_none, \
    spin_roulette

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
        width=2
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
        text='🎰 Ваш текущий баланс: {balance}\n\n'
             'Вы поставили на {dialog_data[title]}\n'
             'Коэффициент на победу {dialog_data[coefficient]}\n\n',
        when=~F['dialog_data']['current_bet']
    ),
    Button(
        id='current_bet', text=Format('Время делать ставки! ⬇️'),
        when=~F['dialog_data']['current_bet']
    ),
    Format(
        text='🎰 Ваш текущий баланс: {balance}\n\n'
             'Вы поставили на {dialog_data[title]}\n'
             'Коэффициент на победу: {dialog_data[coefficient]}\n\n'
             'Ваш потенциальный выигрыш: {dialog_data[potential_gain]} руб.\n\n',
        when=F['dialog_data']['current_bet']
    ),
    Button(
        id='current_bet', text=Format('Ваша ставка: {dialog_data[current_bet]} руб.'),
        when=F['dialog_data']['current_bet']
    ),
    Button(
        id='start_roulette', text=Format('~ Прокрутить рулетку ~'), when=F['dialog_data']['current_bet'],
        on_click=spin_roulette
    ),
    Button(
        id='set_bet_null', text=Format('Обнулить ставку.'),
        when=F['dialog_data']['current_bet'], on_click=set_bet_none
    ),
    Row(
        Button(id='bet_plus_10', text=Format('+10'), on_click=set_bet_clicked),
        Button(id='bet_plus_100', text=Format('+100'), on_click=set_bet_clicked),
        Button(id='bet_plus_1000', text=Format('+1000'), on_click=set_bet_clicked),
    ),
    Row(
        Button(id='bet_minus_10', text=Format('-10'), on_click=set_bet_clicked),
        Button(id='bet_minus_100', text=Format('-100'), on_click=set_bet_clicked),
        Button(id='bet_minus_1000', text=Format('-1000'), on_click=set_bet_clicked),
    ),
    Row(
        Back(id='back', text=Format('🔙 Назад')),
        Button(id='close_dialog', text=Format('❌ Закрыть'), on_click=close_dialog),
    ),
    getter=balance_getter,
    state=CasinoDialog.roulette_set_bet,
)

roulette_spin_window = Window(
    Format(
        text='{roulette_spin}'
    ),
    Button(
        id='text',
        text=Format('text')
    ),
    getter=roulette_spin_getter,
    state=CasinoDialog.roulette_spin
)

casino_dialog = Dialog(
    casino_menu_window,
    roulette_menu_window,
    roulette_choose_bet_window,
    roulette_set_bet_window,
    roulette_spin_window
)
