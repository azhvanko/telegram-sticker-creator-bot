import pytest
from PIL import Image

from core.fonts import FONTS
from core.utils.sticker_creator import COLORS_MAP, create_sticker


@pytest.mark.parametrize(
    'font',
    [font for font in FONTS.values()]
)
@pytest.mark.parametrize(
    'text',
    ['foo', 'foo bar', '123', '!@#']
)
def test_sticker_creator(text, font):
    image = create_sticker(text=text, font_name=font)
    assert isinstance(image, Image.Image)
    assert image.width == 512 and image.height == 512


def test_colors_map():
    for rgb in COLORS_MAP.values():
        for val in rgb:
            assert 0 <= val <= 255
