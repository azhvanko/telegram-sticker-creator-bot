import functools
from dataclasses import dataclass, field
from typing import Callable, Optional, Sequence, Union

from core.types.answer import Answer
from core.types.close_session import CloseSession
from core.types.user_session import UserSession


@dataclass(frozen=True)
class SessionHandler:
    """
    Обработчик пользовательской сессии.
    Перед началом работы необходимо его инициализировать со списком шагов,
    необходимых для создания стикера
    """
    steps: Sequence
    first_step: int = 0
    functions_map: dict = field(default_factory=dict)

    def __post_init__(self):
        if isinstance(self.steps, Sequence) and self.first_step != 0:
            raise KeyError('Индекс первого шага д. б. равен 0')

    @property
    def last_step(self) -> int:
        return len(self.steps) - 1

    def register_function(self, alias: str) -> Callable:
        """
        Декоратор для регистрации функций-обработчиков
        """
        def function_decorator(func):
            if alias not in self.steps:
                raise KeyError(f'Псевдоним {alias} функции {func.__name__} не '
                               f'был добавлен в список steps')
            func.alias = alias
            self.functions_map[alias] = func

            @functools.wraps(func)
            def inner(self, *args, **kwargs):
                return func(self, *args, **kwargs)

            return inner

        return function_decorator

    def handle_session(self, user_session: UserSession,
                       message: Optional[str] = None) -> Sequence[Union[Answer, CloseSession]]:
        """
        В зависимости от номера шага в переданной сессии вызывает
        соответствующую ему функцию-обработчик
        """
        step_number = user_session.current_step
        func = self._get_step_handler(step_number)

        return func(user_session, message)

    def _get_step_handler(self, step_number: int) -> Callable:
        """
        Возвращает функцию-обработчик для шага по его номеру
        """
        function_alias = self.steps[step_number]
        func = self.functions_map[function_alias]

        return func

    def update_current_step(self, user_session: UserSession,
                            command: str = 'next_step') -> None:
        """
        Обновляет текущий шаг пользовательской сессии
        """
        if command == 'next_step':
            if user_session.current_step < self.last_step:
                user_session.current_step += 1
        elif command == 'step_back':
            if user_session.current_step > self.first_step:
                user_session.current_step -= 1
