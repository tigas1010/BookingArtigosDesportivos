"""
Módulo de gestão de utilizadores.
Contém as classes User (abstrata), Client e Administrator.
"""

import json
import os
from abc import ABC, abstractmethod


class User(ABC):
    """
    Classe abstrata base para todos os utilizadores do sistema.
    Implementa persistência em JSON e métodos comuns.
    """
    
    DATA_FILE = "data/users.json"
    
    def __init__(self, id:  int, name: str, email: str, password: str):
        """
        Inicializa um utilizador. 
        
        Args:
            id:  Identificador único do utilizador
            name: Nome completo
            email: Email (usado para login)
            password: Password (armazenada em texto simples - melhorar em produção)
        """
        self._id = id
        self._name = name
        self._email = email
        self._password = password
    
    # ==================== PROPRIEDADES ====================
    
    @property
    def id(self) -> int:
        return self._id
    
    @property
    def name(self) -> str:
        return self._name
    
    @property
    def email(self) -> str:
        return self._email
    
    # ==================== MÉTODOS DE INSTÂNCIA ====================
    
    def login(self, email: str, password: str) -> bool:
        """Verifica as credenciais de login."""
        return self._email == email and self._password == password
    
    @abstractmethod
    def get_type(self) -> str:
        """Retorna o tipo de utilizador ('client' ou 'admin')."""
        pass
    
    @abstractmethod
    def to_dict(self) -> dict:
        """Converte o utilizador para dicionário (para JSON)."""
        pass
    
    def save(self):
        """Guarda ou atualiza este utilizador no ficheiro JSON."""
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
    
    # ==================== MÉTODOS ESTÁTICOS (PERSISTÊNCIA) ====================
    
    @staticmethod
    def _ensure_file():
        """Cria a pasta e ficheiro JSON se não existirem."""
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(User.DATA_FILE):
            with open(User.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    @staticmethod
    def _load_all() -> list:
        """Carrega todos os utilizadores do ficheiro JSON."""
        User._ensure_file()
        try:
            with open(User. DATA_FILE, "r", encoding="utf-8") as f:
                content = f.read().strip()
                return json.loads(content) if content else []
        except json.JSONDecodeError:
            return []
    
    @staticmethod
    def _save_all(users: list):
        """Guarda a lista de utilizadores no ficheiro JSON."""
        User._ensure_file()
        with open(User.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, indent=4, ensure_ascii=False)
    
    @staticmethod
    def get_next_id() -> int:
        """Obtém o próximo ID disponível."""
        users = User._load_all()
        return max((u["id"] for u in users), default=0) + 1
    
    @staticmethod
    def find_by_email(email: str):
        """Procura um utilizador pelo email."""
        users = User._load_all()
        for u in users: 
            if u["email"] == email:
                return User. from_dict(u)
        return None
    
    @staticmethod
    def find_by_id(user_id: int):
        """Procura um utilizador pelo ID."""
        users = User._load_all()
        for u in users:
            if u["id"] == user_id:
                return User.from_dict(u)
        return None
    
    @staticmethod
    def from_dict(data: dict):
        """Cria um objeto User a partir de um dicionário."""
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
    """Classe que representa um cliente do sistema."""
    
    def __init__(self, id: int, name: str, email: str, password: str,
                 address: str, phone: str):
        super().__init__(id, name, email, password)
        self._address = address
        self._phone = phone
    
    @property
    def address(self) -> str:
        return self._address
    
    @property
    def phone(self) -> str:
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
        """Obtém todas as reservas deste cliente."""
        from . reservation import Reservation
        return Reservation.find_by_client(self._id)
    
    @staticmethod
    def create(name: str, email: str, password: str,
               address: str, phone:  str) -> 'Client':
        """Cria e guarda um novo cliente."""
        new_id = User.get_next_id()
        client = Client(new_id, name, email, password, address, phone)
        client.save()
        return client


class Administrator(User):
    """Classe que representa um administrador do sistema."""
    
    def __init__(self, id: int, name: str, email: str, password: str,
                 access_level: int = 1):
        super().__init__(id, name, email, password)
        self._access_level = access_level
    
    @property
    def access_level(self) -> int:
        return self._access_level
    
    def get_type(self) -> str:
        return "admin"
    
    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "type": "admin",
            "name": self._name,
            "email": self._email,
            "password": self._password,
            "access_level": self._access_level
        }
    
    @staticmethod
    def create(name: str, email: str, password: str,
               access_level: int = 1) -> 'Administrator':
        """Cria e guarda um novo administrador."""
        new_id = User.get_next_id()
        admin = Administrator(new_id, name, email, password, access_level)
        admin.save()
        return admin