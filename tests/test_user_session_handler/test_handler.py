from typing import Callable, Sequence

import pytest


def test_handler_steps_count(handler):
    for step in handler.steps:
        if handler.steps.count(step) > 1:
            assert False


def test_handler_first_step(handler):
    assert handler.first_step == 0


def test_handler_last_step(handler):
    assert handler.last_step == len(handler.steps) - 1


def test_steps_equals(handler):
    assert isinstance(handler.steps, Sequence)


def test_functions_map_equals(handler):
    assert isinstance(handler.functions_map, dict)


def test_handle_session(handler, user_session):
    for index, step_name in enumerate(handler.steps):
        user_session.current_step = index
        if step_name == 'set_splitting_numbers':
            user_session.data_class.text = 'foo bar'
        if step_name == 'send_png_sticker':
            message = 'Да'
        else:
            message = None
        result = handler.handle_session(user_session, message)
        assert isinstance(result, Sequence)


def test_get_step_handler(handler):
    for index, step_name in enumerate(handler.steps):
        func = handler._get_step_handler(index)
        assert isinstance(func, Callable)


@pytest.mark.parametrize(
    'message',
    ['next_step', 'step_back']
)
def test_update_current_step(handler, user_session, message):
    for index, step_name in enumerate(handler.steps):
        user_session.current_step = index
        assert handler.update_current_step(user_session, message) is None
