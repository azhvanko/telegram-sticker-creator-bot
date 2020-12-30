from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.types.sticker_parameters import StickerParameters


@dataclass
class UserSession:
    """Структура пользовательской сессии"""
    created: datetime
    current_step: int
    data_class: StickerParameters
    file_path: Optional[str] = None
