
from bs4 import BeautifulSoup
from src.utils.scraping_utils import extract_all_links, extract_images, extract_meta_data
from src.utils.output_utils import save_to_files

def scrape_page(driver, base_url: str, domain:str, output_dir: str):
    # Inicializar BeautifulSoup con la página que deseas scrapear
    # Aquí se asume que has descargado el HTML previamente usando Selenium o Requests
    driver.get(base_url)
    html = driver.page_source # Sustituir con el HTML real de la página
    soup = BeautifulSoup(html, 'html.parser')

    # Llamar a las funciones para extraer datos
    meta_data = extract_meta_data(soup)
    images = extract_images(soup, base_url)
    links = extract_all_links(soup, base_url, domain)

    # Guardar los resultados extraídos
    save_to_files(meta_data, images, links, output_dir)

