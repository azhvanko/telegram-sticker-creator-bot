import os


TOKEN = os.getenv('BOT_TOKEN')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTENT_DIR = os.path.join(BASE_DIR, 'content')
FONTS_DIR = os.path.join(BASE_DIR, 'fonts')
LOGS_DIR = os.path.join(BASE_DIR, 'logs')


ACCESS_IDS = {
    "YOUR_IDS",
    "...",
}


USER_COMMANDS = {
    'START_COMMANDS': (
        'create_sticker',
    ),
    'SERVICE_COMMANDS': (
        'next_step',
        'step_back',
    ),
    'RESET_COMMANDS': (
        'start',
        'reset',
    )
}
ALL_USER_COMMANDS = [item for sublist in USER_COMMANDS.values() for item in sublist]
