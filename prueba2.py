import queue
from factura import Invoice
from Customer import Customer

#TODO Implementar la entrega de las ordenes

class Restaurante:

    def __init__(self):
        self.menu = {}
        self.stock = {}
        self.orders = queue.Queue()
        self.completed_orders = []
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

    # Estructura de la orden
    # number, nit, items {name: (quant, price)}, status 

    def take_order(self, nit, items):
        order_number = self.orders.queue[0]["number"] + 1 if not self.orders.empty() else 1
        order = {"number": order_number, "customer": nit, "items": items, "status": "pendiente"}
        self.orders.put(order)
        self.prepare_order(order)
        return order_number

    def prepare_order(self, order):
        order["status"] = "Listo para servir"
        for item in order["items"]:
            quantity = order["items"][item][0]
            self.stock[item] -= quantity

    def complete_order(self, order):
        order["status"] = "Listo para servir"

    def hand_order(self, order):
        order["status"] = "Entregada"
        self.completed_orders.append(order)

    def generate_invoice(self, order):
        invoice = Invoice(order, self.customers[order["customer"]])
        return invoice
        total_cost = sum(order["items"][item][1] * order["items"][item][0] for item in order["items"])
        return total_cost

    def register_customer(self, nit, customer):
        self.customers[nit] = customer


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

#region
def buscar_cliente(clientes, nit):
    for key in clientes:
        if nit == key:
            return nit
    return -1
#endregion


#funcion para crear pedidos
def add_orden(restaurante:Restaurante):
    while True:
        print("\n*** Menú ***")
        for item, price in restaurante.menu.items():
            print(f"{item}: ${price}")

        # customer_name = input("\nNombre del cliente: ")
        
        # TODO Buscar entre los clientes almacenados segun el nit
        customer_nit = input("\nNumero de Nit: ")
        if not customer_nit:
            customer_nit = "cf"
        
        #region busqueda secuencial
        if buscar_cliente(restaurante.customers, customer_nit) != -1:
            print(restaurante.customers[customer_nit])
        else:
            customer_name = input("Nombre del cliente: ")
            customer = Customer(nit=customer_nit, fname=customer_name)
            restaurante.register_customer(customer_nit, customer)
        #endregion

        #region Busqueda anterior por metodo 'if in dict'
        #if customer_nit in restaurante.customers:
        #    print(restaurante.customers[customer_nit])
        #elif not customer_nit:
        #    customer_nit = "cf"
        #else:
        #    customer_name = input("Nombre del cliente: ")
        #    customer = Customer(nit=customer_nit, fname=customer_name)
        #    restaurante.register_customer(customer_nit, customer)
        #endregion   

        items = {}
        while True:
            item_name = input("Nombre del producto (o 'fin' para finalizar el pedido): ").title()
            if item_name == 'Fin':
                break
            if item_name in restaurante.menu:
                quantity = int(input(f"Cantidad de {item_name}: "))
                if item_name in restaurante.stock and quantity <= restaurante.stock[item_name]:
                    price = restaurante.menu[item_name]
                    items[item_name] = (quantity, price)
                else:
                    print("Producto no disponible en la cantidad solicitada.")
            else:
                print("Producto no encontrado en el menú.")

        if items:
            number = restaurante.take_order(customer_nit, items)
            print(f"Pedido No.{number} registrado con éxito.")

        continuar = input("\n¿Desea tomar otro pedido? (Sí/No): ").lower()
        if continuar != 'sí' or continuar != 'si':
            break

    for order in restaurante.orders.queue:
        restaurante.prepare_order(order)
        print(f"Pedido {order['number']} para {restaurante.customers[order['customer']].get_name()} está {order['status']}.")

    for order in restaurante.orders.queue:
        invoice = restaurante.generate_invoice(order)
        print(f"Factura para {order['customer']}: ${invoice}")

#    for customer, info in restaurante.customers.items():
#        print(f"Información del cliente\n{info}")

#funcion principal del proyecto
def main():
   restaurante = Restaurante()

   restaurante.add_menu_item("Pizza", 12.99)
   restaurante.add_menu_item("Bebida", 2.99)
   restaurante.update_stock("Pizza", 10)
   restaurante.update_stock("Bebida", 20)
   restaurante.register_customer("cf", Customer())
   while True:
        action = input('Que desea realizar:'
                       +'\n1.Tomar pedido'
                       +'\n2.Preparar pedido'
                       +'\n3.Entregar pedido'
                       +'\n4.Procesos administrativos'
                       +'\n5.Salir\n') 
        match(action):
                case '1':
                    add_orden(restaurante)
                    print()
                case '2':
                    pass
                case '3':
                    pass
                case '4':
                    for _ in range(2):
                        user = input('Ingrese el nombre de usuario:\n')
                        password = input('Ingrese la contraseña de administrador:\n')

                        if user == 'admin' and password == 'admin123':
                            menu_admin(restaurante)
                            break
                case '5':
                    break


if __name__ == "__main__":
    main()
