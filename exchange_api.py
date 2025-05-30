import requests

def get_exchange_rate():
    try:
        url = "https://open.er-api.com/v6/latest/USD"
        response = requests.get(url)
        data = response.json()

        print("API'den gelen veri:", data)  # Hataları görmek için

        if "rates" in data and "TRY" in data["rates"]:
            return data["rates"]["TRY"]
        else:
            print("Döviz kuru alınamadı: 'rates' anahtarı yok")
            return None
    except Exception as e:
        print(f"Döviz kuru alınamadı: {e}")
        return None