from base import DECATHLON
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time
import sys

QUERIES_TO_MAKE = ['balón']
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

    def __init__(self, driver=None, url: str = DECATHLON):
        """
        Initializes the DecathlonScraper object.

        Args:
            driver: The web driver used for scraping. If None, a new Chrome driver will be created.
            url: The URL of the Decathlon website.
        """
        if driver is None:
            self.driver = webdriver.Chrome(
                service=Service(), options=webdriver.ChromeOptions())
        else:
            self.driver = driver
        self.url = url

    def get_driver(self):
        """
        Returns the web driver.

        Returns:
            The web driver.
        """
        return self.driver

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
    def __init__(self,  item: str, driver=None, url: str = DECATHLON):
        '''
        Initializes the DecathlonSearch object.
        Parameters:
            item (str): The item to search for.
            driver (object): The web driver used for scraping. If None, a new Chrome driver will be created.
            url (str): The URL of the Decathlon website.

        Returns:
            None'''
        super().__init__(driver, url)
        self.item = item

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
                    products.append({
                        "name": product.text,
                        "url": product.get_attribute("href")
                    })
            try:
                self.next_page()
            except IndexError:
                break

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

    def __init__(self, driver=None, url=None):
        super().__init__(driver, url)

    def scrape(self) -> dict:
        """
        Scrapes the reviews from the website.

        Returns:
            dict: A dictionary containing the scraped reviews data.

        """
        time.sleep(2)
        fetch = self.fetch()
        if fetch:
            return self.parse_reviews_data()

    def parse_reviews_data(self, reviews_css: str = "div.vtmn-review") -> dict:
        pass


class ProductCharacteristicsScraper(DecathlonScraper):

    def __init__(self, driver=None, url=None):
        super().__init__(driver, url)

    def scrape(self) -> dict:
        """
        Scrapes the reviews from the website.

        Returns:
            dict: A dictionary containing the scraped reviews data.

        """
        time.sleep(2)
        fetch = self.fetch()
        if fetch:
            return self.parse_characteristics_data()

    def parse_characteristics_data(self, characteristics_section_css: str = "") -> dict:
        pass


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

    def __init__(self, driver=None, url=None):
        super().__init__(driver, url)

    def scrape(self) -> dict:
        """
        Scrapes the product data from the website.

        Returns:
            dict: A dictionary containing the scraped product data.

        """
        time.sleep(2)
        fetch = self.fetch()
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

    def parse_product_data(self, product_images_css: str = "div.product-images", product_section_css: str = "section.vtmn-font-regular") -> dict:
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
        print('Price:', current_price)

        try:
            previous_price = product_data.find_element(
                By.CSS_SELECTOR, "span.vtmn-price_size--xsmall").text
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
            print('Rating:', rating)
        except NoSuchElementException:
            rating = None
            print('Rating: Not available')

        try:
            reviews_button = product_data.find_element(
                By.CSS_SELECTOR, "button.review-link")
            n_reviews = reviews_button.text.replace(
                ' opiniones', '').replace('Leer las ', '').replace('Leer ', '').replace(' opinión', '').split('\n')[-1]
            print('Reviews:', n_reviews)
        except NoSuchElementException:
            n_reviews = 0
            print('Reviews: Not available')

        return {
            "id": product_id,
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


def query_decathlon(query: str = "balón", search_for='products') -> pd.DataFrame:
    ds = DecathlonSearcher(query)
    products = ds.scrape()
    driver = ds.get_driver()
    product_data = list()
    print(len(products))    # Get the driver to pass to the ProductScraper
    for product in products:
        new_url = product["url"]
        try:
            scraper = MAPPER[search_for]['scraper'](driver, new_url)
            product_data.append(pd.DataFrame(scraper.scrape(), index=[0]))
        except NoSuchElementException:
            print(f"Could not scrape {product['name']}")
            continue

    product_data = pd.concat(product_data, ignore_index=True)
    return product_data


def main(queries: list = QUERIES_TO_MAKE, tipo='products') -> None:
    out = pd.DataFrame()
    for query in queries:
        out = pd.concat([out, query_decathlon(query)])

    out.to_csv(MAPPER[tipo]['output_file'], index=False)
    return None


if __name__ == "__main__":
    if len(
            sys.argv) < 2:
        print("Usage: python -m scraper *<queries> --get <info>")
        print("Example: python -m scraper balón --get products")
        print("Valid info: products, reviews, characteristics")
        main(queries=QUERIES_TO_MAKE, tipo='products')
        sys.exit()
    elif sys.argv[-2] == '--get':
        assert sys.argv[-1] in MAPPER.keys(
        ), f'Invalid info: {sys.argv[-1]}, valid info: {list(MAPPER.keys())}'
        main(queries=sys.argv[2:-2], tipo=sys.argv[-1])
        sys.exit()
    else:
        print('No info provided')
        print('Scraping products by default')
        main(queries=sys.argv[2:], tipo='products')
        sys.exit()
