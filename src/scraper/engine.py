import requests
from bs4 import BeautifulSoup
from src.utils.scraping_utils import extract_all_links, extract_images, extract_meta_data, extract_all_text
from src.utils.output_utils import save_to_files
from concurrent.futures import ThreadPoolExecutor, as_completed
from queue import Queue
from src.scraper.driver import log_in
import os

def is_page_scrapeable(url:str, user_agent:str = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'):
    try:

        response = requests.get(url, headers={'User-Agent':user_agent})
        
       
        if response.status_code != 200:
            return False
        
        # Analizar el contenido de la página con BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        principal = soup.get_text().strip()
        
        
        if len(principal) < 50 or not soup.find(['article', 'main', 'div', 'section']):
            return False

        return True
    
    except requests.RequestException as e:
        return False, "Error al intentar acceder a la URL: {}".format(str(e))
    

def scraper_routine(driver, url_queue:Queue, visited_urls:set, base_url:str, domain:str, output_dir:str):
    if is_page_scrapeable(base_url):
        print(f"Url: {base_url} is scrapeable")
        scrape_page(driver= driver, url_queue=url_queue, visited_urls=visited_urls, base_url = base_url, domain = domain, output_dir=output_dir)
    else:
        print(f"Skipping: {base_url}")

# Main scraping function
def scrape_page(driver, url_queue: Queue, visited_urls: set, base_url: str, domain: str, output_dir: str):
    try:
        driver.get(base_url)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')

        # Llamar a las funciones para extraer datos
        meta_data = extract_meta_data(soup)
        images = extract_images(soup, base_url)
        links = extract_all_links(soup, domain, base_url)
        text = extract_all_text(soup)
        # Save the extracted data
        save_to_files(meta_data, images, links,text, output_dir)

        # Process internal links
        for link in links['internal']:
            if link not in visited_urls:
                visited_urls.add(link)
                url_queue.put(link)

        print(f"Scraper found {len(links['internal'])} internal links.")

    except Exception as e:
        print(f"Error scraping {base_url}: {e}")

# Scraping engine with concurrency
def scraping_engine(driver, base_url, domain, output_dir, max_scrapers=10):
    # Initialize the queue and the set of visited URLs
    url_queue = Queue()
    visited_urls = set()
    
    # Add the initial URL to the queue
    url_queue.put(base_url)
    visited_urls.add(base_url)

    print("Starting engine...")

    # Create a pool of threads for concurrent scraping
    with ThreadPoolExecutor(max_workers=max_scrapers) as executor:
        # List of futures to track active threads
        futures = []
        scraper_id = 0
        while not url_queue.empty() or any([future.running() for future in futures]):
            if len(futures) < max_scrapers and not url_queue.empty():
                # Get the next URL from the queue
                next_url = url_queue.get()

                # Start a new scraping task
                print(f"Starting scraper for URL: {next_url}")
                print(f"Scraper id: {scraper_id}")

                unique_output_dir = os.path.join(output_dir, f"scraper={scraper_id}")
                os.makedirs(unique_output_dir, exist_ok=True)
                unique_output_dir = output_dir +"/" + "scraper="+str(scraper_id)
                future = executor.submit(scraper_routine, driver, url_queue, visited_urls, next_url, domain, unique_output_dir)
                futures.append(future)
                scraper_id += 1
                

            # Clean up completed futures
            for future in as_completed(futures):
                futures.remove(future)

    print("Web scraping engine terminated")
    return "Web scraping engine terminated"
