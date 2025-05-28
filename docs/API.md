# API Documentation

## Core Components

### Scraper

```python
from src.core.scraper import MENABytesNewsScraper

scraper = MENABytesNewsScraper()
articles = scraper.run()
```

#### Methods

- `run()`: Запускает процесс скрапинга и возвращает список статей
- `parse_article(url)`: Парсит отдельную статью по URL
- `extract_company_info(article)`: Извлекает информацию о компании из статьи

### Content Generator

```python
from src.core.generator import ContentGenerator

generator = ContentGenerator()
content = generator.generate(article, platform="telegram")
```

#### Methods

- `generate(article, platform)`: Генерирует контент для указанной платформы
- `format_content(content, style)`: Форматирует контент согласно стилю
- `add_hashtags(content, platform)`: Добавляет релевантные хэштеги

### Scheduler

```python
from src.core.scheduler import Scheduler

scheduler = Scheduler()
scheduler.schedule_job(time="09:00")
```

#### Methods

- `schedule_job(time)`: Планирует ежедневное выполнение задачи
- `run_job()`: Выполняет запланированную задачу
- `stop()`: Останавливает планировщик

## Storage

### Excel Tracker

```python
from src.storage.excel_tracker import ExcelContentTracker

tracker = ExcelContentTracker()
tracker.save_article(article)
```

#### Methods

- `save_article(article)`: Сохраняет статью в Excel
- `save_content(content)`: Сохраняет сгенерированный контент
- `get_article(article_id)`: Получает статью по ID
- `get_content(content_id)`: Получает контент по ID
- `export_content(content_id, path)`: Экспортирует контент в файл

### Google Sheets Tracker

```python
from src.storage.google_sheets_tracker import GoogleSheetsTracker

tracker = GoogleSheetsTracker()
tracker.save_article(article)
```

#### Methods

- `save_article(article)`: Сохраняет статью в Google Sheets
- `save_content(content)`: Сохраняет сгенерированный контент
- `get_article(article_id)`: Получает статью по ID
- `get_content(content_id)`: Получает контент по ID
- `export_content(content_id, path)`: Экспортирует контент в файл

## Content Generation

### Reel Generator

```python
from src.content.reel_generator import ReelGenerator

generator = ReelGenerator()
script = generator.generate(article)
```

#### Methods

- `generate(article)`: Генерирует скрипт для Reels
- `format_script(script)`: Форматирует скрипт
- `add_visual_suggestions(script)`: Добавляет визуальные подсказки

### Style Configuration

```python
from src.content.style_config import StyleConfig

config = StyleConfig()
style = config.get_style("expert_analyst")
```

#### Methods

- `get_style(style_name)`: Получает настройки стиля
- `update_style(style_name, settings)`: Обновляет настройки стиля
- `get_platform_style(platform)`: Получает стиль для платформы

## Utils

### Article Tracker

```python
from src.utils.article_tracker import ArticleTracker

tracker = ArticleTracker()
is_processed = tracker.is_processed(article_id)
```

#### Methods

- `is_processed(article_id)`: Проверяет, обработана ли статья
- `mark_as_processed(article_id)`: Отмечает статью как обработанную
- `get_processing_history(article_id)`: Получает историю обработки

## Data Models

### Article

```python
class Article:
    id: str
    title: str
    url: str
    category: str
    publish_date: datetime
    company_name: str
    funding_amount: float
    content: str
    processed_date: datetime
    status: str
```

### Content

```python
class Content:
    id: str
    article_id: str
    title: str
    url: str
    category: str
    content_type: str
    language: str
    content: str
    created_date: datetime
    status: str
    scheduled_date: datetime
    scheduled_time: time
    platform: str
    published_date: datetime
    published_url: str
    engagement_stats: dict
    tags: list
    dubskiy_rating: int
    notes: str
```

### Reel

```python
class Reel:
    id: str
    article_id: str
    title: str
    script: str
    created_date: datetime
    status: str
    video_url: str
    notes: str
```

## Error Handling

Все компоненты используют стандартные исключения Python:

- `ValueError`: Некорректные входные данные
- `ConnectionError`: Проблемы с подключением
- `PermissionError`: Проблемы с доступом к файлам
- `KeyError`: Отсутствующие ключи в конфигурации

## Logging

Все компоненты используют стандартный модуль logging:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Message")
logger.error("Error message")
```

Логи сохраняются в директории `logs/` с соответствующими префиксами:
- `scraper.log`
- `generator.log`
- `scheduler.log`
- `tracker.log` 