"""
user.py - Modelos de Utilizadores

Este ficheiro define a hierarquia de utilizadores do sistema: 
- User: Classe base abstrata
- Client: Utilizador que pode fazer reservas
- Administrator: Utilizador com poderes de gestão

Padrão utilizado: Herança (Inheritance)
"""

from abc import ABC, abstractmethod


class User(ABC):
    """
    Classe base abstrata para todos os utilizadores.
    
    ABC (Abstract Base Class) significa que esta classe não pode
    ser instanciada diretamente - apenas as subclasses podem. 
    
    Atributos:
        _id:  Identificador único (gerado automaticamente)
        _name: Nome do utilizador
        _email: Email (usado para login)
        _password: Palavra-passe
    """
    
    _id_counter = 0  # Contador estático para gerar IDs únicos
    
    def __init__(self, name:  str, email: str, password:  str):
        """
        Construtor da classe User.
        
        Args:
            name: Nome completo
            email:  Endereço de email
            password: Palavra-passe
        """
        User._id_counter += 1
        self._id = User._id_counter
        self._name = name
        self._email = email
        self._password = password
    
    # ==================== PROPERTIES ====================
    # Properties permitem acesso controlado aos atributos privados
    
    @property
    def id(self):
        """Retorna o ID do utilizador."""
        return self._id
    
    @property
    def name(self):
        """Retorna o nome do utilizador."""
        return self._name
    
    @property
    def email(self):
        """Retorna o email do utilizador."""
        return self._email
    
    # ==================== MÉTODOS ====================
    
    def login(self, email: str, password:  str) -> bool:
        """
        Verifica as credenciais de login.
        
        Args:
            email: Email introduzido
            password: Palavra-passe introduzida
        
        Returns:
            True se as credenciais estão corretas, False caso contrário
        """
        return self._email == email and self._password == password
    
    @abstractmethod
    def get_type(self) -> str:
        """
        Método abstrato que deve ser implementado pelas subclasses.
        Retorna o tipo de utilizador ("client" ou "admin").
        """
        pass


class Client(User):
    """
    Classe que representa um cliente do sistema.
    Herda de User e adiciona funcionalidades específicas de cliente.
    
    Atributos adicionais:
        _address:  Morada do cliente
        _phone: Número de telefone
        _reservations: Lista de reservas do cliente
    """
    
    def __init__(self, name:  str, email: str, password:  str, address: str, phone:  str):
        """
        Construtor do Cliente.
        
        Args:
            name: Nome completo
            email: Email
            password: Palavra-passe
            address: Morada
            phone: Telefone
        """
        super().__init__(name, email, password)  # Chama o construtor da classe pai
        self._address = address
        self._phone = phone
        self._reservations = []  # Lista de reservas do cliente
    
    @property
    def address(self):
        """Retorna a morada do cliente."""
        return self._address
    
    @property
    def phone(self):
        """Retorna o telefone do cliente."""
        return self._phone
    
    @property
    def reservations(self):
        """Retorna a lista de reservas."""
        return self._reservations
    
    def make_reservation(self, reservation):
        """
        Adiciona uma reserva à lista do cliente.
        
        Args:
            reservation: Objeto Reservation a adicionar
        """
        self._reservations.append(reservation)
    
    def get_history(self):
        """
        Retorna o histórico de reservas do cliente.
        
        Returns:
            Lista de todas as reservas
        """
        return self._reservations
    
    def get_type(self) -> str:
        """
        Implementação do método abstrato. 
        
        Returns:
            String "client" identificando o tipo de utilizador
        """
        return "client"


class Administrator(User):
    """
    Classe que representa um administrador do sistema.
    Herda de User e adiciona funcionalidades de gestão.
    
    Atributos adicionais:
        _access_level: Nível de acesso/permissões
    """
    
    def __init__(self, name: str, email: str, password: str, access_level: int = 1):
        """
        Construtor do Administrador. 
        
        Args:
            name: Nome
            email: Email
            password:  Palavra-passe
            access_level: Nível de acesso (default: 1)
        """
        super().__init__(name, email, password)
        self._access_level = access_level
    
    @property
    def access_level(self):
        """Retorna o nível de acesso."""
        return self._access_level
    
    def manage_stock(self, item, available:  bool):
        """
        Altera a disponibilidade de um artigo. 
        
        Args:
            item: Artigo a modificar
            available:  Novo estado de disponibilidade
        """
        item.set_available(available)
    
    def cancel_reservation(self, reservation):
        """
        Cancela uma reserva.
        
        Args:
            reservation: Reserva a cancelar
        """
        reservation.cancel()
    
    def get_type(self) -> str:
        """
        Implementação do método abstrato.
        
        Returns:
            String "admin" identificando o tipo de utilizador
        """
        return "admin"