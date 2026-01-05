"""
Módulo de gestão de reservas de artigos desportivos. 
Implementa o ciclo de vida completo de uma reserva:  criação, confirmação, 
cancelamento e conclusão, com persistência em ficheiro JSON.
"""

import json
import os
from datetime import datetime


class Reservation:  
    """
    Classe que representa uma reserva de artigos desportivos.
    
    Uma reserva associa um cliente a um ou mais artigos durante um período
    de tempo específico.  Possui um ciclo de vida com diferentes estados.
    
    Attributes:
        DATA_FILE (str): Caminho para o ficheiro JSON de armazenamento
        STATES (list): Estados possíveis de uma reserva
    """
    
    # Caminho do ficheiro JSON onde as reservas são guardadas
    DATA_FILE = "data/reservations.json"
    
    # Estados possíveis do ciclo de vida de uma reserva
    # Pending -> Confirmed -> Completed
    #    |          |
    #    v          v
    # Cancelled  Cancelled
    STATES = ["Pending", "Confirmed", "Cancelled", "Completed"]
    
    def __init__(self, id:  int, client_id: int, start_date: datetime,
                 end_date: datetime, item_ids: list = None,
                 total_value: float = 0.0, state: str = "Pending"):
        """
        Inicializa uma nova reserva.
        
        Args:
            id:  Identificador único da reserva
            client_id: ID do cliente que fez a reserva
            start_date: Data e hora de início da reserva
            end_date: Data e hora de fim da reserva
            item_ids: Lista de IDs dos artigos reservados (opcional)
            total_value:  Valor total da reserva em euros (opcional)
            state: Estado inicial da reserva (default: "Pending")
        """
        self._id = id
        self._client_id = client_id
        self._start_date = start_date
        self._end_date = end_date
        self._item_ids = item_ids or []  # Lista vazia se None
        self._total_value = total_value
        self._state = state
    
    # ==================== PROPRIEDADES SIMPLES ====================
    
    @property
    def id(self):
        """Retorna o identificador único da reserva."""
        return self._id
    
    @property
    def client_id(self):
        """Retorna o ID do cliente associado à reserva."""
        return self._client_id
    
    @property
    def start_date(self):
        """Retorna a data e hora de início da reserva."""
        return self._start_date
    
    @property
    def end_date(self):
        """Retorna a data e hora de fim da reserva."""
        return self._end_date
    
    @property
    def item_ids(self):
        """Retorna a lista de IDs dos artigos reservados."""
        return self._item_ids
    
    @property
    def total_value(self):
        """Retorna o valor total da reserva em euros."""
        return self._total_value
    
    @property
    def state(self):
        """Retorna o estado atual da reserva."""
        return self._state
    
    # ==================== PROPRIEDADES COM RELAÇÕES ====================
    
    @property
    def client(self):
        """
        Obtém o objeto Cliente associado a esta reserva.
        
        Estabelece a relação N:1 entre Reservation e User/Client.
        
        Returns:
            Client:  Objeto do cliente, ou None se não encontrado
        """
        from .user import User
        return User.find_by_id(self._client_id)
    
    @property
    def items(self):
        """
        Obtém os objetos SportsItem associados a esta reserva.
        
        Estabelece a relação N:M entre Reservation e SportsItem. 
        
        Returns:
            list[SportsItem]: Lista de artigos reservados
        """
        from . sports_item import SportsItem
        return [SportsItem.find_by_id(item_id) for item_id in self._item_ids]
    
    # ==================== GESTÃO DE ARTIGOS ====================
    
    def add_item(self, item) -> bool:
        """
        Adiciona um artigo à reserva.
        
        Verifica se o artigo está disponível antes de adicionar.
        Marca o artigo como indisponível e recalcula o total.
        
        Args:
            item: Objeto SportsItem a adicionar
            
        Returns: 
            bool: True se adicionado com sucesso, False caso contrário
        """
        # Verificar disponibilidade e se já não está na reserva
        if item.check_availability() and item.id not in self._item_ids:
            self._item_ids.append(item.id)
            
            # Marcar artigo como indisponível para outras reservas
            item.set_available(False)
            item.save()
            
            # Atualizar valor total e guardar reserva
            self.calculate_total()
            self.save()
            return True
        return False
    
    def remove_item(self, item):
        """
        Remove um artigo da reserva. 
        
        Liberta o artigo (marca como disponível) e recalcula o total. 
        
        Args:
            item: Objeto SportsItem a remover
        """
        if item.id in self._item_ids:
            self._item_ids.remove(item.id)
            
            # Libertar o artigo para outras reservas
            item.set_available(True)
            item.save()
            
            # Atualizar valor total e guardar reserva
            self.calculate_total()
            self.save()
    
    def calculate_total(self):
        """
        Calcula o valor total da reserva.
        
        O total é baseado no preço por hora de cada artigo multiplicado
        pela duração da reserva em horas.
        
        Returns:
            float: Valor total da reserva em euros
        """
        # Calcular duração em horas
        hours = (self._end_date - self._start_date).total_seconds() / 3600
        
        # Somar preço de todos os artigos
        items = self.items
        self._total_value = sum(item.price_per_hour * hours for item in items if item)
        
        return self._total_value
    
    # ==================== GESTÃO DE ESTADOS ====================
    
    def confirm(self) -> bool:
        """
        Confirma a reserva.
        
        Transição de estado:  Pending -> Confirmed
        Só é possível confirmar se houver pelo menos um artigo. 
        
        Returns:
            bool: True se confirmada com sucesso, False caso contrário
        """
        if self._state == "Pending" and len(self._item_ids) > 0:
            self._state = "Confirmed"
            self. save()
            return True
        return False
    
    def cancel(self) -> bool:
        """
        Cancela a reserva.
        
        Transição de estado: Pending/Confirmed -> Cancelled
        Liberta todos os artigos reservados.
        
        Returns:
            bool: True se cancelada com sucesso, False caso contrário
        """
        if self._state in ["Pending", "Confirmed"]:
            self._state = "Cancelled"
            
            # Libertar todos os artigos reservados
            for item in self.items:
                if item: 
                    item.set_available(True)
                    item.save()
            
            self.save()
            return True
        return False
    
    def complete(self) -> bool:
        """
        Marca a reserva como concluída. 
        
        Transição de estado: Confirmed -> Completed
        Liberta todos os artigos após o período de reserva.
        
        Returns:
            bool: True se concluída com sucesso, False caso contrário
        """
        if self._state == "Confirmed": 
            self._state = "Completed"
            
            # Libertar todos os artigos após utilização
            for item in self. items:
                if item: 
                    item.set_available(True)
                    item. save()
            
            self. save()
            return True
        return False
    
    # ==================== SERIALIZAÇÃO ====================
    
    def to_dict(self) -> dict:
        """
        Converte a reserva para um dicionário.
        
        As datas são convertidas para formato ISO 8601 para armazenamento JSON.
        
        Returns:
            dict: Dicionário com os dados da reserva
        """
        return {
            "id":  self._id,
            "client_id": self._client_id,
            "start_date":  self._start_date.isoformat(),  # Formato:  YYYY-MM-DDTHH:MM:SS
            "end_date": self._end_date.isoformat(),
            "item_ids": self._item_ids,
            "total_value": self._total_value,
            "state": self._state
        }
    
    # ========== Métodos JSON (Persistência) ==========
    
    @staticmethod
    def _ensure_file():
        """
        Garante que o ficheiro JSON existe.
        
        Cria a pasta 'data' e o ficheiro JSON vazio se não existirem.
        """
        os.makedirs("data", exist_ok=True)
        if not os.path.exists(Reservation.DATA_FILE):
            with open(Reservation.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    @staticmethod
    def _load_all() -> list:
        """
        Carrega todas as reservas do ficheiro JSON.
        
        Returns:
            list: Lista de dicionários com os dados das reservas
        """
        Reservation._ensure_file()
        with open(Reservation. DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @staticmethod
    def _save_all(reservations: list):
        """
        Guarda todas as reservas no ficheiro JSON.
        
        Args:
            reservations: Lista de dicionários com os dados das reservas
        """
        Reservation._ensure_file()
        with open(Reservation.DATA_FILE, "w", encoding="utf-8") as f:
            # default=str permite serializar objetos datetime que não foram convertidos
            json.dump(reservations, f, indent=4, ensure_ascii=False, default=str)
    
    # ==================== OPERAÇÕES CRUD ====================
    
    def save(self):
        """
        Guarda ou atualiza esta reserva no ficheiro JSON.
        
        Se a reserva já existir (mesmo ID), atualiza os seus dados.
        Caso contrário, adiciona como nova reserva.
        """
        reservations = Reservation._load_all()
        
        # Procurar reserva existente para atualizar
        for i, r in enumerate(reservations):
            if r["id"] == self._id:
                reservations[i] = self.to_dict()
                Reservation._save_all(reservations)
                return
        
        # Se não existe, adicionar nova reserva
        reservations.append(self.to_dict())
        Reservation._save_all(reservations)
    
    # ==================== MÉTODOS ESTÁTICOS ====================
    
    @staticmethod
    def get_next_id() -> int:
        """
        Obtém o próximo ID disponível para uma nova reserva.
        
        Os IDs de reserva começam em 101 para fácil identificação.
        
        Returns:
            int:  Próximo ID disponível
        """
        reservations = Reservation._load_all()
        if not reservations:
            return 101  # IDs de reserva começam em 101
        return max(r["id"] for r in reservations) + 1
    
    @staticmethod
    def get_all(client_id: int = None, state: str = None) -> list:
        """
        Obtém todas as reservas com filtros opcionais.
        
        Permite filtrar por cliente e/ou estado da reserva.
        
        Args:
            client_id:  Filtrar por ID do cliente (opcional)
            state: Filtrar por estado da reserva (opcional)
            
        Returns: 
            list[Reservation]: Lista de reservas filtradas
        """
        reservations_data = Reservation._load_all()
        reservations = [Reservation.from_dict(r) for r in reservations_data]
        
        # Aplicar filtro por cliente se especificado
        if client_id:
            reservations = [r for r in reservations if r. client_id == client_id]
        
        # Aplicar filtro por estado se especificado
        if state:
            reservations = [r for r in reservations if r. state == state]
        
        return reservations
    
    @staticmethod
    def find_by_id(reservation_id: int):
        """
        Procura uma reserva pelo seu ID.
        
        Args:
            reservation_id: ID da reserva a procurar
            
        Returns:
            Reservation: Objeto Reservation se encontrado, None caso contrário
        """
        reservations = Reservation._load_all()
        for r in reservations:  
            if r["id"] == reservation_id:
                return Reservation.from_dict(r)
        return None
    
    @staticmethod
    def find_by_client(client_id: int) -> list:
        """
        Obtém todas as reservas de um cliente específico.
        
        Atalho para get_all(client_id=client_id).
        
        Args:
            client_id: ID do cliente
            
        Returns:
            list[Reservation]: Lista de reservas do cliente
        """
        return Reservation. get_all(client_id=client_id)
    
    @staticmethod
    def from_dict(data: dict) -> 'Reservation':
        """
        Cria um objeto Reservation a partir de um dicionário.
        
        Converte as datas do formato ISO 8601 para objetos datetime.
        
        Args:
            data: Dicionário com os dados da reserva
            
        Returns:
            Reservation: Nova instância de Reservation
        """
        return Reservation(
            id=data["id"],
            client_id=data["client_id"],
            start_date=datetime.fromisoformat(data["start_date"]),  # Converter string para datetime
            end_date=datetime.fromisoformat(data["end_date"]),
            item_ids=data.get("item_ids", []),
            total_value=data.get("total_value", 0.0),
            state=data.get("state", "Pending")
        )
    
    @staticmethod
    def create(client_id: int, start_date: datetime, 
               end_date: datetime) -> 'Reservation':
        """
        Cria e guarda uma nova reserva.
        
        A reserva é criada no estado "Pending" sem artigos.
        Os artigos devem ser adicionados posteriormente com add_item().
        
        Args:
            client_id:  ID do cliente que faz a reserva
            start_date: Data e hora de início
            end_date: Data e hora de fim
            
        Returns: 
            Reservation: Nova reserva criada e guardada
        """
        new_id = Reservation.get_next_id()
        reservation = Reservation(new_id, client_id, start_date, end_date)
        reservation.save()
        return reservation
    
    # ==================== REPRESENTAÇÃO ====================
    
    def __str__(self):
        """
        Representação em string da reserva.
        
        Formato legível com todas as informações principais.
        
        Returns:
            str: Descrição formatada da reserva
        """
        items = self.items
        items_str = ", ".join([i.name for i in items if i])
        
        return (f"Reservation #{self._id} | {self._state}\n"
                f"Period: {self._start_date. strftime('%Y-%m-%d %H:%M')} - "
                f"{self._end_date.strftime('%Y-%m-%d %H:%M')}\n"
                f"Items: {items_str}\n"
                f"Total: €{self._total_value:.2f}")