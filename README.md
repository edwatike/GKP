# GrokBot

Telegram бот для автоматизации работы с Grok AI.

## Описание

GrokBot - это Telegram бот, который позволяет:
- Автоматизировать взаимодействие с Grok AI
- Управлять очередью запросов
- Отправлять и получать сообщения через Telegram

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/edwatike/grokbot.git
cd grokbot
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Создайте файл `.env` с необходимыми переменными окружения:
```
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## Использование

1. Запустите бота:
```bash
python main.py
```

2. Отправьте команду `/start` в Telegram для начала работы с ботом.

## Структура проекта

- `main.py` - основной файл бота
- `requirements.txt` - зависимости проекта
- `start_chrome.sh` - скрипт для запуска Chrome с новым профилем
- `prompt_queue.txt` - файл для хранения очереди запросов

## Лицензия

MIT 