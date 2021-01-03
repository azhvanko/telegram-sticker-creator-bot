import io
from typing import NoReturn, Sequence, Union

from aiogram import Bot, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from core.config import ACCESS_IDS, ALL_USER_COMMANDS, TOKEN
from core.logs.log_helper import get_logger
from core.types import Answer, CloseSession
from core.utils.middleware import AccessMiddleware
from core.utils.sessions_dispatcher import SessionsDispatcher
from core.utils.user_session_handler import handler


logger = get_logger()
bot = Bot(token=TOKEN)
dispatcher = Dispatcher(bot, storage=MemoryStorage())
sessions_dispatcher = SessionsDispatcher(user_session_handler=handler)


@dispatcher.message_handler(commands=ALL_USER_COMMANDS)
async def process_command(message: types.Message) -> None:
    """
    Обработка зарегистрированных команд из бота
    """
    answers = sessions_dispatcher.command_handler(
        chat_id=message.from_user.id,
        command=message.text)
    await answer_handler(message.from_user.id, answers)


@dispatcher.message_handler()
async def process_message(message: types.Message) -> None:
    """
    Обработка сообщений из бота
    """
    answers = sessions_dispatcher.message_handler(
        chat_id=message.from_user.id,
        message=message.text)
    await answer_handler(message.from_user.id, answers)


async def answer_handler(chat_id: int,
                         answers: Sequence[Union[Answer, CloseSession]]) -> None:
    """
    Обрабатывает кортеж из ответов пользователю
    """
    for answer in answers:
        if isinstance(answer, Answer):
            try:
                await answer_handler_helper(chat_id, answer)
            except Exception as exc:
                logger.exception(msg=exc)
        elif isinstance(answer, CloseSession):
            sessions_dispatcher.close_session(chat_id)
    return


async def answer_handler_helper(chat_id: int, answer: Answer) -> None:
    """
    Отправляет ответ в зависимости от типа контента в Answer
    """
    if answer.content_path:
        if answer.content_location == 'local':
            content = io.FileIO(answer.content_path, mode='rb')
        else:
            content = answer.content_path

    if answer.content_type == 'message':
        await bot.send_message(chat_id=chat_id,
                               text=answer.text,
                               reply_markup=answer.keyboard)
    elif answer.content_type == 'photo':
        await bot.send_photo(chat_id=chat_id,
                             photo=content,
                             caption=answer.text,
                             reply_markup=answer.keyboard)
    elif answer.content_type == 'document':
        await bot.send_document(chat_id=chat_id,
                                document=content,
                                caption=answer.text,
                                reply_markup=answer.keyboard)


def main() -> NoReturn:
    dispatcher.middleware.setup(LoggingMiddleware(logger))
    dispatcher.middleware.setup(AccessMiddleware(ACCESS_IDS))

    executor.start_polling(dispatcher, skip_updates=True, timeout=60)


if __name__ == '__main__':
    main()
