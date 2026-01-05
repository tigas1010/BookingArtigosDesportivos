import tkinter as tk
import sys
import os

# Adicionar o diretório Projeto ao path para imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Views import LoginView


def main():
    """Função principal que inicializa a aplicação"""
    # Criar janela principal
    root = tk.Tk()
    root.title("Sistema de Reservas de Artigos Desportivos")
    root.geometry("800x600")
    root.resizable(True, True)
    
    # Centralizar janela
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    # Carregar view de login
    LoginView(root)
    
    # Iniciar loop da aplicação
    root.mainloop()


if __name__ == "__main__":
    main()
