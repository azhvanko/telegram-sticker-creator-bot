import datetime

import pytest
import pytz

import core.utils.user_session_handler as ush
from core.fonts import MAX_FONT_NUMBER, MIN_FONT_NUMBER
from core.types import (
    NotCorrectFontNumber, NotCorrectRGBCode, NotCorrectSplittingText,
)


_tz = pytz.timezone('UTC')
_datetime = datetime.datetime.now(_tz)


class TestSetColorHelper:

    @pytest.mark.parametrize(
        'code, result',
        (
            ('Белый', (255, 255, 255)),
            ('255 255 255', (255, 255, 255)),
            ('0 0 0', (0, 0, 0)),
        )
    )
    def test_equals(self, code, result):
        assert ush._set_color_helper(code) == result

    @pytest.mark.parametrize(
        'code',
        (
            '255 255 256',
            'qwerty',
            '255 0',
            '0 0 0 0',
        )
    )
    def test_not_correct_rgb_code(self, code):
        with pytest.raises(NotCorrectRGBCode):
            ush._set_color_helper(code)


class TestSetFontHelper:

    @pytest.mark.parametrize(
        'font_number',
        (
            str(MAX_FONT_NUMBER),
            str(MIN_FONT_NUMBER),
        )
    )
    def test_equals(self, font_number, user_session):
        assert ush._set_font_helper(font_number, user_session) is None

    @pytest.mark.parametrize(
        'font_number',
        (
            str(MAX_FONT_NUMBER + 1),
            str(MIN_FONT_NUMBER - 1),
            '1.5',
            '1 2',
        )
    )
    def test_not_correct_font_number(self, font_number, user_session):
        with pytest.raises(NotCorrectFontNumber):
            ush._set_font_helper(font_number, user_session)


class TestGetSplittingNumbers:

    @pytest.mark.parametrize(
        'pattern, default_pattern, result',
        (
            ('1, 1', (1, 1), (1, 1)),
            ('2', (1, 1), (2,)),
            ('1, 1, 1', (1, 1, 1), (1, 1, 1)),
            ('1, 2', (1, 1, 1), (1, 2)),
            ('2, 1', (1, 1, 1), (2, 1)),
        )
    )
    def test_equals(self, pattern, default_pattern, result):
        assert ush._get_splitting_numbers(pattern, default_pattern) == result

    @pytest.mark.parametrize(
        'pattern, default_pattern',
        (
            ('0 1 1', (1, 1)),
            ('1, 1, 1', (1, 1)),
            ('1', (1, 1)),
            ('0 2', (1, 1)),
            ('2 2', (1, 1, 1)),
            ('1, 2, 1', (1, 1, 1)),
            ('22', (1, 1, 1, 1)),
        )
    )
    def test_not_correct_splitting_text(self, pattern, default_pattern):
        with pytest.raises(NotCorrectSplittingText):
            ush._get_splitting_numbers(pattern, default_pattern)


@pytest.mark.parametrize(
    'code, result',
    (
        ((1, 2, 3), True),
        ((0, 0, 0), True),
        ((255, 255, 255), True),
        ((255, 255), False),
        ((255, 255, 255, 255), False),
        ((0, 256, 0), False),
        ((-1, 0, 255), False),
    )
)
def test_is_valid_rgb_code_equals(code, result):
    assert ush._is_valid_rgb_code(code) == result


@pytest.mark.parametrize(
    'text, result',
    (
        ('text', (1,)),
        ('text text', (1, 1)),
        ('text text, text', (1, 1, 1)),
    )
)
def test_set_splitting_numbers_helper_equals(text, result):
    assert ush._set_splitting_numbers_helper(text) == result


@pytest.mark.parametrize(
    'count, result',
    (
        (2, '2 слова'),
        (4, '4 слова'),
        (5, '5 слов'),
        (8, '8 слов'),
    )
)
def test_get_split_pattern_equals(count, result):
    assert ush._get_split_pattern(count) == result


@pytest.mark.parametrize(
    'pattern, result',
    (
        ((1, 1), '1, 1'),
        ((2, 2), '2, 2'),
    )
)
def test_get_str_splitting_numbers_equals(pattern, result):
    assert ush._get_str_splitting_numbers(pattern) == result


@pytest.mark.parametrize(
    'text, pattern, result',
    (
        ('foo', (1,), ('foo',)),
        ('foo, bar', (1, 1), ('foo,', 'bar')),
        ('foo, bar', (2,), ('foo, bar',)),
        ('t e x t', (1, 1, 1, 1), ('t', 'e', 'x', 't')),
    )
)
def test_get_splitting_text_equals(text, pattern, result):
    assert ush._get_splitting_text(text, pattern) == result


def test_generate_filename_equals():
    assert isinstance(ush._generate_filename(), str)


def test_get_date_formatted_equals():
    assert ush._get_date_formatted(_datetime) == _datetime.strftime('%Y-%m-%d')
