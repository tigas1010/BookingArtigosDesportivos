from models import Client, Administrator, Category, SportsItem, Reservation

class System:
    def __init__(self):
        self._users = []
        self._categories = []
        self._items = []
        self._reservations = []
        self._current_user = None
    
    # User Management
    def register_client(self, name, email, password, address, phone):
        if self._find_user_by_email(email):
            return None
        client = Client(name, email, password, address, phone)
        self._users.append(client)
        return client
    
    def register_admin(self, name, email, password, access_level=1):
        if self._find_user_by_email(email):
            return None
        admin = Administrator(name, email, password, access_level)
        self._users.append(admin)
        return admin
    
    def _find_user_by_email(self, email):
        for u in self._users:
            if u.email == email:
                return u
        return None
    
    def login(self, email, password):
        user = self._find_user_by_email(email)
        if user and user.login(email, password):
            self._current_user = user
            return user
        return None
    
    def logout(self):
        self._current_user = None
    
    @property
    def current_user(self):
        return self._current_user
    
    # Category and Item Management
    def create_category(self, name, description=""):
        category = Category(name, description)
        self._categories. append(category)
        return category
    
    def create_item(self, name, brand, price_per_hour, category=None):
        item = SportsItem(name, brand, price_per_hour, category)
        self._items. append(item)
        return item
    
    def remove_item(self, item):
        if item in self._items:
            self._items.remove(item)
            if item.category:
                item. category.remove_item(item)
            return True
        return False
    
    def list_categories(self):
        return self._categories
    
    def list_items(self, category=None, available_only=False):
        items = self._items
        if category:
            items = [i for i in items if i.category == category]
        if available_only:
            items = [i for i in items if i.available]
        return items
    
    # Reservation Management
    def create_reservation(self, client, start_date, end_date):
        reservation = Reservation(client, start_date, end_date)
        self._reservations.append(reservation)
        client.make_reservation(reservation)
        return reservation
    
    def list_reservations(self, client=None, state=None):
        reservations = self._reservations
        if client:
            reservations = [r for r in reservations if r.client == client]
        if state:
            reservations = [r for r in reservations if r.state == state]
        return reservations
    
    def get_reservation_by_id(self, reservation_id):
        for r in self._reservations:
            if r.id == reservation_id:
                return r
        return None