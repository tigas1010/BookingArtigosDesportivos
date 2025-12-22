import tkinter as tk
from tkinter import ttk, messagebox

class LoginView(ttk.Frame):
    def __init__(self, parent, system, on_login_success):
        super().__init__(parent)
        self.system = system
        self.on_login_success = on_login_success
        self.create_widgets()
    
    def create_widgets(self):
        # Main centered frame
        main_frame = ttk.Frame(self)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title
        title = ttk.Label(main_frame, text="🏀 Reservas de Artigos Desportivos",
                         font=("Helvetica", 18, "bold"))
        title.pack(pady=(0, 30))
        
        # Form frame
        form_frame = ttk.LabelFrame(main_frame, text="Login", padding=20)
        form_frame.pack(padx=20, pady=10)
        
        # Email
        ttk.Label(form_frame, text="Email:").grid(row=0, column=0, sticky="w", pady=5)
        self.email_entry = ttk.Entry(form_frame, width=30)
        self.email_entry.grid(row=0, column=1, pady=5, padx=(10, 0))
        
        # Password
        ttk.Label(form_frame, text="Password:").grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = ttk.Entry(form_frame, width=30, show="*")
        self.password_entry.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        # Buttons
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(btn_frame, text="Entrar", command=self.do_login).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Registar", command=self.open_register).pack(side="left", padx=5)
        
        # Test info
        info_frame = ttk.LabelFrame(main_frame, text="Contas de Teste", padding=10)
        info_frame.pack(pady=(20, 0))
        
        ttk.Label(info_frame, text="Admin:  admin@sistema.com / admin123",
                 font=("Helvetica", 9)).pack()
        ttk.Label(info_frame, text="Cliente: joao@email.com / 123456",
                 font=("Helvetica", 9)).pack()
    
    def do_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        user = self.system.login(email, password)
        if user:
            self.on_login_success(user)
        else:
            messagebox.showerror("Erro", "Credenciais inválidas!")
    
    def open_register(self):
        # Register window
        register_window = tk.Toplevel(self)
        register_window.title("Registar Cliente")
        register_window.geometry("400x350")
        register_window.resizable(False, False)
        register_window.grab_set()
        
        frame = ttk.Frame(register_window, padding=20)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Registo de Novo Cliente",
                 font=("Helvetica", 14, "bold")).pack(pady=(0, 20))
        
        # Fields
        fields_frame = ttk.Frame(frame)
        fields_frame.pack()
        
        labels = ["Nome:", "Email:", "Password:", "Morada:", "Telefone:"]
        self.register_entries = {}
        
        for i, label in enumerate(labels):
            ttk.Label(fields_frame, text=label).grid(row=i, column=0, sticky="w", pady=5)
            entry = ttk.Entry(fields_frame, width=30)
            if label == "Password:":
                entry.config(show="*")
            entry.grid(row=i, column=1, pady=5, padx=(10, 0))
            self.register_entries[label] = entry
        
        def confirm_register():
            name = self.register_entries["Nome:"].get().strip()
            email = self.register_entries["Email:"].get().strip()
            password = self.register_entries["Password:"].get()
            address = self.register_entries["Morada:"].get().strip()
            phone = self.register_entries["Telefone:"].get().strip()
            
            if not all([name, email, password, address, phone]):
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            client = self.system.register_client(name, email, password, address, phone)
            if client: 
                messagebox.showinfo("Sucesso", "Registo efetuado com sucesso!")
                register_window.destroy()
            else:
                messagebox.showerror("Erro", "Email já registado!")
        
        ttk.Button(frame, text="Confirmar Registo",
                  command=confirm_register).pack(pady=20)