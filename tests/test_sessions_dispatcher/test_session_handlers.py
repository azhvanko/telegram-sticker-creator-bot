from typing import Sequence
import pytest

from core.config import ALL_USER_COMMANDS


dict_steps = {
    'set_text': [('/next_step', 0), ('foo bar', 1), ],
    'set_background_color': [('255 255 255', 1), ],
    'set_font': [('font', 0), ('1', 1)],
    'set_font_color': [('0 0 0', 1), ],
    'set_splitting_numbers': [('1 1', 2), ],
    'send_png_sticker': [('Да', 0), ],
}
_len = sum(len(val) for val in dict_steps.values())
list_steps = [dict_steps for _ in range(_len)]


@pytest.mark.parametrize(
    '_dict',
    list_steps
)
def test_handlers(sessions_dispatcher, handler, chat_id, _dict):
    if not sessions_dispatcher._sessions:
        sessions_dispatcher._create_session(chat_id)

    step_index = sessions_dispatcher._sessions[chat_id].current_step
    step = handler.steps[step_index]
    message, shift = _dict[step].pop(0)

    prev_step = sessions_dispatcher._sessions[chat_id].current_step
    if message.startswith('/', 0, 1) and message[1:] in ALL_USER_COMMANDS:
        sd = sessions_dispatcher.command_handler(chat_id, message)
    else:
        sd = sessions_dispatcher.message_handler(chat_id, message)
    assert isinstance(sd, Sequence)
    assert prev_step + shift == sessions_dispatcher._sessions[chat_id].current_step


def test_steps_order(handler):
    assert handler.steps.index('send_png_sticker') == len(handler.steps) - 1
    assert handler.steps.index('send_png_sticker') == handler.steps.index('send_sticker') + 1
    assert handler.steps.index('set_splitting_numbers') > handler.steps.index('set_text')
