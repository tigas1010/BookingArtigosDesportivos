"""
View de autenticação do sistema de booking.  
Implementa o ecrã de login e o formulário de registo de novos clientes.  

Este módulo é o ponto de entrada da aplicação após a inicialização,
apresentando ao utilizador as opções de login ou registo.
"""

import tkinter as tk
from tkinter import messagebox
import re  # Módulo para expressões regulares (validações)


class LoginView:
    """
    Interface gráfica de autenticação. 
    
    Responsável por: 
    - Apresentar formulário de login
    - Autenticar utilizadores (clientes e administradores)
    - Redirecionar para a view apropriada após login
    - Permitir registo de novos clientes
    
    Attributes:
        master:  Referência à janela principal do Tkinter
        frame: Frame que contém o formulário de login
        email_entry: Campo de entrada para o email
        password_entry: Campo de entrada para a password
    """
    
    def __init__(self, master):
        """
        Inicializa a view de login.
        
        Cria o formulário de login com campos de email e password,
        e botões para entrar ou registar novo utilizador.
        
        Args:
            master: Janela principal do Tkinter (tk.Tk)
        """
        self.master = master
        
        # Frame principal do login (centrado com padding)
        self.frame = tk.Frame(master)
        self.frame.pack(pady=50)
        
        # ===== Título =====
        tk.Label(self.frame, text="Login", font=("Arial", 16)).pack(pady=10)
        
        # ===== Campo Email =====
        tk.Label(self.frame, text="Email").pack()
        self.email_entry = tk.Entry(self. frame, width=30)
        self.email_entry.pack(pady=5)
        
        # ===== Campo Password =====
        tk.Label(self. frame, text="Password").pack()
        # show="*" oculta os caracteres digitados
        self.password_entry = tk.Entry(self.frame, show="*", width=30)
        self.password_entry.pack(pady=5)
        
        # ===== Botões =====
        tk. Button(self.frame, text="Entrar", command=self. login, width=20).pack(pady=10)
        tk.Button(self.frame, text="Registar", command=self. open_register, width=20).pack(pady=5)
    
    # ==================== AUTENTICAÇÃO ====================
        
    def login(self):
        """
        Processa a tentativa de login.
        
        Fluxo:
        1. Obtém email e password dos campos
        2. Valida se os campos estão preenchidos
        3. Procura utilizador pelo email
        4. Verifica credenciais
        5. Redireciona para AdminView ou ClientView conforme o tipo de utilizador
        
        Em caso de erro, mostra mensagem apropriada.
        """
        from models import User
        
        # Obter valores dos campos (strip remove espaços)
        email = self.email_entry.get().strip()
        password = self. password_entry.get()
        
        # Validar campos obrigatórios
        if not email or not password:
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        # Procurar utilizador pelo email
        user = User.find_by_email(email)
        
        # Verificar se existe e se a password está correta
        if user and user.login(email, password):
            # Destruir o frame de login
            self.frame.destroy()
            
            # Redirecionar baseado no tipo de utilizador
            if user.get_type() == "admin":
                # Utilizador é administrador -> AdminView
                from . admin_view import AdminView
                AdminView(self.master, user)
            else:
                # Utilizador é cliente -> ClientView
                from .client_view import ClientView
                ClientView(self.master, user)
        else:
            # Credenciais inválidas
            messagebox. showerror("Erro", "Email ou password inválidos!")
    
    # ==================== REGISTO ====================
    
    def open_register(self):
        """
        Abre a janela de registo de novo cliente.
        
        Cria uma janela modal (Toplevel) com formulário completo para registo,
        incluindo validações para todos os campos: 
        - Nome completo (mínimo 2 palavras)
        - Email (formato válido e único)
        - Telefone (formato português)
        - Morada
        - Password (requisitos de segurança)
        - Confirmação de password
        """
        
        # ===== Criar janela modal =====
        register_window = tk.Toplevel(self. master)
        register_window. title("Registar Cliente")
        register_window.geometry("450x780")
        register_window.resizable(False, False)
        register_window.grab_set()  # Torna a janela modal (bloqueia interação com janela pai)
        register_window.configure(bg="white")
        
        # Centralizar janela no ecrã
        register_window. update_idletasks()
        x = (register_window.winfo_screenwidth() - 450) // 2
        y = (register_window.winfo_screenheight() - 700) // 2
        register_window.geometry(f"+{x}+{y}")
        
        # ===== Frame principal com padding =====
        main_frame = tk.Frame(register_window, bg="white", padx=35, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # ===== Título =====
        tk.Label(
            main_frame, 
            text="Criar Conta",
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#333333"
        ).pack(pady=(0, 3))
        
        # ===== Subtítulo =====
        tk.Label(
            main_frame,
            text="Preencha os dados para se registar",
            font=("Arial", 9),
            bg="white",
            fg="#888888"
        ).pack(pady=(0, 15))
        
        # ===== Container do formulário =====
        form_frame = tk.Frame(main_frame, bg="white")
        form_frame.pack(fill="x")
        
        # ========== FUNÇÃO AUXILIAR PARA CRIAR CAMPOS ==========
        
        def create_field(label_text, show=None):
            """
            Cria um campo de formulário com estilo moderno.
            
            Cada campo consiste em:
            - Label com o nome do campo
            - Entry para input do utilizador
            
            Args:
                label_text: Texto da label do campo
                show: Caracter para ocultar input (ex: "●" para passwords)
                
            Returns:
                tk.Entry: O widget de entrada criado
            """
            # Frame container do campo
            field_frame = tk.Frame(form_frame, bg="white")
            field_frame.pack(fill="x", pady=5)
            
            # Label do campo
            label = tk.Label(
                field_frame, 
                text=label_text, 
                font=("Arial", 9),
                bg="white",
                fg="#555555",
                anchor="w"  # Alinhar à esquerda
            )
            label.pack(fill="x")
            
            # Campo de entrada
            entry = tk. Entry(
                field_frame, 
                font=("Arial", 10),
                relief="solid",
                bd=1,
                bg="#fafafa"  # Fundo ligeiramente cinza
            )
            # Ocultar caracteres se especificado (para passwords)
            if show: 
                entry.config(show=show)
            entry.pack(fill="x", ipady=6, pady=(2, 0))  # ipady adiciona padding interno vertical
            
            return entry
        
        # ===== Criar campos do formulário =====
        name_entry = create_field("Nome Completo")
        email_entry = create_field("Email")
        phone_entry = create_field("Telefone")
        address_entry = create_field("Morada")
        
        # Campos de password (caracteres ocultos com ●)
        password_entry = create_field("Password", show="●")
        confirm_password_entry = create_field("Confirmar Password", show="●")
        
        # ===== Dica sobre requisitos da password =====
        tk.Label(
            form_frame,
            text="Mínimo 8 caracteres, 1 maiúscula e 1 número",
            font=("Arial", 8),
            fg="#999999",
            bg="white"
        ).pack(anchor="w", pady=(2, 0))
        
        # ========== FUNÇÕES DE VALIDAÇÃO ==========
        
        def validate_email(email):
            """
            Valida formato do email usando expressão regular.
            
            Padrão aceite:  usuario@dominio.extensao
            Exemplos válidos:  joao@email.com, maria. silva@empresa.pt
            
            Args:
                email: String com o email a validar
                
            Returns:
                bool: True se o formato é válido, False caso contrário
            """
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None
        
        def validate_phone(phone):
            """
            Valida formato do telefone português.
            
            Aceita números que começam com 9, 2 ou 3, seguidos de 8 dígitos.
            - 9XXXXXXXX:  Telemóveis
            - 2XXXXXXXX: Fixos zona sul/ilhas
            - 3XXXXXXXX: Fixos zona norte
            
            Args:
                phone: String com o telefone a validar
                
            Returns:
                bool: True se o formato é válido, False caso contrário
            """
            pattern = r'^[923]\d{8}$'
            # Remove espaços antes de validar
            return re.match(pattern, phone. replace(" ", "")) is not None
        
        def validate_password(password):
            """
            Valida os requisitos de segurança da password.
            
            Requisitos:
            - Mínimo 8 caracteres
            - Pelo menos 1 letra maiúscula
            - Pelo menos 1 letra minúscula
            - Pelo menos 1 número
            
            Args:
                password:  String com a password a validar
                
            Returns:
                tuple: (bool, str) - (válido, mensagem de erro se inválido)
            """
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
            """
            Valida o nome completo. 
            
            Requisitos: 
            - Mínimo 3 caracteres
            - Pelo menos 2 palavras (nome e apelido)
            
            Args:
                name: String com o nome a validar
                
            Returns:
                tuple: (bool, str) - (válido, mensagem de erro se inválido)
            """
            if len(name. strip()) < 3:
                return False, "Nome deve ter pelo menos 3 caracteres"
            if len(name. split()) < 2:
                return False, "Introduza o nome completo (nome e apelido)"
            return True, ""
        
        # ========== FUNÇÃO DE SUBMISSÃO DO REGISTO ==========
        
        def confirm_register():
            """
            Processa o registo de novo cliente. 
            
            Fluxo:
            1. Obtém valores de todos os campos
            2. Valida se todos os campos estão preenchidos
            3. Valida formato do nome
            4. Valida formato do email
            5. Verifica se o email já está registado
            6. Valida formato do telefone
            7. Valida requisitos da password
            8. Verifica se as passwords coincidem
            9. Cria o cliente no sistema
            10. Fecha a janela de registo
            
            Em caso de erro em qualquer validação, mostra mensagem e interrompe. 
            """
            from models import Client, User
            
            # Obter valores dos campos
            name = name_entry.get().strip()
            email = email_entry. get().strip()
            phone = phone_entry.get().strip()
            address = address_entry. get().strip()
            password = password_entry.get()
            confirm_password = confirm_password_entry.get()
            
            # Validar:  todos os campos preenchidos
            if not all([name, email, phone, address, password, confirm_password]):
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            # Validar:  formato do nome
            valid, msg = validate_name(name)
            if not valid:
                messagebox.showerror("Erro", msg)
                return
            
            # Validar: formato do email
            if not validate_email(email):
                messagebox.showerror("Erro", "Email inválido!")
                return
            
            # Validar: email não duplicado
            if User.find_by_email(email):
                messagebox.showerror("Erro", "Este email já está registado!")
                return
            
            # Validar: formato do telefone
            if not validate_phone(phone):
                messagebox.showerror("Erro", "Telefone inválido!\nUse 9 dígitos (ex: 912345678)")
                return
            
            # Validar: requisitos da password
            valid, msg = validate_password(password)
            if not valid: 
                messagebox.showerror("Erro", msg)
                return
            
            # Validar: passwords coincidem
            if password != confirm_password:
                messagebox.showerror("Erro", "As passwords não coincidem!")
                return
            
            # ===== Criar cliente =====
            Client.create(name, email, password, address, phone)
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            
            # Fechar janela de registo (volta ao login)
            register_window.destroy()
        
        # ========== BOTÕES DO FORMULÁRIO ==========
        
        btn_frame = tk.Frame(main_frame, bg="white")
        btn_frame.pack(fill="x", pady=(20, 10))
        
        # ===== Botão Criar Conta (principal) =====
        create_btn = tk.Button(
            btn_frame,
            text="Criar Conta",
            command=confirm_register,
            font=("Arial", 11),
            bg="#333333",           # Fundo escuro
            fg="white",             # Texto branco
            activebackground="#555555",  # Fundo ao clicar
            activeforeground="white",
            relief="flat",          # Sem bordas 3D
            cursor="hand2",         # Cursor de mão ao passar
            pady=10
        )
        create_btn.pack(fill="x")
        
        # ===== Efeito hover no botão =====
        def on_enter(e):
            """Escurece o botão quando o rato entra."""
            create_btn.config(bg="#555555")
            
        def on_leave(e):
            """Restaura cor original quando o rato sai."""
            create_btn.config(bg="#333333")
            
        # Associar eventos de hover
        create_btn.bind("<Enter>", on_enter)
        create_btn.bind("<Leave>", on_leave)
        
        # ===== Botão Cancelar (secundário) =====
        cancel_btn = tk.Button(
            btn_frame,
            text="Cancelar",
            command=register_window.destroy,  # Fecha a janela
            font=("Arial", 10),
            bg="white",             # Fundo branco (discreto)
            fg="#666666",           # Texto cinza
            activebackground="white",
            activeforeground="#333333",
            relief="flat",
            cursor="hand2",
            pady=5
        )
        cancel_btn.pack(fill="x", pady=(10, 0))