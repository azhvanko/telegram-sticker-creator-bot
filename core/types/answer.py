from dataclasses import dataclass
from typing import Optional, Union

from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove


@dataclass
class Answer:
    """Структура ответа на пользовательское сообщение"""
    text: Optional[str] = None
    content_type: str = 'message'
    content_location: str = 'local'
    content_path: Optional[str] = None
    keyboard: Union[ReplyKeyboardMarkup,
                    ReplyKeyboardRemove] = ReplyKeyboardRemove()
