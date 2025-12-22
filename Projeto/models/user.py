from abc import ABC, abstractmethod

class User(ABC):
    _id_counter = 0
    
    def __init__(self, name:  str, email: str, password: str):
        User._id_counter += 1
        self._id = User._id_counter
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


class Client(User):
    def __init__(self, name: str, email: str, password: str, address: str, phone: str):
        super().__init__(name, email, password)
        self._address = address
        self._phone = phone
        self._reservations = []
    
    @property
    def address(self):
        return self._address
    
    @property
    def phone(self):
        return self._phone
    
    @property
    def reservations(self):
        return self._reservations
    
    def make_reservation(self, reservation):
        self._reservations.append(reservation)
    
    def get_history(self):
        return self._reservations
    
    def get_type(self) -> str:
        return "client"


class Administrator(User):
    def __init__(self, name: str, email: str, password: str, access_level: int = 1):
        super().__init__(name, email, password)
        self._access_level = access_level
    
    @property
    def access_level(self):
        return self._access_level
    
    def manage_stock(self, item, available:  bool):
        item.set_available(available)
    
    def cancel_reservation(self, reservation):
        reservation.cancel()
    
    def get_type(self) -> str:
        return "admin"