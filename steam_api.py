import requests

def search_game_info(game_name):

    try:
        search_url =f"https://store.steampowered.com/api/storesearch/?term={game_name}&cc=tr&l=tr"
        response= requests.get(search_url)
        data = response.json()

        if data["total"]== 0:
            return None

        first_game = data["items"][0]
        app_id = first_game["id"]
        game_name = first_game["name"]
        
        detail_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=tr&l=tr"
        detail_response = requests.get(detail_url)
        detail_data = detail_response.json()

        game_data = detail_data.get(str(app_id),{}).get("data",{})
        price_info = game_data.get("price_overview", {})


        if not price_info:
            return{"name": game_name, "price_usd": 0.0 }
        
        final_price_usd = price_info.get("final", 0) / 100


        return {
            "name": game_name,
            "price_usd": final_price_usd
        }
    except Exception as e:
        print(f"Steam API hatası: {e}")
        return None