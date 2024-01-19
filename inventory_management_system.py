from datetime import datetime
from random import random
class User:
    def __init__(self, id, name, email, mobile_number):
        self.user_id = id
        self.name = name
        self.email = email
        self.cart = Cart(id)
        self.mobile_number = mobile_number

    def add_to_cart(self, product):
        self.cart.add_product(product)
    
    def remove_from_cart(self, product):
        self.cart.remove_product(product)
    
    def view_cart(self):
        self.cart.view_cart()
    
    def place_order(self):
        order = Order(self.user_id, self.cart.products)
        order.generate_invoice()
        print("Order placed successfully.")
        self.cart.clear_cart()

class Product:
    def __init__(self, id, name, description, price, quanity_available):
        self.product_id = id
        self.name = name
        self.description = description
        self.price = price
        self.quanity_available = quanity_available
    
    def update_details(self, new_description, new_price, new_quantity):
        self.description = new_description
        self.price = new_price
        self.quanity_available = new_quantity
    
    def restock(self, quantity):
        self.quanity_available += quantity
        print(f"Product {self.name} restocked. New quantity: {self.quanity_available}")
    
    def reduce_stock(self, quantity):
        if self.quanity_available >= quantity:
            self.quanity_available -= quantity
            print(f"Stock Reduced for Product {self.name}. New quantity: {self.quanity_available}.")
        else:
           print(f"Insufficient stock for product {self.name}.") 
    
class Order:
    def __init__(self, user_id, products):
        self.order_id = random()
        self.user_id = user_id
        self.order_status = 'Processing'
        self.order_date = datetime.now()
        self.products = products
        self.total_amount = sum(product.price for product in products)
    
    def update_status(self, new_status):
        self.order_status = new_status
        print(f"Order {self.order_id} status updated to {self.status}.")

    
    def cancel_order(self):
        self.update_status("Cancelled")
        print(f"Order {self.order_id} cancelled.")

    def generate_invoice(self):
        invoice = Invoice(self.user_id, self.order_id, self.products)
        invoice.generate_invoice()

class Cart:
    def __init__(self, user_id):
        self.user_id = user_id
        self.products = []
        self.total_amount = 0

    def add_product(self, product):
        self.products.append(product)
        print(f"Product {product.name} added to the cart for User: {self.user_id}")
    
    def remove_product(self, product):
        if product in self.products:
           self.products.remove(product)
           print(f"Product {product.name} removed from the Cart for User: {self.user_id}.")
        else:
           print(f"Product {product.name} not found in the Cart for User: {self.user_id}.")

    def calculate_total(self):
        self.total_amount = sum(product.price for product in self.products)
        return self.total_amount
    
    def view_cart(self):
        print(f"Cart for User {self.user_id}:")
        for product in self.products:
            print(f"{product.name} - Rs.{product.price}")
        print(f"Total Amount: RS.{self.calculate_total()}")
    
    def clear_cart(self):
        self.products = []
        self.total_amount = 0
        print("Cart cleared")

class Payment:
    def __init__(self, id, user_id, order_id, amount, payment_method):
        self.payment_id = id
        self.user_id = user_id
        self.order_id = order_id
        self.payment_date = datetime.now()
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = "Pending"
    
    def process_payment(self):
        self.payment_status = "Success"
        print(f"Payment {self.payment_id} processed successfully.")

class Invoice:
    def __init__(self, user_id, order_id, products):
        self.invoice_id = random()
        self.user_id = user_id
        self.order_id = order_id
        self.products = products
        self.invoice_date = datetime.now()
        self.total_amount = sum(product.price for product in products)
        self.payment_status = "Success"
    
    def generate_invoice(self):
        print(f"Invoice generated for Order: {self.order_id} for User: {self.user_id}")

class Inventory:
    def __init__(self, product_id, quanity_available, minimum_threshold):
        self.product_id = product_id
        self.quanity_available = quanity_available
        self.minimum_threshold = minimum_threshold
    
    def update_quantity(self, new_quantity):
        self.quanity_available = new_quantity
        print(f"Quantity updated for product {self.product_id}. New quantity: {self.quanity_available}.")
    
    def check_availability(self, required_quantity):
        return self.quanity_available >= required_quantity

class Warehouse:
    def __init__(self, id, location):
        self.warehouse_id = id
        self.location = location
        self.inventory = []
    
    def addProductToWarehouse(self, product, quantity):
        found_inventory = next((inventory for inventory in self.inventory if inventory.product_id == product.product_id), None)
        if found_inventory:
            found_inventory.update_quantity(found_inventory.quanity_available+quantity)
        else:
           new_inventory = Inventory(product.product_id, quantity, 10)
           self.inventory.append(new_inventory)
        print(f"Product {product.name} added to Warehouse {self.warehouse_id}")

    def removeProductFromWarehouse(self, product, quantity):
        found_inventory = next((inventory for inventory in self.inventory if inventory.product_id == product.product_id), None)
        if found_inventory:
            if found_inventory.check_availability(quantity):
               found_inventory.update_quantity(found_inventory.quanity_available - quantity)   
               print(f"Product {product.name} removed from the warehouse {self.warehouse_id}.") 
            else:
               print(f"Insufficient stock in Warehouse {self.warehouse_id} for product {product.name}")
        else:
            print(f"Product {product.name} is not found in Warehouse {self.warehouse_id}")

    def transferProduct(self, product, quantity, destination_warehouse):
        self.removeProductFromWarehouse(product, quantity)
        destination_warehouse.addProductToWarehouse(product, quantity)
        print(f"Product {Product.name} transferred from Warehouse {self.warehouse_id} to Warehouse {destination_warehouse.warehouse_id}.")


if __name__ == '__main__':

    user1 = User(1, "John Doe", "abc@gmail.com", "7011210011")

    pendrive = Product(1, 'sandisk', "Pendrive 256 GB", 500, 5)
    laptop = Product(1, "Macbook", "Mac Notebook", 90000, 5)

    warehouse1 = Warehouse(1, "New Delhi")
    warehouse2 = Warehouse(2, "Kanpur")

    warehouse1.addProductToWarehouse(pendrive, 50)
    warehouse2.addProductToWarehouse(laptop, 200)

    user1.add_to_cart(pendrive)
    user1.add_to_cart(laptop)
    user1.view_cart()
    user1.place_order()



