from datetime import datetime

class Reservation:
    _id_counter = 100
    
    STATES = ["Pending", "Confirmed", "Cancelled", "Completed"]
    
    def __init__(self, client, start_date: datetime, end_date: datetime):
        Reservation._id_counter += 1
        self._id = Reservation._id_counter
        self._client = client
        self._start_date = start_date
        self._end_date = end_date
        self._items = []
        self._total_value = 0.0
        self._state = "Pending"
    
    @property
    def id(self):
        return self._id
    
    @property
    def client(self):
        return self._client
    
    @property
    def start_date(self):
        return self._start_date
    
    @property
    def end_date(self):
        return self._end_date
    
    @property
    def items(self):
        return self._items
    
    @property
    def total_value(self):
        return self._total_value
    
    @property
    def state(self):
        return self._state
    
    def add_item(self, item):
        if item.check_availability():
            self._items.append(item)
            item.set_available(False)
            self.calculate_total()
            return True
        return False
    
    def remove_item(self, item):
        if item in self._items:
            self._items.remove(item)
            item.set_available(True)
            self.calculate_total()
    
    def calculate_total(self):
        hours = (self._end_date - self._start_date).total_seconds() / 3600
        self._total_value = sum(item.price_per_hour * hours for item in self._items)
        return self._total_value
    
    def confirm(self):
        if self._state == "Pending" and len(self._items) > 0:
            self._state = "Confirmed"
            return True
        return False
    
    def cancel(self):
        if self._state in ["Pending", "Confirmed"]:
            self._state = "Cancelled"
            for item in self._items:
                item.set_available(True)
            return True
        return False
    
    def complete(self):
        if self._state == "Confirmed":
            self._state = "Completed"
            for item in self._items:
                item.set_available(True)
            return True
        return False
    
    def __str__(self):
        items_str = ", ".join([i.name for i in self._items])
        return (f"Reservation #{self._id} | {self._state}\n"
                f"Period: {self._start_date.strftime('%Y-%m-%d %H:%M')} - "
                f"{self._end_date.strftime('%Y-%m-%d %H:%M')}\n"
                f"Items: {items_str}\n"
                f"Total: €{self._total_value:.2f}")