import os
import json
import uuid
import logging
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("google_sheets.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class GoogleSheetsTracker:
    """Класс для работы с Google Sheets для хранения и управления контентом"""
    
    def __init__(self, credentials_path=None, spreadsheet_id=None):
        """
        Инициализация трекера Google Sheets
        
        Args:
            credentials_path (str): Путь к JSON-файлу с учетными данными
            spreadsheet_id (str): ID таблицы Google Sheets
        """
        # Получаем значения из переменных окружения или используем переданные параметры
        self.credentials_path = credentials_path or os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH', 'credentials.json')
        self.spreadsheet_id = spreadsheet_id or os.getenv('GOOGLE_SHEETS_ID', '1bVeyg8ugQyCGp0QO5uWXW7V0xtNKvOZH0RLPcrD4_Eo')
        
        self.client = None
        self.spreadsheet = None
        
        # Подключаемся к Google Sheets
        self.connect()
        
        # Проверяем наличие необходимых листов и создаем их при необходимости
        self.ensure_sheets_exist()
    
    def connect(self):
        """Подключение к Google Sheets API"""
        try:
            # Определяем области доступа
            scope = ['https://spreadsheets.google.com/feeds',
                     'https://www.googleapis.com/auth/drive']
            
            # Авторизуемся с помощью учетных данных
            credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_path, scope)
            
            # Создаем клиент gspread
            self.client = gspread.authorize(credentials)
            
            # Открываем таблицу по ID
            self.spreadsheet = self.client.open_by_key(self.spreadsheet_id)
            
            logger.info(f"Успешное подключение к таблице: {self.spreadsheet.title}")
        
        except Exception as e:
            logger.error(f"Ошибка при подключении к Google Sheets: {e}")
            raise
    
    def ensure_sheets_exist(self):
        """Проверяет наличие необходимых листов и создает их при необходимости"""
        required_sheets = {
            'Статьи': [
                'article_id', 'title', 'source_url', 'category',
                'publication_date', 'company_name', 'funding_amount',
                'article_content', 'processing_date', 'processing_status'
            ],
            'Контент': [
                'content_id', 'article_id', 'title', 'source_url', 'category',
                'content_type', 'language', 'content_markdown', 'creation_date',
                'status', 'scheduled_date', 'scheduled_time', 'platform',
                'published_date', 'published_url', 'engagement_stats',
                'tags', 'dubskiy_rating', 'notes'
            ],
            'Reels': [
                'reel_id', 'article_id', 'title', 'script_markdown',
                'creation_date', 'status', 'video_url', 'notes'
            ],
            'Планирование': [
                'schedule_id', 'content_id', 'platform', 'scheduled_date',
                'scheduled_time', 'timezone', 'posting_status', 'priority',
                'campaign_id', 'posting_account'
            ],
            'Логи': [
                'log_id', 'article_id', 'content_id', 'log_type',
                'timestamp', 'message', 'details'
            ],
            'Метаданные': [
                'key', 'value'
            ]
        }
        
        # Получаем список существующих листов
        existing_sheets = [worksheet.title for worksheet in self.spreadsheet.worksheets()]
        
        for sheet_name, headers in required_sheets.items():
            if sheet_name not in existing_sheets:
                logger.info(f"Создание листа: {sheet_name}")
                worksheet = self.spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="26")
                worksheet.append_row(headers)
                
                # Форматирование заголовков
                cell_range = f'A1:{chr(65 + len(headers) - 1)}1'
                worksheet.format(cell_range, {
                    "textFormat": {"bold": True},
                    "horizontalAlignment": "CENTER"
                })
                
                # Устанавливаем ширину столбцов для текстовых полей
                for i, header in enumerate(headers):
                    if header in ['content_markdown', 'article_content', 'script_markdown', 'message', 'details']:
                        worksheet.set_column_width(i + 1, 400)  # Широкие столбцы для текста
                    else:
                        worksheet.set_column_width(i + 1, 150)  # Обычные столбцы
            else:
                logger.info(f"Лист {sheet_name} уже существует")
        
        # Инициализируем метаданные, если лист только что создан
        metadata_sheet = self.spreadsheet.worksheet('Метаданные')
        if metadata_sheet.row_count == 1:  # Только заголовки
            metadata = [
                ['last_update', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['version', '1.0'],
                ['api_keys', '{}'],
                ['default_settings', '{"default_time": "10:00", "default_timezone": "UTC+3"}'],
                ['platform_settings', '{}']
            ]
            for row in metadata:
                metadata_sheet.append_row(row)
    
    def _get_worksheet_as_df(self, sheet_name):
        """Получает данные листа в виде DataFrame"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            logger.error(f"Ошибка при получении данных из листа {sheet_name}: {e}")
            return pd.DataFrame()
    
    def _update_worksheet_from_df(self, sheet_name, df):
        """Обновляет лист данными из DataFrame"""
        try:
            worksheet = self.spreadsheet.worksheet(sheet_name)
            
            # Получаем заголовки
            headers = worksheet.row_values(1)
            
            # Очищаем лист, оставляя только заголовки
            if worksheet.row_count > 1:
                worksheet.delete_rows(2, worksheet.row_count)
            
            # Добавляем данные из DataFrame
            if not df.empty:
                # Преобразуем DataFrame в список списков для добавления в таблицу
                values = df[headers].fillna('').values.tolist()
                
                # Добавляем данные в таблицу
                if values:
                    worksheet.append_rows(values)
            
            return True
        except Exception as e:
            logger.error(f"Ошибка при обновлении листа {sheet_name}: {e}")
            return False
    
    def add_article(self, article_data, article_content=None):
        """Добавляет новую статью в таблицу"""
        # Генерируем уникальный ID
        article_id = str(uuid.uuid4())
        
        # Загружаем текущие данные
        articles_df = self._get_worksheet_as_df('Статьи')
        
        # Если передан контент статьи в виде словаря, преобразуем его в JSON строку
        if article_content and isinstance(article_content, dict):
            article_content = json.dumps(article_content, ensure_ascii=False)
        
        # Если передан контент статьи в виде списка строк, объединяем их
        if article_content and isinstance(article_content, list):
            article_content = "\n\n".join(article_content)
        
        # Создаем новую запись
        new_article = {
            'article_id': article_id,
            'title': article_data.get('title', ''),
            'source_url': article_data.get('link', ''),
            'category': article_data.get('category', ''),
            'publication_date': article_data.get('date', ''),
            'company_name': article_data.get('company_name', ''),
            'funding_amount': article_data.get('funding_amount', ''),
            'article_content': article_content or article_data.get('content', ''),
            'processing_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'processing_status': 'processed'
        }
        
        # Добавляем запись в DataFrame
        articles_df = pd.concat([articles_df, pd.DataFrame([new_article])], ignore_index=True)
        
        # Обновляем лист
        self._update_worksheet_from_df('Статьи', articles_df)
        
        # Обновляем метаданные
        self.update_metadata('last_update', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Добавляем запись в лог
        self.add_log(article_id=article_id, log_type='article_added', 
                    message=f"Добавлена новая статья: {article_data.get('title', '')}")
        
        return article_id
    
    def add_content(self, content_data, article_id, content_markdown=None):
        """Добавляет новый контент, связанный со статьей"""
        # Генерируем уникальный ID
        content_id = str(uuid.uuid4())
        
        # Загружаем текущие данные
        content_df = self._get_worksheet_as_df('Контент')
        
        # Если контент передан в виде пути к файлу, читаем его содержимое
        if not content_markdown and 'content_path' in content_data and os.path.exists(content_data['content_path']):
            try:
                with open(content_data['content_path'], 'r', encoding='utf-8') as f:
                    content_markdown = f.read()
            except Exception as e:
                logger.error(f"Ошибка при чтении файла контента: {e}")
        
        # Создаем новую запись
        new_content = {
            'content_id': content_id,
            'article_id': article_id,
            'title': content_data.get('title', ''),
            'source_url': content_data.get('source_url', ''),
            'category': content_data.get('category', ''),
            'content_type': content_data.get('content_type', ''),
            'language': content_data.get('language', ''),
            'content_markdown': content_markdown or '',
            'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'draft',
            'scheduled_date': '',
            'scheduled_time': '',
            'platform': content_data.get('platform', ''),
            'published_date': '',
            'published_url': '',
            'engagement_stats': '',
            'tags': content_data.get('tags', ''),
            'dubskiy_rating': content_data.get('dubskiy_rating', ''),
            'notes': content_data.get('notes', '')
        }
        
        # Добавляем запись в DataFrame
        content_df = pd.concat([content_df, pd.DataFrame([new_content])], ignore_index=True)
        
        # Обновляем лист
        self._update_worksheet_from_df('Контент', content_df)
        
        # Обновляем метаданные
        self.update_metadata('last_update', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Добавляем запись в лог
        self.add_log(article_id=article_id, content_id=content_id, log_type='content_added', 
                    message=f"Добавлен новый контент типа {content_data.get('content_type', '')} на языке {content_data.get('language', '')}")
        
        return content_id
    
    def add_reel(self, article_id, title, script_markdown, notes=''):
        """Добавляет новый скрипт для Instagram Reel"""
        # Генерируем уникальный ID
        reel_id = str(uuid.uuid4())
        
        # Загружаем текущие данные
        reels_df = self._get_worksheet_as_df('Reels')
        
        # Создаем новую запись
        new_reel = {
            'reel_id': reel_id,
            'article_id': article_id,
            'title': title,
            'script_markdown': script_markdown,
            'creation_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'status': 'draft',
            'video_url': '',
            'notes': notes
        }
        
        # Добавляем запись в DataFrame
        reels_df = pd.concat([reels_df, pd.DataFrame([new_reel])], ignore_index=True)
        
        # Обновляем лист
        self._update_worksheet_from_df('Reels', reels_df)
        
        # Обновляем метаданные
        self.update_metadata('last_update', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Добавляем запись в лог
        self.add_log(article_id=article_id, log_type='reel_added', 
                    message=f"Добавлен новый скрипт для Instagram Reel: {title}")
        
        return reel_id
    
    def add_log(self, log_type, message, article_id=None, content_id=None, details=None):
        """Добавляет новую запись в лог"""
        # Генерируем уникальный ID
        log_id = str(uuid.uuid4())
        
        # Загружаем текущие данные
        logs_df = self._get_worksheet_as_df('Логи')
        
        # Создаем новую запись
        new_log = {
            'log_id': log_id,
            'article_id': article_id or '',
            'content_id': content_id or '',
            'log_type': log_type,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'message': message,
            'details': json.dumps(details) if details else ''
        }
        
        # Добавляем запись в DataFrame
        logs_df = pd.concat([logs_df, pd.DataFrame([new_log])], ignore_index=True)
        
        # Обновляем лист
        self._update_worksheet_from_df('Логи', logs_df)
        
        return log_id
    
    def schedule_content(self, content_id, schedule_data):
        """Планирует публикацию контента"""
        # Генерируем уникальный ID для расписания
        schedule_id = str(uuid.uuid4())
        
        # Загружаем текущие данные
        schedule_df = self._get_worksheet_as_df('Планирование')
        content_df = self._get_worksheet_as_df('Контент')
        
        # Создаем новую запись в расписании
        new_schedule = {
            'schedule_id': schedule_id,
            'content_id': content_id,
            'platform': schedule_data.get('platform', ''),
            'scheduled_date': schedule_data.get('date', ''),
            'scheduled_time': schedule_data.get('time', ''),
            'timezone': schedule_data.get('timezone', 'UTC+3'),
            'posting_status': 'pending',
            'priority': schedule_data.get('priority', 'medium'),
            'campaign_id': schedule_data.get('campaign_id', ''),
            'posting_account': schedule_data.get('account', '')
        }
        
        # Добавляем запись в DataFrame расписания
        schedule_df = pd.concat([schedule_df, pd.DataFrame([new_schedule])], ignore_index=True)
        
        # Обновляем статус контента
        content_mask = content_df['content_id'] == content_id
        if any(content_mask):
            content_df.loc[content_mask, 'status'] = 'scheduled'
            content_df.loc[content_mask, 'scheduled_date'] = schedule_data.get('date', '')
            content_df.loc[content_mask, 'scheduled_time'] = schedule_data.get('time', '')
        
        # Обновляем листы
        self._update_worksheet_from_df('Планирование', schedule_df)
        self._update_worksheet_from_df('Контент', content_df)
        
        # Обновляем метаданные
        self.update_metadata('last_update', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        
        # Добавляем запись в лог
        article_id = ''
        if any(content_mask):
            article_id = content_df.loc[content_mask, 'article_id'].values[0]
        
        self.add_log(article_id=article_id, content_id=content_id, log_type='content_scheduled', 
                    message=f"Запланирована публикация контента на {schedule_data.get('date', '')} {schedule_data.get('time', '')}")
        
        return schedule_id
    
    def update_metadata(self, key, value):
        """Обновляет значение в метаданных"""
        metadata_df = self._get_worksheet_as_df('Метаданные')
        
        # Обновляем значение
        key_mask = metadata_df['key'] == key
        if any(key_mask):
            metadata_df.loc[key_mask, 'value'] = value
        else:
            # Добавляем новую запись, если ключ не существует
            metadata_df = pd.concat([metadata_df, pd.DataFrame([{'key': key, 'value': value}])], ignore_index=True)
        
        # Обновляем лист
        self._update_worksheet_from_df('Метаданные', metadata_df)
    
    def get_all_articles(self):
        """Возвращает все статьи из таблицы"""
        try:
            articles_df = self._get_worksheet_as_df('Статьи')
            return articles_df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Ошибка при чтении статей: {e}")
            return []
    
    def get_all_content(self):
        """Возвращает весь контент из таблицы"""
        try:
            content_df = self._get_worksheet_as_df('Контент')
            return content_df.to_dict(orient='records')
        except Exception as e:
            logger.error(f"Ошибка при чтении контента: {e}")
            return []
    
    def get_content_by_id(self, content_id):
        """Возвращает контент по его ID"""
        try:
            content_df = self._get_worksheet_as_df('Контент')
            content_mask = content_df['content_id'] == content_id
            if any(content_mask):
                return content_df[content_mask].to_dict(orient='records')[0]
            else:
                logger.warning(f"Контент с ID {content_id} не найден")
                return None
        except Exception as e:
            logger.error(f"Ошибка при чтении контента: {e}")
            return None
    
    def get_article_by_id(self, article_id):
        """Возвращает статью по её ID"""
        try:
            articles_df = self._get_worksheet_as_df('Статьи')
            article_mask = articles_df['article_id'] == article_id
            if any(article_mask):
                return articles_df[article_mask].to_dict(orient='records')[0]
            else:
                logger.warning(f"Статья с ID {article_id} не найдена")
                return None
        except Exception as e:
            logger.error(f"Ошибка при чтении статьи: {e}")
            return None
    
    def get_reels_by_article_id(self, article_id):
        """Возвращает все reels для указанной статьи"""
        try:
            reels_df = self._get_worksheet_as_df('Reels')
            reels_mask = reels_df['article_id'] == article_id
            if any(reels_mask):
                return reels_df[reels_mask].to_dict(orient='records')
            else:
                return []
        except Exception as e:
            logger.error(f"Ошибка при чтении reels: {e}")
            return []
    
    def get_logs_by_article_id(self, article_id):
        """Возвращает все логи для указанной статьи"""
        try:
            logs_df = self._get_worksheet_as_df('Логи')
            logs_mask = logs_df['article_id'] == article_id
            if any(logs_mask):
                return logs_df[logs_mask].to_dict(orient='records')
            else:
                return []
        except Exception as e:
            logger.error(f"Ошибка при чтении логов: {e}")
            return []
    
    def export_content_to_file(self, content_id, output_path):
        """Экспортирует контент в файл"""
        content = self.get_content_by_id(content_id)
        if content and content.get('content_markdown'):
            try:
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(content['content_markdown'])
                return True
            except Exception as e:
                logger.error(f"Ошибка при экспорте контента: {e}")
                return False
        return False
    
    def import_content_from_file(self, content_id, input_path):
        """Импортирует контент из файла"""
        if os.path.exists(input_path):
            try:
                with open(input_path, 'r', encoding='utf-8') as f:
                    content_markdown = f.read()
                
                content_df = self._get_worksheet_as_df('Контент')
                content_mask = content_df['content_id'] == content_id
                
                if any(content_mask):
                    content_df.loc[content_mask, 'content_markdown'] = content_markdown
                    self._update_worksheet_from_df('Контент', content_df)
                    return True
            except Exception as e:
                logger.error(f"Ошибка при импорте контента: {e}")
        return False 