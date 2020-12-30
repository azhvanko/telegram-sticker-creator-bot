from core.utils.messages import _messages_map, get_message


def test_step_in_handler(handler):
    for step in _messages_map.keys():
        assert step in handler.steps


def test_step_in_messages_map(handler):
    for step in handler.steps:
        assert step in _messages_map


def test_unsupported_command():
    text = get_message('_', message_type='unsupported_command')
    assert text == ('Присланная команда не поддерживается на данном этапе '
                    'создания стикера')
