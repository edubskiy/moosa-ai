import os
import json
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("reset.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def reset_all_articles():
    """Reset the processed status of all articles"""
    db_file = "data/processed_articles.json"
    
    if not os.path.exists(db_file):
        logger.error(f"Database file not found: {db_file}")
        return False
    
    # Create backup
    backup_file = f"{db_file}.backup"
    try:
        with open(db_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
        
        with open(backup_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2)
        
        logger.info(f"Created backup at {backup_file}")
    except Exception as e:
        logger.error(f"Error creating backup: {e}")
        return False
    
    # Reset database
    try:
        with open(db_file, 'w', encoding='utf-8') as f:
            json.dump([], f)
        
        logger.info(f"Successfully reset all articles")
        logger.info(f"Reset {len(articles)} articles")
        return True
    except Exception as e:
        logger.error(f"Error resetting articles: {e}")
        return False

if __name__ == "__main__":
    reset_all_articles() 