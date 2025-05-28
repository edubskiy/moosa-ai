import os
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("tracker.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class ArticleTracker:
    """Class to track processed articles and avoid duplicates"""
    
    def __init__(self):
        self.db_file = "data/processed_articles.json"
        self.processed_articles = self._load_db()
    
    def _load_db(self):
        """Load the database of processed articles"""
        if not os.path.exists(self.db_file):
            # Create the file if it doesn't exist
            os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
            return []
            
        try:
            with open(self.db_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading article database: {e}")
            return []
    
    def _save_db(self):
        """Save the database of processed articles"""
        try:
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(self.processed_articles, f, indent=2)
            logger.info(f"Article database saved to {self.db_file}")
        except Exception as e:
            logger.error(f"Error saving article database: {e}")
    
    def is_article_processed(self, article):
        """Check if an article has already been processed"""
        article_url = article.get('link', '')
        article_title = article.get('title', '')
        
        # Check if the article is in the database
        for processed in self.processed_articles:
            if processed['url'] == article_url or processed['title'] == article_title:
                logger.info(f"Article already processed: {article_title}")
                return True
                
        logger.info(f"Article not processed yet: {article_title}")
        return False
    
    def mark_article_processed(self, article, output_path):
        """Mark an article as processed"""
        article_data = {
            'url': article.get('link', ''),
            'title': article.get('title', ''),
            'date_processed': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'output_path': output_path
        }
        
        self.processed_articles.append(article_data)
        self._save_db()
        logger.info(f"Article marked as processed: {article['title']}")
    
    def get_processed_articles(self):
        """Get a list of all processed articles"""
        return self.processed_articles
    
    def get_processed_article_by_url(self, url):
        """Get a processed article by URL"""
        for article in self.processed_articles:
            if article['url'] == url:
                return article
        return None
    
    def get_processed_article_by_title(self, title):
        """Get a processed article by title"""
        for article in self.processed_articles:
            if article['title'] == title:
                return article
        return None

    def reset_article_processed(self, article_title):
        """Reset the processed status of an article by title"""
        for i, article in enumerate(self.processed_articles):
            if article['title'] == article_title:
                logger.info(f"Resetting processed status for article: {article_title}")
                self.processed_articles.pop(i)
                self._save_db()
                return True
                
        logger.warning(f"Article not found in processed database: {article_title}")
        return False

if __name__ == "__main__":
    # Simple test
    tracker = ArticleTracker()
    print(f"Currently processed articles: {len(tracker.get_processed_articles())}") 