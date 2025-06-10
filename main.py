from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging


# Configure logging
logging.basicConfig(
    filename='test_report.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


def run_test(query):
    # Initialize Chrome with options to bypass bot detection
    service = Service()
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

    try:
        print(f"Test started for query: '{query}'")
        logging.info(f"Test started for query: '{query}'")

        # Open Google and wait for search field
        driver.get("https://www.google.com") 
        wait = WebDriverWait(driver, 10)

        # Find and use the search box
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Wait for results and extract first title
        try:
            first_result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
            result_text = first_result.text
            print(f"Result found for '{query}': {result_text}")
            logging.info(f"Result found for '{query}': {result_text}")
        except:
            print(f"No results found for query: '{query}'")
            logging.warning(f"No results found for query: '{query}'")

    except Exception as e:
        print(f"Error during test for '{query}': {e}")
        logging.error(f"Error during test for '{query}': {e}")

    finally:
        driver.quit()


# Run tests
if __name__ == "__main__":
    print("Starting automated tests...")
    run_test("Python")
    run_test("лаьыладвыasdasdasdasd123123!!!")
    print("Tests completed. Results saved in test_report.log")
