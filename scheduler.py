import schedule
import time
import logging
import os
from datetime import datetime
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
        logging.FileHandler("scheduler.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def job():
    """Daily job to scrape news and generate content"""
    logger.info(f"Starting scheduled job at {datetime.now()}")
    
    try:
        # Step 1: Scrape latest news
        logger.info("Starting news scraping")
        scraper = MENABytesNewsScraper()
        scraper.run()
        
        # Step 2: Generate content
        logger.info("Starting content generation")
        generator = ContentGenerator()
        generator.run()
        
        # Step 3: Generate Instagram reel script
        logger.info("Starting reel script generation")
        reel_generator = ReelGenerator()
        reel_generator.run()
        
        logger.info("Scheduled job completed successfully")
    except Exception as e:
        logger.error(f"Error in scheduled job: {e}")

def main():
    """Main function to set up and run the scheduler"""
    logger.info("Starting scheduler")
    
    # Get scheduled time from environment variable or use default
    scheduled_time = os.getenv("SCHEDULER_TIME", "09:00")
    
    # Schedule the job to run daily at the specified time
    schedule.every().day.at(scheduled_time).do(job)
    logger.info(f"Job scheduled to run daily at {scheduled_time}")
    
    # Run the job immediately for the first time
    logger.info("Running job immediately for the first time")
    job()
    
    # Keep the script running
    while True:
        schedule.run_pending()
        time.sleep(60)  # Check every minute

if __name__ == "__main__":
    main() 