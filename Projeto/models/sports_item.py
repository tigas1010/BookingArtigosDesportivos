"""
Módulo de gestão de artigos desportivos.
Implementa a classe SportsItem que representa os artigos disponíveis
para aluguer, com persistência em ficheiro JSON.
"""

import json
import os


class SportsItem:
    """
    Classe que representa um artigo desportivo para aluguer.
    
    Cada artigo possui informações como nome, marca, preço por hora,
    categoria associada e estado de disponibilidade.
    
    Attributes:
        DATA_FILE (str): Caminho para o ficheiro JSON de armazenamento
    """
    
    # Caminho do ficheiro JSON onde os artigos são guardados
    DATA_FILE = "data/sports_items.json"
    
    def __init__(self, id: int, name:  str, brand: str, price_per_hour: float,
                 category_id:  int = None, available: bool = True):
        """
        Inicializa um novo artigo desportivo.
        
        Args:
            id:  Identificador único do artigo
            name: Nome do artigo (ex: "Bola de Futebol", "Raquete de Ténis")
            brand: Marca do artigo (ex: "Nike", "Adidas", "Wilson")
            price_per_hour: Preço de aluguer por hora em euros
            category_id: ID da categoria a que pertence (opcional)
            available: Estado de disponibilidade (default: True)
        """
        self._id = id
        self._name = name
        self._brand = brand
        self._price_per_hour = price_per_hour
        self._available = available
        self._category_id = category_id
    
    # ==================== PROPRIEDADES SIMPLES ====================
    
    @property
    def id(self):
        """Retorna o identificador único do artigo."""
        return self._id
    
    @property
    def name(self):
        """Retorna o nome do artigo."""
        return self._name
    
    @property
    def brand(self):
        """Retorna a marca do artigo."""
        return self._brand
    
    @property
    def price_per_hour(self):
        """Retorna o preço de aluguer por hora em euros."""
        return self._price_per_hour
    
    @property
    def available(self):
        """Retorna o estado de disponibilidade do artigo."""
        return self._available
    
    @property
    def category_id(self):
        """Retorna o ID da categoria associada ao artigo."""
        return self._category_id
    
    # ==================== PROPRIEDADES COM RELAÇÕES ====================
    
    @property
    def category(self):
        """
        Obtém o objeto Category associado a este artigo. 
        
        Estabelece a relação N:1 entre SportsItem e Category.
        
        Returns:
            Category:  Objeto da categoria, ou None se não tiver categoria
        """
        if self._category_id:
            from . category import Category
            return Category. find_by_id(self._category_id)
        return None
    
    # ==================== GESTÃO DE DISPONIBILIDADE ====================
    
    def check_availability(self) -> bool:
        """
        Verifica se o artigo está disponível para reserva.
        
        Returns:
            bool: True se disponível, False caso contrário
        """
        return self._available
    
    def set_available(self, available: bool):
        """
        Define o estado de disponibilidade do artigo.
        
        Utilizado quando um artigo é reservado (False) ou 
        quando uma reserva é cancelada/concluída (True).
        
        Args:
            available:  Novo estado de disponibilidade
        """
        self._available = available
    
    # ==================== SERIALIZAÇÃO ====================
    
    def to_dict(self) -> dict:
        """
        Converte o artigo para um dicionário.
        
        Utilizado para serialização JSON. 
        
        Returns:
            dict: Dicionário com os dados do artigo
        """
        return {
            "id":  self._id,
            "name": self._name,
            "brand": self._brand,
            "price_per_hour": self._price_per_hour,
            "available": self._available,
            "category_id": self._category_id
        }
    
    # ========== Métodos JSON (Persistência) ==========
    
    @staticmethod
    def _ensure_file():
        """
        Garante que o ficheiro JSON existe. 
        
        Cria a pasta 'data' e o ficheiro JSON vazio se não existirem.
        Método privado utilizado internamente antes de operações de leitura/escrita.
        """
        os.makedirs("data", exist_ok=True)
        if not os.path. exists(SportsItem.DATA_FILE):
            with open(SportsItem.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    @staticmethod
    def _load_all() -> list:
        """
        Carrega todos os artigos do ficheiro JSON.
        
        Returns:
            list: Lista de dicionários com os dados dos artigos
        """
        SportsItem._ensure_file()
        with open(SportsItem.DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @staticmethod
    def _save_all(items:  list):
        """
        Guarda todos os artigos no ficheiro JSON.
        
        Args:
            items: Lista de dicionários com os dados dos artigos
        """
        SportsItem._ensure_file()
        with open(SportsItem.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(items, f, indent=4, ensure_ascii=False)
    
    # ==================== OPERAÇÕES CRUD ====================
    
    def save(self):
        """
        Guarda ou atualiza este artigo no ficheiro JSON.
        
        Se o artigo já existir (mesmo ID), atualiza os seus dados.
        Caso contrário, adiciona como novo artigo.
        """
        items = SportsItem._load_all()
        
        # Procurar artigo existente para atualizar
        for i, item in enumerate(items):
            if item["id"] == self._id:
                items[i] = self. to_dict()
                SportsItem._save_all(items)
                return
        
        # Se não existe, adicionar novo artigo
        items.append(self.to_dict())
        SportsItem._save_all(items)
    
    def delete(self):
        """
        Remove este artigo do ficheiro JSON.
        
        Filtra a lista de artigos removendo o que tem o mesmo ID.
        """
        items = SportsItem._load_all()
        items = [i for i in items if i["id"] != self._id]
        SportsItem._save_all(items)
    
    # ==================== MÉTODOS ESTÁTICOS ====================
    
    @staticmethod
    def get_next_id() -> int:
        """
        Obtém o próximo ID disponível para um novo artigo.
        
        Returns:
            int:  Próximo ID (máximo atual + 1, ou 1 se não existirem artigos)
        """
        items = SportsItem._load_all()
        if not items: 
            return 1
        return max(i["id"] for i in items) + 1
    
    @staticmethod
    def get_all(category_id: int = None, available_only: bool = False) -> list:
        """
        Obtém todos os artigos com filtros opcionais.
        
        Permite filtrar por categoria e/ou disponibilidade.
        
        Args:
            category_id:  Filtrar por ID da categoria (opcional)
            available_only:  Se True, retorna apenas artigos disponíveis (opcional)
            
        Returns: 
            list[SportsItem]: Lista de artigos filtrados
        """
        items_data = SportsItem._load_all()
        items = [SportsItem.from_dict(i) for i in items_data]
        
        # Aplicar filtro por categoria se especificado
        if category_id:
            items = [i for i in items if i.category_id == category_id]
        
        # Aplicar filtro de disponibilidade se especificado
        if available_only:
            items = [i for i in items if i.available]
        
        return items
    
    @staticmethod
    def find_by_id(item_id: int):
        """
        Procura um artigo pelo seu ID.
        
        Args:
            item_id: ID do artigo a procurar
            
        Returns:
            SportsItem: Objeto SportsItem se encontrado, None caso contrário
        """
        items = SportsItem._load_all()
        for i in items:
            if i["id"] == item_id:
                return SportsItem. from_dict(i)
        return None
    
    @staticmethod
    def find_by_category(category_id: int) -> list:
        """
        Obtém todos os artigos de uma categoria específica.
        
        Atalho para get_all(category_id=category_id).
        
        Args:
            category_id: ID da categoria
            
        Returns:
            list[SportsItem]: Lista de artigos da categoria
        """
        return SportsItem.get_all(category_id=category_id)
    
    @staticmethod
    def from_dict(data: dict) -> 'SportsItem':
        """
        Cria um objeto SportsItem a partir de um dicionário.
        
        Método factory utilizado na deserialização JSON.
        Usa valores por defeito para campos opcionais em falta.
        
        Args:
            data: Dicionário com os dados do artigo
            
        Returns:
            SportsItem: Nova instância de SportsItem
        """
        return SportsItem(
            id=data["id"],
            name=data["name"],
            brand=data["brand"],
            price_per_hour=data["price_per_hour"],
            category_id=data. get("category_id"),  # None se não existir
            available=data.get("available", True)  # True por defeito
        )
    
    @staticmethod
    def create(name: str, brand: str, price_per_hour: float,
               category_id: int = None) -> 'SportsItem':
        """
        Cria e guarda um novo artigo.
        
        Método factory que gera automaticamente o ID e persiste o artigo.
        O artigo é criado como disponível por defeito.
        
        Args:
            name: Nome do artigo
            brand:  Marca do artigo
            price_per_hour: Preço por hora em euros
            category_id: ID da categoria (opcional)
            
        Returns:
            SportsItem: Novo artigo criado e guardado
        """
        new_id = SportsItem.get_next_id()
        item = SportsItem(new_id, name, brand, price_per_hour, category_id, True)
        item.save()
        return item
    
    # ==================== REPRESENTAÇÃO ====================
    
    def __str__(self):
        """
        Representação em string do artigo.
        
        Formato: "Nome (Marca) - €Preço/hour - Estado"
        
        Returns:
            str:  Descrição formatada do artigo
        """
        status = "Available" if self._available else "Unavailable"
        return f"{self._name} ({self._brand}) - €{self._price_per_hour:.2f}/hour - {status}"