from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# Настройка логирования
logging.basicConfig(
    filename='test_report.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Функция для выполнения поиска
def run_test(query):
    # Инициализация браузера
    service = Service()  # Убедись, что chromedriver в PATH
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});")

    try:
        print(f"Тест начат для запроса: '{query}'")
        logging.info(f"Тест начат для запроса: '{query}'")

        # Переход на Google
        driver.get("https://www.google.com")
        wait = WebDriverWait(driver, 10)

        # Поиск поля ввода
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Ожидание результатов
        try:
            first_result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
            result_text = first_result.text
            print(f"Результат найден для '{query}': {result_text}")
            logging.info(f"Результат найден для '{query}': {result_text}")
        except:
            print(f"Нет результатов для запроса: '{query}'")
            logging.warning(f"Нет результатов для запроса: '{query}'")

    except Exception as e:
        print(f"Ошибка при выполнении теста для '{query}': {e}")
        logging.error(f"Ошибка при выполнении теста для '{query}': {e}")

    finally:
        driver.quit()

# Запуск тестов
if __name__ == "__main__":
    print("Запуск автотестов...")
    run_test("Python")
    run_test("лаьыладвыasdasdasdasd123123!!!")
    print("Тесты завершены. Результаты записаны в test_report.log")
