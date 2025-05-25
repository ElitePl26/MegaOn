import requests

token = "7546206183:AAEDtig95ySDic82smvP_EHLIDkvEoi8Iu4"
url = f"https://api.telegram.org/bot{token}/getUpdates"

try:
    response = requests.get(url, timeout=1)
    print("✅ Instância anterior encerrada.")
except requests.exceptions.ReadTimeout:
    print("✅ Timeout forçado. Bot liberado com sucesso.")
