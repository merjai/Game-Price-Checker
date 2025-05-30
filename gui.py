import tkinter as tk
from tkinter import ttk
from steam_api import search_game_info
from exchange_api import get_exchange_rate


def create_main_window():
    root = tk.Tk()
    root.title("Fiyat Sorgulayıcı")
    root.geometry("500x400")

    entry = ttk.Entry(root, width=40)
    entry.pack(pady=10)

    result_label = ttk.Label(root, text="", font=("Helvetica", 12))
    result_label.pack(pady=10)
    
    def on_search():
        game_name= entry.get().strip()
        if game_name:
            game_info = search_game_info(game_name)
            rate = get_exchange_rate()
            if game_info and rate:
                usd = game_info["price_usd"]
                result_label.config(text=f"{game_info['name']}\nUSD: ${usd:.2f}\nTRY: {usd * rate:.2f} TL")
            else:
                result_label.config(text="Bilgi alınamadı")


    search_button = ttk.Button(root, text="ARA", command=on_search)
    search_button.pack(pady=10)

    root.mainloop()   