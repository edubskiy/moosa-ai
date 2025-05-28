# Content Creator Platform

Платформа для автоматизированного создания контента о стартапах в стиле Евгения Дубского.

## Особенности

- 🤖 AI-powered генерация контента
- 📊 Аналитический подход к контенту
- 📱 Поддержка множества платформ (Telegram, LinkedIn, Instagram)
- 🎥 Генерация скриптов для Instagram Reels
- 📅 Планирование публикаций
- 💾 Гибкое хранение (Excel/Google Sheets)
- 📈 Отслеживание метрик и аналитика

## Структура проекта

```
content-creator/
├── src/                    # Исходный код
│   ├── core/              # Основные компоненты
│   ├── storage/           # Системы хранения
│   ├── content/           # Генерация контента
│   └── utils/             # Вспомогательные функции
├── scripts/               # Скрипты для работы с данными
├── templates/             # Шаблоны контента
├── config/                # Конфигурационные файлы
├── docs/                  # Документация
├── tests/                 # Тесты
├── data/                  # Данные
├── media/                 # Медиафайлы
├── output/                # Выходные файлы
└── logs/                  # Логи
```

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/content-creator.git
cd content-creator
```

2. Создайте виртуальное окружение:
```bash
python -m venv python_env
source python_env/bin/activate  # Linux/Mac
# или
python_env\Scripts\activate  # Windows
```

3. Установите зависимости:
```bash
pip install -r requirements.txt
```

4. Настройте переменные окружения:
```bash
cp config/.env.example .env
# Отредактируйте .env файл
```

## Использование

Подробное руководство по использованию платформы находится в [docs/MANUAL.md](docs/MANUAL.md).

### Быстрый старт

1. Запуск полного процесса:
```bash
python main.py
```

2. Генерация контента для конкретной платформы:
```bash
python main.py --platform telegram --article-id <ID_статьи>
```

3. Генерация Reels:
```bash
python main.py --generate-reel --article-id <ID_статьи>
```

## Хранение данных

Платформа поддерживает два варианта хранения:

1. **Excel** (по умолчанию)
   - Локальное хранение
   - Простая интеграция
   - Подходит для небольших проектов

2. **Google Sheets**
   - Облачное хранение
   - Совместный доступ
   - Подходит для командной работы

## Автоматизация

Настройте автоматическую генерацию контента:
```bash
python src/core/scheduler.py
```

## Документация

- [Руководство пользователя](docs/MANUAL.md)
- [API документация](docs/API.md)
- [История изменений](CHANGELOG.md)

## Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функциональности
3. Внесите изменения
4. Создайте pull request

## Лицензия

MIT

## Контакты

Евгений Дубской
- Telegram: [@evgeniydubskiy](https://t.me/evgeniydubskiy)
- LinkedIn: [evgeniydubskiy](https://linkedin.com/in/evgeniydubskiy) 