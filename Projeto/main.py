"""
Módulo principal da aplicação de Booking de Artigos Desportivos. 
Inicializa a janela principal e carrega a view de login.
"""

import tkinter as tk
from views import LoginView


class App(tk.Tk):
    """Classe principal da aplicação."""
    
    def __init__(self):
        super().__init__()
        
        # Configurações da janela
        self.title("🏀 Booking de Artigos Desportivos")
        self.geometry("1000x700")
        self.minsize(900, 600)
        
        # Centralizar janela no ecrã
        self._center_window(1000, 700)
        
        # Iniciar com a view de login
        LoginView(self)
    
    def _center_window(self, width:  int, height: int):
        """Centraliza a janela no ecrã."""
        self.update_idletasks()
        x = (self.winfo_screenwidth() - width) // 2
        y = (self.winfo_screenheight() - height) // 2
        self.geometry(f"+{x}+{y}")


if __name__ == "__main__":
    app = App()
    app.mainloop()