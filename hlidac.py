import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pickle
import os

# URL stránky se směnami
URL = "https://shameless.sinch.cz/react/dashboard/overview"

# Telegram – vlož své údaje
TOKEN = "8492543105:AAFn71vjfme8wOC5GIj1f3PC1uY3Z3XUT6I"
CHAT_ID = "1196810918"

# Funkce pro poslání zprávy na Telegram
def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": msg})

# --- Spuštění Chrome ---
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

driver.get(URL)

# === Přihlášení a uložení cookies ===
if os.path.exists("cookies.pkl"):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
    driver.refresh()
else:
    print("👉 Přihlas se ručně přes Google a pak stiskni ENTER")
    input()
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))

time.sleep(5)

# Funkce, která vrátí počet řádků v tabulce směn
def get_shift_rows():
    return driver.find_elements(By.CSS_SELECTOR, "table tbody tr")

old_count = len(get_shift_rows())
print("Počet směn:", old_count)

# --- HLÍDÁNÍ SMĚN ---
while True:
    time.sleep(8)  # kontrola každých 10 sekund
    driver.refresh()
    time.sleep(5)   # počkej, až se tabulka načte

    new_count = len(get_shift_rows())

    if new_count > old_count:
        send_telegram("🚨 Vyskočila nová směna!")
        old_count = new_count