import tkinter as tk
from tkinter import messagebox
import re


class LoginView:  
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(master)
        self.frame.pack(pady=50)
        
        tk.Label(self.frame, text="Login", font=("Arial", 16)).pack(pady=10)
        
        tk.Label(self. frame, text="Email").pack()
        self.email_entry = tk.Entry(self.frame, width=30)
        self.email_entry.pack(pady=5)
        
        tk.Label(self.frame, text="Password").pack()
        self.password_entry = tk.Entry(self.frame, show="*", width=30)
        self.password_entry.pack(pady=5)
        
        tk.Button(self.frame, text="Entrar", command=self.login, width=20).pack(pady=10)
        tk.Button(self.frame, text="Registar", command=self.open_register, width=20).pack(pady=5)
        
    def login(self):
        from models import User
        
        email = self. email_entry.get().strip()
        password = self.password_entry.get()
        
        if not email or not password: 
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        user = User. find_by_email(email)
        
        if user and user.login(email, password):
            self.frame.destroy()
            
            if user.get_type() == "admin":
                from . admin_view import AdminView
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
        register_window. geometry("450x780")
        register_window. resizable(False, False)
        register_window.grab_set()
        register_window.configure(bg="white")
        
        # Centralizar janela
        register_window.update_idletasks()
        x = (register_window.winfo_screenwidth() - 450) // 2
        y = (register_window.winfo_screenheight() - 700) // 2
        register_window.geometry(f"+{x}+{y}")
        
        # Frame principal
        main_frame = tk.Frame(register_window, bg="white", padx=35, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Título
        tk.Label(
            main_frame, 
            text="Criar Conta",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#333333"
        ).pack(pady=(0, 3))
        
        # Subtítulo
        tk.Label(
            main_frame,
            text="Preencha os dados para se registar",
            font=("Arial", 9),
            bg="white",
            fg="#888888"
        ).pack(pady=(0, 15))
        
        # Frame do formulário
        form_frame = tk.Frame(main_frame, bg="white")
        form_frame.pack(fill="x")
        
        # Função para criar campos modernos
        def create_field(label_text, show=None):
            field_frame = tk.Frame(form_frame, bg="white")
            field_frame.pack(fill="x", pady=5)
            
            label = tk.Label(
                field_frame, 
                text=label_text, 
                font=("Arial", 9),
                bg="white",
                fg="#555555",
                anchor="w"
            )
            label.pack(fill="x")
            
            entry = tk.Entry(
                field_frame, 
                font=("Arial", 10),
                relief="solid",
                bd=1,
                bg="#fafafa"
            )
            if show:
                entry.config(show=show)
            entry.pack(fill="x", ipady=6, pady=(2, 0))
            
            return entry
        
        # Criar campos
        name_entry = create_field("Nome Completo")
        email_entry = create_field("Email")
        phone_entry = create_field("Telefone")
        address_entry = create_field("Morada")
        
        password_entry = create_field("Password", show="●")
        confirm_password_entry = create_field("Confirmar Password", show="●")
        
        # Requisitos da password
        tk.Label(
            form_frame,
            text="Mínimo 8 caracteres, 1 maiúscula e 1 número",
            font=("Arial", 8),
            fg="#999999",
            bg="white"
        ).pack(anchor="w", pady=(2, 0))
        
        # ========== FUNÇÕES DE VALIDAÇÃO ==========
        
        def validate_email(email):
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None
        
        def validate_phone(phone):
            pattern = r'^[923]\d{8}$'
            return re. match(pattern, phone. replace(" ", "")) is not None
        
        def validate_password(password):
            if len(password) < 8:
                return False, "Password deve ter pelo menos 8 caracteres"
            if not any(c.isupper() for c in password):
                return False, "Password deve ter pelo menos 1 letra maiúscula"
            if not any(c.islower() for c in password):
                return False, "Password deve ter pelo menos 1 letra minúscula"
            if not any(c. isdigit() for c in password):
                return False, "Password deve ter pelo menos 1 número"
            return True, ""
        
        def validate_name(name):
            if len(name. strip()) < 3:
                return False, "Nome deve ter pelo menos 3 caracteres"
            if len(name. split()) < 2:
                return False, "Introduza o nome completo (nome e apelido)"
            return True, ""
        
        # ========== CONFIRMAR REGISTO ==========
        
        def confirm_register():
            from models import Client, User
            
            name = name_entry.get().strip()
            email = email_entry.get().strip()
            phone = phone_entry.get().strip()
            address = address_entry.get().strip()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            if not all([name, email, phone, address, password, confirm_password]):
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            valid, msg = validate_name(name)
            if not valid: 
                messagebox.showerror("Erro", msg)
                return
            
            if not validate_email(email):
                messagebox.showerror("Erro", "Email inválido!")
                return
            
            if User.find_by_email(email):
                messagebox.showerror("Erro", "Este email já está registado!")
                return
            
            if not validate_phone(phone):
                messagebox.showerror("Erro", "Telefone inválido!\nUse 9 dígitos (ex: 912345678)")
                return
            
            valid, msg = validate_password(password)
            if not valid: 
                messagebox.showerror("Erro", msg)
                return
            
            if password != confirm_password:
                messagebox.showerror("Erro", "As passwords não coincidem!")
                return
            
            Client.create(name, email, password, address, phone)
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            register_window.destroy()
        
        # ========== BOTÕES ==========
        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(fill="x", pady=(20, 10))
        
        # Botão Criar Conta
        create_btn = tk.Button(
            btn_frame,
            text="Criar Conta",
            command=confirm_register,
            font=("Arial", 11),
            bg="#333333",
            fg="white",
            activebackground="#555555",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            pady=10
        )
        create_btn.pack(fill="x")
        
        # Hover effect
        def on_enter(e):
            create_btn.config(bg="#555555")
        def on_leave(e):
            create_btn.config(bg="#333333")
        create_btn.bind("<Enter>", on_enter)
        create_btn.bind("<Leave>", on_leave)
        
        # Botão Cancelar
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancelar",
            command=register_window.destroy,
            font=("Arial", 10),
            bg="white",
            fg="#666666",
            activebackground="white",
            activeforeground="#333333",
            relief="flat",
            cursor="hand2",
            pady=5
        )
        cancel_btn.pack(fill="x", pady=(10, 0))