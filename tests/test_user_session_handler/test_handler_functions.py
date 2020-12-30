from typing import Sequence

import pytest

from core.types import Answer, CloseSession
from core.utils.user_session_handler import handler
from core.utils.messages import get_message


answers = {
    'set_text': {
        None: get_message('set_text'),
        'step_back': get_message('set_text', message_type='unsupported_command'),
        'next_step': get_message('set_text', message_type='unsupported_command'),
        '😀': ('Текст стикера не может содержать в себе смайлики, пришлите '
               'текст без смайликов'),
        'text': get_message(handler.steps[handler.steps.index('set_text') + 1]),
    },
    'set_background_color': {
        None: get_message('set_background_color'),
        'step_back': get_message(handler.steps[handler.steps.index('set_background_color') - 1]),
        'next_step': get_message(handler.steps[handler.steps.index('set_background_color') + 1]),
        '0 0 0': get_message(handler.steps[handler.steps.index('set_background_color') + 1]),
    },
    'set_font': {
        None: get_message('set_font'),
        'step_back': get_message(handler.steps[handler.steps.index('set_font') - 1]),
        'next_step': get_message(handler.steps[handler.steps.index('set_font') + 1]),
        '1': get_message(handler.steps[handler.steps.index('set_font') + 1]),
    },
    'set_font_color': {
        None: get_message('set_font_color'),
        'step_back': get_message(handler.steps[handler.steps.index('set_font_color') - 1]),
        'next_step': get_message(handler.steps[handler.steps.index('set_font_color') + 1],
                                 splitting_numbers='1, 1', split_pattern='2 слова'),
        '255 255 255': get_message(handler.steps[handler.steps.index('set_font_color') + 1],
                                   splitting_numbers='1, 1', split_pattern='2 слова'),
    },
    'set_splitting_numbers': {
        None: get_message('set_splitting_numbers', splitting_numbers='1, 1, 1',
                          split_pattern='3 слова'),
        'step_back': get_message(handler.steps[handler.steps.index('set_splitting_numbers') - 1]),
        'next_step': get_message(handler.steps[handler.steps.index('set_splitting_numbers') + 1]),
        '2 1': get_message(handler.steps[handler.steps.index('set_splitting_numbers') + 1]),
    },
    'send_sticker': {
        None: get_message('send_sticker'),
    },
    'send_png_sticker': {
        'next_step': get_message('send_png_sticker',
                                 message_type='end_message'),
        'step_back': get_message('send_png_sticker',
                                 message_type='unsupported_command'),
        'Да': get_message('send_png_sticker', message_type='end_message'),
        'Нет': get_message('send_png_sticker', message_type='end_message'),
        'qwerty': 'Пришлите "Да" либо "Нет"',
    }
}


@pytest.mark.parametrize(
    'values',
    [('set_text', key, value) for key, value in answers['set_text'].items()]
)
def test_set_text(user_session, values):
    alias, message_text, answer_text = values
    user_session.current_step = handler.steps.index(alias)
    answer = handler.handle_session(user_session, message_text)
    assert isinstance(answer, Sequence)
    assert isinstance(answer[0], Answer)
    assert answer[0].text == answer_text


@pytest.mark.parametrize(
    'values',
    [('set_background_color', key, value) for key, value in answers['set_background_color'].items()]
)
def test_set_background_color(user_session, values):
    alias, message_text, answer_text = values
    user_session.current_step = handler.steps.index(alias)
    answer = handler.handle_session(user_session, message_text)
    assert isinstance(answer, Sequence)
    assert isinstance(answer[0], Answer)
    assert answer[0].text == answer_text


@pytest.mark.parametrize(
    'values',
    [('set_font', key, value) for key, value in answers['set_font'].items()]
)
def test_set_font(user_session, values):
    alias, message_text, answer_text = values
    user_session.current_step = handler.steps.index(alias)
    answer = handler.handle_session(user_session, message_text)
    assert isinstance(answer, Sequence)
    assert isinstance(answer[0], Answer)
    assert answer[0].text == answer_text


@pytest.mark.parametrize(
    'values',
    [('set_font_color', key, value) for key, value in answers['set_font_color'].items()]
)
def test_set_font_color(user_session, values):
    alias, message_text, answer_text = values
    user_session.current_step = handler.steps.index(alias)
    user_session.data_class.text = 'foo bar'
    answer = handler.handle_session(user_session, message_text)
    assert isinstance(answer, Sequence)
    assert isinstance(answer[0], Answer)
    assert answer[0].text == answer_text


@pytest.mark.parametrize(
    'values',
    [('set_splitting_numbers', key, value) for key, value in answers['set_splitting_numbers'].items()]
)
def test_set_splitting_numbers(user_session, values):
    alias, message_text, answer_text = values
    user_session.current_step = handler.steps.index(alias)
    user_session.data_class.text = 'foo bar baz'
    answer = handler.handle_session(user_session, message_text)
    assert isinstance(answer, Sequence)
    assert isinstance(answer[0], Answer)
    if message_text is None or message_text == 'step_back':
        assert answer[0].text == answer_text
    else:
        assert isinstance(answer[1], Answer)
        assert answer[1].text == answer_text


@pytest.mark.parametrize(
    'values',
    [('send_sticker', key, value) for key, value in answers['send_sticker'].items()]
)
def test_send_sticker(user_session, values):
    alias, message_text, answer_text = values
    user_session.current_step = handler.steps.index(alias)
    user_session.data_class.text = 'foo bar'
    user_session.data_class.splitting_numbers = (1, 1)
    answer = handler.handle_session(user_session, message_text)
    assert isinstance(answer, Sequence)
    assert isinstance(answer[0], Answer)
    assert isinstance(answer[1], Answer)
    assert answer[1].text == answer_text


@pytest.mark.parametrize(
    'values',
    [('send_png_sticker', key, value) for key, value in answers['send_png_sticker'].items()]
)
def test_send_sticker(user_session, values):
    alias, message_text, answer_text = values
    user_session.current_step = handler.steps.index(alias)
    answer = handler.handle_session(user_session, message_text)
    assert isinstance(answer, Sequence)
    if message_text == 'next_step' or message_text == 'Нет':
        assert isinstance(answer[0], CloseSession)
        assert isinstance(answer[1], Answer)
        assert answer[1].text == answer_text
    elif message_text == 'Да':
        assert isinstance(answer[0], Answer)
        assert isinstance(answer[1], CloseSession)
        assert isinstance(answer[2], Answer)
        assert answer[2].text == answer_text
    else:
        assert isinstance(answer[0], Answer)
        assert answer[0].text == answer_text
