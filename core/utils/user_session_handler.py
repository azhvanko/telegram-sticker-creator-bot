import datetime
import os
import re
import uuid
from typing import Optional, Sequence, Union

from emoji import emoji_count

from .sticker_creator import COLORS_MAP, create_sticker
from core.config import CONTENT_DIR, USER_COMMANDS
from core.fonts import (
    EXAMPLE_FONTS_PATH, FONTS, MAX_FONT_NUMBER, MIN_FONT_NUMBER
)
from core.types import (
    Answer, CloseSession, UserSession, SessionHandler,
    NotCorrectFontNumber, NotCorrectRGBCode, NotCorrectSplittingText,
)
from core.utils.keyboards import kb_colors, kb_fonts_numbers, kb_yesno
from core.utils.messages import get_message

# Создаём обработчик и регистрируем в нём функции-обработчики для каждого шага,
# которые проверяют правильность присланных сообщений и всегда отдают ответ
handler = SessionHandler(
    steps=(
        'set_text',
        'set_background_color',
        'set_font',
        'set_font_color',
        'set_splitting_numbers',
        'send_sticker',
        'send_png_sticker',
    )
)


@handler.register_function(alias='set_text')
def _set_text(user_session: UserSession,
              message: Optional[str]) -> Sequence[Answer]:
    """
    Проверяет правильность присланного текста для стикера, обновляет текст в
    экземпляре пользовательской сессии
    """
    alias = _set_text.alias
    if message is None:
        return (Answer(text=get_message(step=alias)),)
    if message in USER_COMMANDS['SERVICE_COMMANDS']:
        return (Answer(text=get_message(step=alias,
                                        message_type='unsupported_command')),)
    if emoji_count(message) > 0:
        return (Answer(text='Текст стикера не может содержать в себе смайлики, '
                            'пришлите текст без смайликов'),)

    user_session.data_class.text = message
    handler.update_current_step(user_session)
    return handler.handle_session(user_session)


@handler.register_function(alias='set_background_color')
def _set_background_color(user_session: UserSession,
                          message: Optional[str]) -> Sequence[Answer]:
    """
    Проверяет правильность присланного RGB-кода цвета для заливки фона стикера,
    обновляет RGB-код цвета в экземпляре пользовательской сессии
    """
    alias = _set_background_color.alias
    if message is None:
        return (Answer(text=get_message(step=alias),
                       keyboard=kb_colors),)
    if message in USER_COMMANDS['SERVICE_COMMANDS']:
        handler.update_current_step(user_session, command=message)
        return handler.handle_session(user_session)

    try:
        user_session.data_class.background_color = _set_color_helper(message)
    except NotCorrectRGBCode as exc:
        return (Answer(text=str(exc), keyboard=kb_colors),)
    else:
        handler.update_current_step(user_session)
        return handler.handle_session(user_session)


@handler.register_function(alias='set_font')
def _set_font(user_session: UserSession,
              message: Optional[str]) -> Sequence[Answer]:
    """
    Проверяет правильность присланного номера шрифта, обновляет шрифт в
    экземпляре пользовательской сессии
    """
    alias = _set_font.alias
    if message is None:
        return (Answer(content_type='photo',
                       content_path=EXAMPLE_FONTS_PATH,
                       content_location='telegram_server',
                       text=get_message(step=alias),
                       keyboard=kb_fonts_numbers),)
    if message in USER_COMMANDS['SERVICE_COMMANDS']:
        handler.update_current_step(user_session, command=message)
        return handler.handle_session(user_session)

    try:
        _set_font_helper(message, user_session)
    except NotCorrectFontNumber as exc:
        return (Answer(text=str(exc)),)
    else:
        handler.update_current_step(user_session)
        return handler.handle_session(user_session)


