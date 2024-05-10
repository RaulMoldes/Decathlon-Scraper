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


def search_decathlon(item):
    driver = webdriver.Chrome(
        service=Service(), options=webdriver.ChromeOptions())
    driver.get(DECATHLON)

    # Wait for the popup to appear and then close it
    popup = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "didomi-popup")))
    print('Popup found')

    popup_close_button = popup.find_element(
        By.CSS_SELECTOR, "span")
    popup_close_button.click()

    time.sleep(2)
    search_box = driver.find_element(By.CSS_SELECTOR, "input.svelte-1xw4dnq")
    search_button = driver.find_element(
        By.CSS_SELECTOR, "button.svelte-1xw4dnq")
    search_box.send_keys(item)
    search_button.click()
    time.sleep(2)
    product_captions = driver.find_elements(
        By.CSS_SELECTOR, "a.dpb-product-model-link svelte-1bclr8g")
    print(product_captions)
    for product in product_captions:
        print(product.get_attribute("href"))

    driver.quit()


search_decathlon("Ropa deportiva")
