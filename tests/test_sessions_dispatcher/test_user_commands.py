from typing import Sequence

import pytest

from core.config import USER_COMMANDS
from core.utils.user_session_handler import handler


@pytest.mark.parametrize('command', USER_COMMANDS['RESET_COMMANDS'])
def test_reset_commands(command, chat_id, sessions_dispatcher):
    command = f'/{command}'
    answer = sessions_dispatcher.command_handler(chat_id, command)
    assert len(answer) == 1
    assert answer[0].text == sessions_dispatcher._get_init_message()[0].text
    assert chat_id not in sessions_dispatcher._sessions
    assert isinstance(answer, Sequence)


@pytest.mark.parametrize('command', USER_COMMANDS['SERVICE_COMMANDS'])
def test_reset_commands(command, chat_id, sessions_dispatcher):
    command = f'/{command}'
    answer = sessions_dispatcher.command_handler(chat_id, command)
    assert len(answer) == 1
    assert chat_id not in sessions_dispatcher._sessions
    assert isinstance(answer, Sequence)


@pytest.mark.parametrize('command', USER_COMMANDS['START_COMMANDS'])
def test_start_commands(command, chat_id, sessions_dispatcher):
    command = f'/{command}'
    answer = sessions_dispatcher.command_handler(chat_id, command)
    assert sessions_dispatcher._sessions[chat_id].current_step == 0
    assert len(answer) == 1
    assert answer[0].text == handler.handle_session(sessions_dispatcher._sessions[chat_id])[0].text
    assert chat_id in sessions_dispatcher._sessions
    assert isinstance(answer, Sequence)
