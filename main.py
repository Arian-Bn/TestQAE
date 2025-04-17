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
import os
import signal
import psutil

# Очистка файла логов перед запуском программы
def clear_log_file(log_filename):
    try:
        with open(log_filename, 'w') as log_file:
            log_file.write("")  # Очищаем содержимое файла
        print("Файл логов успешно очищен.")
    except Exception as e:
        print(f"Ошибка при очистке файла логов: {e}")

# Настройка логирования в память (список)
class MemoryHandler:
    def __init__(self):
        self.logs = []

    def log(self, level, message):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        self.logs.append(f"{timestamp} - {level} - {message}")

    def save_to_file(self, log_filename):
        try:
            with open(log_filename, 'a') as log_file:  # Добавляем записи в файл
                for log in self.logs:
                    log_file.write(log + "\n")
            print(f"Логи успешно сохранены в файл: {log_filename}")
        except Exception as e:
            print(f"Ошибка при сохранении логов в файл: {e}")

# Очистка процессов ChromeDriver
def kill_chromedriver_processes():
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == 'chromedriver':
                os.kill(proc.info['pid'], signal.SIGTERM)
        print("Очистка процессов ChromeDriver выполнена.")
    except Exception as e:
        print(f"Ошибка при очистке процессов ChromeDriver: {e}")

# Основная программа
log_filename = "test_report.log"
memory_handler = MemoryHandler()

try:
    # Очистка файла логов перед запуском
    clear_log_file(log_filename)

    # Очистка процессов ChromeDriver
    kill_chromedriver_processes()

    # Инициализация ChromeDriver
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    memory_handler.log("INFO", "ChromeDriver успешно инициализирован.")

    # Функция для выполнения теста
    def test_search(query):
        try:
            memory_handler.log("INFO", f"Тест запущен для запроса: '{query}'.")

            # Открываем Google
            driver.get("https://www.google.com")
            time.sleep(random.uniform(1, 3))
            memory_handler.log("INFO", "Открыт сайт Google.")

            # Находим поле поиска и вводим текст
            search_box = driver.find_element(By.NAME, "q")
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            memory_handler.log("INFO", f"Выполнен поиск по запросу: '{query}'.")

            # Ждём результаты поиска
            try:
                result = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "h3"))
                )
                result_text = result.text
                memory_handler.log("INFO", f"Первый результат поиска: {result_text}")

                if query.lower() in result_text.lower():
                    print(f"Тест успешно выполнен для запроса: '{query}'. Результат найден.")
                    memory_handler.log("INFO", f"Тест успешно выполнен для запроса: '{query}'. Результат найден.")
                else:
                    print(f"Тест не пройден для запроса: '{query}'. Полученный текст: {result_text}")
                    memory_handler.log("ERROR", f"Тест не пройден для запроса: '{query}'. Полученный текст: {result_text}")

            except:
                no_results_message = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'ничего не найдено')]"))
                )
                message_text = no_results_message.text
                print(f"Тест успешно выполнен для запроса: '{query}'. Результатов нет. Сообщение: {message_text}")
                memory_handler.log("INFO", f"Тест успешно выполнен для запроса: '{query}'. Результатов нет. Сообщение: {message_text}")

        except Exception as e:
            print(f"Произошла ошибка при выполнении теста для запроса: '{query}'. Ошибка: {e}")
            memory_handler.log("ERROR", f"Произошла ошибка при выполнении теста для запроса: '{query}'. Ошибка: {e}")

    # Тестируем успешный запрос
    test_search("Python")

    # Тестируем запрос, для которого результатов нет
    test_search("asdasdasdasd123123!!!")

finally:
    # Закрываем браузер
    time.sleep(2)  # Задержка перед завершением
    driver.quit()
    memory_handler.log("INFO", "Браузер закрыт.")

    # Сохраняем логи в файл
    memory_handler.save_to_file(log_filename)

    # Очищаем процессы ChromeDriver после завершения
    kill_chromedriver_processes()