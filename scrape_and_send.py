import time
import json
import requests # Библиотека для отправки в Make
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# --- НАСТРОЙКИ ---
MAKE_WEBHOOK_URL = "СЮДА_ВСТАВЬ_ТВОЮ_ССЫЛКУ_ИЗ_MAKE"
TARGET_USERNAME = "zuck" # Кого парсим
# -----------------

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless") # Запуск без окна браузера (ОБЯЗАТЕЛЬНО для сервера)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scrape_threads():
    driver = setup_driver()
    url = f"https://www.threads.net/@{TARGET_USERNAME}"
    print(f"Захожу на {url}...")
    driver.get(url)
    
    time.sleep(10) # Ждем прогрузки (тупой метод, но надежный)
    
    # Ищем посты (это примерная логика, классы могут меняться у Meta)
    # Здесь мы ищем текстовые блоки. Meta часто меняет названия классов.
    # Этот код собирает весь текст со страницы.
    posts = []
    elements = driver.find_elements(By.XPATH, '//div[@data-pressable-container="true"]')
    
    for el in elements[:5]: # Берем первые 5
        try:
            text = el.text
            if text:
                posts.append({"text": text, "username": TARGET_USERNAME})
        except:
            pass
            
    driver.quit()
    return posts

def send_to_make(data):
    if not data:
        print("Нет данных для отправки.")
        return
    
    print(f"Отправляю {len(data)} постов в Make...")
    # Отправляем весь список разом
    response = requests.post("https://hook.eu1.make.com/wescwbnt41v81xix191dqr8p0sdqgy39", json={"posts": data})
    print(f"Статус отправки: {response.status_code}")

if __name__ == "__main__":
    data = scrape_threads()
    send_to_make(data)
