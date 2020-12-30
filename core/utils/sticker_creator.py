import os
from typing import Sequence, Tuple

from PIL import Image, ImageDraw, ImageFont

from core.fonts import DEFAULT_FONT
from core.config import FONTS_DIR


DEFAULT_MODE = 'RGBA'
PICTURE_HEIGHT = 512
PICTURE_WIDTH = 512
TEXT_AREA_SIZE = 492  # 512 - 10 * 2
IMAGE_FACTOR = 1.5

RGB_BLACK = (0, 0, 0)
RGB_BLUE = (0, 0, 255)
RGB_GREEN = (0, 255, 0)
RGB_ORANGE = (255, 165, 0)
RGB_PINK = (255, 0, 255)
RGB_PURPLE = (128, 0, 128)
RGB_RED = (255, 0, 0)
RGB_WHITE = (255, 255, 255)
RGB_YELLOW = (255, 255, 0)

COLORS_MAP = {
    'Белый': (255, 255, 255),
    'Чёрный': (0, 0, 0),
    'Красный': (255, 0, 0),
    'Синий': (0, 0, 255),
    'Зелёный': (0, 255, 0),
    'Жёлтый': (255, 255, 0),
    'Оранжевый': (255, 165, 0),
    'Фиолетовый': (128, 0, 128),
    'Розовый': (255, 0, 255),
}


def _get_font_size(words: Sequence[str], font_name: str,
                   max_text_length: int) -> int:
    """
    Подбирает максимальный размер шрифта исходя из предельно возможного размера
    текстовой области
    """
    word_with_max_length = max(words, key=len)
    font_size = int(max_text_length / len(word_with_max_length) * IMAGE_FACTOR)

    if_shorter = if_longer = True

    while if_shorter or if_longer:
        font = _get_font(font_name, font_size)
        current_text_length = _get_text_length_in_px(word_with_max_length, font)

        if current_text_length < max_text_length:
            font_size += 1
            if_shorter = False
        elif current_text_length > max_text_length:
            font_size -= 1
            if_longer = False
        else:
            break

    while True:
        font = _get_font(font_name, font_size)
        text_area_height = _get_text_area_height_in_px(words, font)

        if max_text_length < text_area_height:
            font_size -= 1
        else:
            break

    return font_size - 1


def _get_font(font_name: str, font_size: int) -> ImageFont.ImageFont:
    font = os.path.join(FONTS_DIR, font_name)
    return ImageFont.truetype(font=font, size=font_size)


def _get_text_length_in_px(text: str, font: ImageFont.ImageFont) -> int:
    return ImageFont.ImageFont.getsize(font, text)[0][0]


def _get_text_area_height_in_px(words: Sequence[str],
                                font: ImageFont.ImageFont) -> float:
    result = 0

    for word in words:
        word_width, word_height = _get_word_size_in_px(font, word)
        result += word_width[1] + max(abs(word_height[1]),
                                      int(word_width[1] / 5))

    return result


def _get_word_size_in_px(font: ImageFont.ImageFont,
                         word: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    return ImageFont.ImageFont.getsize(font, word)


def _get_vertical_offset(words: Sequence[str], picture_height: int,
                         font: ImageFont.ImageFont) -> float:
    _, word_height = _get_word_size_in_px(font, words[0])
    offset_first_word = abs(word_height[1])
    text_height = _get_text_area_height_in_px(words, font)

    return (picture_height - text_height - offset_first_word) / 2


def _draw_text(draw: ImageDraw.Draw,
               words: Sequence[str],
               font: ImageFont.ImageFont,
               fill: Sequence[int],
               vertical_offset: float,
               picture_width: int) -> None:
    """
    Нанесение текста на изображение
    """
    y = vertical_offset
    for index, word in enumerate(words):
        word_width, word_height = _get_word_size_in_px(font, word)
        x = (picture_width - word_width[0]) / 2

        draw.multiline_text((x, y), text=word, align='center',
                            fill=fill, font=font)
        y += word_width[1] + max(abs(word_height[1]),
                                 int(word_width[1] / 5))


def create_sticker(text: Sequence[str], *,
                   picture_width: int = PICTURE_WIDTH,
                   picture_height: int = PICTURE_HEIGHT,
                   background_color: Sequence[int] = RGB_WHITE,
                   font_name: str = DEFAULT_FONT,
                   font_color: Sequence[int] = RGB_BLACK,
                   max_text_length: int = TEXT_AREA_SIZE,
                   mode: str = DEFAULT_MODE
                   ) -> Image.Image:
    """
    Создаёт изображение в зависимости от переданных параметров
    """
    image = Image.new(mode, (picture_width, picture_height), background_color)
    draw = ImageDraw.Draw(image, mode=mode)

    font_size = _get_font_size(text, font_name, max_text_length)
    font = _get_font(font_name, font_size)
    vertical_offset = _get_vertical_offset(text, picture_height, font)
    _draw_text(draw, text, font, font_color, vertical_offset, picture_width)

    return image
