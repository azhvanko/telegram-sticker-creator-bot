from typing import Set

from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class AccessMiddleware(BaseMiddleware):
    """
    Аутентификация — пропускаем сообщения только от определённых
    Telegram аккаунтов
    """
    def __init__(self, access_ids: Set):
        self.access_ids = access_ids
        super().__init__()

    async def on_process_message(self, message: types.Message, _) -> None:
        if message.from_user.id not in self.access_ids:
            await message.answer("Access Denied")
            raise CancelHandler()
