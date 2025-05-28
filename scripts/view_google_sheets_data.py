import pandas as pd
import argparse
from google_sheets_tracker import GoogleSheetsTracker

def view_google_sheets_data(show_content=False, article_id=None, content_id=None):
    """Просмотр данных из Google Sheets
    
    Args:
        show_content (bool): Показывать ли полный контент
        article_id (str): ID статьи для фильтрации
        content_id (str): ID контента для фильтрации
    """
    tracker = GoogleSheetsTracker()
    
    # Загружаем данные из всех листов
    try:
        articles_df = tracker._get_worksheet_as_df('Статьи')
        content_df = tracker._get_worksheet_as_df('Контент')
        schedule_df = tracker._get_worksheet_as_df('Планирование')
        metadata_df = tracker._get_worksheet_as_df('Метаданные')
        reels_df = tracker._get_worksheet_as_df('Reels')
        logs_df = tracker._get_worksheet_as_df('Логи')
        
        # Фильтруем по article_id, если указан
        if article_id:
            articles_df = articles_df[articles_df['article_id'] == article_id]
            content_df = content_df[content_df['article_id'] == article_id]
            reels_df = reels_df[reels_df['article_id'] == article_id]
            logs_df = logs_df[logs_df['article_id'] == article_id]
        
        # Фильтруем по content_id, если указан
        if content_id:
            content_df = content_df[content_df['content_id'] == content_id]
            schedule_df = schedule_df[schedule_df['content_id'] == content_id]
            logs_df = logs_df[logs_df['content_id'] == content_id]
        
        print("\n=== СТАТЬИ ===")
        if len(articles_df) > 0:
            print(f"Всего статей: {len(articles_df)}")
            for i, row in articles_df.iterrows():
                print(f"\n{i+1}. {row['title']}")
                print(f"   ID: {row['article_id']}")
                print(f"   Категория: {row['category']}")
                print(f"   Компания: {row['company_name']}")
                print(f"   Финансирование: {row['funding_amount']}")
                print(f"   Дата обработки: {row['processing_date']}")
                
                if show_content and 'article_content' in row and row['article_content']:
                    print(f"\n   СОДЕРЖАНИЕ СТАТЬИ:")
                    print(f"   {'-'*50}")
                    print(f"   {row['article_content']}")
                    print(f"   {'-'*50}")
        else:
            print("Статей не найдено")
        
        print("\n=== КОНТЕНТ ===")
        if len(content_df) > 0:
            print(f"Всего контента: {len(content_df)}")
            for i, row in content_df.iterrows():
                print(f"\n{i+1}. {row['title']} ({row['language']})")
                print(f"   ID: {row['content_id']}")
                print(f"   Тип: {row['content_type']}")
                print(f"   Платформа: {row['platform']}")
                print(f"   Статус: {row['status']}")
                
                if 'scheduled_date' in row and row['scheduled_date']:
                    print(f"   Запланировано на: {row['scheduled_date']} {row['scheduled_time']}")
                
                if show_content and 'content_markdown' in row and row['content_markdown']:
                    print(f"\n   СОДЕРЖАНИЕ:")
                    print(f"   {'-'*50}")
                    print(f"   {row['content_markdown']}")
                    print(f"   {'-'*50}")
        else:
            print("Контента не найдено")
        
        print("\n=== REELS ===")
        if len(reels_df) > 0:
            print(f"Всего скриптов для Reels: {len(reels_df)}")
            for i, row in reels_df.iterrows():
                print(f"\n{i+1}. {row['title']}")
                print(f"   ID: {row['reel_id']}")
                print(f"   ID статьи: {row['article_id']}")
                print(f"   Дата создания: {row['creation_date']}")
                print(f"   Статус: {row['status']}")
                
                if show_content and 'script_markdown' in row and row['script_markdown']:
                    print(f"\n   СКРИПТ:")
                    print(f"   {'-'*50}")
                    print(f"   {row['script_markdown']}")
                    print(f"   {'-'*50}")
        else:
            print("Скриптов для Reels не найдено")
        
        print("\n=== РАСПИСАНИЕ ===")
        if len(schedule_df) > 0:
            print(f"Всего запланировано: {len(schedule_df)}")
            for i, row in schedule_df.iterrows():
                print(f"\n{i+1}. {row['platform']}")
                print(f"   ID расписания: {row['schedule_id']}")
                print(f"   ID контента: {row['content_id']}")
                print(f"   Дата: {row['scheduled_date']}")
                print(f"   Время: {row['scheduled_time']}")
                print(f"   Статус: {row['posting_status']}")
                print(f"   Аккаунт: {row['posting_account']}")
        else:
            print("Запланированных публикаций не найдено")
        
        print("\n=== ЛОГИ ===")
        if len(logs_df) > 0:
            print(f"Всего записей в логе: {len(logs_df)}")
            for i, row in logs_df.iterrows():
                print(f"\n{i+1}. {row['timestamp']} - {row['log_type']}")
                print(f"   Сообщение: {row['message']}")
                if 'article_id' in row and row['article_id']:
                    print(f"   ID статьи: {row['article_id']}")
                if 'content_id' in row and row['content_id']:
                    print(f"   ID контента: {row['content_id']}")
        else:
            print("Записей в логе не найдено")
        
        print("\n=== МЕТАДАННЫЕ ===")
        if len(metadata_df) > 0:
            for i, row in metadata_df.iterrows():
                print(f"{row['key']}: {row['value']}")
        else:
            print("Метаданных не найдено")
            
    except Exception as e:
        print(f"Ошибка при чтении данных из Google Sheets: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Просмотр данных из Google Sheets')
    parser.add_argument('--show-content', action='store_true', help='Показывать полный контент')
    parser.add_argument('--article-id', type=str, help='ID статьи для фильтрации')
    parser.add_argument('--content-id', type=str, help='ID контента для фильтрации')
    
    args = parser.parse_args()
    
    view_google_sheets_data(args.show_content, args.article_id, args.content_id) 