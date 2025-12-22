import tkinter as tk
from tkinter import ttk
from system import System
from views import LoginView, ClientView, AdminView

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("🏀 Sistema de Reservas de Artigos Desportivos")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1000) // 2
        y = (self.winfo_screenheight() - 700) // 2
        self.geometry(f"+{x}+{y}")
        
        # System
        self.system = System()
        
        # Main container
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        
        # Show login
        self.show_login()
    
    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()
    
    def show_login(self):
        self.clear_container()
        login_view = LoginView(self.container, self.system, self.on_login_success)
        login_view.pack(fill="both", expand=True)
    
    def on_login_success(self, user):
        self.clear_container()
        
        if user.get_type() == "client":
            view = ClientView(self.container, self.system, self.logout)
        else:
            view = AdminView(self.container, self.system, self.logout)
        
        view.pack(fill="both", expand=True)
    
    def logout(self):
        self.system.logout()
        self.show_login()


if __name__ == "__main__":
    app = App()
    app.mainloop()