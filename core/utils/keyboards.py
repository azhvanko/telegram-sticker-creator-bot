from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from core.fonts import MIN_FONT_NUMBER, MAX_FONT_NUMBER
from core.utils.sticker_creator import COLORS_MAP


kb_yesno = ReplyKeyboardMarkup(resize_keyboard=True,
                               one_time_keyboard=True).add(KeyboardButton('Да'),
                                                           KeyboardButton('Нет'))

_fonts_numbers = [KeyboardButton(str(i))
                  for i in range(MIN_FONT_NUMBER, MAX_FONT_NUMBER + 1)]
kb_fonts_numbers = ReplyKeyboardMarkup(resize_keyboard=True,
                                       one_time_keyboard=True).add(*_fonts_numbers)

_colors = [KeyboardButton(color) for color in COLORS_MAP.keys()]
kb_colors = ReplyKeyboardMarkup(resize_keyboard=True,
                                one_time_keyboard=True).add(*_colors)
