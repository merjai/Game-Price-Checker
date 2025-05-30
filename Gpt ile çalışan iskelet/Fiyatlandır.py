import requests
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import io
import time

# API anahtarı (Döviz kuru için)
EXCHANGE_API_KEY = "0fbdd32afc8718e9f95ae900"

# Oyun bulunamadı durumu
not_found_displayed = False

# Döviz kuru bilgisi
def get_exchange_rate():
    try:
        url = f"https://v6.exchangerate-api.com/v6/{EXCHANGE_API_KEY}/latest/USD"
        response = requests.get(url)
        data = response.json()
        rate = data['conversion_rates']['TRY']  # USD -> TRY kuru
        return rate
    except Exception as e:
        print(f"API Hatası: {e}")
        return None

def fetch_steam_price():
    global not_found_displayed
    game_name = entry.get().strip()
    if not game_name:
        return

    entry.delete(0, tk.END)

    # Arama isteği
    search_url = f"https://store.steampowered.com/api/storesearch/?term={game_name}&cc=tr&l=tr"
    response = requests.get(search_url)
    data = response.json()

    # Oyun bulunamadı
    if data.get("total") == 0:
        if not not_found_displayed:
            add_game_result_frame(f"{game_name}: Oyun bulunamadı.", None)
            not_found_displayed = True
            root.after(3000, remove_not_found_message)
        return

    not_found_displayed = False

    item = data["items"][0]
    app_id = item["id"]
    game_title = item["name"]

    # Detay isteği
    details_url = f"https://store.steampowered.com/api/appdetails?appids={app_id}&cc=tr&l=tr"
    detail_response = requests.get(details_url)
    detail_data = detail_response.json()
    game_data = detail_data.get(str(app_id), {}).get("data", {})

    if not game_data:
        add_game_result_frame(f"{game_name}: Bilgi alınamadı.", None)
        return

    price_info = game_data.get("price_overview", {})
    if price_info:
        price_usd = price_info["final"] / 100
        price_usd_formatted = price_info["final_formatted"]
    else:
        price_usd = 0
        price_usd_formatted = "Ücretsiz veya fiyat bilgisi yok"

    # Görsel alma
    try:
        image_url = f"https://cdn.akamai.steamstatic.com/steam/apps/{app_id}/header.jpg"
        image_response = requests.get(image_url)
        image_data = image_response.content
        image = Image.open(io.BytesIO(image_data))
        image = image.resize((300, 140))
        image_tk = ImageTk.PhotoImage(image)
    except Exception as e:
        print(f"Resim alınamadı: {e}")
        image_tk = None

    # Döviz kuru hesapla
    exchange_rate = get_exchange_rate()
    if exchange_rate and price_usd > 0:
        price_try = price_usd * exchange_rate
        price_try_formatted = f"₺{price_try:,.2f}"
    else:
        price_try_formatted = "Bilinmiyor"

    add_game_result_frame(f"{game_title} — {price_usd_formatted} / {price_try_formatted}", image_tk)

def add_game_result_frame(text, image_tk):
    result_frame = ttk.Frame(results_container, style="ResultFrame.TFrame")
    result_frame.pack(pady=10, anchor="w", fill="x")

    if image_tk:
        image_label = ttk.Label(result_frame, image=image_tk)
        image_label.image = image_tk
        image_label.pack(side="left", padx=10, pady=5)

    text_label = ttk.Label(result_frame, text=text, font=("Helvetica Neue", 12), justify="left", style="ResultText.TLabel")
    text_label.pack(side="left", padx=10, pady=5)

    canvas.update_idletasks()
    canvas.yview_moveto(1.0)

def remove_not_found_message():
    for widget in results_container.winfo_children():
        if widget.winfo_children():
            text_label = widget.winfo_children()[0]
            if text_label and "Oyun bulunamadı" in text_label.cget("text"):
                widget.destroy()

def close_app():
    root.destroy()

def update_time():
    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    time_label.config(text=current_time)
    root.after(1000, update_time)

def update_exchange_rate():
    rate = get_exchange_rate()
    if rate:
        exchange_rate_label.config(text=f"1 USD = {rate:.2f} TL")
    else:
        exchange_rate_label.config(text="Kur alınamadı")
    root.after(60000, update_exchange_rate)

# === GUI Kurulumu ===
root = tk.Tk()
root.title("Steam Oyun Fiyatı + Görsel")
root.geometry("700x800")
root.resizable(True, True)

# Stil ayarları
style = ttk.Style()
style.configure("TButton", font=("Helvetica Neue", 11), padding=6)
style.configure("TLabel", font=("Helvetica Neue", 12))
style.configure("TFrame", background="#f5f5f5")
style.configure("ResultFrame.TFrame", background="#e0e0e0", relief="flat", padding=5)
style.configure("ResultText.TLabel", font=("Helvetica Neue", 12), background="#e0e0e0", anchor="w", wraplength=600)

# Saat ve döviz kuru göstergesi
time_label = ttk.Label(root, text="", style="TLabel")
time_label.place(x=10, y=10)

exchange_rate_label = ttk.Label(root, text="", style="TLabel")
exchange_rate_label.place(x=500, y=10)

label = ttk.Label(root, text="Oyun Adı:", style="TLabel")
label.pack(pady=15)

entry = ttk.Entry(root, width=60, font=("Helvetica Neue", 12))
entry.pack(pady=10)
entry.bind("<Return>", lambda event: fetch_steam_price())

button_frame = ttk.Frame(root, style="TFrame")
button_frame.pack(pady=15)

search_button = ttk.Button(button_frame, text="Fiyatı Getir", command=fetch_steam_price)
search_button.pack(side="left", padx=10)

exit_button = ttk.Button(button_frame, text="Çıkış", command=close_app)
exit_button.pack(side="left", padx=10)

canvas = tk.Canvas(root, height=600)
scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
results_container = ttk.Frame(canvas)

results_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=results_container, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Başlangıçta saat ve kuru göster
update_time()
update_exchange_rate()

root.mainloop()
