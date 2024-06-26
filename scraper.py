# This is the script to scrape Decathlon website for products, reviews and characteristics.
# The script uses Selenium to scrape the website and Pandas to store the data in CSV files.
# @Author: RaulMoldes
# author-email: raul.moldes.work@gmail.com
# Date: 2024-05-13
# Version: 1.0
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchWindowException, ElementNotInteractableException, ElementClickInterceptedException
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import time
import os
import sys
import argparse

DECATHLON = 'https://www.decathlon.es/es/'
DEFAULT_QUERY = 'balón'
URLS_OUTPUT_FILE = 'data/decathlon_urls.csv'
PRODUCTS_OUTPUT_FILE = 'data/decathlon_products.csv'
REVIEWS_OUTPUT_FILE = 'data/decathlon_reviews.csv'
CHARACTERISTICS_OUTPUT_FILE = 'data/decathlon_characteristics.csv'
GENRES = ['Hombre', 'Mujer', 'Niño', 'Niña']


class DecathlonScraper:
    """
    A class representing a web scraper for Decathlon website.

    Attributes:
        driver: The web driver used for scraping.
        url: The URL of the Decathlon website.

    Methods:
        __init__: Initializes the DecathlonScraper object.
        get_driver: Returns the web driver.
        fetch: Fetches the Decathlon website.
    """

    def __init__(self, query='', driver=None, url: str = DECATHLON):
        """
        Initializes the DecathlonScraper object.

        Args:
            driver: The web driver used for scraping. If None, a new Chrome driver will be created.
            url: The URL of the Decathlon website.
        """
        self.query = query
        if driver is None:
            self.driver = webdriver.Chrome(
                service=Service(), options=webdriver.ChromeOptions())
        else:
            self.driver = driver
        self.url = url

    def remove_popup(self, popup_id: str = "didomi-popup", sleep_time: int = 2) -> bool:
        """
        Removes a popup from the web page.

        Args:
            popup_id (str): The ID of the popup element to be removed. Default is "didomi-popup".
            sleep_time (int): The time to sleep after closing the popup. Default is 2 seconds.

        Returns:
            bool: True if the popup was successfully removed, False otherwise.
        """
        popup = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, popup_id)))

        popup_close_button = popup.find_element(
            By.CSS_SELECTOR, "span")
        popup_close_button.click()
        time.sleep(sleep_time)
        return True

    def get_driver(self):
        """
        Returns the web driver.

        Returns:
            The web driver.
        """
        return self.driver

    def log(self, message: str):
        print(message)

    def fetch(self) -> bool:
        """
        Fetches the Decathlon website.

        Returns:
            True if the website was successfully fetched, False otherwise.
        """
        print(f"Fetching {self.url}")
        self.driver.get(self.url)
        return True


