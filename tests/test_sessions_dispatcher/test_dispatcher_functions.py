import datetime

import pytest

from core.types import (
    UserSession,
    NotCreatedUserSession, NotClosedUserSession,
)


class TestCreateSession:

    def test_equals(self, sessions_dispatcher, chat_id):
        result = sessions_dispatcher._create_session(chat_id)
        assert isinstance(result, UserSession)
        assert chat_id in sessions_dispatcher._sessions

    def test_not_closed_user_session(self, sessions_dispatcher, chat_id):
        sessions_dispatcher._sessions.clear()
        sessions_dispatcher._create_session(chat_id)
        with pytest.raises(NotClosedUserSession):
            sessions_dispatcher._create_session(chat_id)


class TestGetSession:

    def test_equals(self, sessions_dispatcher, chat_id):
        sessions_dispatcher._sessions.clear()
        sessions_dispatcher._create_session(chat_id)
        result = sessions_dispatcher._get_session(chat_id)
        assert isinstance(result, UserSession)
        assert chat_id in sessions_dispatcher._sessions

    def test_not_created_user_session(self, sessions_dispatcher, chat_id):
        sessions_dispatcher._sessions.clear()
        with pytest.raises(NotCreatedUserSession):
            sessions_dispatcher._get_session(chat_id)


def test_close_session(sessions_dispatcher, chat_id):
    command = '/create_sticker'
    sessions_dispatcher.command_handler(chat_id, command)
    result = sessions_dispatcher.close_session(chat_id)
    assert chat_id not in sessions_dispatcher._sessions
    assert result is None


def test_close_old_session(sessions_dispatcher, chat_id):
    command = '/create_sticker'
    sessions_dispatcher.command_handler(chat_id, command)
    _datetime = sessions_dispatcher._get_now_datetime().replace(year=2019)
    sessions_dispatcher._sessions[chat_id].created = _datetime
    result = sessions_dispatcher._close_old_sessions()
    assert result is None
    assert len(sessions_dispatcher._sessions) == 0
    assert chat_id not in sessions_dispatcher._sessions


def test_get_now_datetime(sessions_dispatcher):
    _datetime = sessions_dispatcher._get_now_datetime()
    assert isinstance(_datetime, datetime.datetime)
