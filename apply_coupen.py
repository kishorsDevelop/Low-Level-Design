from abc import ABC, abstractmethod
class Product:
    def __init__(self, id, price, name, product_type):
        self.id = id
        self.price = price
        self.name = name
        self.product_type = product_type

class DiscountStrategy(ABC):
    @abstractmethod
    def apply_discount(self, product_price):
        pass
    
class NPercentOffStrategy(DiscountStrategy):
    def __init__(self, discount_percentage):
        self.discount_percentage = discount_percentage
    
    def apply_discount(self, product_price):
        return product_price * (1 - self.discount_percentage/100)
        
class PPercentOffNextItemStrategy(DiscountStrategy):
    def __init__(self, discount_percentage):
        self.discount_percentage = discount_percentage
        self.applied = False
    
    def apply_discount(self, product_price):
        if self.applied:
            return product_price
        self.applied = True
        return product_price * (1 - self.discount_percentage/100)

class DPercentOffNthItemOfTypeTStrategy(DiscountStrategy):
    def __init__(self, discount_percentage, condition_type, condition_count):
        self.discount_percentage = discount_percentage
        self.condition_type = condition_type
        self.condition_count = condition_count
        self.item_count = 0
    
    def apply_discount(self, product_price):
        if self.condition_type == 'Type2':
            self.item_count += 1
            if self.item_count == self.condition_count:
                self.item_count = 0
                return product_price * (1 - self.discount_percentage/100)
        return product_price

class Coupen:
    def __init__(self, discount_strategy):
        self.discount_strategy = discount_strategy

    def apply_coupen(self, product_price):
        return self.discount_strategy.apply_discount(product_price)

class Shopping_Cart:

    def __init__(self):
        self.coupens = []
        self.products = []

    def add_product(self, product):
        self.products.append(product)
    
    def add_coupen(self, coupen):
        self.coupens.append(coupen)

    def calculate_total(self):
        total_price = sum(product.price for product in self.products)
        for coupen in self.coupens:
            total_price = coupen.apply_coupen(total_price)
        return total_price


if __name__ == '__main__':

    product1 = Product(1, 20, 'A', 'Type1')
    product2 = Product(2, 30, 'B', 'Type2')

    n_percent_off_strategy = NPercentOffStrategy(10)
    p_percent_off_next_item_strategy = PPercentOffNextItemStrategy(5)
    d_percent_off_nth_item_of_type_t_strategy = DPercentOffNthItemOfTypeTStrategy(15, 'Type2', 2)

    coupen1 = Coupen(n_percent_off_strategy)
    coupen2 = Coupen(p_percent_off_next_item_strategy)
    coupen3 = Coupen(d_percent_off_nth_item_of_type_t_strategy)

    cart = Shopping_Cart()

    cart.add_product(product1)
    cart.add_product(product2)

    cart.add_coupen(coupen1)
    cart.add_coupen(coupen2)
    cart.add_coupen(coupen2)
    cart.add_coupen(coupen3)
    cart.add_coupen(coupen3)

    price = cart.calculate_total()

    print(price)
