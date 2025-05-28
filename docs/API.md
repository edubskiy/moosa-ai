# API Documentation

## Core Components

### Scraper

```python
from src.core.scraper import MENABytesNewsScraper

scraper = MENABytesNewsScraper()
articles = scraper.run()
```

#### Methods

- `run()`: Starts the scraping process and returns a list of articles
- `parse_article(url)`: Parses a single article by URL
- `extract_company_info(article)`: Extracts company information from an article

### Content Generator

```python
from src.core.generator import ContentGenerator

generator = ContentGenerator()
content = generator.generate(article, platform="telegram")
```

#### Methods

- `generate(article, platform)`: Generates content for the specified platform
- `format_content(content, style)`: Formats content according to style
- `add_hashtags(content, platform)`: Adds relevant hashtags

### Scheduler

```python
from src/core/scheduler import Scheduler

scheduler = Scheduler()
scheduler.schedule_job(time="09:00")
```

#### Methods

- `schedule_job(time)`: Schedules a daily job
- `run_job()`: Runs the scheduled job
- `stop()`: Stops the scheduler

## Storage

### Excel Tracker

```python
from src.storage.excel_tracker import ExcelContentTracker

tracker = ExcelContentTracker()
tracker.save_article(article)
```

#### Methods

- `save_article(article)`: Saves an article to Excel
- `save_content(content)`: Saves generated content
- `get_article(article_id)`: Gets an article by ID
- `get_content(content_id)`: Gets content by ID
- `export_content(content_id, path)`: Exports content to a file

### Google Sheets Tracker

```python
from src.storage.google_sheets_tracker import GoogleSheetsTracker

tracker = GoogleSheetsTracker()
tracker.save_article(article)
```

#### Methods

- `save_article(article)`: Saves an article to Google Sheets
- `save_content(content)`: Saves generated content
- `get_article(article_id)`: Gets an article by ID
- `get_content(content_id)`: Gets content by ID
- `export_content(content_id, path)`: Exports content to a file

## Content Generation

### Reel Generator

```python
from src.content.reel_generator import ReelGenerator

generator = ReelGenerator()
script = generator.generate(article)
```

#### Methods

- `generate(article)`: Generates a script for Reels
- `format_script(script)`: Formats the script
- `add_visual_suggestions(script)`: Adds visual suggestions

### Style Configuration

```python
from src.content.style_config import StyleConfig

config = StyleConfig()
style = config.get_style("expert_analyst")
```

#### Methods

- `get_style(style_name)`: Gets style settings
- `update_style(style_name, settings)`: Updates style settings
- `get_platform_style(platform)`: Gets style for a platform

## Utils

### Article Tracker

```python
from src.utils.article_tracker import ArticleTracker

tracker = ArticleTracker()
is_processed = tracker.is_processed(article_id)
```

#### Methods

- `is_processed(article_id)`: Checks if an article is processed
- `mark_as_processed(article_id)`: Marks an article as processed
- `get_processing_history(article_id)`: Gets processing history

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

All components use standard Python exceptions:

- `ValueError`: Invalid input
- `ConnectionError`: Connection issues
- `PermissionError`: File access issues
- `KeyError`: Missing configuration keys

## Logging

All components use the standard logging module:

```python
import logging

logger = logging.getLogger(__name__)
logger.info("Message")
logger.error("Error message")
```

Logs are saved in the `logs/` directory with appropriate prefixes:
- `scraper.log`
- `generator.log`
- `scheduler.log`
- `tracker.log` 