
class NotCreatedUserSession(Exception):
    """
    Попытка начать работу с ботом не с помощью стандартных стартовых команд
    """
    pass


class NotClosedUserSession(Exception):
    """
    Попытка создать новую пользовательскую сессию при незакрытой старой
    """
    pass


class NotCorrectRGBCode(Exception):
    """
    Некорректный RGB-код
    """
    pass


class NotCorrectFontNumber(Exception):
    """
    Некорректный номер шрифта из списка
    """
    pass


class NotCorrectSplittingText(Exception):
    """
    Некорректное разбиение пользовательского текста на слова
    """
    pass
