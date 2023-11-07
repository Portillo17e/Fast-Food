import datetime

class Invoice:
    """
    Class Invoice
    """

    def __init__(self, order:dict, customer) -> None:
        """
        Create a new Invoice object.

        order -> Dictionary containing order information

        customer -> Customer information 
        """
        #Tal vez un objeto cliente, almacenado en un diccionario
        #Mejor solo un diccionario?

        self.order_items:list = []
        #Order: number, nit, items {name, quant}, status
        #Order: number, nit, items {name, (quant, price)}, status
        self.total = 0
        #self.items = ""
        self.order = order
        self.customer_name = order["customer"]
        self.customer = customer

    def generate_detail(self):
        order = self.order
        for key in order["items"]:
            food = order['items'][key]
            quantity = food[0]
            price = food[1]
            subtotal = int(quantity) * float(price)
            # append("Quantity Item: price")
            self.order_items.append(f"{quantity} {key}: {subtotal}")
            self.total += subtotal
        return "\n\t" + "\n\t".join(self.order_items).title()

    
    def __str__(self) -> str:
        #items = '\t'+str(self.order_items).replace(',','\n\t').replace('\'',"").replace('[',"").replace(']',"")
        
        #items = "\n\t" + "\n\t".join(self.order_items).title()

        # Invocie Structure
        # Restaurant name
        # Date
        # Order number
        # Customer info
        # Detail
        # Discount
        # Total
        # No of orders for next discount

        detail = self.generate_detail()
        next_discount = 15 - self.customer.get_orders()
        discount_text = ""
        discount = 0
        if next_discount == 14:
            discount =  self.customer.use_discount()
        elif next_discount == 0:
            discount_text += f"Felicidades ha obtenido un descuento de {self.customer.get_discount()}% en su proxima compra"
        else:
            discount_text += f"{next_discount} compras restantes para el próximo descuento"
        discounted = self.total * (discount/100)
        total = self.total - discounted 
            
        return f"{'Nombre del restaurante'}\n{datetime.datetime.now().date()}\n{self.order['number']}\n{self.customer}\n{detail}\n\tDescuento de {discount}%: {discounted}\n\tTotal: {total}\n{discount_text}"
