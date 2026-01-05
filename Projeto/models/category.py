"""
Módulo de gestão de categorias de artigos desportivos.
Implementa persistência em ficheiro JSON.
"""

import json
import os


class Category:
    """
    Classe que representa uma categoria de artigos desportivos.
    
    Cada categoria possui um identificador único, nome e descrição opcional.
    Os dados são persistidos num ficheiro JSON.
    
    Attributes:
        DATA_FILE (str): Caminho para o ficheiro JSON de armazenamento
    """
    
    # Caminho do ficheiro JSON onde as categorias são guardadas
    DATA_FILE = "data/categories.json"
    
    def __init__(self, id: int, name: str, description: str = ""):
        """
        Inicializa uma nova categoria.
        
        Args:
            id:  Identificador único da categoria
            name: Nome da categoria (ex: "Futebol", "Natação")
            description: Descrição opcional da categoria
        """
        self._id = id
        self._name = name
        self._description = description
    
    # ==================== PROPRIEDADES ====================
    
    @property
    def id(self):
        """Retorna o identificador único da categoria."""
        return self._id
    
    @property
    def name(self):
        """Retorna o nome da categoria."""
        return self._name
    
    @property
    def description(self):
        """Retorna a descrição da categoria."""
        return self._description
    
    # ==================== SERIALIZAÇÃO ====================
    
    def to_dict(self) -> dict:
        """
        Converte a categoria para um dicionário. 
        
        Utilizado para serialização JSON.
        
        Returns:
            dict: Dicionário com os dados da categoria
        """
        return {
            "id": self._id,
            "name":  self._name,
            "description": self._description
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
        if not os.path. exists(Category. DATA_FILE):
            with open(Category.DATA_FILE, "w", encoding="utf-8") as f:
                json.dump([], f)
    
    @staticmethod
    def _load_all() -> list:
        """
        Carrega todas as categorias do ficheiro JSON. 
        
        Returns:
            list: Lista de dicionários com os dados das categorias
        """
        Category._ensure_file()
        with open(Category.DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    
    @staticmethod
    def _save_all(categories:  list):
        """
        Guarda todas as categorias no ficheiro JSON.
        
        Args:
            categories: Lista de dicionários com os dados das categorias
        """
        Category._ensure_file()
        with open(Category.DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(categories, f, indent=4, ensure_ascii=False)
    
    # ==================== OPERAÇÕES CRUD ====================
    
    def save(self):
        """
        Guarda ou atualiza esta categoria no ficheiro JSON.
        
        Se a categoria já existir (mesmo ID), atualiza os seus dados.
        Caso contrário, adiciona como nova categoria.
        """
        categories = Category._load_all()
        
        # Procurar categoria existente para atualizar
        for i, c in enumerate(categories):
            if c["id"] == self._id:
                categories[i] = self. to_dict()
                Category._save_all(categories)
                return
        
        # Se não existe, adicionar nova categoria
        categories.append(self.to_dict())
        Category._save_all(categories)
    
    def delete(self):
        """
        Remove esta categoria do ficheiro JSON. 
        
        Filtra a lista de categorias removendo a que tem o mesmo ID.
        """
        categories = Category._load_all()
        categories = [c for c in categories if c["id"] != self._id]
        Category._save_all(categories)
    
    # ==================== MÉTODOS ESTÁTICOS ====================
    
    @staticmethod
    def get_next_id() -> int:
        """
        Obtém o próximo ID disponível para uma nova categoria.
        
        Returns:
            int:  Próximo ID (máximo atual + 1, ou 1 se não existirem categorias)
        """
        categories = Category._load_all()
        if not categories: 
            return 1
        return max(c["id"] for c in categories) + 1
    
    @staticmethod
    def get_all() -> list:
        """
        Obtém todas as categorias como objetos Category.
        
        Returns:
            list[Category]: Lista de objetos Category
        """
        categories_data = Category._load_all()
        return [Category.from_dict(c) for c in categories_data]
    
    @staticmethod
    def find_by_id(category_id:  int):
        """
        Procura uma categoria pelo seu ID.
        
        Args:
            category_id: ID da categoria a procurar
            
        Returns: 
            Category:  Objeto Category se encontrado, None caso contrário
        """
        categories = Category._load_all()
        for c in categories:
            if c["id"] == category_id:
                return Category.from_dict(c)
        return None
    
    @staticmethod
    def from_dict(data: dict) -> 'Category':
        """
        Cria um objeto Category a partir de um dicionário.
        
        Método factory utilizado na deserialização JSON.
        
        Args:
            data: Dicionário com os dados da categoria
            
        Returns:
            Category: Nova instância de Category
        """
        return Category(
            id=data["id"],
            name=data["name"],
            description=data. get("description", "")
        )
    
    @staticmethod
    def create(name: str, description:  str = "") -> 'Category':
        """
        Cria e guarda uma nova categoria.
        
        Método factory que gera automaticamente o ID e persiste a categoria.
        
        Args:
            name: Nome da categoria
            description: Descrição opcional da categoria
            
        Returns: 
            Category: Nova categoria criada e guardada
        """
        new_id = Category.get_next_id()
        category = Category(new_id, name, description)
        category.save()
        return category
    
    # ==================== RELAÇÕES ====================
    
    def get_items(self):
        """
        Obtém todos os artigos que pertencem a esta categoria. 
        
        Estabelece a relação 1:N entre Category e SportsItem.
        
        Returns:
            list[SportsItem]: Lista de artigos desta categoria
        """
        from . sports_item import SportsItem
        return SportsItem.find_by_category(self._id)
    
    # ==================== REPRESENTAÇÃO ====================
    
    def __str__(self):
        """
        Representação em string da categoria.
        
        Returns:
            str: Nome da categoria
        """
        return f"{self._name}"