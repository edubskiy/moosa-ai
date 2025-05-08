import os
import logging
import argparse
from dotenv import load_dotenv
from startup_news_scraper import MENABytesNewsScraper
from content_generator import ContentGenerator
from reel_generator import ReelGenerator

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("main.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def run_scraper():
    """Run the news scraper"""
    logger.info("Starting news scraper")
    scraper = MENABytesNewsScraper()
    scraper.run()
    logger.info("News scraper completed")

def run_content_generator():
    """Run the content generator"""
    logger.info("Starting content generator")
    generator = ContentGenerator()
    generator.run()
    logger.info("Content generator completed")

def run_reel_generator():
    """Run the Instagram reel script generator"""
    logger.info("Starting reel generator")
    generator = ReelGenerator()
    generator.run()
    logger.info("Reel generator completed")

def run_all():
    """Run all components in sequence"""
    logger.info("Running all components")
    run_scraper()
    run_content_generator()
    run_reel_generator()
    logger.info("All components completed")

def main():
    """Main function with command line arguments"""
    parser = argparse.ArgumentParser(description='Startup Content Creation System')
    parser.add_argument('--scrape', action='store_true', help='Run only the news scraper')
    parser.add_argument('--content', action='store_true', help='Run only the content generator')
    parser.add_argument('--reel', action='store_true', help='Run only the Instagram reel generator')
    
    args = parser.parse_args()
    
    # Check if OpenAI API key is set
    if not os.getenv("OPENAI_API_KEY"):
        logger.warning("OpenAI API key not found. Set OPENAI_API_KEY environment variable for AI-powered content generation.")
    
    # Run the selected components or all if none specified
    if args.scrape:
        run_scraper()
    elif args.content:
        run_content_generator()
    elif args.reel:
        run_reel_generator()
    else:
        run_all()

if __name__ == "__main__":
    main() 