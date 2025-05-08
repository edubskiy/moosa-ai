import os
import json
import logging
import random
from datetime import datetime
import openai
from dotenv import load_dotenv
from style_config import STYLE_CONFIG, get_style_element

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
        
        # Load OpenAI API key from environment variable
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            logger.warning("OpenAI API key not found. Please set OPENAI_API_KEY environment variable.")
    
    def load_latest_articles(self):
        """Load the latest scraped articles"""
        today = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(self.data_dir, f"articles_{today}.json")
        
        if not os.path.exists(filename):
            logger.error(f"No articles found for today ({today})")
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
        
        # Extract company name (simple heuristic)
        company_name = ""
        for word in title.split():
            if word[0].isupper() and word.lower() not in ['the', 'a', 'an', 'in', 'on', 'at', 'by', 'for', 'with', 'to']:
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
        if not openai.api_key:
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
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative content writer specializing in Instagram Reels scripts about startups and technology."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            # Extract the generated content
            generated_content = response.choices[0].message.content.strip()
            logger.info("Successfully generated reel script with AI")
            return generated_content
            
        except Exception as e:
            logger.error(f"Error generating reel script with AI: {e}")
            return self.generate_reel_script_without_ai(article_info)
    
    def generate_reel_script_without_ai(self, article_info):
        """Generate Instagram reel script without using AI (fallback method)"""
        logger.info("Generating reel script without AI")
        
        # Select random template
        template = random.choice(STYLE_CONFIG["instagram_reel_templates"])
        
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
        
        # Fill in the template
        hook = template["hook"].format(
            interesting_fact=interesting_fact,
            topic=industry,
            company=company,
            amount=amount
        )
        
        body = template["body"].format(
            visualization=visualization,
            explanation=explanation,
            secret=secret,
            topic=industry
        )
        
        conclusion = template["conclusion"]
        
        # Combine all parts
        hashtags = random.choice(STYLE_CONFIG["hashtags"])
        
        script = f"""
HOOK: {hook}

ОСНОВНАЯ ЧАСТЬ: {body}

ЗАКЛЮЧЕНИЕ: {conclusion}

ВИЗУАЛЬНЫЕ ИДЕИ: 
- Показать логотип и продукт компании
- Использовать анимированную инфографику для объяснения
- Включить эмоциональные реакции пользователей

ХЭШТЕГИ: {hashtags}
        """
        
        return script
    
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
    
    def run(self):
        """Main method to run the reel generator"""
        logger.info("Starting Instagram reel script generation")
        
        # Load articles
        articles = self.load_latest_articles()
        if not articles:
            logger.error("No articles available for reel script generation")
            return
            
        # Get the first article with content
        article = next((a for a in articles if 'content' in a and a['content']), None)
        if not article:
            logger.error("No suitable article found for reel script generation")
            return
            
        # Extract key information
        article_info = self.extract_key_info(article)
        
        # Generate reel script
        script = self.generate_reel_script_with_ai(article_info)
        
        # Save script
        output_file = self.save_reel_script(script, article['title'])
        
        if output_file:
            logger.info(f"Reel script generation completed successfully. Output saved to {output_file}")
        else:
            logger.error("Reel script generation failed")

if __name__ == "__main__":
    generator = ReelGenerator()
    generator.run() 