from abc import ABC, abstractmethod
class Balance:
    def __init__(self, debtor, creditor, amount):
        self.debtor = debtor
        self.creditor = creditor
        self.amount = amount

class Split:
    def __init__(self, user, share):
        self.user = user
        self.share = share

class User:
    def __init__(self, id, name, mobile_number, email):
        self.user_id = id
        self.name = name
        self.mobile_number = mobile_number
        self.email = email
        self.balances = []
    
    def add_balance(self, creditor, amount):
        balance = Balance(self, creditor, amount)
        self.balances.append(balance)

class ExpenseType(ABC):
    @abstractmethod
    def settle_expense(self, expense):
        pass

class EqualExpense(ExpenseType):
    def settle_expense(self, expense):
        split_amount = expense.amount/len(expense.involved_users)
        for split in expense.splits:
            split.user.add_balance(expense.created_by, split_amount)

class ExactExpense(ExpenseType):
    def settle_expense(self, expense):
        split_amount = expense.amount/len(expense.involved_users)
        for split in expense.splits:
            split.user.add_balance(expense.created_by, split.share - split_amount)

class PercentExpense(ExpenseType):
    def settle_expense(self, expense):
        total_share = sum(split.share for split in expense.splits)
        if total_share != 100:
            raise ValueError("Total percentage shares do not add upto 100")
        
        for split in expense.splits:
            split.user.add_balance(expense.created_by, (split.share/100) * expense.amount)

class Expense:
    def __init__(self, id, description, expense_type, amount, created_by, splits):
        self.expense_id = id
        self.description = description
        self.expense_type = self._settle_expenses(expense_type)
        self.amount = amount
        self.involved_users = [split.user for split in splits]
        self.created_by = created_by
        self.splits = splits
    
    def _settle_expenses(self, expense_type):
        if expense_type == 'EQUAL':
           return EqualExpense()   
        elif expense_type == 'UNEQUAL':
           return ExactExpense()
        elif expense_type == 'PERCENT':
           return PercentExpense()
    
    def settle_expense(self):
        self.expense_type.settle_expense(self)

class Group:
      def __init__(self, id, name, users):
          self.group_id = id
          self.name = name
          self.expenses = []
          self.users = users
        
      def add_expense(self, expense):
          self.expenses.append(expense)
        
      def edit_expense(self, id, new_description, new_amount, new_splits):
          for expense in self.expenses:
              if expense.id == id:
                  expense.description = new_description
                  expense.amount = new_amount
                  expense.splits = new_splits
                  break
      
      def delete_expense(self, id):
          for expense in self.expenses:
              if expense.id == id:
                  self.expenses.remove(expense)
                  break
      
      def settle_expense(self):
          all_users = self.users
          for expense in self.expenses:
              for user in expense.involved_users:
                  all_users.append(user)

          transactions = []
          for user in all_users:
              for balance in user.balances:
                  debtor = balance.debtor
                  creditor = balance.creditor
                  amount = balance.amount
                  transactions.append([debtor, creditor, amount])
          
          min_result = self.simplify(transactions)
          for user in all_users:
              user.balances = []

          return min_result
        
      def simplify(self, transactions):
          map = {}
          for debtor, creditor, amount in transactions:
              map[debtor] = map.get(debtor, 0) - map[amount]
              map[creditor] = map.get(creditor, 0) + map[amount]

          balance = []
          for amount in map.values():
              if amount != 0:
                 balance.append(amount)

          return self.dfs(balance, 0)

      def dfs(self, balance, ind):
          
          if balance[ind] == 0:
              return 0

          while ind < len(balance) and balance[ind] == 0:
              ind += 1
          
          res = float('inf')
          for i in range(ind+1, len(balance)):
              if balance[i] * balance[ind] < 0:
                  balance[i] += balance[ind]
                  res = min(res, 1 + self.dfs(balance, ind+1))
                  balance[i] -= balance[ind]
        
          return res

    
class Splitwise:
    def __init__(self):
        self.users = {}
        self.groups = {}
    
    def add_user(self, id, user):
        self.users[id] = user
    
    def add_group(self, id, group):
        self.groups[id] = group
    
    def add_expense(self, user_id, group_id, expense_id, description, expense_type, amount, splits):
        user = self.users[user_id]
        group = self.groups[group_id]
        expense = Expense(expense_id, description, expense_type, amount, user, splits)
        group.add_expense(expense)

        for split in splits:
            if split.user != user:
                user.add_balance(split.user, split.share - amount/len(expense.involved_users))

    def edit_expense(self, group_id, expense_id, new_description, new_amount, new_splits):
        group = self.groups[group_id]
        group.edit_expense(expense_id, new_description, new_amount, new_splits)
    
    def delete_expense(self, group_id, expense_id):
        group = self.groups[group_id]
        group.delete_expense(expense_id)
    
    def settle_expense(self, group_id):
        group = self.groups[group_id]
        group.settle_expenses()
    
    def list_expense_with_friend(self, user_id, friend_id):
        user = self.users[user_id]
        friend = self.users[friend_id]
        expenses_with_friend = []
        for group in self.group.values():
            for expense in group.expenses:
                if user in expense.involved_users and friend in expense.involved_users:
                    expenses_with_friend.append(expense)
        return expenses_with_friend


if __name__ == '__main__':
    user1 = User(1, 'User1', 123456789, 'user1@gmail.com')
    user2 = User(1, 'User2', 123455432, 'user2@gmail.com')
    user3 = User(1, 'User3', 123455342, 'user3@gmail.com')

    splitwise = Splitwise()
    splitwise.add_user(1, user1)
    splitwise.add_user(2, user2)
    splitwise.add_user(3, user3)

    splits = [Split(splitwise.users[1], 30.34), Split(splitwise.users[2], 30.34), Split(splitwise.users[3], 30.34)]

    group1 = Group(1, 'Friends', [splitwise.users[1], splitwise.users[2], splitwise.users[3]])
    
    splitwise.add_group(1, group1)

    splitwise.add_expense(1, 1, 1, 'Dinner', 'EQUAL', 100, splits)
    
    equal_splits = [Split(splitwise.users[1], 30.34), Split(splitwise.users[2], 30.34), Split(splitwise.users[3], 30.34)]

    equal_expense = Expense(1, "Dinner", "EQUAL", 100, user1, equal_splits)

    equal_expense.settle_expense()