class DecathlonSearcher(DecathlonScraper):
    def __init__(self,  query: str = '', driver=None, url: str = DECATHLON):
        '''
        Initializes the DecathlonSearch object.
        Parameters:
            item (str): The item to search for.
            driver (object): The web driver used for scraping. If None, a new Chrome driver will be created.
            url (str): The URL of the Decathlon website.

        Returns:
            None'''
        super().__init__(query, driver, url)
        self.item = query

    def next_page(self, next_page_css: str = "button.vtmn-btn", sleep_time: int = 2) -> bool:
        '''
        Clicks on the next page button.

        Parameters:
            next_page_css (str): The CSS selector for the next page button. Default is "a.next".
            sleep_time (int): The time to sleep after clicking the next page button. Default is 2 seconds.

        Returns:
            bool: True if the next page was successfully clicked, False otherwise.'''
        next_page_button = self.driver.find_elements(
            By.CSS_SELECTOR, next_page_css)[-1]
        next_page_button.click()
        time.sleep(sleep_time)
        return True

    def search(self, search_class: str = "svelte-1xw4dnq", sleep_time: int = 2) -> bool:
        """
        Searches for an item using the provided search class and sleep time.

        Args:
            search_class (str): The CSS class name of the search box and button.
            sleep_time (int): The number of seconds to sleep after clicking the search button.

        Returns:
            bool: True if the search was successful, False otherwise.
        """

        search_box = self.driver.find_element(
            By.CSS_SELECTOR, f"input.{search_class}")
        search_button = self.driver.find_element(
            By.CSS_SELECTOR, f"button.{search_class}")
        search_box.send_keys(self.item)
        search_button.click()
        time.sleep(sleep_time)
        return True

    def find_total_pages(self, total_pages_xpath: str = '//nav[@aria-label="Paginación de la página de lista de productos"]') -> int:
        """
        Finds the total number of pages for the search results.

        Args:
            total_pages_css (str): The CSS selector for the total pages element. Defaults to "nav.vtmn-flex".

        Returns:
            str: The total number of pages for the search results.
        """
        total_pages = self.driver.find_element(
            By.XPATH, total_pages_xpath).text

        total_pages = int(total_pages.split(" ")[-1])
        return total_pages

    def get_products(self, product_item_css: str = ".dpb-product-model-link") -> list:
        """
        Retrieves a list of products from the webpage.

        Args:
            product_item_css (str): The CSS selector for the product items. Defaults to ".dpb-product-model-link".

        Returns:
            list: A list of dictionaries containing the name and URL of each product.
        """
        products = list()

        self.total_pages = self.find_total_pages()
        print(f"Total pages: {self.total_pages}")
        for _ in range(self.total_pages):
            product_captions = self.driver.find_elements(
                By.CSS_SELECTOR, product_item_css)
            for product in product_captions:

                if product.tag_name == "a":
                    out = {
                        "name": product.text,
                        "query": self.query,
                        "url": product.get_attribute("href"),
                        "id": product.get_attribute("href").split("mc=")[-1]
                    }

                    products.append(pd.DataFrame(out, index=[0]))
            try:
                self.next_page()
            except IndexError:
                break
        products = pd.concat(products)
        products.to_csv(URLS_OUTPUT_FILE, index=False)
        return products

    def scrape(self):
        """
        This method performs the scraping process.

        It calls the `fetch` method to retrieve the data,
        then removes any popups using the `remove_popup` method,
        performs a search using the `search` method,
        and finally returns the scraped products using the `get_products` method.

        Returns:
            list: A list of scraped products.
        """
        fetch = self.fetch()
        if fetch:
            popup = self.remove_popup()
        if popup:
            search = self.search()
        if search:
            return self.get_products()


