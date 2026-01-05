"""
View de administração do sistema. 
Permite gerir artigos, categorias e reservas. 

Este módulo implementa a interface gráfica do painel de administração,
onde o administrador pode realizar operações CRUD sobre os recursos do sistema.
"""

import tkinter as tk
from tkinter import ttk, messagebox


class AdminView:
    """
    Interface gráfica do painel de administração.
    
    Fornece uma interface com abas para gerir: 
    - Artigos desportivos (criar, alterar disponibilidade, remover)
    - Categorias (criar, remover)
    - Reservas (visualizar, filtrar, cancelar)
    
    Attributes:
        master:  Referência à janela principal do Tkinter
        user:  Objeto Administrator com os dados do admin autenticado
        frame: Frame principal que contém toda a interface
        notebook: Widget de abas para organizar as diferentes secções
        items_tree: Treeview para listar artigos
        categories_tree:  Treeview para listar categorias
        reservations_tree:  Treeview para listar reservas
        state_var:  Variável para o filtro de estado das reservas
    """
    
    def __init__(self, master, user):
        """
        Inicializa a view de administração.
        
        Cria a estrutura base da interface com cabeçalho e notebook de abas.
        
        Args:
            master:  Janela principal do Tkinter (tk.Tk)
            user: Objeto Administrator autenticado com permissões de admin
        """
        self.master = master
        self.user = user
        
        # Frame principal que contém toda a interface do admin
        self.frame = tk. Frame(master)
        self.frame.pack(fill="both", expand=True)
        
        # Construir os componentes da interface
        self._create_header()
        self._create_notebook()
    
    # ==================== CONSTRUÇÃO DA INTERFACE ====================
    
    def _create_header(self):
        """
        Cria o cabeçalho com título e botão de logout.
        
        O cabeçalho mostra o nome do administrador autenticado
        e fornece acesso rápido ao logout.
        """
        header = tk.Frame(self.frame)
        header.pack(fill="x", padx=10, pady=10)
        
        # Título com nome do administrador
        tk.Label(
            header,
            text=f"🔧 Painel de Administração - {self.user.name}",
            font=("Arial", 14, "bold")
        ).pack(side="left")
        
        # Botão de logout alinhado à direita
        tk.Button(header, text="Logout", command=self.logout).pack(side="right")
    
    def _create_notebook(self):
        """
        Cria o notebook com as abas de gestão.
        
        Organiza a interface em três abas principais:
        1. Gerir Artigos - CRUD de artigos desportivos
        2. Gerir Categorias - CRUD de categorias
        3. Gerir Reservas - Visualização e gestão de reservas
        """
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar cada aba do painel
        self.create_items_tab()
        self.create_categories_tab()
        self.create_reservations_tab()
    
    # ==================== ABA ARTIGOS ====================
    
    def create_items_tab(self):
        """
        Cria a aba de gestão de artigos.
        
        Inclui: 
        - Botões de ação (novo, alterar disponibilidade, remover, atualizar)
        - Tabela com listagem de todos os artigos
        """
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="📦 Gerir Artigos")
        
        # ===== Barra de botões de ação =====
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        # Botões alinhados à esquerda
        tk.Button(btn_frame, text="➕ Novo Artigo", command=self.new_item).pack(side="left")
        tk.Button(btn_frame, text="✏️ Alterar Disponibilidade", 
                  command=self.toggle_availability).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ Remover", command=self.remove_item).pack(side="left")
        
        # Botão de atualizar alinhado à direita
        tk.Button(btn_frame, text="🔄 Atualizar", command=self.load_items).pack(side="right")
        
        # ===== Tabela de artigos (Treeview) =====
        columns = ("ID", "Nome", "Marca", "Preço/Hora", "Categoria", "Estado")
        self.items_tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        # Configurar cabeçalhos e larguras das colunas
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)
        
        # Ajustar larguras específicas
        self.items_tree.column("ID", width=50)
        self.items_tree.column("Nome", width=150)
        self.items_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Carregar dados iniciais
        self.load_items()
    
    def load_items(self):
        """
        Carrega os artigos na tabela. 
        
        Obtém todos os artigos da base de dados e popula a Treeview.
        Para cada artigo, mostra:  ID, nome, marca, preço, categoria e estado.
        """
        from models import SportsItem
        
        # Limpar todos os itens existentes na tabela
        for item in self. items_tree.get_children():
            self.items_tree. delete(item)
        
        # Carregar e inserir cada artigo
        for item in SportsItem.get_all():
            # Obter nome da categoria (ou "-" se não tiver)
            cat_name = item.category. name if item.category else "-"
            
            # Formatar estado de disponibilidade
            status = "✓ Disponível" if item. available else "✗ Indisponível"
            
            # Inserir linha na tabela
            self.items_tree. insert("", "end", values=(
                item.id, item. name, item.brand,
                f"€{item.price_per_hour:.2f}", cat_name, status
            ))
    
    def new_item(self):
        """
        Abre diálogo para criar novo artigo. 
        
        Apresenta um formulário modal com campos para:
        - Nome do artigo
        - Marca
        - Preço por hora
        - Categoria (seleção de categorias existentes)
        
        Valida se existem categorias antes de permitir criar artigos.
        """
        from models import SportsItem, Category
        
        # Verificar se existem categorias (obrigatório ter pelo menos uma)
        categories = Category.get_all()
        if not categories:
            messagebox.showwarning("Aviso", "Crie primeiro uma categoria!")
            return
        
        # ===== Criar janela de diálogo modal =====
        dialog = tk. Toplevel(self.master)
        dialog.title("Novo Artigo")
        dialog.geometry("400x400")
        dialog.resizable(False, False)
        dialog.grab_set()  # Torna o diálogo modal
        dialog.configure(bg="white")
        
        # Centralizar diálogo no ecrã
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 400) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # ===== Conteúdo do formulário =====
        frame = tk.Frame(dialog, bg="white", padx=30, pady=20)
        frame.pack(fill="both", expand=True)
        
        # Título do formulário
        tk.Label(frame, text="Criar Novo Artigo", font=("Arial", 14, "bold"), 
                 bg="white").pack(pady=(0, 20))
        
        # Campo:  Nome
        tk.Label(frame, text="Nome", font=("Arial", 9), bg="white", anchor="w").pack(fill="x")
        name_entry = tk.Entry(frame, font=("Arial", 10), relief="solid", bd=1)
        name_entry.pack(fill="x", ipady=6, pady=(2, 10))
        
        # Campo:  Marca
        tk.Label(frame, text="Marca", font=("Arial", 9), bg="white", anchor="w").pack(fill="x")
        brand_entry = tk.Entry(frame, font=("Arial", 10), relief="solid", bd=1)
        brand_entry.pack(fill="x", ipady=6, pady=(2, 10))
        
        # Campo:  Preço por Hora
        tk.Label(frame, text="Preço por Hora (€)", font=("Arial", 9), 
                 bg="white", anchor="w").pack(fill="x")
        price_entry = tk.Entry(frame, font=("Arial", 10), relief="solid", bd=1)
        price_entry.pack(fill="x", ipady=6, pady=(2, 10))
        
        # Campo:  Categoria (dropdown)
        tk.Label(frame, text="Categoria", font=("Arial", 9), bg="white", anchor="w").pack(fill="x")
        cat_var = tk.StringVar(value=categories[0].name)  # Primeira categoria como default
        cat_combo = ttk.Combobox(frame, textvariable=cat_var,
                                  values=[c.name for c in categories],
                                  state="readonly", font=("Arial", 10))
        cat_combo.pack(fill="x", pady=(2, 10))
        
        def create():
            """
            Função interna que processa a criação do artigo.
            Valida os campos e cria o artigo se tudo estiver correto.
            """
            name = name_entry.get().strip()
            brand = brand_entry.get().strip()
            
            # Validar campos obrigatórios
            if not name or not brand:  
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            # Validar e converter preço
            try:  
                price = float(price_entry.get().replace(",", "."))
            except ValueError:
                messagebox.showerror("Erro", "Preço inválido!")
                return
            
            # Encontrar ID da categoria selecionada
            category_id = next((c.id for c in categories if c.name == cat_var.get()), None)
            
            # Criar artigo e atualizar interface
            SportsItem.create(name, brand, price, category_id)
            messagebox.showinfo("Sucesso", "Artigo criado!")
            dialog.destroy()
            self.load_items()
        
        # Botão de submissão
        tk.Button(frame, text="Criar", command=create, font=("Arial", 10),
                  bg="#333", fg="white", relief="flat", pady=8, 
                  cursor="hand2").pack(fill="x", pady=(15, 0))
    
    def toggle_availability(self):
        """
        Altera a disponibilidade do artigo selecionado.
        
        Inverte o estado de disponibilidade: 
        - Se disponível -> indisponível
        - Se indisponível -> disponível
        
        Requer que um artigo esteja selecionado na tabela.
        """
        from models import SportsItem
        
        # Verificar se há seleção
        selection = self.items_tree.selection()
        if not selection:  
            messagebox.showwarning("Aviso", "Selecione um artigo!")
            return
        
        # Obter ID do artigo selecionado
        item_id = self.items_tree.item(selection[0])["values"][0]
        item = SportsItem.find_by_id(item_id)
        
        if item:  
            # Inverter disponibilidade
            item.set_available(not item.available)
            item.save()
            
            # Feedback ao utilizador
            state_str = "disponível" if item.available else "indisponível"
            messagebox.showinfo("Sucesso", f"Artigo marcado como {state_str}!")
            self.load_items()
    
    def remove_item(self):
        """
        Remove o artigo selecionado. 
        
        Pede confirmação antes de eliminar permanentemente o artigo.
        Requer que um artigo esteja selecionado na tabela. 
        """
        from models import SportsItem
        
        # Verificar se há seleção
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um artigo!")
            return
        
        # Pedir confirmação antes de eliminar
        if messagebox.askyesno("Confirmar", "Remover este artigo?"):
            item_id = self.items_tree. item(selection[0])["values"][0]
            item = SportsItem.find_by_id(item_id)
            if item:
                item.delete()
                messagebox.showinfo("Sucesso", "Artigo removido!")
                self. load_items()
    
    # ==================== ABA CATEGORIAS ====================
    
    def create_categories_tab(self):
        """
        Cria a aba de gestão de categorias.
        
        Inclui:
        - Botões de ação (nova, remover, atualizar)
        - Tabela com listagem de todas as categorias e número de artigos
        """
        frame = tk.Frame(self. notebook)
        self.notebook. add(frame, text="🏷️ Gerir Categorias")
        
        # ===== Barra de botões de ação =====
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="➕ Nova Categoria", command=self.new_category).pack(side="left")
        tk.Button(btn_frame, text="🗑️ Remover", command=self.remove_category).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🔄 Atualizar", command=self.load_categories).pack(side="right")
        
        # ===== Tabela de categorias (Treeview) =====
        columns = ("ID", "Nome", "Descrição", "Nº Artigos")
        self.categories_tree = ttk. Treeview(frame, columns=columns, show="headings", height=18)
        
        # Configurar cabeçalhos
        for col in columns:  
            self.categories_tree.heading(col, text=col)
        
        # Configurar larguras das colunas
        self.categories_tree.column("ID", width=50)
        self.categories_tree.column("Nome", width=200)
        self.categories_tree.column("Descrição", width=300)
        self.categories_tree.column("Nº Artigos", width=100)
        
        self.categories_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Carregar dados iniciais
        self.load_categories()
    
    def load_categories(self):
        """
        Carrega as categorias na tabela.
        
        Obtém todas as categorias e mostra também o número de artigos
        associados a cada uma.
        """
        from models import Category
        
        # Limpar tabela
        for item in self. categories_tree.get_children():
            self.categories_tree. delete(item)
        
        # Carregar e inserir cada categoria
        for cat in Category.get_all():
            self.categories_tree.insert("", "end", values=(
                cat.id, cat.name, cat.description, len(cat.get_items())
            ))
    
    def new_category(self):
        """
        Abre diálogo para criar nova categoria. 
        
        Apresenta um formulário modal com campos para:
        - Nome da categoria (obrigatório)
        - Descrição (opcional)
        """
        from models import Category
        
        # ===== Criar janela de diálogo modal =====
        dialog = tk.Toplevel(self.master)
        dialog.title("Nova Categoria")
        dialog.geometry("400x280")
        dialog.resizable(False, False)
        dialog.grab_set()
        dialog.configure(bg="white")
        
        # Centralizar diálogo
        dialog.update_idletasks()
        x = (dialog. winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 280) // 2
        dialog.geometry(f"+{x}+{y}")
        
        # ===== Conteúdo do formulário =====
        frame = tk.Frame(dialog, bg="white", padx=30, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="Criar Nova Categoria", font=("Arial", 14, "bold"),
                 bg="white").pack(pady=(0, 20))
        
        # Campo: Nome
        tk.Label(frame, text="Nome", font=("Arial", 9), bg="white", anchor="w").pack(fill="x")
        name_entry = tk.Entry(frame, font=("Arial", 10), relief="solid", bd=1)
        name_entry.pack(fill="x", ipady=6, pady=(2, 10))
        
        # Campo: Descrição
        tk.Label(frame, text="Descrição", font=("Arial", 9), bg="white", anchor="w").pack(fill="x")
        desc_entry = tk.Entry(frame, font=("Arial", 10), relief="solid", bd=1)
        desc_entry. pack(fill="x", ipady=6, pady=(2, 10))
        
        def create():
            """Função interna que processa a criação da categoria."""
            name = name_entry.get().strip()
            if not name:
                messagebox. showwarning("Aviso", "Introduza o nome!")
                return
            
            Category.create(name, desc_entry.get().strip())
            messagebox.showinfo("Sucesso", "Categoria criada!")
            dialog.destroy()
            self.load_categories()
        
        # Botão de submissão
        tk.Button(frame, text="Criar", command=create, font=("Arial", 10),
                  bg="#333", fg="white", relief="flat", pady=8,
                  cursor="hand2").pack(fill="x", pady=(15, 0))
    
    def remove_category(self):
        """
        Remove a categoria selecionada.
        
        Validações:
        - Requer que uma categoria esteja selecionada
        - Não permite remover categorias que tenham artigos associados
        - Pede confirmação antes de eliminar
        """
        from models import Category
        
        # Verificar se há seleção
        selection = self.categories_tree.selection()
        if not selection: 
            messagebox.showwarning("Aviso", "Selecione uma categoria!")
            return
        
        item_data = self.categories_tree.item(selection[0])
        
        # Verificar se a categoria tem artigos associados
        if item_data["values"][3] > 0:
            messagebox.showerror("Erro", "Não pode remover categoria com artigos!")
            return
        
        # Pedir confirmação e eliminar
        if messagebox.askyesno("Confirmar", "Remover esta categoria?"):
            cat = Category.find_by_id(item_data["values"][0])
            if cat:
                cat.delete()
                messagebox.showinfo("Sucesso", "Categoria removida!")
                self.load_categories()
    
    # ==================== ABA RESERVAS ====================
    
    def create_reservations_tab(self):
        """
        Cria a aba de gestão de reservas.
        
        Inclui:
        - Filtro por estado da reserva
        - Botões de ação (cancelar, atualizar)
        - Tabela com listagem de reservas
        """
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Gerir Reservas")
        
        # ===== Barra de filtros e botões =====
        filter_frame = tk.Frame(frame)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        # Filtro por estado
        tk.Label(filter_frame, text="Filtrar por estado:").pack(side="left")
        self.state_var = tk.StringVar(value="Todos")
        state_combo = ttk.Combobox(
            filter_frame, textvariable=self.state_var,
            values=["Todos", "Confirmed", "Cancelled", "Completed"],
            state="readonly", width=15
        )
        state_combo.pack(side="left", padx=5)
        # Recarregar quando o filtro muda
        state_combo.bind("<<ComboboxSelected>>", lambda e: self.load_reservations())
        
        # Botões de ação
        tk.Button(filter_frame, text="❌ Cancelar Reserva", 
                  command=self.cancel_reservation).pack(side="left", padx=10)
        tk.Button(filter_frame, text="🔄 Atualizar", 
                  command=self.load_reservations).pack(side="right")
        
        # ===== Tabela de reservas (Treeview) =====
        columns = ("ID", "Cliente", "Data Início", "Data Fim", "Artigos", "Total", "Estado")
        self.reservations_tree = ttk. Treeview(frame, columns=columns, show="headings", height=18)
        
        # Configurar cabeçalhos
        for col in columns: 
            self.reservations_tree. heading(col, text=col)
        
        # Configurar larguras das colunas
        self.reservations_tree.column("ID", width=50)
        self.reservations_tree. column("Cliente", width=120)
        self.reservations_tree.column("Data Início", width=130)
        self.reservations_tree.column("Data Fim", width=130)
        self.reservations_tree.column("Artigos", width=180)
        self.reservations_tree.column("Total", width=80)
        self.reservations_tree.column("Estado", width=100)
        
        self.reservations_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Carregar dados iniciais
        self.load_reservations()
    
    def load_reservations(self):
        """
        Carrega as reservas na tabela.
        
        Aplica o filtro de estado selecionado e mostra: 
        - ID da reserva
        - Nome do cliente
        - Datas de início e fim
        - Artigos reservados
        - Valor total
        - Estado atual
        """
        from models import Reservation
        
        # Limpar tabela
        for item in self. reservations_tree.get_children():
            self.reservations_tree.delete(item)
        
        # Aplicar filtro de estado (None = todos)
        state_filter = self.state_var. get()
        state = None if state_filter == "Todos" else state_filter
        
        # Carregar e inserir cada reserva
        for res in Reservation.get_all(state=state):
            # Obter nome do cliente (ou "Desconhecido" se não encontrado)
            client_name = res.client.name if res.client else "Desconhecido"
            
            # Formatar lista de artigos como string
            items_str = ", ".join([i.name for i in res.items if i])
            
            # Inserir linha na tabela
            self.reservations_tree.insert("", "end", values=(
                res. id, client_name,
                res.start_date. strftime("%Y-%m-%d %H:%M"),
                res.end_date. strftime("%Y-%m-%d %H:%M"),
                items_str, f"€{res.total_value:.2f}", res.state
            ))
    
    def cancel_reservation(self):
        """
        Cancela a reserva selecionada.
        
        Validações:
        - Requer que uma reserva esteja selecionada
        - Só permite cancelar reservas no estado "Confirmed"
        - Pede confirmação antes de cancelar
        
        Ao cancelar, os artigos são libertados automaticamente.
        """
        from models import Reservation
        
        # Verificar se há seleção
        selection = self.reservations_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma reserva!")
            return
        
        item_data = self.reservations_tree.item(selection[0])
        res_id = item_data["values"][0]
        state = item_data["values"][6]
        
        # Verificar se o estado permite cancelamento
        if state != "Confirmed":
            messagebox.showerror("Erro", "Só pode cancelar reservas confirmadas!")
            return
        
        # Pedir confirmação e cancelar
        if messagebox. askyesno("Confirmar", f"Cancelar reserva #{res_id}?"):
            reservation = Reservation.find_by_id(res_id)
            if reservation:
                reservation.cancel()
                messagebox.showinfo("Sucesso", "Reserva cancelada!")
                
                # Atualizar ambas as tabelas (reservas e artigos)
                self. load_reservations()
                self.load_items()  # Artigos foram libertados
    
    # ==================== LOGOUT ====================
    
    def logout(self):
        """
        Termina sessão e volta ao login.
        
        Destrói o frame atual e instancia uma nova LoginView,
        permitindo que outro utilizador faça login.
        """
        self.frame.destroy()
        from . login_view import LoginView
        LoginView(self.master)