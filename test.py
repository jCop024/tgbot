import requests

TOKEN = "8492543105:AAFn71vjfme8wOC5GIj1f3PC1uY3Z3XUT6I"
CHAT_ID = "1196810918"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    print(response.status_code, response.text)

send_telegram("Test zpráva z Pythonu 🚀")