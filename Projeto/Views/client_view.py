import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime


class ClientView:
    def __init__(self, master, user):
        self.master = master
        self.user = user
        self.selected_items = []

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
        frame = tk.Frame(self. notebook)
        self.notebook. add(frame, text="Artigos Disponíveis")

        filter_frame = tk.Frame(frame)
        filter_frame.pack(fill="x", pady=10, padx=10)

        tk.Label(filter_frame, text="Categoria:").pack(side="left")
        self.category_var = tk.StringVar(value="Todas")
        self.category_combo = ttk.Combobox(filter_frame, textvariable=self.category_var,
                                           state="readonly", width=25)
        self.category_combo.pack(side="left", padx=5)
        self.category_combo.bind("<<ComboboxSelected>>", lambda e: self.load_items())

        tk.Button(filter_frame, text="Atualizar", command=self.load_items).pack(side="right")

        columns = ("ID", "Nome", "Marca", "Preço/Hora", "Categoria", "Estado")
        self.items_tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        for col in columns: 
            self.items_tree.heading(col, text=col)
            self.items_tree.column(col, width=100)

        self.items_tree.column("ID", width=50)
        self.items_tree.column("Nome", width=150)
        self.items_tree.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.items_tree.yview)
        self.items_tree.configure(yscrollcommand=scrollbar. set)

        self.load_categories()
        self.load_items()

    def load_categories(self):
        from models import Category
        categories = Category.get_all()
        cat_names = ["Todas"] + [c.name for c in categories]
        self.category_combo["values"] = cat_names

    def load_items(self):
        from models import SportsItem, Category

        for item in self.items_tree.get_children():
            self.items_tree.delete(item)

        category_name = self.category_var.get()
        category_id = None

        if category_name != "Todas":
            categories = Category.get_all()
            for cat in categories: 
                if cat.name == category_name:
                    category_id = cat.id
                    break

        items = SportsItem.get_all(category_id=category_id)

        for item in items:
            cat = item.category
            cat_name = cat.name if cat else "-"
            status = "✓ Disponível" if item.available else "✗ Indisponível"

            self.items_tree.insert("", "end", values=(
                item.id, item.name, item.brand,
                f"€{item. price_per_hour:.2f}", cat_name, status
            ))

    # ==================== ABA RESERVA ====================
    def create_reservation_tab(self):
        frame = tk.Frame(self.notebook)
        self.notebook.add(frame, text="➕ Nova Reserva")

        # Frame esquerdo - Artigos disponíveis
        left_frame = tk.LabelFrame(frame, text="Artigos Disponíveis", padx=10, pady=10)
        left_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        cat_frame = tk.Frame(left_frame)
        cat_frame.pack(fill="x", pady=5)

        tk.Label(cat_frame, text="Categoria:").pack(side="left")
        self.res_category_var = tk.StringVar()
        self.res_category_combo = ttk.Combobox(cat_frame, textvariable=self.res_category_var,
                                                state="readonly", width=20)
        self.res_category_combo.pack(side="left", padx=5)
        self.res_category_combo.bind("<<ComboboxSelected>>", lambda e: self.load_available_items())

        self.available_listbox = tk.Listbox(left_frame, height=12, selectmode="multiple")
        self.available_listbox.pack(fill="both", expand=True, pady=5)

        tk.Button(left_frame, text="Adicionar ➡", command=self.add_to_reservation).pack(pady=5)

        # Frame direito - Reserva atual
        right_frame = tk. LabelFrame(frame, text="Reserva Atual", padx=10, pady=10)
        right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # ========== DATA ==========
        date_frame = tk.LabelFrame(right_frame, text="Data da Reserva", padx=10, pady=8)
        date_frame.pack(fill="x", pady=(0, 10))

        date_row = tk.Frame(date_frame)
        date_row.pack()

        tk.Label(date_row, text="Dia:").pack(side="left")
        self.day_var = tk.StringVar(value=datetime.now().strftime("%d"))
        day_spin = ttk.Spinbox(date_row, from_=1, to=31, width=4, textvariable=self. day_var)
        day_spin.pack(side="left", padx=(2, 10))

        tk.Label(date_row, text="Mês:").pack(side="left")
        self.month_var = tk.StringVar(value=datetime.now().strftime("%m"))
        month_spin = ttk.Spinbox(date_row, from_=1, to=12, width=4, textvariable=self.month_var)
        month_spin.pack(side="left", padx=(2, 10))

        tk.Label(date_row, text="Ano:").pack(side="left")
        self.year_var = tk.StringVar(value=datetime.now().strftime("%Y"))
        year_spin = ttk.Spinbox(date_row, from_=2024, to=2030, width=6, textvariable=self.year_var)
        year_spin.pack(side="left", padx=2)

        # ========== HORÁRIO ==========
        time_frame = tk.LabelFrame(right_frame, text="Horário", padx=10, pady=8)
        time_frame.pack(fill="x", pady=(0, 10))

        start_row = tk.Frame(time_frame)
        start_row.pack(fill="x", pady=3)

        tk.Label(start_row, text="Início:", width=8, anchor="w").pack(side="left")
        self.start_hour_var = tk.StringVar(value="10")
        ttk. Spinbox(start_row, from_=8, to=22, width=4, textvariable=self. start_hour_var,
                    command=self.calculate_total).pack(side="left")
        tk.Label(start_row, text=":").pack(side="left")

        self.start_min_var = tk.StringVar(value="00")
        ttk.Spinbox(start_row, values=("00", "15", "30", "45"), width=4,
                    textvariable=self.start_min_var, command=self.calculate_total).pack(side="left")
        tk.Label(start_row, text="h").pack(side="left")

        end_row = tk.Frame(time_frame)
        end_row.pack(fill="x", pady=3)

        tk.Label(end_row, text="Fim:", width=8, anchor="w").pack(side="left")
        self.end_hour_var = tk.StringVar(value="12")
        ttk.Spinbox(end_row, from_=8, to=22, width=4, textvariable=self.end_hour_var,
                    command=self.calculate_total).pack(side="left")
        tk.Label(end_row, text=":").pack(side="left")

        self.end_min_var = tk.StringVar(value="00")
        ttk.Spinbox(end_row, values=("00", "15", "30", "45"), width=4,
                    textvariable=self.end_min_var, command=self.calculate_total).pack(side="left")
        tk.Label(end_row, text="h").pack(side="left")

        self.duration_label = tk.Label(time_frame, text="Duração: 2h 00min", fg="gray")
        self.duration_label.pack(pady=(5, 0))

        # ========== ARTIGOS SELECIONADOS ==========
        tk.Label(right_frame, text="Artigos selecionados:").pack(anchor="w")
        self.selected_listbox = tk.Listbox(right_frame, height=6)
        self.selected_listbox.pack(fill="both", expand=True, pady=5)

        tk.Button(right_frame, text="⬅ Remover", command=self.remove_from_reservation).pack(pady=5)

        self.total_label = tk.Label(right_frame, text="Total: €0.00", font=("Arial", 12, "bold"))
        self.total_label.pack(pady=10)

        confirm_btn = tk.Button(right_frame, text="Confirmar Reserva",
                                command=self.confirm_reservation,
                                font=("Arial", 10),
                                bg="#333333", fg="white",
                                relief="flat",
                                cursor="hand2",
                                padx=15, pady=5)
        confirm_btn.pack(pady=10)

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

        category_name = self.res_category_var.get()
        category_id = None

        categories = Category.get_all()
        for cat in categories:
            if cat.name == category_name:
                category_id = cat.id
                break

        items = SportsItem.get_all(category_id=category_id, available_only=True)

        for item in items:
            if item.id not in [i.id for i in self. selected_items]:
                self.available_listbox.insert(tk.END, f"{item.id}:  {item.name} - €{item.price_per_hour:.2f}/h")

    def add_to_reservation(self):
        from models import SportsItem

        selections = self.available_listbox. curselection()

        for i in selections:
            item_text = self.available_listbox. get(i)
            item_id = int(item_text. split(": ")[0])

            item = SportsItem.find_by_id(item_id)
            if item and item not in self.selected_items:
                self.selected_items.append(item)
                self.selected_listbox. insert(tk.END, f"{item.name} - €{item.price_per_hour:.2f}/h")

        self.load_available_items()
        self.calculate_total()

    def remove_from_reservation(self):
        selection = self.selected_listbox.curselection()
        if selection:
            idx = selection[0]
            self.selected_items.pop(idx)
            self.selected_listbox.delete(idx)
            self.load_available_items()
            self.calculate_total()

    def get_reservation_dates(self):
        try:
            day = int(self.day_var.get())
            month = int(self.month_var.get())
            year = int(self.year_var.get())

            start_hour = int(self.start_hour_var.get())
            start_min = int(self.start_min_var.get())

            end_hour = int(self.end_hour_var.get())
            end_min = int(self.end_min_var.get())

            start_date = datetime(year, month, day, start_hour, start_min)
            end_date = datetime(year, month, day, end_hour, end_min)

            return start_date, end_date
        except ValueError: 
            return None, None

    def calculate_total(self):
        start_date, end_date = self.get_reservation_dates()

        if start_date and end_date and end_date > start_date: 
            hours = (end_date - start_date).total_seconds() / 3600

            h = int(hours)
            m = int((hours - h) * 60)
            self.duration_label.config(text=f"Duração: {h}h {m: 02d}min", fg="gray")

            total = sum(item.price_per_hour * hours for item in self.selected_items)
            self.total_label.config(text=f"Total: €{total:.2f} ({hours:.1f}h)")
        else:
            self. duration_label.config(text="Duração: inválida", fg="red")
            self.total_label.config(text="Total: €0.00")

    def confirm_reservation(self):
        from models import Reservation

        if not self.selected_items:
            messagebox.showwarning("Aviso", "Selecione pelo menos um artigo!")
            return

        start_date, end_date = self.get_reservation_dates()

        if not start_date or not end_date:
            messagebox.showerror("Erro", "Data ou hora inválida!")
            return

        if end_date <= start_date: 
            messagebox.showerror("Erro", "A hora de fim deve ser depois da hora de início!")
            return

        if start_date < datetime.now():
            messagebox.showerror("Erro", "Não pode fazer reservas no passado!")
            return

        reservation = Reservation. create(self.user.id, start_date, end_date)

        for item in self.selected_items:
            reservation.add_item(item)

        reservation.confirm()

        hours = (end_date - start_date).total_seconds() / 3600
        total = sum(item.price_per_hour * hours for item in self.selected_items)

        messagebox.showinfo("Sucesso",
            f"Reserva #{reservation.id} confirmada!\n\n"
            f"Data: {start_date.strftime('%d/%m/%Y')}\n"
            f"Horário: {start_date.strftime('%H:%M')} - {end_date.strftime('%H:%M')}\n"
            f"Duração: {hours:.1f}h\n"
            f"Total: €{total:.2f}")

        self.selected_items = []
        self.selected_listbox.delete(0, tk. END)
        self.calculate_total()
        self.load_available_items()
        self.load_items()
        self.load_history()

    # ==================== ABA HISTÓRICO ====================
    def create_history_tab(self):
        frame = tk.Frame(self. notebook)
        self.notebook. add(frame, text="Histórico")

        btn_frame = tk.Frame(frame)
        btn_frame.pack(fill="x", padx=10, pady=10)

        tk.Button(btn_frame, text="Atualizar", command=self.load_history).pack(side="left")
        tk.Button(btn_frame, text="Cancelar Reserva", command=self.cancel_reservation).pack(side="left", padx=5)

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
                res.end_date. strftime("%Y-%m-%d %H:%M"),
                items_str,
                f"€{res.total_value:.2f}",
                res.state
            ))

    def cancel_reservation(self):
        from models import Reservation

        selection = self.history_tree.selection()
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