class ProductReviewsScraper(DecathlonScraper):

    def __init__(self, query='', driver=None, url=None):
        super().__init__(query, driver, url)

    def scrape(self) -> dict:
        """
        Scrapes the reviews from the website.

        Returns:
            dict: A dictionary containing the scraped reviews data.

        """
        time.sleep(2)
        fetch = self.fetch()
        try:
            self.remove_popup()
        except (TimeoutException, NoSuchWindowException) as e:
            pass

        if fetch:
            return self.parse_reviews_data()

    def parse_author_data(self, author_data: str) -> tuple:
        """
        Parses the author data from the reviews.

        Args:
            author_data (str): The author data to parse.

        Returns:
            list: A list containing the author data"""
        author_data = author_data.split("|")
        author_data = [data.strip() for data in author_data]

        if len(author_data) < 3:
            author_data.extend('Unknown' for _ in range(3 - len(author_data)))

        name = author_data[0]
        sex = author_data[1] if author_data[1] in [
            'Hombre', 'Mujer'] else 'Unknown'
        location = author_data[2] if '/' not in author_data[2] else 'Unknown'
        return name, sex, location

    def expand_reviews(self, reviews_section, sleep_time=2):
        try:
            expand_reviews_button = reviews_section.find_element(
                By.XPATH, '//span[contains(text(), "Ver todas las opiniones")]/parent::button')
            expand_reviews_button.click()
            time.sleep(sleep_time)
        except NoSuchElementException:
            pass
        return True

    def go_to_reviews(self, sleep_time=2):
        try:
            go_to_reviews_button = self.driver.find_element(
                By.XPATH, '//button[contains(text(), "Opiniones de usuarios")]')
            go_to_reviews_button.click()
            time.sleep(sleep_time)
            return True
        except (NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException) as e:
            return False

    def open_reviews(self, reviews_id="reviews-floor", sleep_time=2):

        try:

            product_reviews = WebDriverWait(self.driver, sleep_time).until(
                EC.presence_of_element_located((By.ID, reviews_id)))
            return self.expand_reviews(product_reviews)

        except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:

            open_reviews_button = WebDriverWait(self.driver, sleep_time).until(
                EC.presence_of_element_located((
                    By.XPATH, '//span[contains(text(), "Opiniones de usuarios")]/following-sibling::button')))
            open_reviews_button.click()
            time.sleep(sleep_time)
            return self.open_reviews(reviews_id, sleep_time)

    def parse_reviews_data(self, sleep_time=2) -> pd.DataFrame:
        if self.go_to_reviews(sleep_time=sleep_time):
            try:
                opened = self.open_reviews(sleep_time=sleep_time)
            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
                opened = False
                return None
        else:
            return None

        if opened:

            product_id = self.url.split("mc=")[-1]

            reviews = self.driver.find_elements(
                By.CSS_SELECTOR, "article.review-item")
            print('---------------------------------------')
            reviews_list = list()
            if len(reviews) == 0:
                return None
            for review in reviews:
                author_data = review.find_element(
                    By.CSS_SELECTOR, "div.vtmn-text-lg").text
                name, sex, location = self.parse_author_data(author_data)
                try:
                    title = review.find_element(
                        By.CSS_SELECTOR, "h3.review-title").text
                    print('Title:', title)
                except NoSuchElementException:
                    title = None
                try:
                    usage = review.find_element(
                        By.CSS_SELECTOR, "div.product-usage").text
                    print('Usage:', usage)
                except NoSuchElementException:
                    usage = None
                try:
                    rating = review.find_element(
                        By.CSS_SELECTOR, "span.vtmn-rating_comment--primary").text
                    rating = float(rating.replace('/5', ''))   # Remove the /5
                    print('Rating:', rating)
                except NoSuchElementException:
                    rating = None
                try:
                    date = review.find_element(
                        By.TAG_NAME, "time").get_attribute("datetime")

                    print('Date:', date)
                except NoSuchElementException:
                    date = None
                try:
                    text = review.find_element(By.CSS_SELECTOR, "p").text
                    print('Text:', text)
                except NoSuchElementException:
                    text = None
                out = {
                    "product_id": product_id,
                    "query": self.query,
                    "title": title,
                    "usage": usage,
                    "author": name,   # Author
                    "Sex": sex,  # Author
                    "Location": location,  # Author
                    "rating": rating,
                    "date": date,
                    "text": text
                }

                reviews_list.append(pd.DataFrame(out, index=[0]))
            return pd.concat(reviews_list, ignore_index=True)


