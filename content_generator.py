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
    
    def select_best_article(self, articles):
        """Select the best article for content generation"""
        if not articles:
            return None
            
        # Filter articles with full content
        articles_with_content = [article for article in articles if 'content' in article and article['content']]
        
        if not articles_with_content:
            logger.warning("No articles with content found")
            return None
            
        # Score articles based on various factors
        scored_articles = []
        for article in articles_with_content:
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
        best_article = scored_articles[0][0]
        logger.info(f"Selected best article: {best_article['title']}")
        return best_article
    
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
        """Generate Russian content using OpenAI API"""
        if not openai.api_key:
            logger.error("OpenAI API key not set")
            return self.generate_russian_content_without_ai(article_info)
            
        try:
            # Prepare the prompt
            prompt = f"""
            Ты - эксперт по созданию контента о стартапах и технологиях для социальных сетей. 
            Напиши пост в стиле основателя технологического стартапа, поэта и маркетолога.
            
            Информация о статье:
            Заголовок: {article_info['title']}
            Компания: {article_info['company_name']}
            Сумма инвестиций: {article_info['funding_amount']}
            Локация: {article_info['location']}
            Краткое содержание: {article_info['content_summary']}
            
            Требования к посту:
            1. Пост должен быть на русском языке
            2. Начни с эмоционального приветствия и эмодзи
            3. Используй вдохновляющий, энергичный тон
            4. Добавь свое экспертное мнение о перспективах стартапа
            5. Заверши призывом к действию
            6. Используй эмодзи для выделения ключевых моментов
            7. Длина поста: 200-300 слов
            8. Добавь хэштеги в конце
            
            Пост будет публиковаться в Telegram, TenChat, VK и Дзен.
            Не упоминай, что это перевод или адаптация статьи.
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative content writer specializing in startup news."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            # Extract the generated content
            generated_content = response.choices[0].message.content.strip()
            logger.info("Successfully generated Russian content with AI")
            return generated_content
            
        except Exception as e:
            logger.error(f"Error generating Russian content with AI: {e}")
            return self.generate_russian_content_without_ai(article_info)
    
    def generate_english_content_with_ai(self, article_info):
        """Generate English content using OpenAI API"""
        if not openai.api_key:
            logger.error("OpenAI API key not set")
            return self.generate_english_content_without_ai(article_info)
            
        try:
            # Prepare the prompt
            prompt = f"""
            You are an expert in creating content about startups and technology for social media.
            Write a post in the style of a tech startup founder, poet, and marketer.
            
            Article information:
            Title: {article_info['title']}
            Company: {article_info['company_name']}
            Investment amount: {article_info['funding_amount']}
            Location: {article_info['location']}
            Summary: {article_info['content_summary']}
            
            Requirements for the post:
            1. The post must be in English
            2. Start with an emotional greeting and emoji
            3. Use an inspiring, energetic tone
            4. Add your expert opinion on the startup's prospects
            5. End with a call to action
            6. Use emojis to highlight key points
            7. Length: 200-300 words
            8. Add hashtags at the end
            
            The post will be published on Medium, LinkedIn, Instagram, and Twitter.
            """
            
            # Call OpenAI API
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a creative content writer specializing in startup news."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            # Extract the generated content
            generated_content = response.choices[0].message.content.strip()
            logger.info("Successfully generated English content with AI")
            return generated_content
            
        except Exception as e:
            logger.error(f"Error generating English content with AI: {e}")
            return self.generate_english_content_without_ai(article_info)
    
    def generate_russian_content_without_ai(self, article_info):
        """Generate Russian content without using AI (fallback method)"""
        logger.info("Generating Russian content without AI")
        
        # Select random style elements
        tone = random.choice(STYLE_CONFIG["tone"])
        phrase = random.choice(STYLE_CONFIG["phrases"])
        
        # Generate intro
        action = "привлек инвестиции" if article_info['funding_amount'] else "запустил инновационный продукт"
        company = article_info['company_name'] if article_info['company_name'] else "этот стартап"
        intro_template = random.choice(STYLE_CONFIG["intro_templates"])
        intro = intro_template.format(company=company, action=action)
        
        # Generate body
        body_template = random.choice(STYLE_CONFIG["body_templates"])
        
        # Generate content for body template
        reason = "Это решение может изменить индустрию и создать новые возможности для бизнеса"
        point1 = "Инновационный подход к решению проблемы"
        point2 = "Сильная команда с опытом в индустрии"
        point3 = "Растущий рынок с большим потенциалом"
        
        special_feature = "Уникальное сочетание технологий и понимания потребностей пользователей"
        reason1 = "Решает реальную проблему пользователей"
        reason2 = "Имеет масштабируемую бизнес-модель"
        
        analysis = "Проект имеет все шансы на успех благодаря фокусу на конкретной нише и глубокому пониманию потребностей клиентов"
        potential = "Высокий, с возможностью международной экспансии"
        
        poetic_view = "Искру инноваций, которая может разжечь пламя технологической революции"
        business_view = "Прочную бизнес-модель с ясным путем к масштабированию"
        
        # Fill in the body template with appropriate values
        body = body_template.format(
            reason=reason,
            point1=point1,
            point2=point2,
            point3=point3,
            special_feature=special_feature,
            reason1=reason1,
            reason2=reason2,
            analysis=analysis,
            potential=potential,
            poetic_view=poetic_view,
            business_view=business_view
        )
        
        # Add article title and summary
        article_info_text = f"\n\n**{article_info['title']}**\n\n{article_info['content_summary'][:200]}...\n\n"
        
        # Generate conclusion
        conclusion = random.choice(STYLE_CONFIG["conclusion_templates"])
        
        # Select hashtags
        hashtags = random.choice(STYLE_CONFIG["hashtags"])
        
        # Combine all parts
        content = f"{intro}\n\n{phrase}{article_info_text}{body}\n\n{conclusion}\n\n{hashtags}"
        
        return content
    
    def generate_english_content_without_ai(self, article_info):
        """Generate English content without using AI (fallback method)"""
        logger.info("Generating English content without AI")
        
        # English versions of style elements
        english_intros = [
            "🚀 Friends! Today I want to share an interesting story about a startup that {action}.",
            "💡 Innovation never sleeps! Today we're focusing on {company}, which {action}.",
            "🔥 Hot news from the startup world! {company} has just {action}.",
            "👨‍💻 Tech entrepreneurs are amazing again! {company} {action}.",
            "🌟 Inspiring story of the day: how {company} {action}."
        ]
        
        english_phrases = [
            "Innovation changes the world!",
            "The technologies of the future are already here!",
            "The startup ecosystem is developing rapidly!",
            "Entrepreneurs who change the rules of the game!",
            "An inspiring success story!",
            "A revolutionary solution for the market!"
        ]
        
        english_conclusions = [
            "What do you think about the future of this startup? Share your opinions in the comments! 💬",
            "Stay tuned! The technological revolution continues! 🚀",
            "Follow the channel to stay updated on the most interesting stories from the world of startups! ✨",
            "Which innovative projects inspire you? Share in the comments! 🔥",
            "Want to learn more about similar projects? Like and share with friends! 👍"
        ]
        
        english_hashtags = [
            "#startups #innovation #technology",
            "#business #investment #startup",
            "#technology #future #innovation",
            "#entrepreneurship #startups #success",
            "#venturecapital #technology #innovation",
            "#fintech #startups #technology"
        ]
        
        # Generate intro
        action = "raised investment" if article_info['funding_amount'] else "launched an innovative product"
        company = article_info['company_name'] if article_info['company_name'] else "this startup"
        intro = random.choice(english_intros).format(company=company, action=action)
        
        # Select random elements
        phrase = random.choice(english_phrases)
        
        # Generate body
        body = f"""
{phrase}