@handler.register_function(alias='set_font_color')
def _set_font_color(user_session: UserSession,
                    message: Optional[str]) -> Sequence[Answer]:
    """
    Проверяет правильность присланного RGB-кода цвета для шрифта, обновляет
    RGB-код цвета в экземпляре пользовательской сессии
    """
    alias = _set_font_color.alias
    if message is None:
        return (Answer(text=get_message(step=alias),
                       keyboard=kb_colors),)
    if message in USER_COMMANDS['SERVICE_COMMANDS']:
        handler.update_current_step(user_session, command=message)
        return handler.handle_session(user_session)

    try:
        user_session.data_class.font_color = _set_color_helper(message)
    except NotCorrectRGBCode as exc:
        return (Answer(text=str(exc), keyboard=kb_colors),)
    else:
        handler.update_current_step(user_session)
        return handler.handle_session(user_session)


@handler.register_function(alias='set_splitting_numbers')
def _set_splitting_numbers(user_session: UserSession,
                           message: Optional[str]) -> Sequence[Answer]:
    """
    Проверяет правильность присланной разбивки текста по строкам, обновляет
    разбивку в экземпляре пользовательской сессии
    """
    alias = _set_splitting_numbers.alias
    if user_session.data_class.splitting_numbers is None:
        user_session.data_class.splitting_numbers = _set_splitting_numbers_helper(
            user_session.data_class.text)

    if message is None and len(user_session.data_class.splitting_numbers) > 1:
        splitting_numbers = _get_str_splitting_numbers(user_session.data_class.splitting_numbers)
        split_pattern = _get_split_pattern(len(user_session.data_class.splitting_numbers))
        return (Answer(text=get_message(step=alias,
                                        splitting_numbers=splitting_numbers,
                                        split_pattern=split_pattern)),)

    if message in USER_COMMANDS['SERVICE_COMMANDS'] or (
            message is None and len(user_session.data_class.splitting_numbers) == 1):
        message = message or 'next_step'
        handler.update_current_step(user_session, command=message)
        return handler.handle_session(user_session)

    try:
        user_session.data_class.splitting_numbers = _get_splitting_numbers(
            message, user_session.data_class.splitting_numbers)
    except NotCorrectSplittingText as exc:
        return (Answer(text=str(exc)),)
    else:
        handler.update_current_step(user_session)
        return handler.handle_session(user_session)


@handler.register_function(alias='send_sticker')
def _send_sticker(user_session: UserSession,
                  message: Optional[str]) -> Sequence[Answer]:
    """
    Создаёт и сохраняет изображение, возращает путь к изображению
    """
    alias = _send_sticker.alias
    if message is None:
        text = _get_splitting_text(user_session.data_class.text,
                                   user_session.data_class.splitting_numbers)
        sticker = create_sticker(
            text=text,
            background_color=user_session.data_class.background_color,
            font_name=user_session.data_class.font_name,
            font_color=user_session.data_class.font_color,
            picture_width=512,
            picture_height=512
        )
        file_name = f'{_get_date_formatted(user_session.created)}_{_generate_filename()}.png'
        user_session.file_path = os.path.join(CONTENT_DIR, file_name)
        sticker.save(user_session.file_path)
        handler.update_current_step(user_session)
        return (
            Answer(content_type='photo',
                   content_path=user_session.file_path),
            Answer(text=get_message(step=alias),
                   keyboard=kb_yesno),
        )


@handler.register_function(alias='send_png_sticker')
def _send_png_sticker(user_session: UserSession,
                      message: Optional[str]) -> Sequence[Union[Answer, CloseSession]]:
    """
    Возвращает финальное сообщение. Опционально возвращает путь к созданному
    стикеру на диске
    """
    alias = _send_png_sticker.alias
    if message in USER_COMMANDS['SERVICE_COMMANDS']:
        if message == 'step_back':
            return (Answer(text=get_message(step=alias,
                                            message_type='unsupported_command')),)
        else:
            message = 'НЕТ'
    message = message.strip().upper()

    if message not in ('ДА', 'НЕТ'):
        return (Answer(text='Пришлите "Да" либо "Нет"'),)
    else:
        if message == 'ДА':
            document = (Answer(content_type='document',
                               content_path=user_session.file_path),)
        else:
            document = tuple()
        return document + (
            CloseSession(),
            Answer(text=get_message(step=alias, message_type='end_message')),
        )


