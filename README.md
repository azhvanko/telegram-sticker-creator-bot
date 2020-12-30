# telegram-sticker-creator-bot
Данный бот поможет вам создать текстовый стикер для Telegram.  
Пример работающего бота - [@textStickerCreatorBot](https://t.me/textStickerCreatorBot)  

---

# Начало работы с ботом

### Устанавливаем/обновляем Python

Для работы с ботом потребуется наличие Python 3.8 и выше.
Проверить версию можно через команду в терминале `python3 -V` или `python -V`.

    $ python3
    Python 3.8.7

### Создаём папку проекта

    $ mkdir telegram-sticker-creator-bot
    $ cd telegram-sticker-creator-bot

### Клонируем/загружаем этот репозиторий

    $ git clone https://github.com/azhvanko/telegram-sticker-creator-bot.git

### Создаём и активируем виртуальное окружение

    $ python -m venv venv
    $ source venv/bin/activate

### Устанавливаем сторонние пакеты

    (venv) $ pip install -r requirements.txt

### Обновляем информацию о шрифтах в `core/fonts/__init__.py`

    FONTS: {...}            # Список ваших шрифтов
    DEFAULT_FONT: ...       # Шрифт по умолчанию
    EXAMPLE_FONTS_PATH: ... # Путь к изображению с примерами шрифтов

### Создаём бота в [@BotFather](https://t.me/BotFather)

Для того, чтобы создать бота в [@BotFather](https://t.me/BotFather) вам необходимо сначала отправить ему команду **/newbot**, далее ввести название бота и его адрес, который должен заканчиваться на `bot`.  
Полученный токен бота необходимо добавить в **ENV** переменную `BOT_TOKEN` в `Dockerfile`.

    ENV BOT_TOKEN="YOUR_TOKEN"

### Docker

Устанавливаем **Docker** и производим его первоначальную настройку как указано здесь - [Install Docker Engine](https://docs.docker.com/engine/install/).  
Далее переходим в директорию с проектом и выполняем следующие команды:

    $ docker build -t sticker_creator_bot .
    $ docker run --name tgbot -d sticker_creator_bot

### Полезные ссылки

Документация и связанные с aiogram ресурсы - [Official aiogram resources](https://docs.aiogram.dev/en/latest/)  
Официальная документация Telegram: Боты - [Telegram Bot API](https://core.telegram.org/bots/api)