**{article_info['title']}**

{article_info['content_summary'][:200]}...

Why is this important? This solution can change the industry and create new business opportunities.

Key points:
✅ Innovative approach to problem-solving
✅ Strong team with industry experience
✅ Growing market with great potential

My analysis as a founder:
This project has every chance of success due to its focus on a specific niche and deep understanding of customer needs.

Growth potential: ⭐⭐⭐⭐⭐
        """
        
        # Generate conclusion
        conclusion = random.choice(english_conclusions)
        
        # Select hashtags
        hashtags = random.choice(english_hashtags)
        
        # Combine all parts
        content = f"{intro}\n\n{body}\n\n{conclusion}\n\n{hashtags}"
        
        return content
    
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
    
    def run(self):
        """Main method to run the content generator"""
        logger.info("Starting content generation")
        
        # Load articles
        articles = self.load_latest_articles()
        if not articles:
            logger.error("No articles available for content generation")
            return
            
        # Select the best article
        best_article = self.select_best_article(articles)
        if not best_article:
            logger.error("Could not select a suitable article")
            return
            
        # Create directory for this article
        article_dir = self.create_article_directory(best_article)
        
        # Save original article info
        self.save_article_info(article_dir, best_article)
        
        # Extract key information
        article_info = self.extract_key_info(best_article)
        
        # Generate Russian content
        russian_content = self.generate_russian_content_with_ai(article_info)
        russian_file = self.save_content(article_dir, russian_content, "russian.md")
        
        # Generate English content
        english_content = self.generate_english_content_with_ai(article_info)
        english_file = self.save_content(article_dir, english_content, "english.md")
        
        # Set up log file for this article
        log_file = os.path.join(article_dir, "logs", "generation.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        logger.addHandler(file_handler)
        
        logger.info(f"Content generation completed successfully for article: {best_article['title']}")
        logger.info(f"Russian content saved to: {russian_file}")
        logger.info(f"English content saved to: {english_file}")
        
        # Remove the file handler to avoid duplicate logs
        logger.removeHandler(file_handler)
        
        return article_dir

if __name__ == "__main__":
    generator = ContentGenerator()
    generator.run() 