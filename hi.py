from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def extract_gainers_data(url):
    # Initialize ChromeDriver (you can use other browsers as well)
    driver = webdriver.Chrome()  # Make sure the path to ChromeDriver is in your system's PATH

    # Open the URL
    driver.get(url)

    try:
        # Use WebDriverWait to wait for the dynamic content to load
        element_present = EC.presence_of_element_located((By.XPATH, 'your_xpath_for_dynamic_content'))
        WebDriverWait(driver, timeout=10).until(element_present)

        # Find and extract information
        tickers = driver.find_elements(By.XPATH, 'your_xpath_for_tickers')

        for ticker in tickers:
            print(ticker.text)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

# Replace 'your_url' with the actual URL of the Yahoo Finance gainers page with filters applied
url = 'your_url'
extract_gainers_data(url)