from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import random
import logging

# Настройка логирования
logging.basicConfig(
    filename="test_report.log",  # Имя файла для записи отчета
    level=logging.INFO,          # Уровень логирования
    format="%(asctime)s - %(levelname)s - %(message)s"  # Формат записи
)

# Настройка ChromeOptions
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Отключаем флаги автоматизации
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])  # Скрываем индикатор автоматизации
chrome_options.add_experimental_option("useAutomationExtension", False)

# Указываем путь к chromedriver.exe
service = Service()  
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

def test_search(query):
    try:
        # Логируем начало теста
        logging.info(f"Тест запущен для запроса: '{query}'.")

        # Шаг 1: Открываем Google
        driver.get("https://www.google.com")
        time.sleep(random.uniform(1, 3))  # Случайная задержка
        logging.info("Открыт сайт Google.")

        # Шаг 2: Находим поле поиска и вводим текст
        search_box = driver.find_element(By.NAME, "q")  # Поле поиска на Google
        search_box.clear()  # Очищаем поле (на случай, если там что-то есть)
        search_box.send_keys(query)  # Вводим текст запроса
        search_box.send_keys(Keys.RETURN)  # Нажимаем Enter
        logging.info(f"Выполнен поиск по запросу: '{query}'.")

        # Шаг 3: Ждём появления результатов поиска или сообщения об их отсутствии
        try:
            # Проверяем наличие заголовков результатов поиска
            result = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "h3"))  # Заголовки результатов поиска
            )
            result_text = result.text
            logging.info(f"Первый результат поиска: {result_text}")

            # Проверяем, содержит ли результат ожидаемый текст
            if query.lower() in result_text.lower():
                print(f"Тест успешно выполнен для запроса: '{query}'. Результат найден.")
                logging.info(f"Тест успешно выполнен для запроса: '{query}'. Результат найден.")
            else:
                print(f"Тест не пройден для запроса: '{query}'. Полученный текст: {result_text}")
                logging.error(f"Тест не пройден для запроса: '{query}'. Полученный текст: {result_text}")

        except:
            # Если результаты не найдены, проверяем наличие сообщения об отсутствии результатов
            no_results_message = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ничего не найдено')]"))
            )
            message_text = no_results_message.text
            print(f"Тест успешно выполнен для запроса: '{query}'. Результатов нет. Сообщение: {message_text}")
            logging.info(f"Тест успешно выполнен для запроса: '{query}'. Результатов нет. Сообщение: {message_text}")

    except Exception as e:
        # Обработка неожиданных ошибок
        print(f"Произошла ошибка при выполнении теста для запроса: '{query}'. Ошибка: {e}")
        logging.error(f"Произошла ошибка при выполнении теста для запроса: '{query}'. Ошибка: {e}")

try:
    # Тестируем успешный запрос
    test_search("Python")

    # Тестируем запрос, для которого результатов нет
    test_search("asdasdasdasd123123!!!")

finally:
    # Закрываем браузер
    driver.quit()
    logging.info("Браузер закрыт.")