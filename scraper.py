from base import DECATHLON
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
import time


class DecathlonScraper:
    def __init__(self,  driver=None, url=DECATHLON):
        if driver is None:
            self.driver = webdriver.Chrome(
                service=Service(), options=webdriver.ChromeOptions())
        else:
            self.driver = driver
        self.url = url

    def get_driver(self):
        return self.driver

    def fetch(self):
        print(f"Fetching {self.url}")
        self.driver.get(self.url)
        return True


class DecathlonSearch(DecathlonScraper):
    def __init__(self,  item, driver=None, url=DECATHLON):
        super().__init__(driver, url)
        self.item = item

    def remove_popup(self, popup_id="didomi-popup", sleep_time=2):
        popup = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located((By.ID, popup_id)))

        popup_close_button = popup.find_element(
            By.CSS_SELECTOR, "span")
        popup_close_button.click()
        time.sleep(sleep_time)
        return True

    def search(self, search_class="svelte-1xw4dnq", sleep_time=2):

        search_box = self.driver.find_element(
            By.CSS_SELECTOR, f"input.{search_class}")
        search_button = self.driver.find_element(
            By.CSS_SELECTOR, f"button.{search_class}")
        search_box.send_keys(self.item)
        search_button.click()
        time.sleep(sleep_time)
        return True

    def get_products(self, product_item_css=".dpb-product-model-link"):
        product_captions = self.driver.find_elements(
            By.CSS_SELECTOR, product_item_css)

        products = list()
        for product in product_captions:
            if product.tag_name == "a":
                products.append({
                    "name": product.text,
                    "url": product.get_attribute("href")
                })
        return products

    def scrape(self):

        fetch = self.fetch()
        if fetch:
            popup = self.remove_popup()
        if popup:
            search = self.search()
        if search:
            return self.get_products()


class ProductScraper(DecathlonScraper):
    def __init__(self, driver=None, url=None):
        super().__init__(driver, url)

    def scrape(self):
        time.sleep(2)
        fetch = self.fetch()
        if fetch:
            return self.parse_product_data()

    def parse_product_data(self, product_section_css="section.vtmn-font-regular"):

        product_data = self.driver.find_element(
            By.CSS_SELECTOR, product_section_css)
        print('---------------------------------------')
        name = product_data.find_element(By.CSS_SELECTOR, "h1").text
        print('Product Name:', name)
        brand = product_data.find_element(By.TAG_NAME, "a").text
        print('Brand:', brand)
        brand_url = product_data.find_element(
            By.TAG_NAME, "a").get_attribute("href")
        price = product_data.find_element(
            By.CSS_SELECTOR, "span.vtmn-price").text
        print('Price:', price)
        reviews_url = product_data.find_element(
            By.CLASS_NAME, "review-link").get_attribute("href")
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

        return {
            "name": name,
            "brand": brand,
            "brand_url": brand_url,
            "price": price,
            "reviews_url": reviews_url,
            "description": description,
            "color": color
        }


def main(query="balón de fútbol"):
    ds = DecathlonSearch(query)
    products = ds.scrape()
    driver = ds.get_driver()
    product_data = list()    # Get the driver to pass to the ProductScraper
    for product in products:
        new_url = product["url"]
        pds = ProductScraper(driver, new_url)
        product_data.append(pds.scrape())

    return product_data


if __name__ == "__main__":
    print(main())
