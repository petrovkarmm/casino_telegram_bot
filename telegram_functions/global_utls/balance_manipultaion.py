from telegram_functions.middlewares.balance_middleware import test_user_balance


async def balance_manipulation(user_id: int, amount: (int, float)):
    current_user_balance = test_user_balance[user_id]
    test_user_balance[user_id] = current_user_balance + amount