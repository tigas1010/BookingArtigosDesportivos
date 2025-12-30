import json
import os
from datetime import datetime

class Reservation: 
    
    DATA_FILE = "data/reservations.json"
    STATES = ["Pending", "Confirmed", "Cancelled", "Completed"]
    
    def __init__(self, id:  int, client_id: int, start_date: datetime,
                 end_date: datetime, item_ids: list = None,
                 total_value: float = 0.0, state: str = "Pending"):
        self._id = id
        self._client_id = client_id
        self._start_date = start_date
        self._end_date = end_date
        self._item_ids = item_ids or []
        self._total_value = total_value
        self._state = state
    
    @property
    def id(self):
        return self._id
    
    @property
    def client_id(self):
        return self._client_id
    
    @property
    def client(self):
        """Obtém o cliente da reserva"""
        from .user import User
        return User.find_by_id(self._client_id)
    
    @property
    def start_date(self):
        return self._start_date
    
    @property
    def end_date(self):
        return self._end_date
    
    @property
    def item_ids(self):
        return self._item_ids
    
    @property
    def items(self):
        """Obtém os artigos da reserva"""
        from .sports_item import SportsItem
        return [SportsItem.find_by_id(item_id) for item_id in self._item_ids]
    
    @property
    def total_value(self):
        return self._total_value
    
    @property
    def state(self):
        return self._state
    
    def add_item(self, item) -> bool:
        """Adiciona um artigo à reserva"""
        if item.check_availability() and item.id not in self._item_ids:
            self._item_ids. append(item.id)
            item.set_available(False)
            item.save()
            self. calculate_total()
            self.save()
            return True
        return False
    
    def remove_item(self, item):
        """Remove um artigo da reserva"""
        if item. id in self._item_ids:
            self._item_ids. remove(item.id)
            item.set_available(True)
            item.save()
            self.calculate_total()
            self.save()
    
    def calculate_total(self):
        """Calcula o valor total da reserva"""
        hours = (self._end_date - self._start_date).total_seconds() / 3600
        items = self.items
        self._total_value = sum(item.price_per_hour * hours for item in items if item)
        return self._total_value
    
    def confirm(self) -> bool:
        if self._state == "Pending" and len(self._item_ids) > 0:
            self._state = "Confirmed"
            self.save()
            return True
        return False
    
    def cancel(self) -> bool:
        if self._state in ["Pending", "Confirmed"]:
            self._state = "Cancelled"
            # Libertar artigos
            for item in self.items:
                if item: 
                    item.set_available(True)
                    item.save()
            self.save()
            return True
        return False
    
    def complete(self) -> bool:
        if self._state == "Confirmed":
            self._state = "Completed"
            # Libertar artigos
            for item in self.items:
                if item:
                    item. set_available(True)
                    item.save()
            self.save()
            return True
        return False
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "client_id": self._client_id,
            "start_date": self._start_date. isoformat(),
            "end_date": self._end_date.isoformat(),
            "item_ids": self._item_ids,
            "total_value": self._total_value,
            "state": self._state
        }
    
    # ========== Métodos JSON ==========
    
    @staticmethod
    def _ensure_file():
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(Reservation.DATA_FILE):
            with open(Reservation. DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    @staticmethod
    def _load_all() -> list:
        Reservation._ensure_file()
        with open(Reservation.DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @staticmethod
    def _save_all(reservations: list):
        Reservation._ensure_file()
        with open(Reservation.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(reservations, f, indent=4, ensure_ascii=False, default=str)
    
    def save(self):
        reservations = Reservation._load_all()
        
        for i, r in enumerate(reservations):
            if r["id"] == self._id:
                reservations[i] = self.to_dict()
                Reservation._save_all(reservations)
                return
        
        reservations.append(self.to_dict())
        Reservation._save_all(reservations)
    
    @staticmethod
    def get_next_id() -> int:
        reservations = Reservation._load_all()
        if not reservations:
            return 101
        return max(r["id"] for r in reservations) + 1
    
    @staticmethod
    def get_all(client_id: int = None, state: str = None) -> list:
        """Obtém todas as reservas com filtros opcionais"""
        reservations_data = Reservation._load_all()
        reservations = [Reservation.from_dict(r) for r in reservations_data]
        
        if client_id:
            reservations = [r for r in reservations if r.client_id == client_id]
        if state:
            reservations = [r for r in reservations if r. state == state]
        
        return reservations
    
    @staticmethod
    def find_by_id(reservation_id: int):
        """Procura reserva por ID"""
        reservations = Reservation._load_all()
        for r in reservations: 
            if r["id"] == reservation_id:
                return Reservation.from_dict(r)
        return None
    
    @staticmethod
    def find_by_client(client_id: int) -> list:
        """Obtém reservas de um cliente"""
        return Reservation.get_all(client_id=client_id)
    
    @staticmethod
    def from_dict(data: dict) -> 'Reservation':
        return Reservation(
            id=data["id"],
            client_id=data["client_id"],
            start_date=datetime.fromisoformat(data["start_date"]),
            end_date=datetime.fromisoformat(data["end_date"]),
            item_ids=data.get("item_ids", []),
            total_value=data.get("total_value", 0.0),
            state=data. get("state", "Pending")
        )
    
    @staticmethod
    def create(client_id: int, start_date: datetime, 
               end_date: datetime) -> 'Reservation':
        """Cria e guarda uma nova reserva"""
        new_id = Reservation. get_next_id()
        reservation = Reservation(new_id, client_id, start_date, end_date)
        reservation.save()
        return reservation
    
    def __str__(self):
        items = self.items
        items_str = ", ".join([i.name for i in items if i])
        return (f"Reservation #{self._id} | {self._state}\n"
                f"Period: {self._start_date. strftime('%Y-%m-%d %H:%M')} - "
                f"{self._end_date.strftime('%Y-%m-%d %H:%M')}\n"
                f"Items:  {items_str}\n"
                f"Total: €{self._total_value:.2f}")