class ProductCharacteristicsScraper(DecathlonScraper):

    def __init__(self, query='', driver=None, url=None):
        super().__init__(query, driver, url)

    def scrape(self) -> dict:
        """
        Scrapes the reviews from the website.

        Returns:
            dict: A dictionary containing the scraped reviews data.

        """
        time.sleep(2)
        fetch = self.fetch()
        try:
            self.remove_popup()
        except (TimeoutException, NoSuchWindowException) as e:
            pass
        if fetch:
            return self.parse_characteristics_data()

    def go_to_characteristics(self, sleep_time=2):
        try:
            go_to_chars_button = self.driver.find_element(
                By.XPATH, '//button[contains(text(), "Características principales")]')
            go_to_chars_button.click()
            time.sleep(sleep_time)
            return True
        except NoSuchElementException:
            return False

    def open_characteristics(self, characteristics_class="benefit", sleep_time=2):

        try:

            product_characteristics = WebDriverWait(self.driver, sleep_time).until(
                EC.presence_of_element_located((By.CLASS_NAME, characteristics_class)))
            return True

        except (NoSuchElementException, TimeoutException, ElementNotInteractableException) as e:

            open_characteristics_button = WebDriverWait(self.driver, sleep_time).until(
                EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Características principales")]/following-sibling::button')))

            open_characteristics_button.click()
            time.sleep(sleep_time)
            return self.open_characteristics(characteristics_class, sleep_time)

    def parse_characteristics_data(self, sleep_time=2) -> pd.DataFrame:
        if self.go_to_characteristics(sleep_time=sleep_time):
            opened = self.open_characteristics(sleep_time=sleep_time)
        else:
            return None
        if opened:

            product_id = self.url.split("mc=")[-1]

            characteristics = self.driver.find_elements(
                By.CLASS_NAME, "benefit")
            print('---------------------------------------')
            characteristics_list = list()
            if len(characteristics) == 0:
                return None
            for characteristic in characteristics:
                title = characteristic.find_element(
                    By.CSS_SELECTOR, "h3").text
                print('Title:', title)
                try:
                    description = characteristic.find_element(
                        By.CSS_SELECTOR, "p").text
                    print('Description:', description)
                except NoSuchElementException:
                    description = None
                out = {
                    "query": self.query,  # "balón
                    "product_id": product_id,
                    "title": title,
                    "description": description
                }

                characteristics_list.append(pd.DataFrame(out, index=[0]))
            return pd.concat(characteristics_list, ignore_index=True)


class ProductScraper(DecathlonScraper):
    """
    A class representing a product scraper.

    This class inherits from the DecathlonScraper class and provides methods to scrape product data from a website.

    Attributes:
        driver (WebDriver): The WebDriver instance used for web scraping.
        url (str): The URL of the website to scrape.

    Methods:
        scrape(): Scrapes the product data from the website.
        check_genres(product_name: str) -> str: Checks the genre of the product based on its name.
        parse_product_data(product_section_css: str = "section.vtmn-font-regular") -> dict: Parses the product data from the web page.

    """

    def __init__(self, query='', driver=None, url=None):
        super().__init__(query, driver, url)

    def scrape(self) -> pd.DataFrame:
        """
        Scrapes the product data from the website.

        Returns:
            dict: A dictionary containing the scraped product data.

        """
        time.sleep(2)
        fetch = self.fetch()
        try:
            self.remove_popup()
        except (TimeoutException, NoSuchWindowException) as e:
            pass
        if fetch:
            return self.parse_product_data()

    def check_genres(self, product_name: str) -> str:
        """
        Checks the genre of the product based on its name.

        Args:
            product_name (str): The name of the product.

        Returns:
            str: The genre of the product.

        """
        if any(genre in product_name for genre in GENRES):
            for genre in GENRES:
                if genre.lower() in product_name.lower():
                    return genre
        else:
            return 'Unisex'

    def parse_product_data(self, product_images_css: str = "div.product-images", product_section_css: str = "section.vtmn-font-regular") -> pd.DataFrame:
        """
        Parses the product data from the web page.

        Args:
            product_section_css (str, optional): The CSS selector for the product section on the web page. Defaults to "section.vtmn-font-regular".

        Returns:
            dict: A dictionary containing the parsed product data.

        """
        product_id = self.url.split("mc=")[-1]

        product_picture = self.driver.find_element(
            By.CSS_SELECTOR, product_images_css)
        product_data = self.driver.find_element(
            By.CSS_SELECTOR, product_section_css)

        print('---------------------------------------')
        name = product_data.find_element(By.CSS_SELECTOR, "h1").text
        genre = self.check_genres(name)
        if genre != 'Unisex':
            name = name.replace(genre, '')
        print('Genre:', genre)
        print('Product Name:', name)
        brand = product_data.find_element(By.TAG_NAME, "a").text
        print('Brand:', brand)

        try:

            sticker = product_picture.find_element(
                By.CLASS_NAME,  "sticker-item").text
            print('Sticker:', sticker)
        except NoSuchElementException:
            sticker = None
            print('Sticker: Not available')

        current_price = product_data.find_element(
            By.CSS_SELECTOR, "span.vtmn-price_size--large").text
        current_price = float(current_price.split(' ')[0].replace(',', '.'))
        print('Price:', current_price)

        try:
            previous_price = product_data.find_element(
                By.CSS_SELECTOR, "span.vtmn-price_size--xsmall").text
            previous_price = float(previous_price.split(' ')[
                                   0].replace(',', '.'))

            discount = True
        except NoSuchElementException:
            previous_price = None
            discount = False

        print('Previous Price:', previous_price)
        print('Discount:', discount)
        description = product_data.find_element(
            By.CSS_SELECTOR, "p.product-description").text
        print('Description:', description)
        try:
            color = product_data.find_element(
                By.CSS_SELECTOR, "span.current-model-color").text
            print('Color:', color)
        except NoSuchElementException:
            color = None
            print('Color: Not available')

        try:
            rating = product_data.find_element(
                By.CSS_SELECTOR, "span.vtmn-rating_comment--primary").text
            rating = float(rating.replace('/5', ''))   # Remove the /5
            print('Rating:', rating)
        except NoSuchElementException:
            rating = None
            print('Rating: Not available')

        try:
            reviews_button = product_data.find_element(
                By.CSS_SELECTOR, "button.review-link")
            n_reviews = reviews_button.text.replace(
                ' opiniones', '').replace('Leer las ', '').replace('Leer ', '').replace(' opinión', '').split('\n')[-1]
            n_reviews = int(n_reviews)
            print('Reviews:', n_reviews)
        except NoSuchElementException:
            n_reviews = 0
            print('Reviews: Not available')
        out = {
            "id": product_id,
            "query": self.query,  # "balón
            "name": name,
            "genre": genre,  # "Hombre", "Mujer", "Niño", "Niña", "Unisex
            "brand": brand,
            "sticker": sticker,
            "price": current_price,
            "previous_price": previous_price,
            "discount": discount,
            "description": description,
            "rating": rating,
            "n_reviews": n_reviews,
            "color": color
        }

        return pd.DataFrame(out, index=[0])


MAPPER = {

    'products': {
        'output_file': PRODUCTS_OUTPUT_FILE,
        'scraper': ProductScraper,

    },
    'reviews': {
        'output_file': REVIEWS_OUTPUT_FILE,
        'scraper': ProductReviewsScraper
    },
    'characteristics': {
        'output_file': CHARACTERISTICS_OUTPUT_FILE,
        'scraper': ProductCharacteristicsScraper
    }
}


def query_decathlon(query: str = "balón", search_for='reviews', driver=None, max_workers=10) -> pd.DataFrame:
    """
    Queries Decathlon website for product information.

    Args:
        query (str, optional): The search query. Defaults to "balón".
        search_for (str, optional): The type of information to search for. Defaults to 'reviews'.
        driver (object, optional): The driver object for web scraping. Defaults to None.
        max_workers (int, optional): The maximum number of worker threads. Defaults to 10.

    Returns:
        pd.DataFrame: A DataFrame containing the scraped product data.
    """
    products = pd.read_csv(URLS_OUTPUT_FILE)
    product_data = list()
    # Get the driver to pass to the ProductScraper
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for row in products.iterrows():

            try:
                scraper = MAPPER[search_for]['scraper'](
                    query=query, driver=driver, url=row[1]["url"])
                result = executor.submit(scraper.scrape())
                scraped = result.result
                if scraped is not None:
                    product_data.append(scraped)

            except Exception as e:

                print(f"Could not scrape {search_for} of {row[1]['name']}")
                with open('errors.txt', 'a') as f:
                    f.write(
                        f"Could not scrape {search_for} of {row[1]['name']}.\n")
                continue

    product_data = pd.concat(product_data, ignore_index=True)
    return product_data


def main(query: str, max_workers=10, search=True):
    """
    Main function for the scraper module.

    Args:
        query (str): The search query to be used.
        max_workers (int, optional): The maximum number of workers for concurrent scraping. Defaults to 10.
        search (bool, optional): Flag indicating whether to perform a search or not. Defaults to True.

    Returns:
        bool: True if the scraping process is successful.
    """
    if search:
        searcher = DecathlonSearcher(query=query)
        driver = searcher.get_driver()
        products = searcher.scrape()
        products.to_csv(URLS_OUTPUT_FILE, index=False)
        print(f"URLs saved to {URLS_OUTPUT_FILE}")
    else:
        driver = webdriver.Chrome(
            service=Service(), options=webdriver.ChromeOptions())
    for search_for in MAPPER.keys():
        data = query_decathlon(query=query, search_for=search_for,
                               driver=driver, max_workers=max_workers)

        data.to_csv(MAPPER[search_for]['output_file'], index=False)
        print(f"Data saved to {MAPPER[search_for]['output_file']}")
    return True


if __name__ == "__main__":
    assert len(sys.argv) > 1, "Please provide a query to search for"
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", type=str,
                        help="The query to search for", required=True)
    parser.add_argument("--max_workers", type=int,
                        help="The maximum number of workers to use", default=10)
    args = parser.parse_args()
    main(args.query, args.max_workers, search=False)
