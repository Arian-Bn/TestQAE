from selenium import webdriver #Открывает браузер и управляет им
from selenium.webdriver.chrome.service import Service #Помогает запустить ChromeDriver как отдельную службу (нужно для связи с браузером). 
from selenium.webdriver.common.by import By #Используется, чтобы искать элементы на странице (по имени, id, CSS-классу и т.д.). 
from selenium.webdriver.common.keys import Keys #Позволяет "печатать" и нажимать клавиши, например Enter или Tab. 
from selenium.webdriver.support.ui import WebDriverWait #Ждёт, пока нужный элемент появится на странице (вместо глупого time.sleep()). 
from selenium.webdriver.support import expected_conditions as EC #Список условий для ожидания: "элемент виден", "страница загрузилась" и т.п. 
import time #Стандартная библиотека Python для пауз (time.sleep())
import logging #Для записи логов в файл: какие шаги выполнились, где ошибка и т.д. 

# Настройка логирования
logging.basicConfig(
    filename='test_report.log',
    level=logging.INFO, #Будут записываться только сообщения уровня INFO и выше (например, WARNING, ERROR).
    #DEBUG – детали (по умолчанию не пишутся)
    #INFO – нормальная работа
    #WARNING – что-то может сломаться
    #ERROR – серьёзная ошибка
    #CRITICAL – критическая ошибка
    format='%(asctime)s - %(levelname)s - %(message)s' #Формат сообщений в логе: 
    #%(asctime)s – время события
    #%(levelname)s – уровень сообщения (INFO, WARNING и т.д.)
    #%(message)s – само сообщение, которое ты отправляешь в лог
     
)

# Функция для выполнения поиска
def run_test(query):
    # Инициализация браузера
    service = Service() #Создаёт службу для запуска ChromeDriver.
    options = webdriver.ChromeOptions() #Создаём настройки браузера (опции). 
    options.add_argument("--disable-blink-features=AutomationControlled") #Отключаем флаг, который говорит сайту: "Этот браузер управляется роботом". 
    options.add_experimental_option("excludeSwitches", ["enable-automation"])#Убираем надпись в браузере: "Chrome is being controlled by automated software" . 
    options.add_experimental_option("useAutomationExtension", False)#    Отключаем автоматизированное расширение — ещё один способ выглядеть как обычный пользователь. 
    
    driver = webdriver.Chrome(service=service, options=options)#Запускаем браузер Google Chrome с этими настройками. 
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined});") #Убираем свойство navigator.webdriver, чтобы сайт не понял, что мы робот. 

    try:
        print(f"Тест начат для запроса: '{query}'")
        logging.info(f"Тест начат для запроса: '{query}'")

        # Переход на Google
        driver.get("https://www.google.com") #Переходим на главную страницу Google.
        wait = WebDriverWait(driver, 10)#Готовим функцию, которая будет ждать элементы до 10 секунд. 

        # Поиск поля ввода
        search_box = wait.until(EC.presence_of_element_located((By.NAME, "q"))) #Ждём появления поля поиска (его имя — "q"). 
        search_box.clear()#Очищаем поле поиска, если там был старый текст. 
        search_box.send_keys(query)#Вводим наш поисковой запрос. 
        search_box.send_keys(Keys.RETURN)#Нажимаем Enter — искать!

        # Ожидание результатов
        try:
            first_result = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "h3")))
            result_text = first_result.text
            print(f"Результат найден для '{query}': {result_text}")
            logging.info(f"Результат найден для '{query}': {result_text}")
        except:
            print(f"Нет результатов для запроса: '{query}'")
            logging.warning(f"Нет результатов для запроса: '{query}'")
            #Ждём, пока появится первый результат поиска (заголовок h3).
            #Если нашли — выводим его.
            #Если нет — пишем, что ничего не нашлось. 

    except Exception as e:
        print(f"Ошибка при выполнении теста для '{query}': {e}")
        logging.error(f"Ошибка при выполнении теста для '{query}': {e}")
        #Ловим любую ошибку и выводим её в консоль и в лог.

    finally:
        driver.quit()
        #Закрываем браузер даже если была ошибка.

# Запуск тестов
if __name__ == "__main__": #    Это проверка: "Если я запустил этот файл сам, а не подключил как модуль — делай то, что внутри". 
     #(Всё, что внутри, будет работать только при прямом запуске файла.) 
    print("Запуск автотестов...")
    run_test("Python")
    run_test("лаьыладвыasdasdasdasd123123!!!")
    print("Тесты завершены. Результаты записаны в test_report.log")


#ChromeDriver — это отдельная программа, которая позволяет инструментам автоматизации (например, Selenium WebDriver) управлять браузером Google Chrome или Chromium.
