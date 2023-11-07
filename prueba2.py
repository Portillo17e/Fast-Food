from collections import deque

class Restaurante:
    def __init__(self):
        self.menu = {}
        self.stock = {}
        self.orders = deque ()
        self.customers = deque ()

    def add_menu_item(self, item_name, price):
        self.menu[item_name] = price

    def update_stock(self, item_name, quantity):
        if item_name in self.stock:
            self.stock[item_name] += quantity
        else:
            self.stock[item_name] = quantity

    def take_order(self, customer_name, items):
        order = {"customer": customer_name, "items": items, "status": "pendiente"}
        self.orders.append(order)

    def prepare_order(self, order):
        order["status"] = "en preparación"
        for item, quantity in order["items"].items():
            self.stock[item] -= quantity

    def complete_order(self, order):
        order["status"] = "listo para servir"

    def generate_invoice(self, order):
        total_cost = sum(self.menu[item] * quantity for item, quantity in order["items"].items())
        return total_cost

    def register_customer(self, customer_name, customer_info):
        self.customers[customer_name] = customer_info

def main():
    restaurante = Restaurante()

    restaurante.add_menu_item("Pizza", 12.99)
    restaurante.add_menu_item("Bebida", 2.99)
    restaurante.update_stock("Pizza", 10)
    restaurante.update_stock("Bebida", 20)

    while True:
        print("\n*** Menú ***")
        for item, price in restaurante.menu.items():
            print(f"{item}: ${price}")

        customer_name = input("\nNombre del cliente: ")

        items = {}
        while True:
            item_name = input("Nombre del producto (o 'fin' para finalizar el pedido): ")
            if item_name == 'fin':
                break
            if item_name in restaurante.menu:
                quantity = int(input(f"Cantidad de {item_name}: "))
                if item_name in restaurante.stock and quantity <= restaurante.stock[item_name]:
                    items[item_name] = quantity
                else:
                    print("Producto no disponible en la cantidad solicitada.")
            else:
                print("Producto no encontrado en el menú.")

        if items:
            restaurante.take_order(customer_name, items)
            print("Pedido registrado con éxito.")

        continuar = input("\n¿Desea tomar otro pedido? (Sí/No): ").lower()
        if continuar != 'sí':
            break

    for order in restaurante.orders:
        restaurante.prepare_order(order)
        print(f"Pedido para {order['customer']} está {order['status']}.")

    for order in restaurante.orders:
        invoice = restaurante.generate_invoice(order)
        print(f"Factura para {order['customer']}: ${invoice}")

    for customer, info in restaurante.customers.items():
        print(f"Información del cliente {customer}: {info}")

if __name__ == "__main__":
    main()
