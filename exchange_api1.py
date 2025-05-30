import requests

def get_exchange_rate():

    try:
        url = "https://v6.exchangerate-api.com/v6/0fbdd32afc8718e9f95ae900/latest/USD"
        response = requests.get(url)
        data = response.json()

        print("API den gelen veri:", data)   #DEBUG Command

        rate = data["rates"]["TRY"]
        return rate
    except Exception as e:
        print(f"Döviz kuru alınamadı: {e}")
        return None