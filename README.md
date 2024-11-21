# Zkraper

Zkraper is a Python-based web scraping tool that uses Selenium with Google Chrome in headless mode for automated browsing and data extraction. The project is designed to run inside a Docker container, ensuring an isolated and consistent environment.

# Steps:

1. **Build the image**
`docker build -t zkraper:V0 .`

2 **Run the container**
`docker run -it zkraper:v0 --rm "%cd%":/app `
