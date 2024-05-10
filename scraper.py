from base import DECATHLON
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selectorlib import Extractor
import requests
import json
import time


class DecathlonScraper:
    def __init__(self, driver=webdriver.Chrome(service=Service(), options=webdriver.ChromeOptions()), url=DECATHLON):
        self.driver = driver
        self.url = url

    def fetch(self):
        return self.driver.get(self.url)


class DecathlonSearch(DecathlonScraper):
    def __init__(self, item, driver=webdriver.Chrome(service=Service(), options=webdriver.ChromeOptions()), url=DECATHLON):
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
        self.fetch()
        self.remove_popup()
        self.search()
        return self.get_products()
