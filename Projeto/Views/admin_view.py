import tkinter as tk
from tkinter import ttk, messagebox

class AdminView:
    def __init__(self, master, user):
        self.master = master
        self.user = user  # Admin logado
        
        self.frame = tk.Frame(master)
        self.frame.pack(fill="both", expand=True)
        
        # Header
        header = tk.Frame(self.frame)
        header.pack(fill="x", padx=10, pady=10)
        
        tk.Label(header, text=f"🔧 Painel de Administração - {user.name}", 
                font=("Arial", 14, "bold")).pack(side="left")
        tk.Button(header, text="Logout", command=self.logout).pack(side="right")
        
        # Notebook (abas)
        self.notebook = ttk.Notebook(self. frame)
        self.notebook. pack(fill="both", expand=True, padx=10, pady=10)
        
        # Criar abas
        self.create_items_tab()
        self.create_categories_tab()
        self.create_reservations_tab()
    
    # ==================== ABA ARTIGOS ====================
    def create_items_tab(self):
        frame = tk.Frame(self. notebook)
        self.notebook. add(frame, text="📦 Gerir Artigos")
        
        # Botões
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="➕ Novo Artigo", command=self. new_item).pack(side="left")
        tk.Button(btn_frame, text="✏️ Alterar Disponibilidade", command=self.toggle_availability).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ Remover", command=self.remove_item).pack(side="left")
        tk.Button(btn_frame, text="🔄 Atualizar", command=self.load_items).pack(side="right")
        
        # Treeview
        columns = ("ID", "Nome", "Marca", "Preço/Hora", "Categoria", "Estado")
        self.items_tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)
        
        self.items_tree. column("ID", width=50)
        self.items_tree.column("Nome", width=150)
        self.items_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.load_items()
    
    def load_items(self):
        from models import SportsItem
        
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        items = SportsItem.get_all()
        
        for item in items:
            cat = item.category
            cat_name = cat.name if cat else "-"
            status = "✓ Disponível" if item.available else "✗ Indisponível"
            
            self.items_tree.insert("", "end", values=(
                item.id, item.name, item.brand,
                f"€{item. price_per_hour:.2f}", cat_name, status
            ))
    
    def new_item(self):
        from models import SportsItem, Category
        
        dialog = tk.Toplevel(self.master)
        dialog.title("Novo Artigo")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="Criar Novo Artigo", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Nome
        tk.Label(frame, text="Nome:").pack(anchor="w")
        name_entry = tk.Entry(frame, width=35)
        name_entry.pack(pady=2)
        
        # Marca
        tk.Label(frame, text="Marca:").pack(anchor="w")
        brand_entry = tk.Entry(frame, width=35)
        brand_entry.pack(pady=2)
        
        # Preço
        tk.Label(frame, text="Preço por Hora (€):").pack(anchor="w")
        price_entry = tk.Entry(frame, width=35)
        price_entry.pack(pady=2)
        
        # Categoria
        tk. Label(frame, text="Categoria:").pack(anchor="w")
        categories = Category.get_all()
        cat_names = [c.name for c in categories]
        cat_var = tk.StringVar()
        cat_combo = ttk.Combobox(frame, textvariable=cat_var, values=cat_names, state="readonly", width=32)
        cat_combo.pack(pady=2)
        if cat_names:
            cat_combo.set(cat_names[0])
        
        def create():
            name = name_entry. get().strip()
            brand = brand_entry.get().strip()
            
            try:
                price = float(price_entry.get())
            except ValueError:
                messagebox. showerror("Erro", "Preço inválido!")
                return
            
            if not name or not brand:
                messagebox. showwarning("Aviso", "Preencha todos os campos!")
                return
            
            # Encontrar categoria
            category_id = None
            for cat in categories:
                if cat.name == cat_var.get():
                    category_id = cat.id
                    break
            
            SportsItem.create(name, brand, price, category_id)
            messagebox.showinfo("Sucesso", "Artigo criado!")
            dialog.destroy()
            self.load_items()
        
        tk.Button(frame, text="Criar", command=create, width=20).pack(pady=20)
    
    def toggle_availability(self):
        from models import SportsItem
        
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um artigo!")
            return
        
        item_data = self.items_tree.item(selection[0])
        item_id = item_data["values"][0]
        
        item = SportsItem.find_by_id(item_id)
        if item:
            new_state = not item.available
            item.set_available(new_state)
            item.save()
            
            state_str = "disponível" if new_state else "indisponível"
            messagebox.showinfo("Sucesso", f"Artigo marcado como {state_str}!")
            self.load_items()
    
    def remove_item(self):
        from models import SportsItem
        
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um artigo!")
            return
        
        if messagebox.askyesno("Confirmar", "Remover este artigo?"):
            item_data = self.items_tree.item(selection[0])
            item_id = item_data["values"][0]
            
            item = SportsItem.find_by_id(item_id)
            if item:
                item.delete()
                messagebox.showinfo("Sucesso", "Artigo removido!")
                self. load_items()
    
    # ==================== ABA CATEGORIAS ====================
    def create_categories_tab(self):
        frame = tk.Frame(self. notebook)
        self.notebook. add(frame, text="🏷️ Gerir Categorias")
        
        # Botões
        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Button(btn_frame, text="➕ Nova Categoria", command=self.new_category).pack(side="left")
        tk.Button(btn_frame, text="🗑️ Remover", command=self.remove_category).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🔄 Atualizar", command=self.load_categories).pack(side="right")
        
        # Treeview
        columns = ("ID", "Nome", "Descrição", "Nº Artigos")
        self.categories_tree = ttk. Treeview(frame, columns=columns, show="headings", height=18)
        
        for col in columns:
            self. categories_tree.heading(col, text=col)
        
        self.categories_tree. column("ID", width=50)
        self.categories_tree. column("Nome", width=200)
        self.categories_tree.column("Descrição", width=300)
        self.categories_tree.column("Nº Artigos", width=100)
        
        self.categories_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self. load_categories()
    
    def load_categories(self):
        from models import Category
        
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
        
        categories = Category.get_all()
        
        for cat in categories:
            items = cat.get_items()
            self.categories_tree.insert("", "end", values=(
                cat.id, cat.name, cat.description, len(items)
            ))
    
    def new_category(self):
        from models import Category
        
        dialog = tk. Toplevel(self.master)
        dialog.title("Nova Categoria")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        frame = tk.Frame(dialog, padx=20, pady=20)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="Criar Nova Categoria", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Nome
        tk. Label(frame, text="Nome: ").pack(anchor="w")
        name_entry = tk.Entry(frame, width=35)
        name_entry.pack(pady=2)
        
        # Descrição
        tk.Label(frame, text="Descrição:").pack(anchor="w")
        desc_entry = tk. Entry(frame, width=35)
        desc_entry.pack(pady=2)
        
        def create():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            
            if not name: 
                messagebox.showwarning("Aviso", "Introduza o nome!")
                return
            
            Category.create(name, desc)
            messagebox.showinfo("Sucesso", "Categoria criada!")
            dialog.destroy()
            self.load_categories()
        
        tk.Button(frame, text="Criar", command=create, width=20).pack(pady=20)
    
    def remove_category(self):
        from models import Category
        
        selection = self.categories_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma categoria!")
            return
        
        item_data = self.categories_tree.item(selection[0])
        num_items = item_data["values"][3]
        
        if num_items > 0:
            messagebox.showerror("Erro", "Não pode remover categoria com artigos associados!")
            return
        
        if messagebox.askyesno("Confirmar", "Remover esta categoria?"):
            cat_id = item_data["values"][0]
            
            cat = Category.find_by_id(cat_id)
            if cat:
                cat.delete()
                messagebox.showinfo("Sucesso", "Categoria removida!")
                self.load_categories()
    
    # ==================== ABA RESERVAS ====================
    def create_reservations_tab(self):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="📋 Gerir Reservas")
        
        # Filtros
        filter_frame = tk.Frame(frame)
        filter_frame.pack(fill="x", padx=10, pady=10)
        
        tk.Label(filter_frame, text="Filtrar por estado:").pack(side="left")
        self.state_var = tk.StringVar(value="Todos")
        state_combo = ttk.Combobox(filter_frame, textvariable=self.state_var,
                                   values=["Todos", "Pending", "Confirmed", "Cancelled", "Completed"],
                                   state="readonly", width=15)
        state_combo.pack(side="left", padx=5)
        state_combo.bind("<<ComboboxSelected>>", lambda e: self.load_reservations())
        
        tk.Button(filter_frame, text="❌ Cancelar Reserva", command=self.cancel_reservation).pack(side="left", padx=10)
        tk.Button(filter_frame, text="🔄 Atualizar", command=self.load_reservations).pack(side="right")
        
        # Treeview
        columns = ("ID", "Cliente", "Data Início", "Data Fim", "Artigos", "Total", "Estado")
        self.reservations_tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        for col in columns:
            self.reservations_tree.heading(col, text=col)
        
        self.reservations_tree.column("ID", width=50)
        self.reservations_tree.column("Cliente", width=120)
        self.reservations_tree.column("Data Início", width=130)
        self.reservations_tree.column("Data Fim", width=130)
        self.reservations_tree.column("Artigos", width=180)
        self.reservations_tree.column("Total", width=80)
        self.reservations_tree.column("Estado", width=100)
        
        self.reservations_tree.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.load_reservations()
    
    def load_reservations(self):
        from models import Reservation
        
        for item in self. reservations_tree.get_children():
            self.reservations_tree.delete(item)
        
        state_filter = self.state_var. get()
        state = None if state_filter == "Todos" else state_filter
        
        reservations = Reservation.get_all(state=state)
        
        for res in reservations:
            client = res.client
            client_name = client.name if client else "Desconhecido"
            
            items = res.items
            items_str = ", ".join([i.name for i in items if i])
            
            self.reservations_tree.insert("", "end", values=(
                res.id,
                client_name,
                res.start_date.strftime("%Y-%m-%d %H:%M"),
                res.end_date. strftime("%Y-%m-%d %H:%M"),
                items_str,
                f"€{res.total_value:.2f}",
                res.state
            ))
    
    def cancel_reservation(self):
        from models import Reservation
        
        selection = self.reservations_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma reserva!")
            return
        
        item_data = self.reservations_tree.item(selection[0])
        res_id = item_data["values"][0]
        state = item_data["values"][6]
        
        if state not in ["Pending", "Confirmed"]:
            messagebox.showerror("Erro", "Esta reserva não pode ser cancelada!")
            return
        
        if messagebox.askyesno("Confirmar", f"Cancelar reserva #{res_id}?"):
            reservation = Reservation.find_by_id(res_id)
            if reservation:
                reservation.cancel()
                messagebox.showinfo("Sucesso", "Reserva cancelada!")
                self. load_reservations()
                self.load_items()
    
    # ==================== LOGOUT ====================
    def logout(self):
        self.frame. destroy()
        from . login_view import LoginView
        LoginView(self.master)