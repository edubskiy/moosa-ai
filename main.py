#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import logging
import argparse
from datetime import datetime

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.scraper import MENABytesNewsScraper
from src.core.generator import ContentGenerator
from src.content.reel_generator import ReelGenerator
from src.storage.excel_tracker import ExcelContentTracker
from src.storage.google_sheets_tracker import GoogleSheetsTracker
from src.utils.article_tracker import ArticleTracker

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/main.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def setup_tracker(use_google_sheets=False):
    """Инициализация трекера контента"""
    if use_google_sheets:
        return GoogleSheetsTracker()
    return ExcelContentTracker()

def process_article(article, platform, tracker, generator, reel_generator):
    """Обработка одной статьи"""
    try:
        # Генерация контента
        content = generator.generate(article, platform)
        if content:
            tracker.save_content(content)
            logger.info(f"Сгенерирован контент для {platform}: {content.title}")

        # Генерация Reels
        if platform == "instagram":
            reel = reel_generator.generate(article)
            if reel:
                tracker.save_reel(reel)
                logger.info(f"Сгенерирован скрипт для Reels: {reel.title}")

        return True
    except Exception as e:
        logger.error(f"Ошибка при обработке статьи {article.id}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Startup Content Creator')
    parser.add_argument('--platform', choices=['telegram', 'linkedin', 'instagram'], 
                      help='Платформа для генерации контента')
    parser.add_argument('--article-id', help='ID статьи для обработки')
    parser.add_argument('--generate-reel', action='store_true', 
                      help='Генерация скрипта для Instagram Reels')
    parser.add_argument('--google-sheets', action='store_true',
                      help='Использовать Google Sheets вместо Excel')
    args = parser.parse_args()

    try:
        # Инициализация компонентов
        scraper = MENABytesNewsScraper()
        generator = ContentGenerator()
        reel_generator = ReelGenerator()
        tracker = setup_tracker(args.google_sheets)
        article_tracker = ArticleTracker()

        # Получение статей
        if args.article_id:
            articles = [tracker.get_article(args.article_id)]
        else:
            articles = scraper.run()

        # Обработка статей
        for article in articles:
            if article_tracker.is_processed(article.id):
                logger.info(f"Статья {article.id} уже обработана")
                continue

            if args.platform:
                # Обработка для конкретной платформы
                if process_article(article, args.platform, tracker, generator, reel_generator):
                    article_tracker.mark_as_processed(article.id)
            elif args.generate_reel:
                # Генерация только Reels
                reel = reel_generator.generate(article)
                if reel:
                    tracker.save_reel(reel)
                    article_tracker.mark_as_processed(article.id)
                    logger.info(f"Сгенерирован скрипт для Reels: {reel.title}")
            else:
                # Обработка для всех платформ
                platforms = ['telegram', 'linkedin', 'instagram']
                for platform in platforms:
                    if process_article(article, platform, tracker, generator, reel_generator):
                        article_tracker.mark_as_processed(article.id)

        logger.info("Обработка завершена успешно")

    except Exception as e:
        logger.error(f"Произошла ошибка: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 