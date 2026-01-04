import tkinter as tk

class SystemView:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack()
        tk.Label(self.frame, text="Sistema Loja Desportiva").pack()

# Adicionar estes imports no final
from .login_view import LoginView
from .client_view import ClientView
from .admin_view import AdminView