def _set_color_helper(code: str) -> Sequence[int]:
    """
    Возвращает RGB-код
    """
    if code.capitalize() in COLORS_MAP:
        return COLORS_MAP[code]

    pattern = r'\d+'
    rgb_code = tuple([int(i) for i in re.findall(pattern, code)])

    if _is_valid_rgb_code(rgb_code):
        return rgb_code

    raise NotCorrectRGBCode(
        'Вы прислали недопустимый RGB-код.\n'
        'Корректный RGB-код должен состоять из 3-х целых чисел, '
        'каждое число д. б. в диапазоне от 0 до 255'
    )


def _set_font_helper(font_number: str, user_session: UserSession) -> None:
    """
    Проверяет номер присланного шрифта
    """
    try:
        index = int(font_number)
        user_session.data_class.font_name = FONTS[index]
    except (ValueError, KeyError):
        raise NotCorrectFontNumber(
            f'Вы прислали неверный номер шрифта. Корректный номер д. б. целым '
            f'числом в диапазоне от {MIN_FONT_NUMBER} до {MAX_FONT_NUMBER}'
        )
    else:
        return


def _is_valid_rgb_code(rgb_code: Sequence[int]) -> bool:
    """
    Проверяет валидность RGB-кода
    """
    if len(rgb_code) != 3:
        return False

    for i in rgb_code:
        if i < 0 or i > 255:
            return False

    return True


def _set_splitting_numbers_helper(text: str) -> Sequence[int]:
    """
    Возвращает дефолтную разбивку текста по строкам
    """
    words_count = len(text.split())

    return tuple([1 for _ in range(words_count)])


def _get_split_pattern(count: int) -> str:
    if count <= 4:
        return f'{count} слова'
    return f'{count} слов'


def _get_splitting_numbers(text: str,
                           default_splitting: Sequence[int]) -> Sequence[int]:
    """
    Проверяет корректность присланной разбивки текста
    """
    pattern = r'\d+'
    user_splitting_text = tuple([int(i) for i in re.findall(pattern, text)])

    flag = (sum(default_splitting) == sum(user_splitting_text))

    for i in user_splitting_text:
        if not flag:
            break
        flag = flag and i > 0

    if flag:
        return user_splitting_text

    raise NotCorrectSplittingText(
        'Сумма чисел в присланной разбивке не равна количеству слов в вашем '
        'тексте для стикера либо разбивка содержит недопустимые числа.\n'
        'Примеры валидной разбивки текста:\n'
        '"Текст из 2 строк" - "2, 2"\n'
        '"Текст из 3 строк" - "1, 2, 1"\n'
        '"Текст из 4 строк" - "1, 1, 1, 1"'
    )


def _get_str_splitting_numbers(numbers: Sequence[int]) -> str:
    str_splitting_numbers = re.sub(r'[()]', '', str(numbers))

    return str_splitting_numbers


def _get_splitting_text(text: str,
                        split_pattern: Sequence[int]) -> Sequence[str]:
    """
    Разбивает текст по шаблону
    """
    split_text = text.split()
    words = []
    index = 0

    for i in split_pattern:
        temp = []
        for _ in range(i):
            temp.append(split_text[index])
            index += 1
        words.append(' '.join(temp))

    return tuple(words)


def _generate_filename() -> str:
    """
    Генерирует уникальную строку для названия файла
    """
    return str(uuid.uuid4())


def _get_date_formatted(_datetime: datetime.datetime) -> str:
    """
    Возвращает дату строкой
    """
    return _datetime.strftime('%Y-%m-%d')
