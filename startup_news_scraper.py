import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class MENABytesNewsScraper:
    """Class to scrape startup news from MENABytes website"""
    
    def __init__(self):
        self.base_url = "https://www.menabytes.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        self.data_dir = "data"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def fetch_page(self, url):
        """Fetch HTML content from a URL"""
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logger.error(f"Error fetching {url}: {e}")
            return None
    
    def extract_articles(self, html):
        """Extract article data from HTML content"""
        if not html:
            return []
            
        soup = BeautifulSoup(html, 'html.parser')
        articles = []
        
        # Find all article elements (adjust selectors based on actual website structure)
        article_elements = soup.select('article') or soup.select('.post')
        
        for article in article_elements:
            try:
                # Extract title
                title_element = article.select_one('h2 a') or article.select_one('.entry-title a')
                if not title_element:
                    continue
                    
                title = title_element.text.strip()
                link = title_element.get('href')
                if not link.startswith('http'):
                    link = self.base_url + link
                
                # Extract category/tag if available
                category_element = article.select_one('.cat-links a') or article.select_one('.entry-meta .category')
                category = category_element.text.strip() if category_element else "Startup"
                
                # Extract date if available
                date_element = article.select_one('.posted-on time') or article.select_one('.entry-date')
                date = date_element.text.strip() if date_element else datetime.now().strftime("%Y-%m-%d")
                
                # Check if it's a startup-related article
                if self.is_startup_related(title, category):
                    articles.append({
                        'title': title,
                        'link': link,
                        'category': category,
                        'date': date
                    })
            except Exception as e:
                logger.error(f"Error extracting article data: {e}")
                continue
                
        return articles
    
    def is_startup_related(self, title, category):
        """Check if article is related to startups"""
        startup_keywords = [
            'startup', 'funding', 'investment', 'seed', 'series', 'venture', 'raised',
            'million', 'fintech', 'techstars', 'accelerator', 'incubator', 'founder',
            'entrepreneur', 'launch', 'acquisition', 'exit'
        ]
        
        title_lower = title.lower()
        category_lower = category.lower()
        
        # Check if any keyword is in the title or category
        return any(keyword in title_lower or keyword in category_lower for keyword in startup_keywords)
    
    def get_article_details(self, url):
        """Get detailed content from an article page"""
        html = self.fetch_page(url)
        if not html:
            return None
            
        soup = BeautifulSoup(html, 'html.parser')
        
        try:
            # Extract article content
            content_element = soup.select_one('.entry-content') or soup.select_one('article .content')
            if not content_element:
                return None
                
            # Extract paragraphs
            paragraphs = [p.text.strip() for p in content_element.find_all('p') if p.text.strip()]
            
            # Extract main image if available
            image_element = soup.select_one('.post-thumbnail img') or soup.select_one('.entry-content img')
            image_url = image_element.get('src') if image_element else None
            
            return {
                'content': paragraphs,
                'image_url': image_url
            }
        except Exception as e:
            logger.error(f"Error extracting article details from {url}: {e}")
            return None
    
    def save_articles(self, articles):
        """Save articles to a JSON file"""
        if not articles:
            logger.info("No articles to save")
            return
            
        today = datetime.now().strftime("%Y-%m-%d")
        filename = os.path.join(self.data_dir, f"articles_{today}.json")
        
        # Check if file exists and load existing data
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
                
            # Get existing URLs to avoid duplicates
            existing_urls = [article['link'] for article in existing_data]
            
            # Only add new articles
            new_articles = [article for article in articles if article['link'] not in existing_urls]
            if new_articles:
                combined_articles = existing_data + new_articles
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(combined_articles, f, ensure_ascii=False, indent=2)
                logger.info(f"Added {len(new_articles)} new articles to {filename}")
            else:
                logger.info("No new articles to add")
        else:
            # Create new file
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved {len(articles)} articles to {filename}")
    
    def run(self):
        """Main method to run the scraper"""
        logger.info("Starting MENABytes news scraper")
        
        # Fetch the homepage
        html = self.fetch_page(self.base_url)
        if not html:
            logger.error("Failed to fetch homepage")
            return
            
        # Extract articles
        articles = self.extract_articles(html)
        logger.info(f"Found {len(articles)} articles on homepage")
        
        # Get detailed content for each article
        for article in articles:
            details = self.get_article_details(article['link'])
            if details:
                article.update(details)
                logger.info(f"Added details for article: {article['title']}")
        
        # Save articles
        self.save_articles(articles)
        logger.info("Scraping completed")

if __name__ == "__main__":
    scraper = MENABytesNewsScraper()
    scraper.run() 