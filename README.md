[![Selenium](https://img.shields.io/badge/Selenium-%2343B02A.svg?style=for-the-badge&logo=Selenium&logoColor=white)](https://www.selenium.dev)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup-%2343B02A.svg?style=for-the-badge&logo=BeautifulSoup&logoColor=white)](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
[![pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

# Selenium Real Estate Scraper

## Overview

This Python-based web scraper is designed to extract property data from nehnutelnosti.sk, a Slovak leading real-estate website, using Selenium and BeautifulSoup. The scraper navigates through multiple pages of property listings of a selected region, extracts key details, and compiles the data into a pandas DataFrame.

## Features

- **Headless Browsing**: Uses Firefox in headless mode for efficient scraping without a GUI.
- **Pagination Handling**: Automatically navigates through multiple pages of property listings.
- **Data Extraction**: Extracts key property details including street, title, type, size, and price.
- **Timestamp**: Adds a timestamp to each scraped entry for tracking.
- **Progress Tracking**: Uses `tqdm` to display a progress bar during scraping.
- **Error Handling**: Implements safe methods to handle potential AttributeErrors during data extraction.
- **Customizable**: Easily adaptable for different regions of the same website, as well as other property websites with similar structures.

## Requirements

- Python 3.6+
- Selenium
- BeautifulSoup4
- pandas
- tqdm
- Firefox browser
- GeckoDriver (Firefox WebDriver)

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/property-scraper.git
   cd property-scraper

2. **Install required packages:**

    ```bash 
    pip install -r requirements.txt

## Usage

1. **Configure the scraper:**

    Open property_scraper.py and update the region_website variable with the URL of the property listing website you want to scrape.

    If name == 'main': setup_logging()

    ```bash
    # define the required arguments
    region_website = 'https://www.nehnutelnosti.sk/bratislava/'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") 
    filename = f"nehnutelnosti_sk_bratislava_{timestamp}.csv"

    logging.info(f"Starting scraping from {region_website}")

2. **Run the script:**

    ```bash
    python property_scraper.py

## Customization

- **Scraping all pages:** Remove the line `last_page = 2` in the `scrape_data()` method to scrape all available pages.

- **Adjusting wait times:** Modify the `WebDriverWait` timeout in the `scrape_data()` method if needed for slower websites.

- **Adding more fields:** Extend the `extract_property_data()` method to scrape additional information from each listing.

- **Changing the browser:** Modify the `setup_driver()` method to use a different webdriver (e.g., Chrome) if preferred.


## Data Output

The scraper outputs a pandas DataFrame with the following columns:

| Column           | Description                                     |
|------------------|-------------------------------------------------|
| street           | The street address of the property              |
| title            | The title of the property listing               |
| type             | The type of property (e.g., apartment, house)   |
| size             | The size of the property                        |
| price            | The listed price of the property                |
| current_datetime | Timestamp of when the data was scraped          |


## Error Handling

The scraper implements error handling in several ways:

- **WebDriverWait:** ensures page elements are loaded before scraping.
- **safe_find() method:** handles potential `AttributeError`s during data extraction.
- **try-except blocks:** handles exceptions and continues scraping.

## Performance Considerations

- **Headless mode:** improves performance and reduces resource usage.
- **Multi-threading or multiprocessing:** consider implementing for even faster scraping of large datasets.
