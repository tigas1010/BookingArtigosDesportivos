class SportsItem:
    _id_counter = 0
    
    def __init__(self, name: str, brand: str, price_per_hour: float, category=None):
        SportsItem._id_counter += 1
        self._id = SportsItem._id_counter
        self._name = name
        self._brand = brand
        self._price_per_hour = price_per_hour
        self._available = True
        self._category = category
        
        if category:
            category.add_item(self)
    
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
    def category(self):
        return self._category
    
    def check_availability(self) -> bool:
        return self._available
    
    def set_available(self, available: bool):
        self._available = available
    
    def __str__(self):
        status = "Available" if self._available else "Unavailable"
        return f"{self._name} ({self._brand}) - €{self._price_per_hour:.2f}/hour - {status}"