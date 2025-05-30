import tkinter as tk
from tkinter import ttk
import requests

root = tk.Tk()
root.title("Oyun Fiyat Derleyici")
root.geometry("600x400")


etiket = ttk.Label(root, text="Oyun Adı:")
etiket.pack(pady=10)

giris_kutusu = ttk.Entry(root, width=40)
giris_kutusu.pack(pady=10)

sonuc_etiketi = ttk.Label(root, text="", font=("Halvetica", 12))
sonuc_etiketi.pack(pady=10)


arama_butonu = ttk.Button(root, text="ARA")
arama_butonu.pack(pady=10)

root.mainloop()