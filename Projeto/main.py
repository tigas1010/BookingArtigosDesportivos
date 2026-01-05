import tkinter as tk
from tkinter import ttk
from views import LoginView
from models import User, Client, Administrator, Category, SportsItem

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self. title("🏀 Booking de Artigos Desportivos")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # Centralizar janela
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1000) // 2
        y = (self.winfo_screenheight() - 700) // 2
        self.geometry(f"+{x}+{y}")
        
        # Mostrar login (passa self como master)
        LoginView(self)

if __name__ == "__main__":
    app = App()
    app.mainloop()