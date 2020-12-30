import datetime
import os

import pytest
import pytz

from core.config import CONTENT_DIR
from core.types import UserSession, StickerParameters
from core.utils.sessions_dispatcher import SessionsDispatcher
from core.utils.user_session_handler import handler as _handler


@pytest.fixture(scope='session')
def chat_id():
    return 42


@pytest.fixture(scope='session')
def handler():
    return _handler


@pytest.fixture(scope='module')
def sessions_dispatcher(handler):
    return SessionsDispatcher(
        user_session_handler=handler
    )


_tz = pytz.timezone('Europe/Minsk')
_datetime = datetime.datetime.now(_tz)
_current_step = 0

@pytest.fixture(scope='function')
def user_session():
    return UserSession(
        created=_datetime,
        current_step=_current_step,
        data_class=StickerParameters()
    )


@pytest.fixture(scope='session', autouse=True)
def del_tmp_images():
    yield
    for file in os.listdir(path=CONTENT_DIR):
        if file.endswith('.png'):
            os.remove(os.path.join(CONTENT_DIR, file))
