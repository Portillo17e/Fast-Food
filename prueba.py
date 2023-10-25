class Restaurante:
    def __init__(self):
        self.menu = {}  # Menús y precios
        self.stock = {}  # Inventario de productos
        self.orders = []  # Lista de pedidos
        self.customers = {}  # Información de clientes

    def add_menu_item(self, item_name, price):
        self.menu[item_name] = price

    def update_stock(self, item_name, quantity):
        if item_name in self.stock:
            self.stock[item_name] += quantity
        else:
            self.stock[item_name] = quantity

    def take_order(self, customer_name, items):
        # Realizar validaciones antes de registrar el pedido
        if self.check_stock_availability(items):
            order = {"customer": customer_name, "items": items, "status": "pendiente"}
            self.orders.append(order)
        else:
            print("Algunos productos no están disponibles en la cantidad solicitada.")

    def process_order(self, order):
        # Procesar el pedido, actualizar el stock, cambiar el estado del pedido, etc.
        for item, quantity in order["items"].items():
            self.stock[item] -= quantity
        order["status"] = "listo para servir"

    def generate_invoice(self, order):
        total_cost = sum(self.menu[item] * quantity for item, quantity in order["items"].items())
        return total_cost

    def register_customer(self, customer_name, customer_info):
        self.customers[customer_name] = customer_info

    def check_stock_availability(self, items):
        for item, quantity in items.items():
            if item not in self.stock or self.stock[item] < quantity:
                return False
        return True

# Ejemplo de uso:
restaurante = Restaurante()

restaurante.add_menu_item("Pizza", 12.99)
restaurante.add_menu_item("Bebida", 2.99)

restaurante.update_stock("Pizza", 10)
restaurante.update_stock("Bebida", 20)

def tomar_pedido():
    customer_name = input("Nombre del cliente: ")
    items = {}
    while True:
        item_name = input("Nombre del producto (o 'fin' para finalizar el pedido): ")
        if item_name == 'fin':
            break
        if item_name in restaurante.menu:
            quantity = int(input("Cantidad: "))
            items[item_name] = quantity
        else:
            print("Producto no encontrado en el menú.")
    if items:
        restaurante.take_order(customer_name, items)
        print("Pedido registrado con éxito.")

while True:
    tomar_pedido()
    continuar = input("¿Desea tomar otro pedido? (Sí/No): ").lower()
    if continuar != 'sí':
        break

for order in restaurante.orders:
    restaurante.process_order(order)
    invoice = restaurante.generate_invoice(order)
    print(f"Factura para {order['customer']}: ${invoice}")

print("Inventario actual:")
for item, quantity in restaurante.stock.items():
    print(f"{item}: {quantity}")

# Registrar información del cliente
customer_name = input("Nombre del cliente para registrar: ")
customer_info = input("Información del cliente: ")
restaurante.register_customer(customer_name, customer_info)

print("Clientes registrados:")
for customer, info in restaurante.customers.items():
    print(f"{customer}: {info}")
