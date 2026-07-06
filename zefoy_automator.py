#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Автоматизация Zefoy.com – увеличение лайков на указанное видео TikTok
# Зависимости: pip install selenium undetected-chromedriver fake-useragent

import time
import random
import sys
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

# =============================================
# КОНФИГУРАЦИЯ – измените под свои нужды
# =============================================
TARGET_URL = "https://vt.tiktok.com/ZSCGUyw7Y/"   # ваша ссылка
USE_PROXY = None  # например "http://user:pass@ip:port" или None
HEADLESS = False  # True – без открытия окна браузера, False – видимый режим
WAIT_MULTIPLIER = 1.5  # множитель всех задержек (можно увеличить для слабого интернета)

# =============================================
# ИНИЦИАЛИЗАЦИЯ ДРАЙВЕРА
# =============================================
def init_driver():
    options = uc.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    ua = UserAgent().random
    options.add_argument(f'--user-agent={ua}')
    if HEADLESS:
        options.add_argument('--headless=new')
    if USE_PROXY:
        options.add_argument(f'--proxy-server={USE_PROXY}')
    driver = uc.Chrome(options=options, version_main=114)  # укажите свою основную версию Chrome
    return driver

# =============================================
# ОБРАБОТКА КАПЧИ (ПРОСТАЯ ПАУЗА ДЛЯ РУЧНОГО РЕШЕНИЯ)
# =============================================
def handle_captcha(driver):
    # Если появляется Cloudflare или reCAPTCHA, ждём ручного вмешательства
    print("[!] Обнаружена капча. Решите её в браузере и нажмите Enter в консоли...")
    input("Нажмите Enter после прохождения капчи...")

# =============================================
# ПЕРЕХОД НА ZEFOY И ВЕРИФИКАЦИЯ "ЧЕЛОВЕК"
# =============================================
def verify_human(driver):
    driver.get("https://zefoy.com/")
    time.sleep(4 * WAIT_MULTIPLIER)
    # Попытка найти кнопку "Click here to verify"
    try:
        verify_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Click here')] | //a[contains(text(),'verify')]"))
        )
        verify_btn.click()
        print("[*] Кнопка верификации нажата.")
    except:
        print("[*] Кнопка верификации не найдена, возможно уже пройдена.")
    # Ожидание подтверждения
    time.sleep(8 * WAIT_MULTIPLIER)
    # Проверка на капчу
    if "captcha" in driver.page_source.lower():
        handle_captcha(driver)

# =============================================
# ВСТАВКА ССЫЛКИ В ПОЛЕ ВВОДА
# =============================================
def paste_link(driver, url):
    # Ищем поле ввода (обычно единственное input на странице)
    try:
        input_field = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='text' or not(@type)]"))
        )
        input_field.clear()
        input_field.send_keys(url)
        print(f"[+] Ссылка {url} вставлена.")
        time.sleep(2 * WAIT_MULTIPLIER)
    except Exception as e:
        print(f"[-] Не удалось найти поле ввода: {e}")
        return False
    return True

# =============================================
# ВЫБОР УСЛУГИ "LIKES" И ЗАПУСК
# =============================================
def select_likes_service(driver):
    # Ищем все кнопки с иконками сервисов. Обычно кнопка "Likes" содержит сердечко.
    try:
        # Находим элемент, содержащий "Likes" или иконку ❤
        likes_buttons = driver.find_elements(By.XPATH, "//div[contains(@class,'service')]//button | //button[contains(.,'Likes') or contains(.,'Like')]")
        for btn in likes_buttons:
            if 'like' in btn.text.lower() or '❤' in btn.get_attribute('innerHTML'):
                btn.click()
                print("[+] Выбран сервис 'Likes'.")
                time.sleep(3 * WAIT_MULTIPLIER)
                return True
        # Альтернативный поиск по картинке
        likes_icon = driver.find_elements(By.XPATH, "//img[contains(@src,'heart') or contains(@src,'like')]/..")
        if likes_icon:
            likes_icon[0].click()
            print("[+] Выбран сервис 'Likes' (по иконке).")
            time.sleep(3 * WAIT_MULTIPLIER)
            return True
    except Exception as e:
        print(f"[-] Ошибка при выборе лайков: {e}")
    return False

def click_start(driver):
    try:
        # Кнопка старта может быть "Start", "Send", "Submit"
        start_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Start') or contains(text(),'Send') or contains(text(),'Submit')]"))
        )
        start_btn.click()
        print("[+] Процесс запущен.")
        return True
    except:
        print("[-] Кнопка запуска не найдена.")
        return False

# =============================================
# ОЖИДАНИЕ ЗАВЕРШЕНИЯ И ВЫВОД СТАТИСТИКИ
# =============================================
def wait_for_completion(driver):
    time.sleep(5 * WAIT_MULTIPLIER)
    # Ищем сообщения о завершении, например "Success", "Completed", "Done"
    try:
        status = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(),'Completed') or contains(text(),'Success') or contains(text(),'Done')]"))
        )
        print(f"[✓] Результат: {status.text}")
    except:
        print("[!] Таймаут ожидания. Проверьте страницу вручную.")
    # Логируем оставшееся количество (если отображается)
    try:
        count_elem = driver.find_element(By.XPATH, "//span[contains(text(),'Sent') or contains(text(),'Added')]")
        print(f"[i] {count_elem.text}")
    except:
        pass

# =============================================
# ГЛАВНАЯ ФУНКЦИЯ
# =============================================
def main():
    print("=== Vostro Zefoy Automator ===")
    driver = init_driver()
    try:
        verify_human(driver)
        if not paste_link(driver, TARGET_URL):
            sys.exit(1)
        if not select_likes_service(driver):
            print("Сервис лайков не найден. Возможно, изменился интерфейс Zefoy.")
            input("Нажмите Enter для завершения...")
            sys.exit(1)
        if click_start(driver):
            wait_for_completion(driver)
        else:
            print("Не удалось запустить. Возможно, потребуется ручное вмешательство.")
            input("Проверьте браузер и нажмите Enter...")
    except Exception as e:
        print(f"Критическая ошибка: {e}")
    finally:
        print("Завершение работы. Браузер будет закрыт.")
        driver.quit()

if __name__ == "__main__":
    main()
