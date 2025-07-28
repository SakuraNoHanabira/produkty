import json
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from difflib import get_close_matches

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

url = "https://raw.githubusercontent.com/SakuraNoHanabira/produkty/main/produkty.json"

def load_products_codes(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        products_codes = json.loads(response.text)
        print(f"✅ Załadowano {len(products_codes)} produktów z GitHub.")
        return products_codes
    except Exception as e:
        print(f"❌ Błąd przy pobieraniu produktów: {e}")
        return {}

def find_best_match(name, dictionary):
    matches = get_close_matches(name, dictionary, n=1, cutoff=0.5)
    return matches[0] if matches else None

products_codes = load_products_codes(url)

# Tutaj jest zmiana — webdriver-manager automatycznie dobierze chromedriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://easy-plu.knowledge-hero.com/login")

input("🔐 Zaloguj się ręcznie, a potem naciśnij Enter, by rozpocząć...")

print("\n✅ Automatyczne rozpoznawanie produktów uruchomione.\n")

last_product = None

try:
    while True:
        try:
            product_element = driver.find_element(By.XPATH, "//h1[contains(@class, 'font-bold')]")
            product_name = product_element.text.strip()

            if product_name != last_product:
                print(f"\n🛒 Nowy produkt: {product_name}")

                matched = find_best_match(product_name, products_codes.keys())

                if matched:
                    code = products_codes[matched]
                    print(f"➡️ Wpisuję kod PLU: {code} (dopasowano do: {matched})")

                    input_field = driver.find_element(By.XPATH, "//input[@id='plu-number-input']")
                    input_field.clear()
                    input_field.send_keys(code)
                    input_field.send_keys(Keys.ENTER)
                else:
                    print(f"❌ Nie znaleziono kodu dla produktu: {product_name}")

                last_product = product_name

        except Exception as e:
            print(f"⚠️ Błąd podczas rozpoznawania produktu: {e}")

        time.sleep(0.7)

except KeyboardInterrupt:
    print("\n🛑 Zatrzymano ręcznie (Ctrl+C).")
