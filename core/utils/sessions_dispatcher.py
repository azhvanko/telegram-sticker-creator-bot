import asyncio
import datetime
import os
from typing import Dict, Sequence, Union

import pytz

from core.config import USER_COMMANDS
from core.types import (
    Answer, CloseSession, SessionHandler, StickerParameters, UserSession,
    NotCreatedUserSession, NotClosedUserSession,
)


class SessionsDispatcher:
    """
    Диспетчер сессий - принимает сообщения из бота, отдаёт ответ,
    создаёт/закрывает сессии
    """
    def __init__(self, user_session_handler):
        self._sessions: Dict[int, UserSession] = {}
        self._user_session_handler: SessionHandler = user_session_handler

    @staticmethod
    def _get_init_message() -> Sequence[Answer]:
        """
        Возвращает стартовое сообщение
        """
        return (Answer(text='Начните работу с ботом с помощью одной из '
                            'доступных стартовых команд.\n\n'
                            'Стартовые команды:\n'
                            '/create_sticker - начать создание стикера\n\n'
                            'Сервисные команды:\n'
                            '/next_step - пропустить текущий шаг (будет '
                            'установлено значение по умолчанию)\n'
                            '/step_back - вернуться к предыдущему шагу\n'
                            '/reset - начать создание стикера сначала'),)

    def command_handler(self, chat_id: int,
                        command: str) -> Sequence[Union[Answer, CloseSession]]:
        """
        Промежуточный обработчик для команд из бота
        """
        command = command[1:]

        if command in USER_COMMANDS['RESET_COMMANDS']:
            self.close_session(chat_id)
            return self._get_init_message()

        if command in USER_COMMANDS['START_COMMANDS']:
            try:
                user_session = self._create_session(chat_id)
            except NotClosedUserSession as exc:
                return (Answer(text=str(exc)),)
            else:
                return self._user_session_handler.handle_session(user_session)

        if command in USER_COMMANDS['SERVICE_COMMANDS']:
            try:
                user_session = self._get_session(chat_id)
            except NotCreatedUserSession as exc:
                return (Answer(text=str(exc)),)
            else:
                return self._user_session_handler.handle_session(user_session,
                                                                 message=command)

    def message_handler(self, chat_id: int,
                        message: str) -> Sequence[Union[Answer, CloseSession]]:
        """
        Промежуточный обработчик для сообщений из бота
        """
        if chat_id not in self._sessions:
            return (Answer(text='Для начала работы с ботом используйте одну из '
                                'доступных стартовых команд.\n\n'
                                'Стартовые команды:\n'
                                '/create_sticker - начать создание стикера'),)

        user_session = self._sessions[chat_id]
        return self._user_session_handler.handle_session(user_session=user_session,
                                                         message=message)

    def close_session(self, chat_id: int) -> None:
        """
        Закрывает сессию, удаляет созданный стикер (если он был создан)
        """
        if chat_id in self._sessions:
            try:
                os.remove(self._sessions[chat_id].file_path)
            except (FileNotFoundError, TypeError):
                pass
            self._sessions.pop(chat_id, None)

    async def close_old_sessions(self) -> None:
        creation_limit = 600  # 10 min
        while True:
            await asyncio.sleep(creation_limit / 2)
            current_time = self._get_now_datetime()

            close_list = set()
            for chat_id, session in self._sessions.items():
                if (current_time - session.created).total_seconds() > creation_limit:
                    close_list.add(chat_id)

            for chat_id in close_list:
                self.close_session(chat_id)

    def _create_session(self, chat_id: int) -> UserSession:
        """
        Создаёт сессию и возвращает её. Если сессия уже создана - возвращает
        ошибку
        """
        if chat_id in self._sessions:
            raise NotClosedUserSession(
                'Вы не закончили создавать предыдущий стикер.\n'
                'Если вы хотите начать сначала - пришлите команду /reset'
            )
        self._sessions[chat_id] = UserSession(
            created=self._get_now_datetime(),
            current_step=self._user_session_handler.first_step,
            data_class=StickerParameters()
        )

        return self._sessions[chat_id]

    def _get_session(self, chat_id: int) -> UserSession:
        """
        Возращает созданную ранее сессию. Если сессия ещё не создана -
        возвращает ошибку
        """
        if chat_id not in self._sessions:
            raise NotCreatedUserSession(
                'Для начала работы с ботом введите одну из доступных '
                'стартовых команд.\n\n'
                'Стартовые команды:\n'
                '/create_sticker - начать создание стикера'
            )
        return self._sessions[chat_id]

    @staticmethod
    def _get_now_datetime() -> datetime.datetime:
        """
        Возвращает текущий datetime с учётом указанной временной зоны
        """
        tz = pytz.timezone('Europe/Minsk')
        now = datetime.datetime.now(tz)
        return now
