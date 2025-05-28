import os
import json
import logging
import random
from datetime import datetime, timedelta
import openai
from dotenv import load_dotenv
from style_config import STYLE_CONFIG, get_style_element
from article_tracker import ArticleTracker
from excel_tracker import ExcelContentTracker
from google_sheets_tracker import GoogleSheetsTracker

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("reel_generator.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ReelGenerator:
    """Class to generate Instagram reel scripts based on startup content"""
    
    def __init__(self):
        self.data_dir = "data"
        self.output_dir = "output"
        self.reels_dir = os.path.join(self.output_dir, "reels")
        os.makedirs(self.reels_dir, exist_ok=True)
        
        # Initialize article tracker
        self.tracker = ArticleTracker()
        
        # Load OpenAI API key from environment variable
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            logger.warning("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
        else:
            self.client = openai.OpenAI(api_key=self.api_key)
    
    def load_latest_articles(self, test_file=None):
        """Load the latest scraped articles or from a test file if specified"""
        # If test file is provided, use it
        if test_file:
            logger.info(f"Using test file: {test_file}")
            try:
                with open(test_file, 'r', encoding='utf-8') as f:
                    articles = json.load(f)
                logger.info(f"Loaded {len(articles)} articles from test file {test_file}")
                return articles
            except Exception as e:
                logger.error(f"Error loading articles from test file: {e}")
                return None
        
        # Otherwise, use the normal flow
        today = datetime.now().strftime("%Y-%m-%d")
        tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        
        logger.info(f"Looking for articles with dates: today={today}, tomorrow={tomorrow}")
        
        # For testing purposes, try tomorrow's file first
        test_mode = True  # Set to True for testing with tomorrow's articles
        
        if test_mode:
            # Try tomorrow's date first (for testing)
            filename = os.path.join(self.data_dir, f"articles_{tomorrow}.json")
            logger.info(f"Test mode: Checking for tomorrow's file first: {filename}")
            
            if os.path.exists(filename):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        articles = json.load(f)
                    logger.info(f"Loaded {len(articles)} articles from {filename}")
                    return articles
                except Exception as e:
                    logger.error(f"Error loading articles: {e}")
        
        # Normal flow - try today's articles
        filename = os.path.join(self.data_dir, f"articles_{today}.json")
        logger.info(f"Checking for file: {filename}")
        
        if not os.path.exists(filename):
            logger.info(f"No articles found for today ({today})")
            return None
            
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                articles = json.load(f)
            logger.info(f"Loaded {len(articles)} articles from {filename}")
            return articles
        except Exception as e:
            logger.error(f"Error loading articles: {e}")
            return None
    
    def extract_key_info(self, article):
        """Extract key information from an article"""
        title = article['title']
        content = article['content'] if 'content' in article else []
        
        # Extract company name (improved heuristic)
        company_name = ""
        
        # First, try to find the company name in the first paragraph of content
        if content and len(content) > 0:
            first_para = content[0]
            words = first_para.split()
            for i, word in enumerate(words):
                if word.endswith(',') and i > 0 and words[i-1][0].isupper():
                    company_name = words[i-1]
                    break
        
        # If not found in first paragraph, look for specific patterns in title
        if not company_name:
            title_words = title.split()
            for i, word in enumerate(title_words):
                if i < len(title_words) - 1 and word[0].isupper() and title_words[i+1].lower() in ['raises', 'secures', 'gets', 'receives', 'announces', 'launches']:
                    company_name = word.strip("'s").strip(",").strip(".")
                    break
        
        # Look for "fintech startup X" pattern
        if not company_name:
            title_lower = title.lower()
            if "startup" in title_lower:
                startup_index = title_lower.find("startup")
                words_after = title[startup_index:].split()
                if len(words_after) > 1 and words_after[1][0].isupper():
                    company_name = words_after[1].strip("'s").strip(",").strip(".")
        
        # Fallback to first capitalized word not in stopwords
        if not company_name:
            stopwords = ['the', 'a', 'an', 'in', 'on', 'at', 'by', 'for', 'with', 'to', 'saudi', 'dubai', 'egypt', 'uae', 'fintech', 'startup']
            for word in title.split():
                if word[0].isupper() and word.lower() not in stopwords:
                    company_name = word.strip("'s").strip(",").strip(".")
                    break
        
        # Extract funding amount if present
        funding_amount = ""
        if 'million' in title.lower() or '$' in title:
            for i, word in enumerate(title.split()):
                if word.lower() == 'million' and i > 0:
                    try:
                        amount = title.split()[i-1]
                        if amount.startswith('$'):
                            funding_amount = amount
                        else:
                            funding_amount = f"${amount}"
                    except:
                        pass
        
        # Extract industry (simple heuristic)
        industry = ""
        industry_keywords = ['fintech', 'healthtech', 'edtech', 'proptech', 'ecommerce', 'saas', 'ai', 'blockchain']
        for keyword in industry_keywords:
            if keyword in title.lower() or any(keyword in p.lower() for p in content[:3] if p):
                industry = keyword
                break
        
        # If no specific industry found, use generic term
        if not industry:
            industry = "технологический сектор"
        
        return {
            'title': title,
            'company_name': company_name,
            'funding_amount': funding_amount,
            'industry': industry,
            'content_summary': '\n'.join(content[:3]) if content else ""
        }
    
    def generate_reel_script_with_ai(self, article_info):
        """Generate Instagram reel script using OpenAI API"""
        if not self.api_key:
            logger.error("OpenAI API key not set")
            return self.generate_reel_script_without_ai(article_info)
            
        try:
            # Prepare the prompt
            prompt = f"""
            Напиши сценарий для Instagram Reels о стартапе.
            
            Информация о стартапе:
            Название: {article_info['company_name']}
            Заголовок статьи: {article_info['title']}
            Сумма инвестиций: {article_info['funding_amount']}
            Индустрия: {article_info['industry']}
            Краткое содержание: {article_info['content_summary'][:300]}
            
            Требования к сценарию:
            1. Сценарий должен быть на русском языке
            2. Структура: цепляющее начало (hook) → основная часть → призыв к действию
            3. Начало должно привлечь внимание за первые 3 секунды
            4. Общая продолжительность ролика: 30-60 секунд
            5. Добавь идеи для визуального сопровождения
            6. Текст должен быть энергичным и вдохновляющим
            7. Формат ответа:
            
            HOOK: [текст для первых 3-5 секунд]
            
            ОСНОВНАЯ ЧАСТЬ: [основное содержание]
            
            ЗАКЛЮЧЕНИЕ: [призыв к действию]
            
            ВИЗУАЛЬНЫЕ ИДЕИ: [краткие идеи для визуального сопровождения]
            
            ХЭШТЕГИ: [5-7 релевантных хэштегов]
            """
            
            # Call OpenAI API with new client format
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты опытный копирайтер, специализирующийся на создании сценариев для Instagram Reels."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            # Extract the response text
            script = response.choices[0].message.content.strip()
            
            logger.info(f"Generated reel script with AI for {article_info['title']}")
            return script
            
        except Exception as e:
            logger.error(f"Error generating reel script with AI: {str(e)}")
            return self.generate_reel_script_without_ai(article_info)
    
    def generate_reel_script_without_ai(self, article_info):
        """Generate Instagram reel script without using AI (fallback method)"""
        logger.info("Generating reel script without AI")
        
        # Select random template that doesn't require 'metric' key
        templates = [t for t in STYLE_CONFIG["instagram_reel_templates"] if "metric" not in t["hook"]]
        if not templates:
            # If all templates require 'metric', use the first one and provide a default value
            template = STYLE_CONFIG["instagram_reel_templates"][0]
        else:
            template = random.choice(templates)
        
        # Fill in the template
        company = article_info['company_name'] if article_info['company_name'] else "этот стартап"
        industry = article_info['industry']
        amount = article_info['funding_amount'].replace('$', '') if article_info['funding_amount'] else "миллионы"
        
        # Generate interesting fact
        interesting_facts = [
            f"90% стартапов терпят неудачу в первый год",
            f"инвестиции в {industry} выросли на 200% за последний год",
            f"успешные стартапы проходят в среднем через 3 пивота",
            f"только 0.05% стартапов получают венчурное финансирование"
        ]
        interesting_fact = random.choice(interesting_facts)
        
        # Generate visualization
        visualizations = [
            f"команда {company} работает день и ночь над решением, которое изменит {industry}",
            f"инвесторы выстраиваются в очередь, чтобы вложиться в перспективный стартап",
            f"пользователи восторженно отзываются о новом продукте, который упрощает их жизнь"
        ]
        visualization = random.choice(visualizations)
        
        # Generate explanation
        explanations = [
            f"они создали уникальную технологию, которая решает проблему эффективности",
            f"их платформа соединяет поставщиков и потребителей напрямую, устраняя посредников",
            f"их алгоритм использует ИИ для оптимизации процессов"
        ]
        explanation = random.choice(explanations)
        
        # Generate secret
        secrets = [
            f"они фокусируются на реальной проблеме и предлагают простое решение",
            f"их команда состоит из экспертов с опытом в {industry}",
            f"они нашли уникальную нишу, которую игнорировали крупные игроки"
        ]
        secret = random.choice(secrets)
        
        # Additional variables that might be needed by some templates
        problem = "доступ к заработанным деньгам до дня зарплаты"
        solution = "интеграция с HR-системами компаний"
        result = "увеличение удержания сотрудников на 31%"
        before = "сотрудники ждали зарплату до конца месяца"
        after = "мгновенный доступ к заработанным средствам"
        future = "полноценная финансовая платформа для сотрудников"
        metric = "удержание персонала"
        percentage = "31"
        time_period = "6 месяцев"
        step1 = "анализ проблемы"
        step2 = "разработка решения"
        step3 = "интеграция с существующими системами"
        outcome = "рост удовлетворенности сотрудников"
        
        # Prepare format arguments with all possible variables
        format_args = {
            "interesting_fact": interesting_fact,
            "topic": industry,
            "company": company,
            "amount": amount,
            "visualization": visualization,
            "explanation": explanation,
            "secret": secret,
            "problem": problem,
            "solution": solution,
            "result": result,
            "before": before,
            "after": after,
            "future": future,
            "metric": metric,
            "percentage": percentage,
            "time_period": time_period,
            "step1": step1,
            "step2": step2,
            "step3": step3,
            "outcome": outcome
        }
        
        # Fill in the template safely
        try:
            hook = template["hook"].format(**format_args)
        except KeyError as e:
            logger.warning(f"Missing key in hook template: {e}")
            hook = f"Стартап за 30 секунд! {company} делает то, что изменит {industry}!"
            
        try:
            body = template["body"].format(**format_args)
        except KeyError as e:
            logger.warning(f"Missing key in body template: {e}")
            body = f"Вот как это работает: {explanation}. Представляете масштаб?"
        
        conclusion = template["conclusion"]
        
        # Get hashtags with required brand hashtags
        hashtags = random.choice(STYLE_CONFIG["hashtags"])
        
        # Get social media links
        social_links = STYLE_CONFIG["social_links"]["russian"]
        
        # Generate Dubskiy Rating
        rating_score = self.generate_dubskiy_rating_for_reel(article_info)
        
        script = f"""
HOOK: {hook}

ОСНОВНАЯ ЧАСТЬ: {body}

{rating_score}

ЗАКЛЮЧЕНИЕ: {conclusion}

ВИЗУАЛЬНЫЕ ИДЕИ: 
- Показать логотип и продукт компании
- Использовать анимированную инфографику для объяснения
- Включить эмоциональные реакции пользователей
- Визуализировать "Рейтинг Дубского" с анимацией появления ракет

{social_links}

ХЭШТЕГИ: {hashtags}
        """
        
        return script
    
    def generate_dubskiy_rating_for_reel(self, article_info):
        """Generate Dubskiy Rating for Instagram Reel"""
        # Determine rating score based on article info
        score = 3  # Default score
        
        # Adjust score based on funding amount
        if article_info['funding_amount']:
            try:
                # Extract numeric value from funding amount
                amount_str = article_info['funding_amount'].replace('$', '').replace(' million', '')
                amount = float(amount_str)
                if amount > 50:
                    score = 5
                elif amount > 20:
                    score = 4
                elif amount > 5:
                    score = 3
                else:
                    score = 2
            except:
                pass
                
        # Get rating info from style config
        rating_config = STYLE_CONFIG["dubskiy_rating"]
        rating_scale = rating_config["scale"]
        
        # Get the appropriate rating level
        rating_level = next((level for level in rating_scale if level["score"] == score), rating_scale[2])
        
        return f"РЕЙТИНГ ДУБСКОГО: {rating_level['symbol']} ({score}/5)\n{rating_level['description']}"
    
    def save_reel_script(self, script, article_title):
        """Save generated reel script to a file"""
        if not script:
            logger.error("No script to save")
            return
            
        # Create a safe filename
        safe_title = ''.join(c if c.isalnum() or c in ' -_' else '_' for c in article_title)
        safe_title = safe_title[:50]  # Limit length
        
        today = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(self.reels_dir, f"{today}_reel_{safe_title}.md")
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(script)
            logger.info(f"Reel script saved to {filename}")
            return filename
        except Exception as e:
            logger.error(f"Error saving reel script: {e}")
            return None
    
    def select_best_article(self, articles):
        """Select the best article for reel script generation"""
        if not articles:
            return None
            
        # Filter articles with full content
        articles_with_content = [article for article in articles if 'content' in article and article['content']]
        
        if not articles_with_content:
            logger.warning("No articles with content found")
            return None
            
        # Filter out already processed articles
        unprocessed_articles = [article for article in articles_with_content 
                               if not self.tracker.is_article_processed(article)]
        
        if not unprocessed_articles:
            logger.warning("All articles have already been processed")
            return None
            
        # Score articles based on various factors
        scored_articles = []
        for article in unprocessed_articles:
            score = 0
            
            # Score based on content length
            content_length = sum(len(p) for p in article['content'])
            if content_length > 2000:
                score += 3
            elif content_length > 1000:
                score += 2
            else:
                score += 1
                
            # Score based on keywords in title
            title_lower = article['title'].lower()
            important_keywords = ['million', 'funding', 'investment', 'launch', 'startup', 'innovation', 'technology']
            for keyword in important_keywords:
                if keyword in title_lower:
                    score += 1
            
            # Add to scored articles
            scored_articles.append((article, score))
            
        # Sort by score (descending)
        scored_articles.sort(key=lambda x: x[1], reverse=True)
        
        # Return the highest scored article
        if scored_articles:
            best_article = scored_articles[0][0]
            logger.info(f"Selected best article: {best_article['title']}")
            return best_article
        else:
            logger.warning("No suitable unprocessed articles found")
            return None
    
    def run(self, test_file=None):
        """Run the reel script generator"""
        # Load the latest articles
        articles = self.load_latest_articles(test_file)
        
        if not articles:
            logger.warning("No articles found to process")
            return
        
        # Select the best article for reel script generation
        best_article = self.select_best_article(articles)
        
        if not best_article:
            logger.warning("No suitable article found for reel script generation")
            return
        
        # Extract key information from the article
        article_info = self.extract_key_info(best_article)
        
        # Generate reel script
        logger.info("Generating Instagram Reel script")
        if self.api_key:
            reel_script = self.generate_reel_script_with_ai(article_info)
        else:
            reel_script = self.generate_reel_script_without_ai(article_info)
        
        # Generate Dubskiy rating for the reel
        dubskiy_rating = self.generate_dubskiy_rating_for_reel(article_info)
        
        # Save the reel script
        script_path = self.save_reel_script(reel_script, best_article['title'])
        
        logger.info(f"Reel script saved to: {script_path}")
        
        # Если трекер - это экземпляр ExcelContentTracker или GoogleSheetsTracker,
        # добавляем скрипт в соответствующую таблицу
        if isinstance(self.tracker, (ExcelContentTracker, GoogleSheetsTracker)):
            logger.info("Adding reel script to tracker")
            
            # Получаем ID статьи из трекера
            article_id = None
            
            # Сначала пытаемся найти статью по URL
            if 'link' in best_article and best_article['link']:
                articles_df = self.tracker.get_all_articles()
                if not articles_df.empty:
                    matching_articles = articles_df[articles_df['source_url'] == best_article['link']]
                    if not matching_articles.empty:
                        article_id = matching_articles.iloc[0]['article_id']
            
            # Если статья не найдена по URL, добавляем ее
            if not article_id:
                article_id = self.tracker.add_article(best_article, best_article.get('content', ''))
                logger.info(f"Added article to tracker with ID: {article_id}")
            
            # Добавляем скрипт для Instagram Reel
            reel_id = self.tracker.add_reel(
                article_id, 
                f"Instagram Reel: {best_article['title']}", 
                reel_script, 
                f"Dubskiy Rating: {dubskiy_rating}"
            )
            logger.info(f"Added reel script to tracker with ID: {reel_id}")
        
        logger.info(f"Reel script generation completed for article: {best_article['title']}")
        return script_path

if __name__ == "__main__":
    generator = ReelGenerator()
    generator.run() 