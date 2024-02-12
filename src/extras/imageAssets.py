from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# URL of the website with a query string
url = 'https://yashrajbharti.github.io/Pokemon-Image-Downloader-Upgrade/?id=656'

# Set up a headless Chrome browser using Selenium
options = Options()
options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
driver = webdriver.Chrome(options=options)

# Load the page using the headless browser
driver.get(url)

# Introduce a delay (1 second in this example) to ensure the page is fully loaded
time.sleep(1)

# Get the page source after it's fully loaded
page_source = driver.page_source

# Close the headless browser
driver.quit()

# Parse the HTML content of the page
soup = BeautifulSoup(page_source, 'html.parser')

# Find all <img> elements in the HTML
img_tags = soup.find_all('img')

# Extract the attributes from each <img> tag
img_info = [{'src': img.get('src', ''), 'alt': img.get('alt', ''), 'form': img.get('data-form', ''), 'shiny':  img.get('data-shiny', '')}
            for img in img_tags]

# Print the list of image information
print("List of image information:")
for img_data in img_info:
    if img_data['alt'] != 'github' and img_data['alt']:
        print(
            f"Src: {img_data['src']}, Name: {img_data['alt']}, Form: {img_data['form']}, Shiny:  {img_data['shiny']}")
