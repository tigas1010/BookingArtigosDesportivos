import json
import os

class SportsItem:
    
    DATA_FILE = "data/sports_items.json"
    
    def __init__(self, id: int, name: str, brand: str, price_per_hour: float,
                 category_id:  int = None, available: bool = True):
        self._id = id
        self._name = name
        self._brand = brand
        self._price_per_hour = price_per_hour
        self._available = available
        self._category_id = category_id
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def brand(self):
        return self._brand
    
    @property
    def price_per_hour(self):
        return self._price_per_hour
    
    @property
    def available(self):
        return self._available
    
    @property
    def category_id(self):
        return self._category_id
    
    @property
    def category(self):
        """Obtém a categoria do artigo"""
        if self._category_id:
            from .category import Category
            return Category.find_by_id(self._category_id)
        return None
    
    def check_availability(self) -> bool:
        return self._available
    
    def set_available(self, available:  bool):
        self._available = available
    
    def to_dict(self) -> dict:
        return {
            "id":  self._id,
            "name": self._name,
            "brand": self._brand,
            "price_per_hour": self._price_per_hour,
            "available": self._available,
            "category_id": self._category_id
        }
    
    # ========== Métodos JSON ==========
    
    @staticmethod
    def _ensure_file():
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(SportsItem.DATA_FILE):
            with open(SportsItem.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    @staticmethod
    def _load_all() -> list:
        SportsItem._ensure_file()
        with open(SportsItem.DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @staticmethod
    def _save_all(items: list):
        SportsItem._ensure_file()
        with open(SportsItem.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=4, ensure_ascii=False)
    
    def save(self):
        items = SportsItem._load_all()
        
        for i, item in enumerate(items):
            if item["id"] == self._id:
                items[i] = self.to_dict()
                SportsItem._save_all(items)
                return
        
        items.append(self.to_dict())
        SportsItem._save_all(items)
    
    def delete(self):
        items = SportsItem._load_all()
        items = [i for i in items if i["id"] != self._id]
        SportsItem._save_all(items)
    
    @staticmethod
    def get_next_id() -> int:
        items = SportsItem._load_all()
        if not items: 
            return 1
        return max(i["id"] for i in items) + 1
    
    @staticmethod
    def get_all(category_id: int = None, available_only: bool = False) -> list:
        """Obtém todos os artigos com filtros opcionais"""
        items_data = SportsItem._load_all()
        items = [SportsItem.from_dict(i) for i in items_data]
        
        if category_id:
            items = [i for i in items if i.category_id == category_id]
        if available_only:
            items = [i for i in items if i.available]
        
        return items
    
    @staticmethod
    def find_by_id(item_id: int):
        """Procura artigo por ID"""
        items = SportsItem._load_all()
        for i in items: 
            if i["id"] == item_id:
                return SportsItem.from_dict(i)
        return None
    
    @staticmethod
    def find_by_category(category_id: int) -> list:
        """Obtém artigos de uma categoria"""
        return SportsItem. get_all(category_id=category_id)
    
    @staticmethod
    def from_dict(data: dict) -> 'SportsItem':
        return SportsItem(
            id=data["id"],
            name=data["name"],
            brand=data["brand"],
            price_per_hour=data["price_per_hour"],
            category_id=data. get("category_id"),
            available=data.get("available", True)
        )
    
    @staticmethod
    def create(name: str, brand: str, price_per_hour: float,
               category_id: int = None) -> 'SportsItem': 
        """Cria e guarda um novo artigo"""
        new_id = SportsItem.get_next_id()
        item = SportsItem(new_id, name, brand, price_per_hour, category_id, True)
        item.save()
        return item
    
    def __str__(self):
        status = "Available" if self._available else "Unavailable"
        return f"{self._name} ({self._brand}) - €{self._price_per_hour:.2f}/hour - {status}"