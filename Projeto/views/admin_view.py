import tkinter as tk
from tkinter import ttk, messagebox

class AdminView(ttk.Frame):
    def __init__(self, parent, system, on_logout):
        super().__init__(parent)
        self.system = system
        self.on_logout = on_logout
        self.admin = system.current_user
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header, text=f"🔧 Painel de Administração - {self.admin.name}",
                 font=("Helvetica", 14, "bold")).pack(side="left")
        ttk.Button(header, text="Logout", command=self.on_logout).pack(side="right")
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabs
        self.create_items_tab()
        self.create_categories_tab()
        self.create_reservations_tab()
    
    def create_items_tab(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="📦 Gerir Artigos")
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(btn_frame, text="➕ Novo Artigo",
                  command=self.new_item).pack(side="left")
        ttk.Button(btn_frame, text="✏️ Editar Disponibilidade",
                  command=self.toggle_availability).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🗑️ Remover",
                  command=self.remove_item).pack(side="left")
        ttk.Button(btn_frame, text="🔄 Atualizar",
                  command=self.update_items).pack(side="right")
        
        # Treeview
        columns = ("ID", "Nome", "Marca", "Preço/Hora", "Categoria", "Estado")
        self.items_tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=120)
        
        self.items_tree.column("ID", width=50)
        self.items_tree.pack(fill="both", expand=True)
        
        self.update_items()
    
    def create_categories_tab(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="🏷️ Gerir Categorias")
        
        # Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(btn_frame, text="➕ Nova Categoria",
                  command=self.new_category).pack(side="left")
        ttk.Button(btn_frame, text="🗑️ Apagar Categoria",
                  command=self.remove_category).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="🔄 Atualizar",
                  command=self.update_categories).pack(side="right")
        
        # Treeview
        columns = ("ID", "Nome", "Descrição", "Nº Artigos")
        self.categories_tree = ttk.Treeview(frame, columns=columns, show="headings", height=18)
        
        for col in columns:
            self.categories_tree.heading(col, text=col)
        
        self.categories_tree.column("ID", width=50)
        self.categories_tree.column("Nome", width=200)
        self.categories_tree.column("Descrição", width=300)
        self.categories_tree.column("Nº Artigos", width=100)
        
        self.categories_tree.pack(fill="both", expand=True)
        
        self.update_categories()
    
    def create_reservations_tab(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="📋 Gerir Reservas")
        
        # Filters
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(filter_frame, text="Filtrar por estado:").pack(side="left")
        self.state_combo = ttk.Combobox(filter_frame, state="readonly",
            values=["Todos", "Pending", "Confirmed", "Cancelled", "Completed"], width=15)
        self.state_combo.set("Todos")
        self.state_combo.pack(side="left", padx=5)
        self.state_combo.bind("<<ComboboxSelected>>", lambda e: self.update_reservations())
        
        ttk.Button(filter_frame, text="❌ Cancelar Reserva",
                  command=self.cancel_reservation).pack(side="left", padx=10)
        ttk.Button(filter_frame, text="🔄 Atualizar",
                  command=self.update_reservations).pack(side="right")
        
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
        
        self.reservations_tree.pack(fill="both", expand=True)
        
        self.update_reservations()
    
    def update_items(self):
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        for item in self.system.list_items():
            cat_name = item.category.name if item.category else "-"
            status = "✓ Disponível" if item.available else "✗ Indisponível"
            self.items_tree.insert("", "end", values=(
                item.id, item.name, item.brand,
                f"€{item.price_per_hour:.2f}", cat_name, status
            ))
    
    def update_categories(self):
        for item in self.categories_tree.get_children():
            self.categories_tree.delete(item)
        
        for cat in self.system.list_categories():
            self.categories_tree.insert("", "end", values=(
                cat.id, cat.name, cat.description, len(cat.items)
            ))
    
    def update_reservations(self):
        for item in self.reservations_tree.get_children():
            self.reservations_tree.delete(item)
        
        state_filter = self.state_combo.get()
        state = None if state_filter == "Todos" else state_filter
        
        for reservation in self.system.list_reservations(state=state):
            items_str = ", ".join([i.name for i in reservation.items])
            self.reservations_tree.insert("", "end", values=(
                reservation.id,
                reservation.client.name,
                reservation.start_date.strftime("%Y-%m-%d %H:%M"),
                reservation.end_date.strftime("%Y-%m-%d %H:%M"),
                items_str,
                f"€{reservation.total_value:.2f}",
                reservation.state
            ))
    
    def new_item(self):
        dialog = tk.Toplevel(self)
        dialog.title("Novo Artigo")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Criar Novo Artigo",
                 font=("Helvetica", 12, "bold")).pack(pady=(0, 15))
        
        fields_frame = ttk.Frame(frame)
        fields_frame.pack()
        
        ttk.Label(fields_frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(fields_frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(fields_frame, text="Marca:").grid(row=1, column=0, sticky="w", pady=5)
        brand_entry = ttk.Entry(fields_frame, width=30)
        brand_entry.grid(row=1, column=1, pady=5)
        
        ttk.Label(fields_frame, text="Preço/Hora (€):").grid(row=2, column=0, sticky="w", pady=5)
        price_entry = ttk.Entry(fields_frame, width=30)
        price_entry.grid(row=2, column=1, pady=5)
        
        ttk.Label(fields_frame, text="Categoria:").grid(row=3, column=0, sticky="w", pady=5)
        cat_combo = ttk.Combobox(fields_frame, state="readonly", width=27,
            values=[c.name for c in self.system.list_categories()])
        cat_combo.grid(row=3, column=1, pady=5)
        
        def create():
            name = name_entry.get().strip()
            brand = brand_entry.get().strip()
            try:
                price = float(price_entry.get())
            except: 
                messagebox.showerror("Erro", "Preço inválido!")
                return
            
            if not name or not brand:
                messagebox.showwarning("Aviso", "Preencha todos os campos!")
                return
            
            category = None
            for c in self.system.list_categories():
                if c.name == cat_combo.get():
                    category = c
                    break
            
            self.system.create_item(name, brand, price, category)
            messagebox.showinfo("Sucesso", "Artigo criado!")
            dialog.destroy()
            self.update_items()
        
        ttk.Button(frame, text="Criar", command=create).pack(pady=20)
    
    def new_category(self):
        dialog = tk.Toplevel(self)
        dialog.title("Nova Categoria")
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        frame = ttk.Frame(dialog, padding=20)
        frame.pack(fill="both", expand=True)
        
        ttk.Label(frame, text="Criar Nova Categoria",
                 font=("Helvetica", 12, "bold")).pack(pady=(0, 15))
        
        fields_frame = ttk.Frame(frame)
        fields_frame.pack()
        
        ttk.Label(fields_frame, text="Nome:").grid(row=0, column=0, sticky="w", pady=5)
        name_entry = ttk.Entry(fields_frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)
        
        ttk.Label(fields_frame, text="Descrição:").grid(row=1, column=0, sticky="w", pady=5)
        desc_entry = ttk.Entry(fields_frame, width=30)
        desc_entry.grid(row=1, column=1, pady=5)
        
        def create():
            name = name_entry.get().strip()
            desc = desc_entry.get().strip()
            
            if not name: 
                messagebox.showwarning("Aviso", "Introduza o nome!")
                return
            
            self.system.create_category(name, desc)
            messagebox.showinfo("Sucesso", "Categoria criada!")
            dialog.destroy()
            self.update_categories()
        
        ttk.Button(frame, text="Criar", command=create).pack(pady=20)
    
    def toggle_availability(self):
        selection = self.items_tree.selection()
        if not selection: 
            messagebox.showwarning("Aviso", "Selecione um artigo!")
            return
        
        item_data = self.items_tree.item(selection[0])
        item_id = item_data["values"][0]
        
        for item in self.system.list_items():
            if item.id == item_id:
                new_state = not item.available
                self.admin.manage_stock(item, new_state)
                state_str = "disponível" if new_state else "indisponível"
                messagebox.showinfo("Sucesso", f"Artigo marcado como {state_str}!")
                self.update_items()
                break
    
    def remove_item(self):
        selection = self.items_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um artigo!")
            return
        
        if messagebox.askyesno("Confirmar", "Remover este artigo?"):
            item_data = self.items_tree.item(selection[0])
            item_id = item_data["values"][0]
            
            for item in self.system.list_items():
                if item.id == item_id:
                    self.system.remove_item(item)
                    messagebox.showinfo("Sucesso", "Artigo removido!")
                    self.update_items()
                    break
    
    def cancel_reservation(self):
        selection = self.reservations_tree.selection()
        if not selection: 
            messagebox.showwarning("Aviso", "Selecione uma reserva!")
            return
        
        item_data = self.reservations_tree.item(selection[0])
        reservation_id = item_data["values"][0]
        state = item_data["values"][6]
        
        if state not in ["Pending", "Confirmed"]:
            messagebox.showerror("Erro", "Esta reserva não pode ser cancelada!")
            return
        
        if messagebox.askyesno("Confirmar", f"Cancelar reserva #{reservation_id}?"):
            reservation = self.system.get_reservation_by_id(reservation_id)
            if reservation:
                self.admin.cancel_reservation(reservation)
                messagebox.showinfo("Sucesso", "Reserva cancelada!")
                self.update_reservations()
                self.update_items()
    
    def remove_category(self):
        selection = self.categories_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma categoria!")
            return
        
        item_data = self.categories_tree.item(selection[0])
        category_id = item_data["values"][0]
        num_items = item_data["values"][3]
        
        # Avisar se a categoria tem artigos
        msg = f"Remover esta categoria?"
        if num_items > 0:
            msg = f"Esta categoria tem {num_items} artigo(s) associado(s).\nOs artigos ficarão sem categoria.\n\nRemover mesmo assim?"
        
        if messagebox.askyesno("Confirmar", msg):
            for cat in self.system.list_categories():
                if cat.id == category_id:
                    self.system.remove_category(cat)
                    messagebox.showinfo("Sucesso", "Categoria removida!")
                    self.update_categories()
                    self.update_items()  # Atualizar lista de artigos
                    break