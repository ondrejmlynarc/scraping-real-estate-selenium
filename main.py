from property_scraping import Scraper
from datetime import datetime
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    setup_logging()

    # Define the required arguments
    region_website = 'https://www.nehnutelnosti.sk/bratislava/'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nehnutelnosti_sk_bratislava_{timestamp}.csv"

    logging.info(f"Starting scraping from {region_website}")

    try:
        # Scrape the data
        scraper_instance = Scraper(region_website)
        df = scraper_instance.scrape_data()

        # Save data to CSV
        df.to_csv(filename, index=False)
        logging.info(f"Data successfully saved to {filename}")
        logging.info(f"Total records scraped: {len(df)}")

    except Exception as e:
        logging.error(f"An error occurred during scraping: {str(e)}")

    logging.info("Scraping process completed")