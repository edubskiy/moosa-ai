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
        logging.FileHandler("generator.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ContentGenerator:
    """Class to generate content based on scraped articles"""
    
    def __init__(self):
        self.data_dir = "data"
        self.output_dir = "output"
        os.makedirs(self.output_dir, exist_ok=True)
        
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
    
    def select_best_article(self, articles):
        """Select the best article for content generation"""
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
                            funding_amount = f"${amount} million"
                    except:
                        pass
        
        # Extract location
        location = ""
        location_keywords = ['dubai', 'saudi', 'egypt', 'uae', 'qatar', 'bahrain', 'kuwait', 'oman', 'jordan', 'lebanon']
        for word in title.split():
            if word.lower() in location_keywords:
                location = word
                break
        
        return {
            'title': title,
            'company_name': company_name,
            'funding_amount': funding_amount,
            'location': location,
            'content_summary': '\n'.join(content[:3]) if content else ""
        }
    
    def generate_russian_content_with_ai(self, article_info):
        """Generate Russian content for Telegram and TenChat using OpenAI API"""
        if not self.api_key:
            logger.error("OpenAI API key not set")
            return self.generate_russian_content_without_ai(article_info)
            
        try:
            # Prepare the prompt
            prompt = f"""
            Создай пост для Telegram о стартапе. 
            
            Информация о стартапе:
            Название: {article_info.get('company_name', '')}
            Заголовок статьи: {article_info.get('title', '')}
            Сумма инвестиций: {article_info.get('funding_amount', '')}
            Краткое содержание: {article_info.get('content_summary', '')[:300]}
            
            Требования к посту:
            1. Пост должен быть на русском языке
            2. Структура: яркое начало → основная часть с фактами → заключение с призывом к действию
            3. Стиль: {get_style_element('tone', 'russian')}
            4. Длина: 150-200 слов
            5. Добавь эмодзи для визуального разделения
            6. В конце добавь рейтинг Дубского (от 1 до 5 ракет 🚀) и краткое обоснование
            7. Добавь 4-5 релевантных хэштегов
            8. Добавь призыв подписаться на канал: @https://t.me/evgeniydubskiy
            """
            
            # Call OpenAI API with new client format
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Ты опытный копирайтер, специализирующийся на создании контента о стартапах и технологиях."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            # Extract the response text
            content = response.choices[0].message.content.strip()
            
            logger.info(f"Generated Russian content with AI for {article_info['title']}")
            return content
            
        except Exception as e:
            logger.error(f"Error generating Russian content with AI: {str(e)}")
            return self.generate_russian_content_without_ai(article_info)
    
    def generate_english_content_with_ai(self, article_info):
        """Generate English content for LinkedIn and Medium using OpenAI API"""
        if not self.api_key:
            logger.error("OpenAI API key not set")
            return self.generate_english_content_without_ai(article_info)
            
        try:
            # Prepare the prompt
            prompt = f"""
            Create a post about a startup for LinkedIn and Medium. 
            
            Startup information:
            Name: {article_info.get('company_name', '')}
            Article title: {article_info.get('title', '')}
            Funding amount: {article_info.get('funding_amount', '')}
            Summary: {article_info.get('content_summary', '')[:300]}
            
            Requirements:
            1. The post should be in English
            2. Structure: attention-grabbing opening → main part with facts → conclusion with a call to action
            3. Style: {get_style_element('tone', 'english')}
            4. Length: 150-200 words
            5. Add emojis for visual separation
            6. At the end, add Dubskiy Rating (from 1 to 5 rockets 🚀) and a brief justification
            7. Add 4-5 relevant hashtags
            8. Add links to social media: Instagram: @https://www.instagram.com/erarta.ai/ and X: @https://x.com/evgeniydubskiy
            """
            
            # Call OpenAI API with new client format
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an experienced copywriter specializing in content about startups and technology."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            # Extract the response text
            content = response.choices[0].message.content.strip()
            
            logger.info(f"Generated English content with AI for {article_info['title']}")
            return content
            
        except Exception as e:
            logger.error(f"Error generating English content with AI: {str(e)}")
            return self.generate_english_content_without_ai(article_info)
    
    def generate_russian_content_without_ai(self, article_info):
        """Generate Russian content without using AI (fallback method)"""
        logger.info("Generating Russian content without AI")
        
        # Select random templates
        intro_template = random.choice(STYLE_CONFIG["intro_templates"])
        body_template = random.choice(STYLE_CONFIG["body_templates"])
        conclusion_template = random.choice(STYLE_CONFIG["conclusion_templates"])
        hashtags = random.choice(STYLE_CONFIG["hashtags"])
        
        # Get social media links for Russian content
        social_links = STYLE_CONFIG["social_links"]["russian"]
        
        # Generate Dubskiy Rating
        rating_info = self.generate_dubskiy_rating(article_info, "russian")
        
        # Fill in the templates
        company = article_info['company_name'] if article_info['company_name'] else "этот стартап"
        action = f"привлек {article_info['funding_amount']}" if article_info['funding_amount'] else "развивается"
        
        intro = intro_template.format(company=company, action=action)
        
        # Generate random content for body template
        reason = "Это решение может изменить индустрию и создать новые возможности для бизнеса"
        point1 = "Инновационный подход к решению проблемы"
        point2 = "Сильная команда с опытом в индустрии"
        point3 = "Растущий рынок с большим потенциалом"
        
        special_feature = "Уникальный подход к решению проблемы, который отличает их от конкурентов"
        reason1 = "Потенциал масштабирования на международные рынки"
        reason2 = "Сильная технологическая база и инновационный продукт"
        
        analysis = "Проект имеет все шансы на успех благодаря фокусу на конкретной нише и глубокому пониманию потребностей клиентов"
        potential = "⭐⭐⭐⭐⭐"
        
        poetic_view = "Революционное решение, которое меняет правила игры"
        business_view = "Сильная бизнес-модель с потенциалом быстрого роста"
        
        # Format body template with generated content
        body_content = {
            "reason": reason,
            "point1": point1, "point2": point2, "point3": point3,
            "special_feature": special_feature, "reason1": reason1, "reason2": reason2,
            "analysis": analysis, "potential": potential,
            "poetic_view": poetic_view, "business_view": business_view,
            "problem": "Существующие решения неэффективны и дороги",
            "solution": "Инновационный подход с использованием новых технологий",
            "innovation": "Применение ИИ и машинного обучения для оптимизации процессов",
            "prospects": "Расширение на новые рынки и развитие дополнительных функций",
            "market": "Быстрорастущий сегмент с большим потенциалом",
            "growth": "Ежегодный рост более 30%",
            "impact": "Изменение подхода к решению проблемы в индустрии",
            "situation": "Компания столкнулась с проблемой эффективности",
            "actions": "Внедрение новой технологии и оптимизация процессов",
            "result": "Увеличение производительности на 40% и снижение затрат",
            "insights": "Инновационные решения могут значительно повысить эффективность бизнеса",
            "before": "Низкая эффективность и высокие затраты",
            "after": "Оптимизированные процессы и снижение расходов",
            "growth_percentage": "40",
            "forecast": "Дальнейший рост и расширение на новые рынки"
        }
        
        try:
            body = body_template.format(**body_content)
        except KeyError as e:
            logger.warning(f"Missing key in body template: {e}")
            body = f"Почему это важно? {reason}\n\nКлючевые моменты:\n✅ {point1}\n✅ {point2}\n✅ {point3}"
        
        # Combine all parts
        content = f"{intro}\n\n{get_style_element('phrases', random.randint(0, len(STYLE_CONFIG['phrases'])-1))}\n\n**{article_info['title']}**\n\n{article_info['content_summary'][:200]}...\n\n{body}{rating_info}\n\n{conclusion_template}{social_links}\n{hashtags}%"
        
        return content
    
    def generate_english_content_without_ai(self, article_info):
        """Generate English content without using AI (fallback method)"""
        logger.info("Generating English content without AI")
        
        # Select random phrases and templates
        phrase = random.choice([
            "Innovation never sleeps!",
            "The future of technology is here!",
            "Startup ecosystem is evolving rapidly!",
            "Entrepreneurs who change the rules of the game!",
            "Inspiring success story!",
            "Revolutionary market solution!",
            "The future is being created today!",
            "Technology is the new oil!",
            "Investing in innovation is the path to success!",
            "Startups are the engine of progress!",
            "From idea to millions: the startup journey",
            "Technologies that solve real problems"
        ])
        
        # Get social media links for English content
        social_links = STYLE_CONFIG["social_links"]["english"]
        
        # Generate Dubskiy Rating
        rating_info = self.generate_dubskiy_rating(article_info, "english")
        
        # Get English hashtags
        hashtags = random.choice(STYLE_CONFIG["english_hashtags"])
        
        # Fill in the templates
        company = article_info['company_name'] if article_info['company_name'] else "this startup"
        action = f"raised {article_info['funding_amount']}" if article_info['funding_amount'] else "is developing"
        
        # Generate intro
        intro_templates = [
            f"💡 {phrase} Today we're focusing on {company}, which {action}.",
            f"🚀 Breakthrough in the tech world! {company} {action} and is changing the game.",
            f"💎 Found a gem for you! {company} {action} and deserves your attention.",
            f"🔍 My innovation radar detected: {company} {action}.",
            f"⚡️ Entrepreneurial energy in action! {company} {action}.",
            f"💰 Investment case of the day: {company} {action} and here's why it matters."
        ]
        intro = random.choice(intro_templates)
        
        # Generate body content
        reason = "This solution can change the industry and create new business opportunities."
        point1 = "Innovative approach to problem-solving"
        point2 = "Strong team with industry experience"
        point3 = "Growing market with great potential"
        
        body_templates = [
            f"Why is this important? {reason}\n\nKey points:\n✅ {point1}\n✅ {point2}\n✅ {point3}",
            f"My analysis as a founder:\nThis project has every chance of success due to its focus on a specific niche and deep understanding of customer needs.\n\nGrowth potential: ⭐⭐⭐⭐⭐",
            f"Three reasons why this is interesting:\n\n1️⃣ Innovative approach to solving real problems\n2️⃣ Strong team with proven expertise\n3️⃣ Significant market opportunity"
        ]
        body = random.choice(body_templates)
        
        # Generate conclusion
        conclusion_templates = [
            "Follow the channel to stay updated on the most interesting stories from the world of startups! ✨",
            "Like if you think such solutions are the future!",
            "What innovative projects inspire you? Share in the comments! 🔥",
            "Want to learn more about similar projects? Like and share with friends! 👍",
            "Innovation is the path to the future. Let's follow technology development together! 🌐"
        ]
        conclusion = random.choice(conclusion_templates)
        
        # Combine all parts
        content = f"{intro}\n\n\n{phrase}\n\n**{article_info['title']}**\n\n{article_info['content_summary'][:200]}...\n\n{body}{rating_info}\n\n{conclusion}{social_links}\n{hashtags}%"
        
        return content
    
    def generate_dubskiy_rating(self, article_info, language="russian"):
        """Generate Dubskiy Rating for a startup"""
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
        rating_level = next((level for level in rating_scale if level["score"] == score), rating_scale[2])  # Default to middle rating
        
        # Format the rating based on language
        if language == "english":
            return rating_config["english_format"].format(
                symbol=rating_level["symbol"],
                score=rating_level["score"],
                description=rating_level["english_description"]
            )
        else:
            return rating_config["format"].format(
                symbol=rating_level["symbol"],
                score=rating_level["score"],
                description=rating_level["description"]
            )
    
    def create_article_directory(self, article):
        """Create a directory for the article"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Create a safe title for directory name
        safe_title = ''.join(c if c.isalnum() or c in ' -_' else '_' for c in article['title'])
        safe_title = safe_title[:50]  # Limit length
        
        # Create directory path
        article_dir = os.path.join(self.output_dir, f"{today}_{safe_title}")
        os.makedirs(article_dir, exist_ok=True)
        
        # Create subdirectories
        os.makedirs(os.path.join(article_dir, "reels"), exist_ok=True)
        os.makedirs(os.path.join(article_dir, "logs"), exist_ok=True)
        
        return article_dir
    
    def save_content(self, article_dir, content, filename):
        """Save generated content to a file"""
        if not content:
            logger.error(f"No content to save for {filename}")
            return None
            
        filepath = os.path.join(article_dir, filename)
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Content saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving content to {filepath}: {e}")
            return None
    
    def save_article_info(self, article_dir, article):
        """Save the original article information"""
        filepath = os.path.join(article_dir, "article_info.json")
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(article, f, ensure_ascii=False, indent=2)
            logger.info(f"Article info saved to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving article info: {e}")
            return None
    
    def run(self, test_file=None):
        """Run the content generator"""
        # Load the latest articles
        articles = self.load_latest_articles(test_file)
        
        if not articles:
            logger.warning("No articles found to process")
            return
        
        # Select the best article for content generation
        best_article = self.select_best_article(articles)
        
        if not best_article:
            logger.warning("No suitable article found for content generation")
            return
        
        # Extract key information from the article
        article_info = self.extract_key_info(best_article)
        
        # Create directory for the article
        article_dir = self.create_article_directory(best_article)
        
        # Generate content in Russian
        logger.info("Generating Russian content")
        if self.api_key:
            russian_content = self.generate_russian_content_with_ai(article_info)
        else:
            russian_content = self.generate_russian_content_without_ai(article_info)
        
        # Save Russian content
        self.save_content(article_dir, russian_content, "telegram_post_ru.md")
        
        # Generate content in English
        logger.info("Generating English content")
        if self.api_key:
            english_content = self.generate_english_content_with_ai(article_info)
        else:
            english_content = self.generate_english_content_without_ai(article_info)
        
        # Save English content
        self.save_content(article_dir, english_content, "linkedin_post_en.md")
        
        # Generate Dubskiy rating
        russian_rating = self.generate_dubskiy_rating(article_info, "russian")
        english_rating = self.generate_dubskiy_rating(article_info, "english")
        
        # Save article info
        self.save_article_info(article_dir, best_article)
        
        # Mark article as processed
        self.tracker.mark_article_processed(best_article, article_dir)
        
        # Если трекер - это экземпляр ExcelContentTracker или GoogleSheetsTracker,
        # добавляем контент в соответствующую таблицу
        if isinstance(self.tracker, (ExcelContentTracker, GoogleSheetsTracker)):
            logger.info("Adding content to tracker")
            
            # Добавляем статью в трекер
            article_id = self.tracker.add_article(best_article, best_article.get('content', ''))
            
            # Добавляем русский контент
            russian_content_data = {
                'title': best_article['title'],
                'source_url': best_article.get('link', ''),
                'category': best_article.get('category', ''),
                'content_type': 'telegram_post',
                'language': 'ru',
                'platform': 'Telegram',
                'tags': '#стартапы #инновации #технологии #евгенийдубский #эрартаэйай',
                'dubskiy_rating': russian_rating,
                'notes': 'Автоматически сгенерированный пост'
            }
            
            russian_content_path = os.path.join(article_dir, "telegram_post_ru.md")
            if os.path.exists(russian_content_path):
                with open(russian_content_path, 'r', encoding='utf-8') as f:
                    russian_content_text = f.read()
                
                russian_content_id = self.tracker.add_content(
                    russian_content_data, 
                    article_id, 
                    russian_content_text
                )
                logger.info(f"Added Russian content with ID: {russian_content_id}")
            
            # Добавляем английский контент
            english_content_data = {
                'title': best_article['title'],
                'source_url': best_article.get('link', ''),
                'category': best_article.get('category', ''),
                'content_type': 'linkedin_post',
                'language': 'en',
                'platform': 'LinkedIn',
                'tags': '#analytics #businesscases #startupexperience #evgeniydubskiy #erartaai',
                'dubskiy_rating': english_rating,
                'notes': 'Automatically generated post'
            }
            
            english_content_path = os.path.join(article_dir, "linkedin_post_en.md")
            if os.path.exists(english_content_path):
                with open(english_content_path, 'r', encoding='utf-8') as f:
                    english_content_text = f.read()
                
                english_content_id = self.tracker.add_content(
                    english_content_data, 
                    article_id, 
                    english_content_text
                )
                logger.info(f"Added English content with ID: {english_content_id}")
        
        logger.info(f"Content generation completed for article: {best_article['title']}")
        return article_dir

if __name__ == "__main__":
    generator = ContentGenerator()
    generator.run() 