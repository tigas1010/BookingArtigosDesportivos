import tkinter as tk
from tkinter import messagebox

class LoginView: 
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(pady=50)
        
        tk.Label(self.frame, text="Login", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self.frame, text="Email").pack()
        self.email_entry = tk.Entry(self.frame, width=30)
        self.email_entry.pack(pady=5)
        
        tk.Label(self.frame, text="Password").pack()
        self.password_entry = tk.Entry(self.frame, show="*", width=30)
        self.password_entry.pack(pady=5)
        
        tk.Button(self.frame, text="Entrar", command=self.login, width=20).pack(pady=10)
        tk.Button(self.frame, text="Registar", command=self.open_register, width=20).pack(pady=5)
        
        # Info de teste
        info_frame = tk.LabelFrame(self.frame, text="Contas de Teste", padx=10, pady=10)
        info_frame.pack(pady=20)
        tk.Label(info_frame, text="Admin:  admin@sistema.com / admin123").pack()
        tk.Label(info_frame, text="Cliente: joao@email.com / 123456").pack()
    
    def login(self):
        from models import User
        
        email = self.email_entry.get().strip()
        password = self. password_entry.get()
        
        if not email or not password:
            messagebox. showwarning("Aviso", "Preencha todos os campos!")
            return
        
        # Procurar utilizador na base de dados
        user = User.find_by_email(email)
        
        if user and user. login(email, password):
            self.frame.destroy()
            
            if user.get_type() == "admin":
                from .admin_view import AdminView
                AdminView(self.master, user)
            else:
                from .client_view import ClientView
                ClientView(self.master, user)
        else:
            messagebox.showerror("Erro", "Email ou password inválidos!")
    
    def open_register(self):
        """Abre janela de registo"""
        register_window = tk.Toplevel(self.master)
        register_window.title("Registar Cliente")
        register_window.geometry("400x350")
        register_window.resizable(False, False)
        register_window.grab_set()
        
        frame = tk.Frame(register_window, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="Registo de Novo Cliente", font=("Arial", 14)).pack(pady=10)
        
        tk.Label(frame, text="Nome: ").pack(anchor="w")
        name_entry = tk.Entry(frame, width=35)
        name_entry.pack(pady=2)
        
        tk.Label(frame, text="Email:").pack(anchor="w")
        email_entry = tk.Entry(frame, width=35)
        email_entry.pack(pady=2)
        
        tk. Label(frame, text="Password:").pack(anchor="w")
        password_entry = tk. Entry(frame, width=35, show="*")
        password_entry.pack(pady=2)
        
        tk.Label(frame, text="Morada:").pack(anchor="w")
        address_entry = tk.Entry(frame, width=35)
        address_entry.pack(pady=2)
        
        tk.Label(frame, text="Telefone:").pack(anchor="w")
        phone_entry = tk.Entry(frame, width=35)
        phone_entry.pack(pady=2)
        
        def confirm_register():
            from models import Client, User
            
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            password = password_entry.get()
            address = address_entry.get().strip()
            phone = phone_entry.get().strip()
            
            if not all([name, email, password, address, phone]):
                messagebox. showwarning("Aviso", "Preencha todos os campos!")
                return
            
            # Verificar se email já existe
            if User.find_by_email(email):
                messagebox.showerror("Erro", "Email já registado!")
                return
            
            Client.create(name, email, password, address, phone)
            messagebox.showinfo("Sucesso", "Registo efetuado com sucesso!")
            register_window.destroy()
        
        tk.Button(frame, text="Confirmar Registo", command=confirm_register, width=20).pack(pady=20)