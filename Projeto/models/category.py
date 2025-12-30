import json
import os

class Category:
    
    DATA_FILE = "data/categories.json"
    
    def __init__(self, id: int, name: str, description: str = ""):
        self._id = id
        self._name = name
        self._description = description
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name":  self._name,
            "description": self._description
        }
    
    # ========== Métodos JSON ==========
    
    @staticmethod
    def _ensure_file():
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(Category. DATA_FILE):
            with open(Category.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    @staticmethod
    def _load_all() -> list:
        Category._ensure_file()
        with open(Category.DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @staticmethod
    def _save_all(categories: list):
        Category._ensure_file()
        with open(Category.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(categories, f, indent=4, ensure_ascii=False)
    
    def save(self):
        categories = Category._load_all()
        
        for i, c in enumerate(categories):
            if c["id"] == self._id:
                categories[i] = self.to_dict()
                Category._save_all(categories)
                return
        
        categories.append(self. to_dict())
        Category._save_all(categories)
    
    def delete(self):
        categories = Category._load_all()
        categories = [c for c in categories if c["id"] != self._id]
        Category._save_all(categories)
    
    @staticmethod
    def get_next_id() -> int:
        categories = Category._load_all()
        if not categories:
            return 1
        return max(c["id"] for c in categories) + 1
    
    @staticmethod
    def get_all() -> list:
        """Obtém todas as categorias"""
        categories_data = Category._load_all()
        return [Category.from_dict(c) for c in categories_data]
    
    @staticmethod
    def find_by_id(category_id: int):
        """Procura categoria por ID"""
        categories = Category._load_all()
        for c in categories:
            if c["id"] == category_id: 
                return Category.from_dict(c)
        return None
    
    @staticmethod
    def from_dict(data: dict) -> 'Category':
        return Category(
            id=data["id"],
            name=data["name"],
            description=data. get("description", "")
        )
    
    @staticmethod
    def create(name: str, description:  str = "") -> 'Category':
        """Cria e guarda uma nova categoria"""
        new_id = Category.get_next_id()
        category = Category(new_id, name, description)
        category.save()
        return category
    
    def get_items(self):
        """Obtém artigos desta categoria"""
        from . sports_item import SportsItem
        return SportsItem.find_by_category(self._id)
    
    def __str__(self):
        return f"{self._name}"