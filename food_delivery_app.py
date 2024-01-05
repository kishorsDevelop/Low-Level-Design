"""
Requirements:-
A food delivery system requires the interaction of the restaurants, customers and delivery boys with the admin.
Restaurants can register themselves.
Users can create, update, delete, get their profiles.
User can search for the restaurant using a restaurant name, city name.
Restaurants can add, update the food menu.
User can see the food menu. User can get the food items based on Meal type or Cuisine type.
User can add/remove items to/from the cart. User can get all the items of the cart.
User can place or cancel the order. User can get all the orders ordered by him/her.
User can apply the coupons. User can get the detailed bill containing tax details.
User can make a payment using different modes of payment — credit card, wallet, etc.
Delivery boy can get all the deliveries made by him using his Id.
User can get the order status anytime. Success, Out for Delivery, Delivered, etc.
"""
from enum import Enum

class OrderStatus(Enum):
    SUCCESS = 'Success'
    OUT_FOR_DELIVERY = 'Out for Delivery'
    DELIVERED = 'Delivered'

class PaymentMethod(Enum):
    CREDIT_CARD = 'Credit Card'
    WALLET = 'Wallet'
    UPI = 'UPI'

class City:
    def __init__(self, name):
        self.name = name
        self.restaurants = {}
    
    def add_restaurant(self, restaurant):
        self.restaurants[restaurant.name] = restaurant
    
    def get_restaurant(self, restaurant_name):
        return self.restaurants.get(restaurant_name, None)

class Restaurant:
    def __init__(self, name):
        self.name = name
        self.orders = []
        self.food_menu = []
    
    def add_orders(self, order):
        self.orders.append(order)
    
    def register(self, city):
        city.add_restaurant(self)
        print(f"Restaurant {self.name} is successfully registered in {city.name} city!")
    
    def add_food_item_in_menu(self, food_item):
        self.food_menu.append(food_item)
    
    def update_food_menu(self, updated_menu):
        self.food_menu = updated_menu
        print(f"Food menu for {self.name} in {self.city} updated successfully.")

class Order:
    def __init__(self, id, status, food_items):
        self.id = id
        self.status = status
        self.food_items = food_items

class Food_Item:
    def __init__(self, name, price, cuisine_type, meal_type):
        self.name = name
        self.price = price
        self.cuisine_type = cuisine_type
        self.meal_type = meal_type

class Profile:
    def __init__(self, name, email, password, phone_no):
        self.name = name
        self.email = email
        self.password = password
        self.phone_no = phone_no

class Payment:
    def __init__(self, amount, payment_mode):
        self.amount = amount
        self.payment_mode = payment_mode

class User:
    def __init__(self, name):
        self.name = name
        self.cart = []
        self.orders = []
    
    def create_profile(self, new_profile):
        self.profile = new_profile
        print("Profile Created Successfully")
    
    def update_profile(self, updated_profile):
        if updated_profile:
            self.profile = updated_profile
            print("Profile Updated Successfully")
        else:
            print("No Updates Available")
    
    def delete_profile(self):
        self.profile = None
        print("Profile Deleted Successfully")
    
    def get_profile(self):
        if self.profile:
            print("User Profile:")
            print(f"{self.profile.name}, {self.profile.email}, {self.profile.phone_no}")
        else:
            print("No profile available")

    def search_restaurant(self, name, city):
        restaurant = city.get_restaurant(name)
        return restaurant
    
    def view_food_menu(self, restaurant):
        print(f"Food Menu of {restaurant.name} in {restaurant.city.name}:")
        print("Food Name\tPrice\tCuisineType\tMeal Type")
        for food_item in restaurant.food_menu:
            print(f"{food_item.name}\t\t{food_item.price}\t{food_item.cuisine_type}\t{food_item.meal_type}")

    def add_to_cart(self, food_item):
        self.cart.append(food_item)
        print(f"{food_item.name} added to the cart.")
    
    def remove_from_cart(self, food_item):
        if food_item not in self.cart:
            print(f"{food_item} is not in the cart.")
        else:
            self.cart.remove(food_item)
            print(f"{food_item} removed from the cart.")
    
    def place_order(self, restaurant):
        if not self.cart:
            print("Cart is empty. Add items to the Cart before placing an order.")
            return
        order_id = len(self.orders) + 1
        order = Order(order_id, OrderStatus.SUCCESS, self.cart)
        print(f"Order: {order_id} is placed Successfully!")
        restaurant.add_orders(order)
        self.orders.append(order)
        self.cart = []
        return order
    
    def cancel_order(self, order):
        for orders in self.orders:
            if orders.id == order.id and orders.status == OrderStatus.SUCCESS:
                print(f"Order {order.id} is Cancelled Successfully!")
                self.orders.remove(order)
            else:
                print(f"Cannot Cancel Order {order.id}. Order is already in progress!")
                return
        print(f"Order {order.id} is not found.")

    def get_all_orders(self):
        if not self.orders:
            print("No orders Found.")
            return
        
        for order in self.orders:
            print("All Orders: ")
            print(order.id, ", ", order.status)
            print("Food Name\tPrice\tCuisineType\tMeal Type")
            for item in order.food_items:
                print(f"{item.name}\t\t{item.price}\t{item.cuisine_type}\t{item.meal_type}")
    
    def apply_coupens(self, total_amount, coupen):
        return total_amount - (coupen.discount/100) * total_amount

    def make_payment(self, payment_mode, coupen):
        if not self.orders:
            print("No orders to make Payment for.")
            return
        total_amount = 0
        for order in self.orders:
            for food_item in order.food_items:
                total_amount += food_item.price
        if coupen:
            total_amount = self.apply_coupens(total_amount, coupen)
        payment = Payment(total_amount, payment_mode)
        print(f"Payment of {total_amount} made using {payment_mode}")

class Coupen:
    def __init__(self, code):
        self.discount = code

class Delivery_Boy:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.deliveries = []
    
    def add_delivery(self, order):
        print(f"{self.name} got Delivery with Order id {order.id}!")
        self.deliveries.append(order)

    def view_deliveries(self):
        print(f"All Deliveries of {self.name} : ")
        for delivery in self.deliveries:
            print(f"Order_id: {delivery.id}, Status: {delivery.status}")


if __name__ == '__main__':
    
    food_item1 = Food_Item("Burger", 50, "American", "Lunch")
    food_item2 = Food_Item("Pizza", 98, "Italian", "Dinner")
    
    city = City("Akshardham")
    restaurant = Restaurant("Haldiram")
    restaurant.register(city) # Add restaurant in city
    restaurant.add_food_item_in_menu(food_item1)
    restaurant.add_food_item_in_menu(food_item2)

    profile = Profile('ABC', 'abc@gmail.com', 'abc@123', '+91-9999888811')

    user = User("ABC")
    user.create_profile(profile)
    user.get_profile()
    found_restaurant = user.search_restaurant("Haldiram", city)
    if not found_restaurant:
        print("Restaurant not found.")

    user.add_to_cart(food_item1)
    order = user.place_order(found_restaurant)
    coupen = Coupen(10)
    user.make_payment(PaymentMethod.CREDIT_CARD, coupen)

    delivery_boy = Delivery_Boy(1, "Swiggy")
    delivery_boy.add_delivery(order)
    delivery_boy.view_deliveries()

    user.get_all_orders()
    

    
