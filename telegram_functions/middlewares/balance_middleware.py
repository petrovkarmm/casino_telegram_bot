from typing import Any, Callable, Dict, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

test_user_balance = {

}


class BalanceUpdater(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id

        # заменить на get_or_create на бэке
        if user_id not in test_user_balance:
            test_user_balance[user_id] = 100

        data["balance"] = test_user_balance.get(event.from_user.id)
        data["user_id"] = user_id

        return await handler(event, data)
