import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ClientView: 
    def __init__(self, master, user):
        self.master = master
        self.user = user  # Cliente logado
        self.selected_items = []  # Artigos selecionados para reserva
        
        self.frame = tk.Frame(master)
        self.frame.pack(fill="both", expand=True)
        
        # Header
        header = tk.Frame(self.frame)
        header.pack(fill="x", padx=10, pady=10)
        
        tk.Label(header, text=f"Bem-vindo, {user.name}!", 
                font=("Arial", 14, "bold")).pack(side="left")
        tk.Button(header, text="Logout", command=self.logout).pack(side="right")
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self. frame)
        self.notebook. pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar abas
        self.create_items_tab()
        self.create_reservation_tab()
        self.create_history_tab()
    
    # ==================== ABA ARTIGOS ====================
    def create_items_tab(self):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="Artigos Disponíveis")
        
        # Filtro por categoria
        filter_frame = tk.Frame(frame)
        filter_frame.pack(fill="x", pady=10, padx=10)
        
        tk.Label(filter_frame, text="Categoria:").pack(side="left")
        self.category_var = tk.StringVar(value="Todas")
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var, 
                                           state="readonly", width=25)
        self.category_combo.pack(side="left", padx=5)
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self.load_items())
        
        tk.Button(filter_frame, text="Atualizar", command=self.load_items).pack(side="right")
        
        # Treeview de artigos
        columns = ("ID", "Nome", "Marca", "Preço/Hora", "Categoria", "Estado")
        self.items_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self. items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)
        
        self.items_tree.column("ID", width=50)
        self.items_tree.column("Nome", width=150)
        self.items_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar. set)
        
        # Carregar dados
        self.load_categories()
        self.load_items()
    
    def load_categories(self):
        from models import Category
        categories = Category.get_all()
        cat_names = ["Todas"] + [c.name for c in categories]
        self.category_combo["values"] = cat_names
    
    def load_items(self):
        from models import SportsItem, Category
        
        # Limpar treeview
        for item in self.items_tree. get_children():
            self.items_tree.delete(item)
        
        # Filtrar por categoria
        category_name = self.category_var.get()
        category_id = None
        
        if category_name != "Todas":
            categories = Category.get_all()
            for cat in categories: 
                if cat.name == category_name:
                    category_id = cat.id
                    break
        
        # Carregar artigos
        items = SportsItem.get_all(category_id=category_id)
        
        for item in items:
            cat = item.category
            cat_name = cat.name if cat else "-"
            status = "✓ Disponível" if item.available else "✗ Indisponível"
            
            self.items_tree.insert("", "end", values=(
                item.id, item.name, item.brand,
                f"€{item.price_per_hour:.2f}", cat_name, status
            ))
    
    # ==================== ABA RESERVA ====================
    def create_reservation_tab(self):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="➕ Nova Reserva")
        
        # Frame esquerdo - Artigos disponíveis
        left_frame = tk.LabelFrame(frame, text="Artigos Disponíveis", padx=10, pady=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Categoria
        cat_frame = tk.Frame(left_frame)
        cat_frame.pack(fill="x", pady=5)
        
        tk.Label(cat_frame, text="Categoria:").pack(side="left")
        self.res_category_var = tk.StringVar()
        self.res_category_combo = ttk.Combobox(cat_frame, textvariable=self.res_category_var,
                                                state="readonly", width=20)
        self.res_category_combo.pack(side="left", padx=5)
        self.res_category_combo.bind("<<ComboboxSelected>>", lambda e: self.load_available_items())
        
        # Lista de artigos disponíveis
        self.available_listbox = tk.Listbox(left_frame, height=12, selectmode="multiple")
        self.available_listbox.pack(fill="both", expand=True, pady=5)
        
        tk.Button(left_frame, text="Adicionar ➡", command=self.add_to_reservation).pack(pady=5)
        
        # Frame direito - Reserva atual
        right_frame = tk. LabelFrame(frame, text="Reserva Atual", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        # Datas
        dates_frame = tk.Frame(right_frame)
        dates_frame.pack(fill="x", pady=5)
        
        tk.Label(dates_frame, text="Data Início (YYYY-MM-DD HH:MM):").pack(anchor="w")
        self.start_date_entry = tk.Entry(dates_frame, width=20)
        self.start_date_entry.pack(anchor="w", pady=2)
        self.start_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d 10:00"))
        
        tk.Label(dates_frame, text="Data Fim (YYYY-MM-DD HH:MM):").pack(anchor="w")
        self.end_date_entry = tk.Entry(dates_frame, width=20)
        self.end_date_entry.pack(anchor="w", pady=2)
        self.end_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d 12:00"))
        
        # Lista de artigos selecionados
        tk.Label(right_frame, text="Artigos selecionados:").pack(anchor="w", pady=(10, 0))
        self.selected_listbox = tk.Listbox(right_frame, height=8)
        self.selected_listbox.pack(fill="both", expand=True, pady=5)
        
        tk.Button(right_frame, text="⬅ Remover", command=self.remove_from_reservation).pack(pady=5)
        
        # Total
        self.total_label = tk.Label(right_frame, text="Total: €0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=10)
        
        # Botão confirmar
        tk.Button(right_frame, text="✓ Confirmar Reserva", command=self.confirm_reservation,
                 bg="green", fg="white", font=("Arial", 10, "bold")).pack(pady=5)
        
        # Carregar categorias
        self.load_res_categories()
    
    def load_res_categories(self):
        from models import Category
        categories = Category.get_all()
        cat_names = [c.name for c in categories]
        self.res_category_combo["values"] = cat_names
        if cat_names:
            self. res_category_combo.set(cat_names[0])
            self.load_available_items()
    
    def load_available_items(self):
        from models import SportsItem, Category
        
        self.available_listbox.delete(0, tk.END)
        
        # Encontrar categoria selecionada
        category_name = self.res_category_var.get()
        category_id = None
        
        categories = Category.get_all()
        for cat in categories:
            if cat.name == category_name:
                category_id = cat.id
                break
        
        # Carregar artigos disponíveis
        items = SportsItem.get_all(category_id=category_id, available_only=True)
        
        for item in items:
            if item.id not in [i.id for i in self.selected_items]:
                self.available_listbox.insert(tk.END, f"{item.id}:  {item.name} - €{item.price_per_hour:.2f}/h")
    
    def add_to_reservation(self):
        from models import SportsItem
        
        selections = self.available_listbox.curselection()
        
        for i in selections:
            item_text = self.available_listbox. get(i)
            item_id = int(item_text. split(": ")[0])
            
            item = SportsItem.find_by_id(item_id)
            if item and item not in self.selected_items:
                self.selected_items.append(item)
                self.selected_listbox.insert(tk. END, f"{item.name} - €{item.price_per_hour:.2f}/h")
        
        self.load_available_items()
        self.calculate_total()
    
    def remove_from_reservation(self):
        selection = self.selected_listbox. curselection()
        if selection:
            idx = selection[0]
            self.selected_items.pop(idx)
            self.selected_listbox.delete(idx)
            self.load_available_items()
            self.calculate_total()
    
    def calculate_total(self):
        try:
            start = datetime.strptime(self. start_date_entry.get(), "%Y-%m-%d %H:%M")
            end = datetime.strptime(self.end_date_entry.get(), "%Y-%m-%d %H:%M")
            
            hours = (end - start).total_seconds() / 3600
            if hours > 0:
                total = sum(item.price_per_hour * hours for item in self.selected_items)
                self.total_label.config(text=f"Total: €{total:.2f} ({hours:.1f}h)")
            else:
                self.total_label.config(text="Total: €0.00")
        except ValueError:
            self.total_label.config(text="Total: €0.00")
    
    def confirm_reservation(self):
        from models import Reservation
        
        if not self.selected_items:
            messagebox.showwarning("Aviso", "Selecione pelo menos um artigo!")
            return
        
        try:
            start = datetime.strptime(self.start_date_entry.get(), "%Y-%m-%d %H:%M")
            end = datetime.strptime(self.end_date_entry.get(), "%Y-%m-%d %H:%M")
            
            if end <= start:
                messagebox.showerror("Erro", "Data fim deve ser posterior à data início!")
                return
        except ValueError:
            messagebox. showerror("Erro", "Formato de data inválido!  Use YYYY-MM-DD HH:MM")
            return
        
        # Criar reserva
        reservation = Reservation.create(self.user.id, start, end)
        
        for item in self.selected_items:
            reservation.add_item(item)
        
        reservation.confirm()
        
        messagebox.showinfo("Sucesso", f"Reserva #{reservation.id} confirmada!\nTotal: €{reservation.total_value:.2f}")
        
        # Limpar
        self.selected_items = []
        self.selected_listbox.delete(0, tk.END)
        self.calculate_total()
        self.load_available_items()
        self.load_items()
        self.load_history()
    
    # ==================== ABA HISTÓRICO ====================
    def create_history_tab(self):
        frame = tk.Frame(self. notebook)
        self.notebook. add(frame, text="Histórico")
        
        # Botões
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="Atualizar", command=self.load_history).pack(side="left")
        tk.Button(btn_frame, text="Cancelar Reserva", command=self.cancel_reservation).pack(side="left", padx=5)
        
        # Treeview
        columns = ("ID", "Data Início", "Data Fim", "Artigos", "Total", "Estado")
        self.history_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
        
        self.history_tree. column("ID", width=50)
        self.history_tree. column("Data Início", width=130)
        self.history_tree.column("Data Fim", width=130)
        self.history_tree.column("Artigos", width=200)
        self.history_tree.column("Total", width=80)
        self.history_tree.column("Estado", width=100)
        
        self.history_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.load_history()
    
    def load_history(self):
        from models import Reservation
        
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        reservations = Reservation.find_by_client(self.user.id)
        
        for res in reservations:
            items = res.items
            items_str = ", ".join([i.name for i in items if i])
            
            self.history_tree.insert("", "end", values=(
                res.id,
                res.start_date. strftime("%Y-%m-%d %H:%M"),
                res.end_date.strftime("%Y-%m-%d %H:%M"),
                items_str,
                f"€{res.total_value:.2f}",
                res.state
            ))
    
    def cancel_reservation(self):
        from models import Reservation
        
        selection = self.history_tree. selection()
        if not selection: 
            messagebox.showwarning("Aviso", "Selecione uma reserva!")
            return
        
        item = self.history_tree.item(selection[0])
        res_id = item["values"][0]
        state = item["values"][5]
        
        if state not in ["Pending", "Confirmed"]:
            messagebox.showerror("Erro", "Esta reserva não pode ser cancelada!")
            return
        
        if messagebox.askyesno("Confirmar", f"Cancelar reserva #{res_id}?"):
            reservation = Reservation.find_by_id(res_id)
            if reservation:
                reservation.cancel()
                messagebox.showinfo("Sucesso", "Reserva cancelada!")
                self.load_history()
                self.load_items()
                self.load_available_items()
    
    # ==================== LOGOUT ====================
    def logout(self):
        self.frame.destroy()
        from . login_view import LoginView
        LoginView(self.master)