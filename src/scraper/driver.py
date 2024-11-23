import os
import json
import time
import re
from selenium import webdriver  # Usar selenium-wire en lugar de selenium
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def start_driver(driver_options_path: str):
    # Load driver configuration from the JSON file
    with open(driver_options_path, 'r') as file:
        driver_config = json.load(file)

   
    # Use webdrivermanager to install ChromeDriver if needed
    chrome_driver_path = ChromeDriverManager().install()

    # Set up Chrome options
    options = ChromeOptions()

    # Add Chrome options dynamically from the JSON configuration
    if 'user_agent' in driver_config:
        options.add_argument(f"user-agent={driver_config['user_agent']}")

    if driver_config.get("headless", False):
        options.add_argument("--headless")

    if driver_config.get("no_sandbox", False):
        options.add_argument("--no-sandbox")

    if driver_config.get("disable_dev_shm_usage", False):
        options.add_argument("--disable-dev-shm-usage")

    if driver_config.get("disable_web_security", False):
        options.add_argument("--disable-web-security")

    if driver_config.get("disable_notifications", False):
        options.add_argument("--disable-notifications")

    if driver_config.get("disable_extensions", False):
        options.add_argument("--disable-extensions")
    else:
        extensions = driver_config.get("extensions", [])
        if len(extensions) > 0:
            for ext in extensions:
                options.add_argument(f"--load-extension={os.path.abspath(ext)}")

    if driver_config.get("ignore_certificate_errors", False):
        options.add_argument("--ignore-certificate-errors")
        
    if driver_config.get("disable_translate", False):
        options.add_argument("--disable-features=Translate")
        
    if driver_config.get("password_store", None):
        options.add_argument(f"--password-store={driver_config['password_store']}")

    if driver_config.get("allow_running_insecure_content", False):
        options.add_argument("--allow-running-insecure-content")

    if driver_config.get("no_default_browser_check", False):
        options.add_argument("--no-default-browser-check")

    if driver_config.get("no_first_run", False):
        options.add_argument("--no-first-run")

    if 'log_level' in driver_config:
        options.add_argument(f"--log-level={driver_config['log_level']}")

    if driver_config.get("no_proxy_server", False):
        options.add_argument("--no-proxy-server")

    if 'no_blink_features' in driver_config:
        options.add_argument(f"--no-blink-features={driver_config['no_blink_features']}")

    if driver_config.get("enable_javascript", False):
        options.add_argument("--enable-javascript")

    if driver_config.get("experimental_options", {}) != {}:
        options.add_experimental_option(
                "prefs",
                driver_config["experimental_option"]
            )

    # Initialize Chrome WebDriver with the service and options
    serv = ChromeService(chrome_driver_path)
    driver = webdriver.Chrome(service=serv, options=options)


    return driver

def quit_driver(driver):
    driver.quit()
    return True



def log_in(driver, login_url, username_pattern=".*user.*|.*email.*", password_pattern=".*pass.*", username = os.getenv("USERNAME"), password = os.getenv("PASSWORD")):
    """
    Función para intentar hacer login usando expresiones regulares para detectar los campos de usuario, contraseña y el botón submit.
    Si encuentra los campos correctos, procede con el login.
    """
    # Acceder a la URL de login
    driver.get(login_url)

    # Buscar todos los campos de entrada en el formulario
    inputs = driver.find_elements(By.TAG_NAME, 'input')

    # Inicializar variables para los elementos de usuario y contraseña
    user_elem = None
    pass_elem = None
    submit_elem = None

    # Iterar sobre los campos de entrada y buscar los que coincidan con los patrones
    for input_elem in inputs:
        name_attribute = input_elem.get_attribute("name")

        # Comprobar si el nombre del campo de entrada coincide con el patrón del nombre de usuario
        if name_attribute and re.match(username_pattern, name_attribute, re.IGNORECASE):
            user_elem = input_elem  # Encontramos el campo de usuario

        # Comprobar si el nombre del campo de entrada coincide con el patrón de la contraseña
        elif name_attribute and re.match(password_pattern, name_attribute, re.IGNORECASE):
            pass_elem = input_elem  # Encontramos el campo de la contraseña

        # Buscar el campo submit (input con type="submit")
        if input_elem.get_attribute("type") == "submit":
            submit_elem = input_elem  # Encontramos el botón submit

        # Si ya encontramos los campos de usuario, contraseña y el botón submit, no seguimos buscando
        if user_elem and pass_elem and submit_elem:
            break

    # Si se encontraron los campos de usuario, contraseña y el botón submit
    if user_elem and pass_elem and submit_elem:
        try:
            # Ingresar el nombre de usuario y la contraseña
            user_elem.send_keys(username)
            pass_elem.send_keys(password)

            # Enviar el formulario haciendo clic en el botón submit
            submit_elem.click()

            # Esperar un poco para que se procese el login
            time.sleep(5)

            # Verificar si el login fue exitoso (esto puede depender de tu aplicación)
            if "login_success_page" in driver.current_url:  # Cambiar esto a la URL de éxito del login
                print(f"Login exitoso usando los patrones de campo de usuario, contraseña y submit.")
                
                # Extraer cookies
                cookies = driver.get_cookies()
                
                # Pasar las cookies a las URLs hijas
                for cookie in cookies:
                    driver.add_cookie(cookie)
                return driver  # Retorna el driver con las cookies de sesión
            else:
                print("Login fallido o no requerido. Continuando con el scraping sin login.")
        
        except Exception as e:
            print(f"Error realizando login: {e}")
    else:
        print("No se encontraron los campos de usuario, contraseña o submit adecuados. Continuando sin login.")
    
    return driver