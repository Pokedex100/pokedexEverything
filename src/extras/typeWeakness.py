from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re


def getWeaknessTypes(type1, type2=None):
    if type2 is None:
        type2 = "none"
    # URL of the website with two query strings
    url = 'https://yashrajbharti.github.io/Pokemon-Type-Weakness-Calculator/?type1={}&type2={}'.format(
        type1, type2)

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

    pattern = re.compile(r'\D*(\d+)\D*')

    # Find all <li> elements in the HTML
    li_elements = soup.find_all('li')

    # Print the content of each <li> element
    arr = []
    for li in li_elements:
        if (int(pattern.search(li.text).group(1)) >= 2):
            arr.append(re.sub(r':.*', '', li.text.strip()))
    return (arr)
