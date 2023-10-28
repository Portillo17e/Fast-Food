import queue
class Restaurante:
    def __init__(self):
        self.menu = {}
        self.stock = {}
        self.orders = []
        self.customers = {}

    def add_menu_item(self, item_name, price):
        self.menu[item_name] = price

    def update_price(self,item_name,new_price):
        self.menu[item_name] = new_price

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


#funcion para actualizar stock de platillos 
def update_stock(restaurant):
    try:
        product = input('Ingrese el nombre del producto: \n')
        new_stock = int(input('Ingrese cuanta cantidad desea agregar al stock acctual: \n'))
        if product in restaurant.stock:
            restaurant.update_stock(product, new_stock)
            print('Producto actualizado correctamente!')
    except ValueError:
        print('Se ingreso un tipo de valor incorrecto!')

#funcion para actualizar precios de platillos 
def update_price(restaurant):
    try:
        product = input('Ingrese el nombre del producto: \n')
        new_price = int(input('Ingrese el nuevo precio del producto: \n'))
        if product in restaurant.stock:
            restaurant.update_price(product, new_price)
            print('Producto actualizado correctamente!')
    except ValueError:
        print('Se ingreso un tipo de valor incorrecto!')


#funcion para agregar alimentos al menu
def add_menu(restaurant):
    try:
        product = input('Ingrese el nombre del producto: \n')
        price = int(input('Ingrese el nuevo precio del producto: \n'))
        if product in restaurant.stock:
            restaurant.add_menu_item(product, price)
            print('Producto agregado correctamente!')
    except ValueError:
        print('Se ingreso un tipo de valor incorrecto!')

#menu para el personal del restaurante
def menu_admin(restaurant):
    while True:
        #aqui se añaden las opciones de ver el estado de las ordenes
        print('Bienvenido al sistema del restaurante')
        action = input('Que desea realizar:\n1.Agregar alimentos al menu\n2.Actualizar stock de alimentos\n3.Actualizar precios de alimentos\n4.Salir\n') 

        match(action):
            case '1':
                add_menu(restaurant)
            case '2':
                update_stock(restaurant)
            case '3':
                update_price(restaurant)
            case '4':
                break
            case __:
                print('Ingreso una opcion fuera del reango!')



#funcion para crear pedidos
def add_orden(restaurante):
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

#funcion principal del proyecto
def main():
   restaurante = Restaurante()

   restaurante.add_menu_item("Pizza", 12.99)
   restaurante.add_menu_item("Bebida", 2.99)
   restaurante.update_stock("Pizza", 10)
   restaurante.update_stock("Bebida", 20)
   while True:
        action = input('Que desea realizar:\n1.Realizar pedido\n2.Procesos administrativos\n3.Salir\n') 
        match(action):
                case '1':
                    add_orden(restaurante)
                    print()
                case '2':
                    for _ in range(2):
                        user = input('Ingrese el nombre de usuario:\n')
                        password = input('Ingrese la contraseña de administrador:\n')

                        if user == 'admin' and password == 'admin123':
                            menu_admin(restaurante)
                            break
                case '3':
                    break


if __name__ == "__main__":
    main()
