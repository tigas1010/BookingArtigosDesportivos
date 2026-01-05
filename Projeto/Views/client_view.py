"""
View do cliente do sistema de booking. 
Permite visualizar artigos, fazer reservas e consultar histórico. 

Este módulo implementa a interface gráfica para clientes,
onde podem navegar pelos artigos disponíveis, criar novas reservas
e gerir as suas reservas existentes.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class ClientView:
    """
    Interface gráfica do painel do cliente.
    
    Fornece uma interface com abas para: 
    - Visualizar artigos disponíveis (com filtro por categoria)
    - Criar novas reservas (selecionar artigos, data e horário)
    - Consultar histórico de reservas (com opção de cancelamento)
    
    Attributes:
        master:  Referência à janela principal do Tkinter
        user: Objeto Client com os dados do cliente autenticado
        selected_items: Lista de artigos selecionados para a reserva atual
        frame: Frame principal que contém toda a interface
        notebook: Widget de abas para organizar as diferentes secções
        items_tree: Treeview para listar artigos na aba de visualização
        history_tree:  Treeview para listar histórico de reservas
        available_listbox: Listbox com artigos disponíveis para reserva
        selected_listbox: Listbox com artigos selecionados para reserva
        category_var: Variável para filtro de categoria (aba artigos)
        res_category_var: Variável para filtro de categoria (aba reserva)
        day_var, month_var, year_var:  Variáveis para a data da reserva
        start_hour_var, start_min_var:  Variáveis para hora de início
        end_hour_var, end_min_var:  Variáveis para hora de fim
        duration_label: Label que mostra a duração calculada
        total_label: Label que mostra o valor total da reserva
    """
    
    def __init__(self, master, user):
        """
        Inicializa a view do cliente.
        
        Cria a estrutura base da interface com cabeçalho e notebook de abas.
        
        Args:
            master:  Janela principal do Tkinter (tk.Tk)
            user: Objeto Client autenticado
        """
        self.master = master
        self. user = user
        
        # Lista para armazenar os artigos selecionados para a reserva atual
        self.selected_items = []

        # Frame principal que contém toda a interface do cliente
        self.frame = tk.Frame(master)
        self.frame.pack(fill="both", expand=True)

        # ===== Cabeçalho =====
        header = tk.Frame(self.frame)
        header.pack(fill="x", padx=10, pady=10)

        # Mensagem de boas-vindas com nome do cliente
        tk.Label(header, text=f"Bem-vindo, {user.name}!", 
                font=("Arial", 14, "bold")).pack(side="left")
        
        # Botão de logout alinhado à direita
        tk.Button(header, text="Logout", command=self.logout).pack(side="right")

        # ===== Notebook (abas) =====
        self.notebook = ttk.Notebook(self.frame)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # Criar as três abas principais
        self.create_items_tab()
        self.create_reservation_tab()
        self.create_history_tab()

    # ==================== ABA ARTIGOS ====================
    
    def create_items_tab(self):
        """
        Cria a aba de visualização de artigos.
        
        Permite ao cliente ver todos os artigos disponíveis no sistema,
        com opção de filtrar por categoria.  Esta aba é apenas informativa,
        para fazer reservas o cliente deve usar a aba "Nova Reserva".
        """
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Artigos Disponíveis")

        # ===== Barra de filtros =====
        filter_frame = tk.Frame(frame)
        filter_frame.pack(fill="x", pady=10, padx=10)

        # Filtro por categoria
        tk.Label(filter_frame, text="Categoria:").pack(side="left")
        self.category_var = tk.StringVar(value="Todas")
        self.category_combo = ttk. Combobox(filter_frame, textvariable=self. category_var,
                                           state="readonly", width=25)
        self.category_combo.pack(side="left", padx=5)
        # Recarregar artigos quando a categoria muda
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self.load_items())

        # Botão de atualização manual
        tk.Button(filter_frame, text="Atualizar", command=self.load_items).pack(side="right")

        # ===== Tabela de artigos (Treeview) =====
        columns = ("ID", "Nome", "Marca", "Preço/Hora", "Categoria", "Estado")
        self.items_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        # Configurar cabeçalhos e larguras das colunas
        for col in columns:  
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)

        # Ajustar larguras específicas
        self.items_tree.column("ID", width=50)
        self.items_tree.column("Nome", width=150)
        self.items_tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Scrollbar vertical (configurada mas não empacotada visualmente)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self. items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)

        # Carregar dados iniciais
        self.load_categories()
        self.load_items()

    def load_categories(self):
        """
        Carrega as categorias no dropdown de filtro.
        
        Obtém todas as categorias da base de dados e popula o combobox,
        incluindo a opção "Todas" no início.
        """
        from models import Category
        categories = Category. get_all()
        # "Todas" permite ver artigos de todas as categorias
        cat_names = ["Todas"] + [c.name for c in categories]
        self.category_combo["values"] = cat_names

    def load_items(self):
        """
        Carrega os artigos na tabela de visualização.
        
        Aplica o filtro de categoria selecionado e mostra todos os artigos
        (disponíveis e indisponíveis) para informação do cliente.
        """
        from models import SportsItem, Category

        # Limpar tabela existente
        for item in self.items_tree. get_children():
            self.items_tree.delete(item)

        # Determinar filtro de categoria
        category_name = self.category_var.get()
        category_id = None

        # Encontrar ID da categoria se não for "Todas"
        if category_name != "Todas": 
            categories = Category.get_all()
            for cat in categories:  
                if cat.name == category_name:
                    category_id = cat.id
                    break

        # Obter artigos (com ou sem filtro de categoria)
        items = SportsItem.get_all(category_id=category_id)

        # Inserir cada artigo na tabela
        for item in items:
            cat = item.category
            cat_name = cat.name if cat else "-"
            # Indicador visual de disponibilidade
            status = "✓ Disponível" if item.available else "✗ Indisponível"

            self.items_tree.insert("", "end", values=(
                item.id, item.name, item.brand,
                f"€{item. price_per_hour:.2f}", cat_name, status
            ))

    # ==================== ABA RESERVA ====================
    
    def create_reservation_tab(self):
        """
        Cria a aba de nova reserva.
        
        Interface dividida em dois painéis:
        - Esquerdo: Artigos disponíveis para seleção (por categoria)
        - Direito: Configuração da reserva (data, horário, artigos selecionados, total)
        
        O cliente seleciona artigos, define a data e horário,
        e o sistema calcula automaticamente o valor total.
        """
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="➕ Nova Reserva")

        # ===== PAINEL ESQUERDO - Artigos disponíveis =====
        left_frame = tk.LabelFrame(frame, text="Artigos Disponíveis", padx=10, pady=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Filtro de categoria para artigos disponíveis
        cat_frame = tk.Frame(left_frame)
        cat_frame.pack(fill="x", pady=5)

        tk.Label(cat_frame, text="Categoria:").pack(side="left")
        self.res_category_var = tk.StringVar()
        self.res_category_combo = ttk.Combobox(cat_frame, textvariable=self.res_category_var,
                                                state="readonly", width=20)
        self.res_category_combo.pack(side="left", padx=5)
        # Recarregar artigos quando a categoria muda
        self. res_category_combo.bind("<<ComboboxSelected>>", lambda e: self.load_available_items())

        # Lista de artigos disponíveis (permite seleção múltipla)
        self.available_listbox = tk. Listbox(left_frame, height=12, selectmode="multiple")
        self.available_listbox.pack(fill="both", expand=True, pady=5)

        # Botão para adicionar artigos selecionados à reserva
        tk.Button(left_frame, text="Adicionar ➡", command=self.add_to_reservation).pack(pady=5)

        # ===== PAINEL DIREITO - Configuração da reserva =====
        right_frame = tk. LabelFrame(frame, text="Reserva Atual", padx=10, pady=10)
        right_frame. pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ========== Secção:  DATA ==========
        date_frame = tk.LabelFrame(right_frame, text="Data da Reserva", padx=10, pady=8)
        date_frame.pack(fill="x", pady=(0, 10))

        date_row = tk.Frame(date_frame)
        date_row.pack()

        # Spinbox para o dia (1-31)
        tk.Label(date_row, text="Dia:").pack(side="left")
        self.day_var = tk.StringVar(value=datetime.now().strftime("%d"))
        day_spin = ttk.Spinbox(date_row, from_=1, to=31, width=4, textvariable=self.day_var)
        day_spin.pack(side="left", padx=(2, 10))

        # Spinbox para o mês (1-12)
        tk.Label(date_row, text="Mês:").pack(side="left")
        self.month_var = tk. StringVar(value=datetime.now().strftime("%m"))
        month_spin = ttk. Spinbox(date_row, from_=1, to=12, width=4, textvariable=self.month_var)
        month_spin.pack(side="left", padx=(2, 10))

        # Spinbox para o ano (2024-2030)
        tk.Label(date_row, text="Ano:").pack(side="left")
        self.year_var = tk.StringVar(value=datetime.now().strftime("%Y"))
        year_spin = ttk.Spinbox(date_row, from_=2024, to=2030, width=6, textvariable=self. year_var)
        year_spin.pack(side="left", padx=2)

        # ========== Secção: HORÁRIO ==========
        time_frame = tk.LabelFrame(right_frame, text="Horário", padx=10, pady=8)
        time_frame.pack(fill="x", pady=(0, 10))

        # Linha da hora de início
        start_row = tk.Frame(time_frame)
        start_row.pack(fill="x", pady=3)

        tk.Label(start_row, text="Início:", width=8, anchor="w").pack(side="left")
        
        # Spinbox para hora de início (8-22)
        self.start_hour_var = tk.StringVar(value="10")
        ttk. Spinbox(start_row, from_=8, to=22, width=4, textvariable=self.start_hour_var,
                    command=self.calculate_total).pack(side="left")
        tk.Label(start_row, text=":").pack(side="left")

        # Spinbox para minutos de início (intervalos de 15 min)
        self.start_min_var = tk.StringVar(value="00")
        ttk.Spinbox(start_row, values=("00", "15", "30", "45"), width=4,
                    textvariable=self.start_min_var, command=self.calculate_total).pack(side="left")
        tk.Label(start_row, text="h").pack(side="left")

        # Linha da hora de fim
        end_row = tk. Frame(time_frame)
        end_row.pack(fill="x", pady=3)

        tk.Label(end_row, text="Fim:", width=8, anchor="w").pack(side="left")
        
        # Spinbox para hora de fim (8-22)
        self.end_hour_var = tk. StringVar(value="12")
        ttk.Spinbox(end_row, from_=8, to=22, width=4, textvariable=self.end_hour_var,
                    command=self.calculate_total).pack(side="left")
        tk.Label(end_row, text=":").pack(side="left")

        # Spinbox para minutos de fim (intervalos de 15 min)
        self.end_min_var = tk.StringVar(value="00")
        ttk.Spinbox(end_row, values=("00", "15", "30", "45"), width=4,
                    textvariable=self.end_min_var, command=self.calculate_total).pack(side="left")
        tk.Label(end_row, text="h").pack(side="left")

        # Label que mostra a duração calculada
        self.duration_label = tk.Label(time_frame, text="Duração:  2h 00min", fg="gray")
        self.duration_label.pack(pady=(5, 0))

        # ========== Secção: ARTIGOS SELECIONADOS ==========
        tk.Label(right_frame, text="Artigos selecionados:").pack(anchor="w")
        
        # Lista de artigos adicionados à reserva
        self.selected_listbox = tk.Listbox(right_frame, height=6)
        self.selected_listbox.pack(fill="both", expand=True, pady=5)

        # Botão para remover artigo selecionado
        tk.Button(right_frame, text="⬅ Remover", command=self. remove_from_reservation).pack(pady=5)

        # ========== Secção: TOTAL E CONFIRMAÇÃO ==========
        # Label que mostra o valor total calculado
        self.total_label = tk.Label(right_frame, text="Total: €0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=10)

        # Botão de confirmação da reserva
        confirm_btn = tk.Button(right_frame, text="Confirmar Reserva",
                                command=self.confirm_reservation,
                                font=("Arial", 10),
                                bg="#333333", fg="white",
                                relief="flat",
                                cursor="hand2",
                                padx=15, pady=5)
        confirm_btn.pack(pady=10)

        # Carregar categorias no dropdown
        self.load_res_categories()

    def load_res_categories(self):
        """
        Carrega as categorias no dropdown da aba de reserva.
        
        Seleciona automaticamente a primeira categoria e carrega
        os artigos disponíveis dessa categoria.
        """
        from models import Category
        categories = Category.get_all()
        cat_names = [c.name for c in categories]
        self.res_category_combo["values"] = cat_names
        
        # Selecionar primeira categoria por defeito
        if cat_names: 
            self.res_category_combo.set(cat_names[0])
            self.load_available_items()

    def load_available_items(self):
        """
        Carrega os artigos disponíveis para reserva.
        
        Mostra apenas artigos: 
        - Da categoria selecionada
        - Que estejam disponíveis (not reserved)
        - Que ainda não foram adicionados à reserva atual
        """
        from models import SportsItem, Category

        # Limpar lista
        self.available_listbox. delete(0, tk.END)

        # Encontrar ID da categoria selecionada
        category_name = self.res_category_var.get()
        category_id = None

        categories = Category.get_all()
        for cat in categories: 
            if cat.name == category_name:
                category_id = cat.id
                break

        # Obter apenas artigos disponíveis da categoria
        items = SportsItem.get_all(category_id=category_id, available_only=True)

        # Filtrar artigos já selecionados e adicionar à lista
        for item in items:
            # Não mostrar artigos já adicionados à reserva
            if item.id not in [i.id for i in self.selected_items]:
                self.available_listbox.insert(
                    tk.END, 
                    f"{item.id}:  {item.name} - €{item.price_per_hour:.2f}/h"
                )

    def add_to_reservation(self):
        """
        Adiciona os artigos selecionados à reserva atual.
        
        Move os artigos da lista de disponíveis para a lista de selecionados.
        Permite seleção múltipla para adicionar vários artigos de uma vez.
        Atualiza o cálculo do total após adicionar. 
        """
        from models import SportsItem

        # Obter índices dos itens selecionados na listbox
        selections = self.available_listbox. curselection()

        for i in selections:
            # Extrair ID do artigo do texto da listbox
            item_text = self.available_listbox. get(i)
            item_id = int(item_text. split(": ")[0])

            # Obter objeto do artigo e adicionar à lista de selecionados
            item = SportsItem.find_by_id(item_id)
            if item and item not in self.selected_items:
                self.selected_items.append(item)
                # Mostrar na lista de selecionados
                self.selected_listbox.insert(
                    tk.END, 
                    f"{item.name} - €{item.price_per_hour:.2f}/h"
                )

        # Atualizar lista de disponíveis (remover os adicionados)
        self.load_available_items()
        # Recalcular total
        self.calculate_total()

    def remove_from_reservation(self):
        """
        Remove o artigo selecionado da reserva atual.
        
        Move o artigo de volta para a lista de disponíveis. 
        Atualiza o cálculo do total após remover.
        """
        selection = self.selected_listbox. curselection()
        if selection:
            idx = selection[0]
            # Remover da lista interna
            self.selected_items.pop(idx)
            # Remover da listbox visual
            self.selected_listbox.delete(idx)
            # Atualizar lista de disponíveis
            self.load_available_items()
            # Recalcular total
            self.calculate_total()

    def get_reservation_dates(self):
        """
        Obtém as datas de início e fim a partir dos campos do formulário.
        
        Converte os valores dos spinboxes (dia, mês, ano, horas, minutos)
        em objetos datetime. 
        
        Returns:
            tuple: (start_date, end_date) como objetos datetime,
                   ou (None, None) se os valores forem inválidos
        """
        try:
            # Obter valores dos campos de data
            day = int(self.day_var.get())
            month = int(self.month_var.get())
            year = int(self.year_var.get())

            # Obter valores dos campos de hora
            start_hour = int(self.start_hour_var. get())
            start_min = int(self.start_min_var.get())

            end_hour = int(self.end_hour_var.get())
            end_min = int(self.end_min_var.get())

            # Criar objetos datetime
            start_date = datetime(year, month, day, start_hour, start_min)
            end_date = datetime(year, month, day, end_hour, end_min)

            return start_date, end_date
        except ValueError:  
            # Retornar None se houver erro na conversão (data inválida)
            return None, None

    def calculate_total(self):
        """
        Calcula e atualiza o total da reserva.
        
        O cálculo é baseado em:
        - Duração da reserva (diferença entre hora fim e início)
        - Soma dos preços por hora de todos os artigos selecionados
        
        Atualiza também o label de duração.
        Chamado automaticamente quando o horário ou artigos mudam.
        """
        start_date, end_date = self.get_reservation_dates()

        # Verificar se as datas são válidas e fim > início
        if start_date and end_date and end_date > start_date:  
            # Calcular duração em horas
            hours = (end_date - start_date).total_seconds() / 3600

            # Formatar duração para exibição (horas e minutos)
            h = int(hours)
            m = int((hours - h) * 60)
            self.duration_label.config(text=f"Duração: {h}h {m: 02d}min", fg="gray")

            # Calcular valor total (soma dos preços * horas)
            total = sum(item.price_per_hour * hours for item in self.selected_items)
            self.total_label.config(text=f"Total: €{total:.2f} ({hours:.1f}h)")
        else:
            # Indicar duração inválida
            self. duration_label.config(text="Duração: inválida", fg="red")
            self.total_label.config(text="Total: €0.00")

    def confirm_reservation(self):
        """
        Confirma e cria a reserva.
        
        Validações realizadas:
        - Pelo menos um artigo deve estar selecionado
        - Data e hora devem ser válidas
        - Hora de fim deve ser posterior à hora de início
        - Não permite reservas no passado
        
        Após criar a reserva: 
        - Cria o objeto Reservation
        - Adiciona todos os artigos
        - Confirma a reserva
        - Limpa o formulário
        - Atualiza todas as listas
        """
        from models import Reservation

        # Validar:  pelo menos um artigo selecionado
        if not self.selected_items:
            messagebox.showwarning("Aviso", "Selecione pelo menos um artigo!")
            return

        # Obter e validar datas
        start_date, end_date = self.get_reservation_dates()

        if not start_date or not end_date:
            messagebox.showerror("Erro", "Data ou hora inválida!")
            return

        # Validar:  fim depois do início
        if end_date <= start_date:  
            messagebox.showerror("Erro", "A hora de fim deve ser depois da hora de início!")
            return

        # Validar: não permitir reservas no passado
        if start_date < datetime.now():
            messagebox.showerror("Erro", "Não pode fazer reservas no passado!")
            return

        # ===== Criar a reserva =====
        reservation = Reservation. create(self.user. id, start_date, end_date)

        # Adicionar todos os artigos selecionados
        for item in self.selected_items:
            reservation.add_item(item)

        # Confirmar a reserva (muda estado para "Confirmed")
        reservation.confirm()

        # Calcular valores para mensagem de confirmação
        hours = (end_date - start_date).total_seconds() / 3600
        total = sum(item.price_per_hour * hours for item in self.selected_items)

        # Mostrar mensagem de sucesso com detalhes
        messagebox.showinfo("Sucesso",
            f"Reserva #{reservation.id} confirmada!\n\n"
            f"Data: {start_date.strftime('%d/%m/%Y')}\n"
            f"Horário: {start_date.strftime('%H:%M')} - {end_date.strftime('%H:%M')}\n"
            f"Duração: {hours:.1f}h\n"
            f"Total:  €{total:.2f}")

        # ===== Limpar formulário =====
        self.selected_items = []
        self.selected_listbox.delete(0, tk. END)
        self.calculate_total()
        
        # Atualizar todas as listas
        self.load_available_items()
        self.load_items()
        self.load_history()

    # ==================== ABA HISTÓRICO ====================
    
    def create_history_tab(self):
        """
        Cria a aba de histórico de reservas.
        
        Mostra todas as reservas do cliente com opção de: 
        - Visualizar detalhes de cada reserva
        - Cancelar reservas pendentes ou confirmadas
        """
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Histórico")

        # ===== Barra de botões =====
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(btn_frame, text="Atualizar", command=self.load_history).pack(side="left")
        tk.Button(btn_frame, text="Cancelar Reserva", command=self.cancel_reservation).pack(side="left", padx=5)

        # ===== Tabela de histórico (Treeview) =====
        columns = ("ID", "Data Início", "Data Fim", "Artigos", "Total", "Estado")
        self.history_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        # Configurar cabeçalhos
        for col in columns:  
            self.history_tree.heading(col, text=col)

        # Configurar larguras das colunas
        self.history_tree.column("ID", width=50)
        self.history_tree.column("Data Início", width=130)
        self.history_tree.column("Data Fim", width=130)
        self.history_tree.column("Artigos", width=200)
        self.history_tree.column("Total", width=80)
        self.history_tree.column("Estado", width=100)

        self.history_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Carregar dados iniciais
        self.load_history()

    def load_history(self):
        """
        Carrega o histórico de reservas do cliente.
        
        Obtém todas as reservas associadas ao cliente autenticado
        e popula a tabela de histórico. 
        """
        from models import Reservation

        # Limpar tabela
        for item in self.history_tree. get_children():
            self.history_tree.delete(item)

        # Obter reservas do cliente atual
        reservations = Reservation.find_by_client(self.user.id)

        # Inserir cada reserva na tabela
        for res in reservations:
            # Formatar lista de artigos como string
            items = res.items
            items_str = ", ".join([i.name for i in items if i])

            self.history_tree.insert("", "end", values=(
                res.id,
                res.start_date.strftime("%Y-%m-%d %H:%M"),
                res.end_date. strftime("%Y-%m-%d %H:%M"),
                items_str,
                f"€{res.total_value:.2f}",
                res.state
            ))

    def cancel_reservation(self):
        """
        Cancela a reserva selecionada. 
        
        Validações:
        - Requer que uma reserva esteja selecionada
        - Só permite cancelar reservas nos estados "Pending" ou "Confirmed"
        - Pede confirmação antes de cancelar
        
        Ao cancelar, os artigos são automaticamente libertados.
        """
        from models import Reservation

        # Verificar se há seleção
        selection = self.history_tree.selection()
        if not selection: 
            messagebox.showwarning("Aviso", "Selecione uma reserva!")
            return

        # Obter dados da reserva selecionada
        item = self.history_tree.item(selection[0])
        res_id = item["values"][0]
        state = item["values"][5]

        # Verificar se o estado permite cancelamento
        if state not in ["Pending", "Confirmed"]:
            messagebox.showerror("Erro", "Esta reserva não pode ser cancelada!")
            return

        # Pedir confirmação e cancelar
        if messagebox. askyesno("Confirmar", f"Cancelar reserva #{res_id}?"):
            reservation = Reservation.find_by_id(res_id)
            if reservation:
                reservation.cancel()
                messagebox.showinfo("Sucesso", "Reserva cancelada!")
                
                # Atualizar todas as listas (artigos foram libertados)
                self.load_history()
                self.load_items()
                self.load_available_items()

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