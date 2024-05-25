from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def get_ticker_symbols(offset, count):
    url = f'https://finance.yahoo.com/gainers?offset={offset}&count={count}'

    # Use Selenium in headless mode
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run Chrome in headless mode (no GUI)

    # Create a webdriver with the specified options
    driver = webdriver.Chrome(options=chrome_options)  # You need to have ChromeDriver installed

    try:
        driver.get(url)

        # Scroll down to load additional content
        for _ in range(3):  # You may need to adjust the number of scrolls based on the page structure
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Give the content some time to load

        # Get the page source after scrolling
        page_source = driver.page_source
    finally:
        # Close the browser
        driver.quit()

    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Extract the ticker symbols
    stocks = [stock.text for stock in soup.find_all(attrs={'data-test': 'quoteLink'})]

    return stocks

# Your existing code
offset = 25
count = 25
print(get_ticker_symbols(offset, count))