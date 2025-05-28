import os
import json
from datetime import datetime
import pandas as pd
from excel_tracker import ExcelContentTracker

def create_test_post():
    """Создает тестовый пост и добавляет его в Excel"""
    # Создаем тестовую статью
    article_data = {
        'title': 'Тестовая статья о стартапе',
        'link': 'https://example.com/test-article',
        'category': 'Fintech',
        'date': datetime.now().strftime('%Y-%m-%d'),
        'company_name': 'TestStartup',
        'funding_amount': '$5 million'
    }
    
    # Создаем тестовый контент статьи
    article_content = [
        "TestStartup, инновационный финтех-стартап, привлек $5 миллионов в раунде финансирования серии А, возглавляемом Venture Capital Partners.",
        "Основанный в 2023 году, TestStartup разрабатывает революционную платформу для цифровых платежей, которая упрощает финансовые операции для малого и среднего бизнеса.",
        "\"Наша миссия - сделать финансовые операции доступными и простыми для всех\", - говорит CEO компании. \"Это финансирование поможет нам расширить наши предложения и выйти на новые рынки\".",
        "Компания планирует использовать привлеченные средства для разработки новых функций и расширения команды."
    ]
    
    print("Подготовлены данные для тестовой статьи")
    
    # Создаем тестовый пост для Telegram на русском языке
    russian_post_content = """🚀 Прорыв в мире финтех! TestStartup привлек $5 миллионов.

Революционное решение для рынка!

**Тестовая статья о стартапе**

TestStartup, инновационный финтех-стартап, привлек $5 миллионов в раунде финансирования серии А, возглавляемом Venture Capital Partners.

Конкретный пример из практики:

🔍 Ситуация: Компания столкнулась с проблемой эффективности
🛠️ Действия: Внедрение новой технологии и оптимизация процессов
📈 Результат: Увеличение производительности на 40% и снижение затрат
💡 Выводы: Инновационные решения могут значительно повысить эффективность бизнеса

📊 **Рейтинг Дубского**: 🚀🚀🚀 (3/5)
Сильное решение с реальными бизнес-перспективами

Как вы думаете, какое будущее ждет этот стартап? Делитесь мнениями в комментариях! 💬

Подписывайтесь на мой Telegram канал: @https://t.me/evgeniydubskiy
#стартапы #инновации #технологии #евгенийдубский #эрартаэйай #erartaai"""
    
    print("Подготовлен тестовый пост на русском языке")
    
    # Создаем тестовый пост для LinkedIn на английском языке
    english_post_content = """⚡️ Entrepreneurial energy in action! TestStartup raised $5 million.

Entrepreneurs who change the rules of the game!

**Test article about a startup**

TestStartup, an innovative fintech startup, has raised $5 million in a Series A funding round led by Venture Capital Partners.

My analysis as a founder:
This project has every chance of success due to its focus on a specific niche and deep understanding of customer needs.

Growth potential: ⭐⭐⭐⭐⭐

📊 **Dubskiy Rating**: 🚀🚀🚀 (3/5)
Strong solution with real business prospects

Follow the channel to stay updated on the most interesting stories from the world of startups! ✨

Follow me on social media:
Instagram: @https://www.instagram.com/erarta.ai/
X: @https://x.com/evgeniydubskiy
#analytics #businesscases #startupexperience #evgeniydubskiy #erartaai"""
    
    print("Подготовлен тестовый пост на английском языке")
    
    # Создаем тестовый скрипт для Instagram Reel
    reel_script = """# Скрипт для Instagram Reel: TestStartup привлекает $5 миллионов

## Основные кадры:

### Кадр 1 (0-3 сек):
- **Визуал**: Логотип TestStartup с анимированным эффектом появления
- **Текст на экране**: "Финтех-революция: $5 млн инвестиций"
- **Голос за кадром**: "TestStartup привлек 5 миллионов долларов на революцию в финтех-индустрии!"

### Кадр 2 (3-6 сек):
- **Визуал**: Графики роста и диаграммы финансовых показателей
- **Текст на экране**: "Проблема: Сложные финансовые операции для бизнеса"
- **Голос за кадром**: "Малый бизнес ежедневно сталкивается с проблемами в финансовых операциях..."

### Кадр 3 (6-9 сек):
- **Визуал**: Демонстрация интерфейса платформы TestStartup
- **Текст на экране**: "Решение: Простая и доступная платформа"
- **Голос за кадром**: "Инновационная платформа TestStartup упрощает все финансовые процессы одним кликом!"

### Кадр 4 (9-12 сек):
- **Визуал**: Команда стартапа в офисе
- **Текст на экране**: "Основано в 2023 году"
- **Голос за кадром**: "Молодая команда с амбициозными планами уже привлекла внимание крупных инвесторов."

### Кадр 5 (12-15 сек):
- **Визуал**: Инфографика с планами развития
- **Текст на экране**: "Планы: расширение функций и команды"
- **Голос за кадром**: "Привлеченные средства пойдут на разработку новых функций и расширение команды."

### Финальный кадр (15-18 сек):
- **Визуал**: Логотип Евгения Дубского и призыв к действию
- **Текст на экране**: "Подписывайтесь на @evgeniydubskiy"
- **Голос за кадром**: "Следите за новостями стартапов вместе со мной! Ставьте лайк и подписывайтесь!"

## Музыка:
Энергичная, современная бизнес-музыка, создающая атмосферу инноваций и прогресса.

## Хэштеги:
#финтех #стартапы #инвестиции #бизнес #евгенийдубский #erartaai"""
    
    print("Подготовлен тестовый скрипт для Instagram Reel")
    
    # Создаем экземпляр трекера Excel
    tracker = ExcelContentTracker()
    
    # Добавляем статью в Excel вместе с контентом
    article_id = tracker.add_article(article_data, article_content)
    print(f"Статья добавлена в Excel с ID: {article_id}")
    
    # Добавляем русский пост в Excel
    russian_content_data = {
        'title': article_data['title'],
        'source_url': article_data['link'],
        'category': article_data['category'],
        'content_type': 'telegram_post',
        'language': 'ru',
        'platform': 'Telegram',
        'tags': '#стартапы #инновации #технологии #евгенийдубский #эрартаэйай',
        'dubskiy_rating': '3/5',
        'notes': 'Тестовый пост на русском языке'
    }
    
    russian_content_id = tracker.add_content(russian_content_data, article_id, russian_post_content)
    print(f"Русский пост добавлен в Excel с ID: {russian_content_id}")
    
    # Добавляем английский пост в Excel
    english_content_data = {
        'title': article_data['title'],
        'source_url': article_data['link'],
        'category': article_data['category'],
        'content_type': 'linkedin_post',
        'language': 'en',
        'platform': 'LinkedIn',
        'tags': '#analytics #businesscases #startupexperience #evgeniydubskiy #erartaai',
        'dubskiy_rating': '3/5',
        'notes': 'Тестовый пост на английском языке'
    }
    
    english_content_id = tracker.add_content(english_content_data, article_id, english_post_content)
    print(f"Английский пост добавлен в Excel с ID: {english_content_id}")
    
    # Добавляем скрипт для Instagram Reel
    reel_id = tracker.add_reel(article_id, "TestStartup привлекает $5 миллионов", reel_script, 
                              "Тестовый скрипт для демонстрации хранения в Excel")
    print(f"Скрипт для Instagram Reel добавлен в Excel с ID: {reel_id}")
    
    # Планируем публикацию русского поста
    schedule_data = {
        'platform': 'Telegram',
        'date': (datetime.now() + pd.Timedelta(days=1)).strftime('%Y-%m-%d'),
        'time': '10:00',
        'timezone': 'UTC+3',
        'priority': 'high',
        'account': '@evgeniydubskiy'
    }
    
    schedule_id = tracker.schedule_content(russian_content_id, schedule_data)
    print(f"Запланирована публикация русского поста с ID расписания: {schedule_id}")
    
    # Экспортируем контент для демонстрации
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # Экспортируем русский пост
    russian_export_path = os.path.join(output_dir, "exported_russian_post.md")
    tracker.export_content_to_file(russian_content_id, russian_export_path)
    print(f"Русский пост экспортирован в файл: {russian_export_path}")
    
    # Экспортируем английский пост
    english_export_path = os.path.join(output_dir, "exported_english_post.md")
    tracker.export_content_to_file(english_content_id, english_export_path)
    print(f"Английский пост экспортирован в файл: {english_export_path}")
    
    print("\nВсе данные успешно добавлены в Excel!")
    print(f"Путь к Excel-файлу: {tracker.excel_path}")

if __name__ == "__main__":
    create_test_post() 