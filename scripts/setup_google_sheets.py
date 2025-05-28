#!/usr/bin/env python3
import os
import shutil
import json
import argparse
import sys

def setup_google_sheets():
    """Настройка интеграции с Google Sheets"""
    print("Настройка интеграции с Google Sheets...")
    
    # Проверяем наличие файла credentials.json.example
    if not os.path.exists('credentials.json.example'):
        print("Ошибка: Файл credentials.json.example не найден.")
        return False
    
    # Проверяем наличие файла credentials.json
    if os.path.exists('credentials.json'):
        overwrite = input("Файл credentials.json уже существует. Перезаписать? (y/n): ")
        if overwrite.lower() != 'y':
            print("Настройка отменена.")
            return False
    
    # Копируем файл примера
    print("Копирование файла credentials.json.example в credentials.json...")
    shutil.copy('credentials.json.example', 'credentials.json')
    
    # Запрашиваем данные для настройки
    print("\nДля настройки интеграции с Google Sheets необходимо выполнить следующие шаги:")
    print("1. Создайте проект в Google Cloud Console (https://console.cloud.google.com/)")
    print("2. Включите Google Sheets API и Google Drive API")
    print("3. Создайте учетные данные сервисного аккаунта")
    print("4. Скачайте JSON-файл с учетными данными")
    print("5. Создайте новую таблицу Google Sheets и предоставьте доступ сервисному аккаунту")
    print("6. Скопируйте ID таблицы из URL (часть между /d/ и /edit)")
    
    # Запрашиваем ID таблицы
    spreadsheet_id = input("\nВведите ID таблицы Google Sheets: ")
    
    # Запрашиваем путь к файлу с учетными данными
    credentials_file = input("Введите путь к скачанному JSON-файлу с учетными данными (оставьте пустым, чтобы использовать credentials.json): ")
    
    # Если указан путь к файлу, копируем его в credentials.json
    if credentials_file and os.path.exists(credentials_file):
        shutil.copy(credentials_file, 'credentials.json')
        print(f"Файл {credentials_file} скопирован в credentials.json")
    
    # Обновляем файл .env
    env_file = '.env'
    env_example = 'env.example'
    
    # Если .env не существует, но существует env.example, копируем его
    if not os.path.exists(env_file) and os.path.exists(env_example):
        shutil.copy(env_example, env_file)
    
    # Обновляем или добавляем переменные в .env
    env_vars = {}
    if os.path.exists(env_file):
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key] = value
    
    env_vars['GOOGLE_SHEETS_ID'] = spreadsheet_id
    env_vars['GOOGLE_SHEETS_CREDENTIALS_PATH'] = 'credentials.json'
    
    # Записываем обновленные переменные в .env
    with open(env_file, 'w', encoding='utf-8') as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")
    
    print(f"\nНастройки сохранены в файле {env_file}")
    print("ID таблицы Google Sheets:", spreadsheet_id)
    print("Путь к файлу учетных данных:", 'credentials.json')
    
    # Проверяем содержимое файла credentials.json
    try:
        with open('credentials.json', 'r', encoding='utf-8') as f:
            creds = json.load(f)
            if 'client_email' in creds:
                print("\nEmail сервисного аккаунта:", creds['client_email'])
                print("Не забудьте предоставить доступ к таблице для этого email!")
    except Exception as e:
        print(f"Ошибка при чтении файла credentials.json: {e}")
    
    print("\nНастройка завершена. Теперь вы можете запустить:")
    print("python main.py --google-sheets")
    print("или")
    print("python create_test_post_google.py")
    
    return True

def test_connection():
    """Тестирование подключения к Google Sheets"""
    try:
        from google_sheets_tracker import GoogleSheetsTracker
        
        print("Тестирование подключения к Google Sheets...")
        tracker = GoogleSheetsTracker()
        
        # Получаем заголовок таблицы
        title = tracker.spreadsheet.title
        print(f"Успешное подключение к таблице: {title}")
        
        # Получаем список листов
        sheets = [ws.title for ws in tracker.spreadsheet.worksheets()]
        print(f"Листы в таблице: {', '.join(sheets)}")
        
        return True
    except Exception as e:
        print(f"Ошибка при подключении к Google Sheets: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Настройка интеграции с Google Sheets')
    parser.add_argument('--test', action='store_true', help='Тестировать подключение к Google Sheets')
    
    args = parser.parse_args()
    
    if args.test:
        success = test_connection()
    else:
        success = setup_google_sheets()
    
    sys.exit(0 if success else 1) 