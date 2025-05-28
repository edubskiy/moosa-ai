# Changelog

## [Unreleased]
### Added
- Интеграция с Google Sheets для хранения и управления контентом
- Класс GoogleSheetsTracker для работы с Google Sheets API
- Возможность выбора между Excel и Google Sheets для хранения контента
- Автоматическое создание и форматирование листов в Google Sheets
- Командная строка с опцией --google-sheets для выбора хранилища
- Скрипт setup_google_sheets.py для настройки интеграции с Google Sheets
- Поддержка переменных окружения для конфигурации Google Sheets
- Файл view_google_sheets_data.py для просмотра данных из Google Sheets

### Changed
- Обновлен файл setup.sh для поддержки Google Sheets
- Изменено имя виртуального окружения с venv на python_env

## [0.4.0] - 2025-05-14
### Added
- Хранение контента в формате Markdown непосредственно в Excel
- Хранение скриптов для Instagram Reels в Excel
- Система логирования в Excel
- Функции экспорта и импорта контента из Excel в файлы
- Расширенные возможности просмотра данных с фильтрацией

### Changed
- Переработана структура Excel-таблицы для хранения всего контента
- Улучшено форматирование Excel для удобного просмотра

## [0.3.0] - 2025-05-14
### Added
- Интеграция с Excel для хранения и управления контентом
- Система отслеживания статей и контента в Excel
- Планирование публикаций постов
- Метаданные для отслеживания изменений
- Скрипты для создания тестовых постов и просмотра данных

## [0.2.0] - 2025-05-13
### Added
- Организация выходных данных по папкам для каждой статьи
- Сохранение всех материалов (посты, reels, логи) в папке статьи
- Метаданные статьи в JSON формате
- Генерация контента на русском и английском языках

### Fixed
- Исправлена проблема с дублированием контента

## [0.1.0] - 2025-05-08
### Added
- Скрапер новостей с menabytes.com
- Генератор контента для социальных сетей
- Генератор скриптов для Instagram reels
- Планировщик для автоматизации
- Конфигурация стилей для настройки контента

## [1.3.0] - 2025-05-13

### Added
- Article tracking system to prevent duplicate content generation
- JSON database for storing information about processed articles
- Integration of article tracker with content and reel generators
- Improved company name extraction algorithm for more accurate content
- Support for filtering out already processed articles

### Changed
- Updated content generator to prioritize unprocessed articles
- Modified reel generator to check for previously processed content
- Enhanced article selection logic to consider processing history

## [1.2.0] - 2025-05-12

### Added
- Information style principles from Habr article on effective writing (https://habr.com/ru/companies/ttt/articles/203334/
https://marhr.ru/kak-pisat-teksty-dlya-soczsetej-v-kotorye-poveryat-sotrudniki-razbor-s-primerami/)
- Trust-building elements based on MarHR recommendations
- New post structure type for building trust with audience
- Case study format for Telegram posts
- Additional templates focused on concrete examples and real cases
- New Instagram reel template for showcasing real business metrics

### Changed
- Enhanced tone descriptors with "informative" and "concrete" values
- Added more fact-based signature phrases
- Expanded body templates with case study and data comparison formats
- Improved conclusion templates with engagement-focused questions

## [1.1.0] - 2025-05-10

### Added
- Enhanced style configuration system based on best practices from vc.ru article @https://vc.ru/marketing/519763-rukovodstvo-po-sozdaniyu-tekstov-dlya-socialnyh-setei-ot-strategii-do-oformleniya-publikacii 
- Brand DNA and Big Idea concepts for more consistent messaging
- Post structures for different content goals (привлечение, активация, удержание, продажа)
- Visual guidelines for consistent image styling
- Telegram-specific formats for different types of content
- Additional Instagram reel templates with improved structure
- More engaging call-to-action templates for post conclusions

### Changed
- Updated tone descriptors to focus more on expertise and trustworthiness
- Refined body templates with better visual structure and information hierarchy
- Improved hashtag selection for better discoverability
- Modified content voice from "founder" to "expert analyst" for better positioning

## [1.0.0] - 2025-05-08

### Added
- Initial release of Startup Content Creator
- Web scraper for MENABytes.com to collect startup news
- Content generator for Telegram and TenChat posts with customizable style
- Instagram Reel script generator with visual suggestions
- Automated scheduling system for daily content generation
- Style configuration system for personalized content
- Support for both AI-powered (OpenAI) and template-based content generation
- Command-line interface for running individual components or the full system
- Setup script for easy installation and configuration
