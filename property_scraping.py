# from selenium.webdriver.firefox.options import Options
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from bs4 import BeautifulSoup
# import time
# from datetime import datetime
# from tqdm import tqdm
# import pandas as pd
# import logging

# class Scraper:
#     def __init__(self, region_website):
#         self.region_website = region_website
#         self.driver = self.setup_driver()

#     def setup_driver(self):
#         options = Options()
#         # options.add_argument("--headless")
#         options.headless = True  # Run Firefox in headless mode (no GUI)
#         options.add_argument("--disable-gpu")  # Disable GPU acceleration (may help with stability)
#         driver = webdriver.Firefox(options=options)
#         return driver

#     def scrape_data(self):
#         data_list = []
#         self.driver.get(self.region_website)
#         WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'content')))

#         # Dynamically find the last page number
#         last_page_element = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[7]/div/div/div[1]/div[17]/div/div/ul/li[5]/a')
#         last_page = int(last_page_element.get_attribute('innerHTML').strip())
#         last_page = 2

#         for page_num in tqdm(range(1, last_page + 1), desc="Scraping Pages"):
#             current_url = f'{self.region_website}?p[page]={page_num}'
#             self.driver.get(current_url)
#             WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'advertisement-item--content')))

#             html = self.driver.page_source
#             soup = BeautifulSoup(html, 'html.parser')
#             elements = soup.find_all('div', class_='advertisement-item--content')

#             for property in elements:
#                 try:
#                     street = property.find_all('div', class_="advertisement-item--content__info d-block text-truncate")[0].get('title')
#                 except AttributeError:
#                     street = None

#                 try:
#                     title = property.find('h2', class_="mb-0 d-none d-md-block").text.strip()
#                 except AttributeError:
#                     title = None

#                 try:
#                     features = property.find_all('div', class_="advertisement-item--content__info")
#                     type = features[1].text.split('•')[0].strip()
#                 except AttributeError:
#                     type = None

#                 try:
#                     size = features[1].find('span').text.strip()
#                 except AttributeError:
#                     size = None

#                 try:
#                     price = property.find_all('div', class_="advertisement-item--content__price col-auto pl-0 pl-md-3 pr-0 text-right mt-2 mt-md-0 align-self-end")
#                     price = price[0]['data-adv-price']
#                 except AttributeError:
#                     price = None

#                 current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
#                 data_list.append({'street': street, 'title': title, 'type': type, 'size': size, 'price': price, 'current_datetime': current_datetime})

#         self.driver.quit()
#         return pd.DataFrame(data_list)




from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
from tqdm import tqdm
import pandas as pd

class Scraper:
    def __init__(self, region_website):
        self.region_website = region_website
        self.driver = self.setup_driver()

    def setup_driver(self):
        # Configure and return a headless Firefox webdriver
        options = Options()
        options.headless = True  # Run in headless mode (no GUI)
        options.add_argument("--disable-gpu")  # Disable GPU acceleration for stability
        return webdriver.Firefox(options=options)

    def scrape_data(self):
        data_list = []
        self.driver.get(self.region_website)
        
        # Wait for the content to load
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'content')))

        # Find the last page number
        last_page_element = self.driver.find_element(By.XPATH, '//*[@id="content"]/div[7]/div/div/div[1]/div[17]/div/div/ul/li[5]/a')
        last_page = int(last_page_element.get_attribute('innerHTML').strip())
        last_page = 2  # Override for testing. Remove this line for full scraping

        # Iterate through each page
        for page_num in tqdm(range(1, last_page + 1), desc="Scraping Pages"):
            page_url = f'{self.region_website}?p[page]={page_num}'
            self.driver.get(page_url)
            
            # Wait for the property listings to load
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'advertisement-item--content')))

            # Parse the page content
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            property_elements = soup.find_all('div', class_='advertisement-item--content')

            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            
            # Extract data from each property listing
            for property_element in property_elements:
                data_list.append(self.extract_property_data(property_element, current_datetime))

        self.driver.quit()
        
        # Convert the list of dictionaries to a DataFrame and return it
        return pd.DataFrame(data_list)

    def extract_property_data(self, property_element, current_datetime):
        # Helper function to safely extract data and handle AttributeErrors
        def safe_find(method, *args, **kwargs):
            try:
                return method(*args, **kwargs)
            except AttributeError:
                return None

        # Extract individual property details
        street = safe_find(property_element.find, 'div', class_="advertisement-item--content__info d-block text-truncate")
        street = street.get('title') if street else None

        title = safe_find(property_element.find, 'h2', class_="mb-0 d-none d-md-block")
        title = title.text.strip() if title else None

        features = property_element.find_all('div', class_="advertisement-item--content__info")
        type = safe_find(lambda: features[1].text.split('•')[0].strip())
        size = safe_find(lambda: features[1].find('span').text.strip())

        price = safe_find(property_element.find, 'div', class_="advertisement-item--content__price col-auto pl-0 pl-md-3 pr-0 text-right mt-2 mt-md-0 align-self-end")
        price = price['data-adv-price'] if price else None

        # Return a dictionary of property data
        return {
            'street': street,
            'title': title,
            'type': type,
            'size': size,
            'price': price,
            'current_datetime': current_datetime
        }