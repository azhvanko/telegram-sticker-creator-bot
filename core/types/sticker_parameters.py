from dataclasses import dataclass
from typing import Optional, Sequence

from core.fonts import DEFAULT_FONT
from core.utils.sticker_creator import RGB_BLACK, RGB_WHITE


@dataclass
class StickerParameters:
    """Параметры, необходимые для создания стикера"""
    text: Optional[str] = None
    splitting_numbers: Optional[Sequence[int]] = None
    font_name: str = DEFAULT_FONT
    font_color: Sequence[int] = RGB_BLACK
    background_color: Sequence[int] = RGB_WHITE
