from abc import ABC, abstractmethod
class ATMState(ABC):
    @abstractmethod
    def insert_card(self):
        pass

    @abstractmethod
    def insert_pin(self, pin):
        pass

    @abstractmethod
    def withdraw_cash(self, amount):
        pass

class HasNoCard(ATMState):
    def insert_card(self):
        print("Card is Inserted!")
        return HasCard()
    
    def insert_pin(self, pin):
        print("Please Insert Card First.")
    
    def withdraw_cash(self, amount):
        print("Please Insert Card First.")
    
class HasCard(ATMState):
    def insert_card(self):
        print("Card is Already Inserted!")
    
    def insert_pin(self, pin):
        if pin == '1234':
            print("Pin is Correct. Enter Amount to withdraw... ")
            return WithdrawCashState()
        else:
            print("Invalid Pin, Insert Correct Pin...")
            return HasCard()
    
    def withdraw_cash(self, amount):
        print("Please Insert Card First.")

class WithdrawCashState(ATMState):
    def insert_card(self):
        print("Card is Already Inserted!")
    
    def insert_pin(self, pin):
        print("Withdrawing Cash. Kindly wait...")
    
    def withdraw_cash(self, amount):
        if amount%500 != 0 and amount%200 != 0 and amount%100 != 0:
            print("Please Enter Valid amount...")
            return HasCard()
        remainder = amount
        withdraw_handlers = [FiveHundredDollars(), TwoHundredDollars(), OneHundredDollars()]
        for handler in withdraw_handlers:
            remainder = handler.process_request(remainder)
            if remainder == 0:
                break
        return HasNoCard()

class WithdrawHandler(ABC):
    @abstractmethod
    def process_request(self, amount):
        pass

class FiveHundredDollars(WithdrawHandler):
    def process_request(self, amount):
        if amount and amount >= 500:
            notes = amount//500
            print(f"Withdrawing {notes} Rs.500")
            remainder = amount%500
            if remainder > 0:
                return remainder

class TwoHundredDollars(WithdrawHandler):
    def process_request(self, amount):
        if amount and amount >= 200:
            notes = amount//200
            print(f"Withdrawing {notes} Rs.200")
            remainder = amount%200
            if remainder > 0:
                return remainder
        
class OneHundredDollars(WithdrawHandler):
    def process_request(self, amount):
        if amount and amount >= 100:
            notes = amount//100
            print(f"Withdrawing {notes} Rs.100")
            remainder = amount%100
            if remainder > 0:
                return remainder

class ATM:
    def __init__(self):
        self.state = HasNoCard()
    
    def set_state(self, state):
        self.state = state
    
    def insert_card(self):
        self.set_state(self.state.insert_card())
    
    def insert_pin(self, pin):
        self.set_state(self.state.insert_pin(pin))
    
    def withdraw_cash(self, amount):
        self.set_state(self.state.withdraw_cash(amount))

if __name__ == '__main__':
    atm = ATM()
    atm.insert_card()
    atm.insert_pin('1234')
    atm.withdraw_cash(5300)
