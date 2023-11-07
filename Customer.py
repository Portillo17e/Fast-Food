import random

class Customer:
    def __init__(self, dpi = "NA", fname = "Consumidor final", nit = "cf") -> None:
        #self._dpi = dpi
        self._name = fname
        self._nit = nit
        self._orders = 0
        self._discount = 0

    def add_order(self):
        self.orders += 1
        # Cada 15 ordenes se le dará un descuento aleatorio entre 20% y 30% 
        if self.orders % 15 == 0 and self._nit != "cf":
            self.discount = random.randint(20, 30)

    def get_orders(self):
        return self._orders
    
    def get_name(self):
        return self._name
    def set_name(self, name):
        self._name = name
    
    # def get_dpi(self):
    #     return self._dpi
    # def set_dpi(self, dpi):
    #     self._dpi = dpi
    
    def get_nit(self):
        return self._nit
    def set_nit(self, nit):
        self._nit = nit
    
    def get_discount(self):
        return self.discount
    def use_discount(self):
        discount = self.discount
        self.discount = 0
        return discount
    
    def __str__(self) -> str:
        return f"Nit: {self._nit}\nNombre: {self._name}"