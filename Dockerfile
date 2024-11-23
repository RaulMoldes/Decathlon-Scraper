# Usa una imagen base de Python 3.11
FROM python:3.11-slim


WORKDIR /app

# Evitar las preguntas interactivas durante la instalación
ENV DEBIAN_FRONTEND=noninteractive


# Actualizar el sistema e instalar dependencias necesarias
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    apt-transport-https \
    ca-certificates \
    curl \
    --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Añadir el repositorio oficial de Google Chrome y su clave GPG
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Instalar Google Chrome
RUN apt-get update && apt-get install -y \
    google-chrome-stable \
    --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Instalar Firefox
RUN apt-get update && apt-get install -y \
    firefox-esr \
    --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Añadir el repositorio oficial de Microsoft Edge y su clave GPG
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" >> /etc/apt/sources.list.d/microsoft-edge.list'

# Instalar Microsoft Edge
RUN apt-get update && apt-get install -y \
    microsoft-edge-stable \
    --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
    
# Copiar el archivo requirements.txt al contenedor
COPY requirements.txt /app/requirements.txt

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

# Verifica que Google Chrome está instalado correctamente
RUN google-chrome --version

CMD ["bash"]
