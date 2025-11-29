import customtkinter as ctk
from database.models import obtener_productos

def iniciar_ui():
    ctk.set_appearance_mode("dark")
    app = ctk.CTk()
    app.title("Tracker de Precios")

    productos = obtener_productos()

    lista = ctk.CTkComboBox(app, values=[p["nombre"] for p in productos])
    lista.pack(pady=20)

    app.mainloop()
