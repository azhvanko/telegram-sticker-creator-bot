import io
import os

from core.config import FONTS_DIR
from core.fonts import *


def test_count_fonts_equals():
    for file in os.listdir(path=FONTS_DIR):
        if file[-4:] in {'.ttf', 'otf'}:
            assert file in FONTS.values()


def test_min_max_font_number_equals():
    assert MIN_FONT_NUMBER != 0
    assert MIN_FONT_NUMBER == min(FONTS.keys())
    assert MAX_FONT_NUMBER == max(FONTS.keys())


def test_default_font():
    assert DEFAULT_FONT in FONTS.values()


def test_example_fonts_path():
    assert isinstance(EXAMPLE_FONTS_PATH, (str, io.BufferedReader))
