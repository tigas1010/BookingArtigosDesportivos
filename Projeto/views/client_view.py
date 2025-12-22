import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry

class ClientView(ttk.Frame):
    def __init__(self, parent, system, on_logout):
        super().__init__(parent)
        self.system = system
        self.on_logout = on_logout
        self.client = system.current_user
        self.selected_items = []
        self.create_widgets()
    
    def create_widgets(self):
        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header, text=f"👤 Bem-vindo, {self.client.name}! ",
                 font=("Helvetica", 14, "bold")).pack(side="left")
        ttk.Button(header, text="Logout", command=self.on_logout).pack(side="right")
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Tabs
        self.create_items_tab()
        self.create_new_reservation_tab()
        self.create_history_tab()
    
    def create_items_tab(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="📦 Artigos Disponíveis")
        
        # Category filter
        filter_frame = ttk.Frame(frame)
        filter_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(filter_frame, text="Categoria:").pack(side="left")
        self.category_combo = ttk.Combobox(filter_frame, state="readonly", width=30)
        self.category_combo.pack(side="left", padx=(5, 10))
        self.category_combo.bind("<<ComboboxSelected>>", self.filter_items)
        
        ttk.Button(filter_frame, text="Mostrar Todos",
                  command=self.show_all_items).pack(side="left")
        
        # Items treeview
        columns = ("ID", "Nome", "Marca", "Preço/Hora", "Categoria", "Estado")
        self.items_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=120)
        
        self.items_tree.column("ID", width=50)
        self.items_tree.pack(fill="both", expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar.set)
        
        self.update_categories()
        self.update_items()
    
    def create_new_reservation_tab(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="➕ Nova Reserva")
        
        # Left frame - Item selection
        left_frame = ttk.LabelFrame(frame, text="Artigos Disponíveis", padding=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Category
        cat_frame = ttk.Frame(left_frame)
        cat_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(cat_frame, text="Categoria:").pack(side="left")
        self.reservation_cat_combo = ttk.Combobox(cat_frame, state="readonly", width=25)
        self.reservation_cat_combo.pack(side="left", padx=5)
        self.reservation_cat_combo.bind("<<ComboboxSelected>>", self.filter_reservation_items)
        
        # Available items list
        self.available_items_list = tk.Listbox(left_frame, height=10, selectmode="multiple")
        self.available_items_list.pack(fill="both", expand=True)
        
        ttk.Button(left_frame, text="Adicionar à Reserva ➡",
                  command=self.add_item_to_reservation).pack(pady=10)
        
        # Right frame - Current reservation
        right_frame = ttk.LabelFrame(frame, text="Reserva Atual", padding=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Dates
        dates_frame = ttk.Frame(right_frame)
        dates_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(dates_frame, text="Data Início:").grid(row=0, column=0, sticky="w", pady=2)
        self.start_date = DateEntry(dates_frame, width=12, date_pattern="yyyy-mm-dd")
        self.start_date.grid(row=0, column=1, padx=5, pady=2)
        
        self.start_hour = ttk.Combobox(dates_frame, values=[f"{h:02d}:00" for h in range(8, 22)], width=6)
        self.start_hour.set("10:00")
        self.start_hour.grid(row=0, column=2, pady=2)
        
        ttk.Label(dates_frame, text="Data Fim:").grid(row=1, column=0, sticky="w", pady=2)
        self.end_date = DateEntry(dates_frame, width=12, date_pattern="yyyy-mm-dd")
        self.end_date.grid(row=1, column=1, padx=5, pady=2)
        
        self.end_hour = ttk.Combobox(dates_frame, values=[f"{h:02d}:00" for h in range(8, 22)], width=6)
        self.end_hour.set("12:00")
        self.end_hour.grid(row=1, column=2, pady=2)
        
        # Selected items list
        ttk.Label(right_frame, text="Artigos selecionados:").pack(anchor="w")
        self.reservation_items_list = tk.Listbox(right_frame, height=8)
        self.reservation_items_list.pack(fill="both", expand=True)
        
        ttk.Button(right_frame, text="⬅ Remover",
                  command=self.remove_item_from_reservation).pack(pady=5)
        
        # Total and confirm
        self.total_label = ttk.Label(right_frame, text="Total:  €0.00",
                                    font=("Helvetica", 12, "bold"))
        self.total_label.pack(pady=10)
        
        ttk.Button(right_frame, text="✓ Confirmar Reserva",
                  command=self.confirm_reservation).pack()
        
        self.update_reservation_combo()
    
    def create_history_tab(self):
        frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(frame, text="📋 Histórico de Reservas")
        
        # Action buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(btn_frame, text="🔄 Atualizar",
                  command=self.update_history).pack(side="left")
        ttk.Button(btn_frame, text="❌ Cancelar Reserva",
                  command=self.cancel_client_reservation).pack(side="left", padx=5)
        
        # History treeview
        columns = ("ID", "Data Início", "Data Fim", "Artigos", "Total", "Estado")
        self.history_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.history_tree.heading(col, text=col)
        
        self.history_tree.column("ID", width=50)
        self.history_tree.column("Data Início", width=130)
        self.history_tree.column("Data Fim", width=130)
        self.history_tree.column("Artigos", width=200)
        self.history_tree.column("Total", width=80)
        self.history_tree.column("Estado", width=100)
        
        self.history_tree.pack(fill="both", expand=True)
        
        self.update_history()
    
    def update_categories(self):
        categories = ["Todas"] + [c.name for c in self.system.list_categories()]
        self.category_combo["values"] = categories
        self.category_combo.set("Todas")
    
    def update_reservation_combo(self):
        categories = [c.name for c in self.system.list_categories()]
        self.reservation_cat_combo["values"] = categories
        if categories:
            self.reservation_cat_combo.set(categories[0])
            self.filter_reservation_items(None)
    
    def update_items(self, category=None):
        for item in self.items_tree.get_children():
            self.items_tree.delete(item)
        
        items = self.system.list_items(category=category)
        for item in items:
            cat_name = item.category.name if item.category else "-"
            status = "✓ Disponível" if item.available else "✗ Indisponível"
            self.items_tree.insert("", "end", values=(
                item.id, item.name, item.brand,
                f"€{item.price_per_hour:.2f}", cat_name, status
            ))
    
    def filter_items(self, event):
        selection = self.category_combo.get()
        if selection == "Todas":
            self.update_items()
        else:
            for cat in self.system.list_categories():
                if cat.name == selection:
                    self.update_items(category=cat)
                    break
    
    def filter_reservation_items(self, event):
        self.available_items_list.delete(0, tk.END)
        selection = self.reservation_cat_combo.get()
        
        for cat in self.system.list_categories():
            if cat.name == selection:
                items = self.system.list_items(category=cat, available_only=True)
                for item in items:
                    if item not in self.selected_items:
                        self.available_items_list.insert(tk.END,
                            f"{item.id}: {item.name} - €{item.price_per_hour:.2f}/h")
                break
    
    def show_all_items(self):
        self.category_combo.set("Todas")
        self.update_items()
    
    def add_item_to_reservation(self):
        selections = self.available_items_list.curselection()
        for i in selections:
            item_text = self.available_items_list.get(i)
            item_id = int(item_text.split(": ")[0])
            
            for item in self.system.list_items():
                if item.id == item_id and item not in self.selected_items:
                    self.selected_items.append(item)
                    self.reservation_items_list.insert(tk.END,
                        f"{item.name} - €{item.price_per_hour:.2f}/h")
        
        self.filter_reservation_items(None)
        self.calculate_reservation_total()
    
    def remove_item_from_reservation(self):
        selection = self.reservation_items_list.curselection()
        if selection:
            idx = selection[0]
            self.selected_items.pop(idx)
            self.reservation_items_list.delete(idx)
            self.filter_reservation_items(None)
            self.calculate_reservation_total()
    
    def calculate_reservation_total(self):
        try:
            start_datetime = datetime.strptime(
                f"{self.start_date.get()} {self.start_hour.get()}",
                "%Y-%m-%d %H:%M"
            )
            end_datetime = datetime.strptime(
                f"{self.end_date.get()} {self.end_hour.get()}",
                "%Y-%m-%d %H:%M"
            )
            
            hours = (end_datetime - start_datetime).total_seconds() / 3600
            if hours > 0:
                total = sum(i.price_per_hour * hours for i in self.selected_items)
                self.total_label.config(text=f"Total: €{total:.2f} ({hours:.1f}h)")
            else:
                self.total_label.config(text="Total: €0.00")
        except:
            self.total_label.config(text="Total: €0.00")
    
    def confirm_reservation(self):
        if not self.selected_items:
            messagebox.showwarning("Aviso", "Selecione pelo menos um artigo!")
            return
        
        try:
            start_datetime = datetime.strptime(
                f"{self.start_date.get()} {self.start_hour.get()}",
                "%Y-%m-%d %H:%M"
            )
            end_datetime = datetime.strptime(
                f"{self.end_date.get()} {self.end_hour.get()}",
                "%Y-%m-%d %H:%M"
            )
            
            if end_datetime <= start_datetime:
                messagebox.showerror("Erro", "Data de fim deve ser posterior à data de início!")
                return
            
            if start_datetime < datetime.now():
                messagebox.showerror("Erro", "Data de início não pode ser no passado!")
                return
            
        except ValueError:
            messagebox.showerror("Erro", "Datas inválidas!")
            return
        
        # Create reservation
        reservation = self.system.create_reservation(self.client, start_datetime, end_datetime)
        for item in self.selected_items:
            reservation.add_item(item)
        reservation.confirm()
        
        messagebox.showinfo("Sucesso",
            f"Reserva #{reservation.id} confirmada!\nTotal: €{reservation.total_value:.2f}")
        
        # Clear
        self.selected_items = []
        self.reservation_items_list.delete(0, tk.END)
        self.calculate_reservation_total()
        self.filter_reservation_items(None)
        self.update_items()
        self.update_history()
    
    def update_history(self):
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        reservations = self.client.get_history()
        for reservation in reservations:
            items_str = ", ".join([i.name for i in reservation.items])
            self.history_tree.insert("", "end", values=(
                reservation.id,
                reservation.start_date.strftime("%Y-%m-%d %H:%M"),
                reservation.end_date.strftime("%Y-%m-%d %H:%M"),
                items_str,
                f"€{reservation.total_value:.2f}",
                reservation.state
            ))
    
    def cancel_client_reservation(self):
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione uma reserva!")
            return
        
        item = self.history_tree.item(selection[0])
        reservation_id = item["values"][0]
        state = item["values"][5]
        
        if state not in ["Pending", "Confirmed"]:
            messagebox.showerror("Erro", "Esta reserva não pode ser cancelada!")
            return
        
        if messagebox.askyesno("Confirmar", f"Cancelar reserva #{reservation_id}?"):
            reservation = self.system.get_reservation_by_id(reservation_id)
            if reservation:
                reservation.cancel()
                messagebox.showinfo("Sucesso", "Reserva cancelada!")
                self.update_history()
                self.update_items()
                self.filter_reservation_items(None)