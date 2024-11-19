import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from queue import Queue
from bs4 import BeautifulSoup

# Paso 1: Configuración de Selenium y abrir la página web
def setup_driver():
    # Usar opciones de Chrome para evitar que aparezcan popups de forma automática
    chrome_options = Options()
  #  chrome_options.add_argument("--headless")  # Ejecutar en segundo plano sin abrir el navegado# Asegúrate de tener el path correcto del chromedriver
    driver = webdriver.Chrome(options=chrome_options)
    return driver



# Paso 2: Cerrar los popups (si existen)
def close_popups(driver):
    try:
        # Esperar hasta que un popup de cierre sea visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//button[contains(text(), 'Cerrar') or contains(text(), 'Aceptar') or contains(@class, 'close') or contains(@aria-label, 'Cerrar')]"))
        )
        
        # Buscar el primer botón que coincida con los criterios
        close_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Cerrar') or contains(text(), 'Aceptar') or contains(@class, 'close') or contains(@aria-label, 'Cerrar')]")
        
        # Hacer clic en el botón de cerrar
        close_button.click()
        print("Popup cerrado.")
    
    except Exception as e:
        print("No se encontró un popup o ya se cerró.")
        # Puedes agregar más detalles de la excepción si es necesario: print(f"Error: {str(e)}")


# Paso 3: Obtener todas las URLs de la página
def get_all_urls(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    links = soup.find_all('a', href=True)
    urls = [link['href'] for link in links]
    return urls

# Paso 4: Scrapeo de contenido de texto (p) de la URL
def scrape_url(driver, url):
    driver.get(url)
    time.sleep(2)  # Espera para que cargue el contenido (puedes ajustarlo según tu caso)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Obtener todo el texto dentro de las etiquetas <p>
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    return text

def main():
    # Iniciar el driver
    driver = setup_driver()
    print("Soy un scraper estoy scrapeando")
    # Paso 1: Cargar la página web
    start_url = "https://www.marca.com"
    driver.get(start_url)
    time.sleep(2)  # Espera a que la página cargue
    print(start_url)
    # Paso 2: Cerrar cualquier popup si aparece
    close_popups(driver)
    
    # Paso 3: Obtener todas las URLs de la página
    urls = get_all_urls(driver)
    print(urls)
    # Colocar las URLs en una cola (queue)
    url_queue = Queue()
    for url in urls:
        url_queue.put(url)
    
    # Paso 4: Scrapeo de cada URL en la cola
    while not url_queue.empty():
        url = url_queue.get()
        print(f"Scrapeando {url}...")
        try:
            text = scrape_url(driver, url)
            print(f"Texto de {url}: {text[:200]}...")  # Muestra solo los primeros 200 caracteres
        except Exception as e:
            print(f"No se pudo scrapeear {url}: {str(e)}")
    
    # Cerrar el driver
    driver.quit()

if __name__ == "__main__":
    main()