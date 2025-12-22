class Category: 
    _id_counter = 0
    
    def __init__(self, name: str, description: str = ""):
        Category._id_counter += 1
        self._id = Category._id_counter
        self._name = name
        self._description = description
        self._items = []
    
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def description(self):
        return self._description
    
    @property
    def items(self):
        return self._items
    
    def add_item(self, item):
        self._items.append(item)
        item._category = self
    
    def remove_item(self, item):
        if item in self._items:
            self._items.remove(item)
            item._category = None
    
    def __str__(self):
        return f"{self._name}"