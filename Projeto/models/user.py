import json
import os
from abc import ABC, abstractmethod

class User(ABC):
    
    DATA_FILE = "data/users.json"
    
    def __init__(self, id: int, name: str, email: str, password: str):
        self._id = id
        self._name = name
        self._email = email
        self._password = password
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def email(self):
        return self._email
    
    def login(self, email: str, password: str) -> bool:
        return self._email == email and self._password == password
    
    @abstractmethod
    def get_type(self) -> str:
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        pass
    
    # ========== Métodos JSON ==========
    
    @staticmethod
    def _ensure_file():
        """Cria pasta e ficheiro se não existirem"""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(User.DATA_FILE):
            with open(User.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    @staticmethod
    def _load_all() -> list:
        """Carrega todos os users do JSON"""
        User._ensure_file()
        with open(User.DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @staticmethod
    def _save_all(users: list):
        """Guarda todos os users no JSON"""
        User._ensure_file()
        with open(User.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
    
    def save(self):
        """Guarda ou atualiza este user"""
        users = User._load_all()
        
        # Atualizar se já existe
        for i, u in enumerate(users):
            if u["id"] == self._id:
                users[i] = self. to_dict()
                User._save_all(users)
                return
        
        # Adicionar novo
        users.append(self.to_dict())
        User._save_all(users)
    
    @staticmethod
    def get_next_id() -> int:
        """Obtém o próximo ID disponível"""
        users = User._load_all()
        if not users:
            return 1
        return max(u["id"] for u in users) + 1
    
    @staticmethod
    def find_by_email(email: str):
        """Procura user por email"""
        users = User._load_all()
        for u in users:
            if u["email"] == email:
                return User.from_dict(u)
        return None
    
    @staticmethod
    def find_by_id(user_id: int):
        """Procura user por ID"""
        users = User._load_all()
        for u in users:
            if u["id"] == user_id: 
                return User.from_dict(u)
        return None
    
    @staticmethod
    def from_dict(data: dict):
        """Cria User a partir de dict"""
        if data["type"] == "client":
            return Client(
                id=data["id"],
                name=data["name"],
                email=data["email"],
                password=data["password"],
                address=data["address"],
                phone=data["phone"]
            )
        elif data["type"] == "admin": 
            return Administrator(
                id=data["id"],
                name=data["name"],
                email=data["email"],
                password=data["password"],
                access_level=data["access_level"]
            )
        return None


class Client(User):
    
    def __init__(self, id: int, name: str, email: str, password: str, 
                 address: str, phone: str):
        super().__init__(id, name, email, password)
        self._address = address
        self._phone = phone
    
    @property
    def address(self):
        return self._address
    
    @property
    def phone(self):
        return self._phone
    
    def get_type(self) -> str:
        return "client"
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "type": "client",
            "name": self._name,
            "email": self._email,
            "password": self._password,
            "address": self._address,
            "phone": self._phone
        }
    
    def get_reservations(self):
        """Obtém reservas do cliente"""
        from .reservation import Reservation
        return Reservation.find_by_client(self._id)
    
    @staticmethod
    def create(name: str, email: str, password: str, 
               address: str, phone: str) -> 'Client':
        """Cria e guarda um novo cliente"""
        new_id = User.get_next_id()
        client = Client(new_id, name, email, password, address, phone)
        client.save()
        return client


class Administrator(User):
    
    def __init__(self, id: int, name: str, email: str, password: str, 
                 access_level: int = 1):
        super().__init__(id, name, email, password)
        self._access_level = access_level
    
    @property
    def access_level(self):
        return self._access_level
    
    def get_type(self) -> str:
        return "admin"
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "type":  "admin",
            "name":  self._name,
            "email": self._email,
            "password": self._password,
            "access_level": self._access_level
        }
    
    def manage_stock(self, item, available: bool):
        item.set_available(available)
        item.save()
    
    def cancel_reservation(self, reservation):
        reservation.cancel()
    
    @staticmethod
    def create(name: str, email: str, password: str, 
               access_level: int = 1) -> 'Administrator':
        """Cria e guarda um novo administrador"""
        new_id = User.get_next_id()
        admin = Administrator(new_id, name, email, password, access_level)
        admin.save()
        return admin