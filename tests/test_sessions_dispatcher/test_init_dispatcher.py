from core.types import SessionHandler
from core.utils.sessions_dispatcher import SessionsDispatcher


def test_init_sessions_dispatcher(sessions_dispatcher):
    assert isinstance(sessions_dispatcher, SessionsDispatcher)
    assert isinstance(sessions_dispatcher._user_session_handler, SessionHandler)
    assert len(sessions_dispatcher._sessions) == 0
