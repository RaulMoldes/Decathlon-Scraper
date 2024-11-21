from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service



path = ChromeDriverManager().install()
# Configura el navegador con el driver manager
options = webdriver.ChromeOptions()

# Cambia el User-Agent por uno específico para evitar detecciones automáticas.
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
options.add_argument(f"user-agent={user_agent}")

# Ejecutar Chrome en modo 'headless', es decir, sin interfaz gráfica.
options.add_argument("--headless")

# Ejecutar Chrome sin sandboxing. Esto es necesario para que funcione correctamente dentro de contenedores Docker.
options.add_argument("--no-sandbox")

# Soluciona problemas de memoria compartida que pueden ocurrir en contenedores Docker. Evita errores por falta de memoria.
options.add_argument("--disable-dev-shm-usage")

# Desactiva la seguridad web, permitiendo realizar acciones que normalmente están restringidas por motivos de seguridad.
options.add_argument("--disable-web-security")

# Desactiva las notificaciones emergentes en las páginas web, como las solicitudes de permisos o notificaciones push.
options.add_argument("--disable-notifications")

# Desactiva todas las extensiones instaladas en el navegador. Esto hace que el entorno sea más predecible y libre de interferencias.
options.add_argument("--disable-extensions")

# Ignora errores de certificado SSL, lo cual permite navegar en sitios web con certificados inseguros.
options.add_argument("--ignore-certificate-errors")

# Permite la carga de contenido inseguro (no HTTPS) en sitios web seguros (HTTPS), desactivando la protección de contenido mixto.
options.add_argument("--allow-running-insecure-content")

# Evita que Chrome verifique si es el navegador predeterminado en el sistema, acelerando el inicio.
options.add_argument("--no-default-browser-check")

# Desactiva la configuración inicial y la primera ejecución del navegador para agilizar el arranque.
options.add_argument("--no-first-run")

# Establece el nivel de registro del navegador a 3 (sólo errores), lo que reduce la cantidad de registros generados.
options.add_argument("--log-level=3")

# Desactiva el uso del proxy, lo que permite que las conexiones se realicen directamente sin pasar por servidores intermedios.
options.add_argument("--no-proxy-server")

# Oculta la propiedad `navigator.webdriver` y otras características que delatan que se está usando un navegador automatizado.
options.add_argument("--no-blink-features=AutomationControlled")

options.add_argument("--enable-javascript")

serv = Service(path)

# Inicializa el navegador
driver = webdriver.Chrome(service=serv, options=options)

# Ejemplo simple de navegación
driver.get("http://www.google.com")
print(driver.title)  # Debería imprimir "Google"

# Cierra el navegador
driver.quit()
