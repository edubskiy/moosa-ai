import argparse
import logging
from article_tracker import ArticleTracker

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

def main():
    """Reset the processed status of an article"""
    parser = argparse.ArgumentParser(description='Reset the processed status of an article')
    parser.add_argument('--title', type=str, required=True, help='Title of the article to reset')
    
    args = parser.parse_args()
    
    title = args.title
    
    tracker = ArticleTracker()
    result = tracker.reset_article_processed(title)
    
    if result:
        logger.info(f"Successfully reset article: {title}")
    else:
        logger.error(f"Failed to reset article: {title}")

if __name__ == "__main__":
    main() 