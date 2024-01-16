class Split:
    def __init__(self, user, share):
        self.user = user
        self.share = share

class Balance:
    def __init__(self, debtor, creditor, amount):
        self.debter = debtor
        self.creditor = creditor
        self.amount = amount

class User:
    def __init__(self, id, name, mobile_number, email):
        self.id = id
        self.name = name
        self.mobile_number = mobile_number
        self.email = email
        self.balances = []
        self.notifications = []

    def add_balance(self, creditor, amount):
        balance = Balance(self, creditor, amount)
        self.balances.append(balance)
    
    def notify(self, message):
        self.notifications.append(message)

    def print_notifications(self):
        print(f"Notifications for User {self.id}:")
        for notification in self.notifications:
            print(f" - {notification}")  

class Group:
    def __init__(self, id, name, users):
        self.group_id = id
        self.name = name
        self.users = users
        self.expenses = []
    
    def add_expense(self, expense):
        self.expenses.append(expense)
        for user in expense.involved_users:
            user.notify(f"Expense '{expense.description} added in group '{self.name}'")
    
    def edit_expense(self, expense_id, new_description, new_amount, new_splits):
        for expense in self.expenses:
            if expense.id == expense_id:
                expense.description = new_description
                expense.amount = new_amount
                expense.split = new_splits
                expense.notify_users(f"Expense edited in group '{self.name}'" 
                                     f"New description: {new_description}, New Amount: {new_amount}")

    def delete_expense(self, expense_id):
        for expense in self.expenses:
            if expense.id == expense_id:
                self.expenses.remove(expense)
                expense.notify_users(f"Expense '{expense.description}' deleted in group '{self.name}' ")

    def settle_expenses(self):
        all_users = self.users
        for expense in self.expenses:
            for user in expense.involved_users:
                all_users.append(user)
        
        transactions = []
        for user in all_users:
            for balance in user.balances:
                transactions.append([balance.debtor, balance.creditor, balance.amount])

        simplify_debt = self.simplify(transactions)

        for user in all_users:
            user.balances = []
        
        for user in all_users:
            user.notify_users("All expense settles in the group")
        
    def print_notifications(self):
        print(f"Notification for Group {self.group_id} ({self.name}):")
        for expense in self.expenses:
            expense.notify_users("Expense settled in the group.")
    
    def simplify(self, transactions):
        map = {}
        for trans in transactions:
            map[trans[0]] = map.get(trans[0], 0) - trans[2]
            map[trans[1]] = map.get(trans[1], 0) + trans[2]
        
        balance = []
        for key, val in map.items():
            if val != 0:
                balance.append(val)
        
        def backtrack(ind):
    
            while ind < len(balance) and balance[ind] == 0:
                ind += 1
            
            if ind == len(balance):
                return 0
            
            res = float('inf')

            for i in range(ind+1, len(balance)):
                if balance[i] * balance[ind] < 0:
                    balance[i] += balance[ind]
                    res = min(res, 1 + backtrack(ind+1))
                    balance[i] -= balance[ind]
            
            return res

        return backtrack(0)

class Expense:
    def __init__(self, id, description, expense_type, amount, splits, created_by):
        self.id = id
        self.description = description
        self.expense_type = expense_type
        self.amount = amount
        self.splits = splits
        self.involved_users = [split.user for split in splits]
        self.created_by = created_by
        self.notifications = []

    def notify_users(self, message):
        for user in self.involved_users:
            user.notify(message)

    def settle_expense(self):
        if self.expense_type == 'EQUAL':
            self.settle_expense_equal()
        elif self.expense_type == 'UNEQUAL':
            self.settle_expense_unequal()
        elif self.expense_type == 'PERCENT':
            self.settle_expense_percent()
    
    def settle_expense_equal(self):
        split_amount = self.amount/len(self.involved_users)
        for split in self.splits:
            split.user.add_balance(self.created_by, split_amount)
    
    def settle_expense_unequal(self):
        split_amount = self.amount/len(self.involved_users)
        for split in self.splits:
            split.user.add_balance(self.created_by, split.share - split_amount)

    def settle_expense_percent(self):
        total_percent = sum(split.share for split in self.splits)
        if total_percent != 100:
            raise ValueError("Total percentage shares do not add upto 100")
        
        for split in self.splits:
            split_amount = (split.share/100) * self.amount
            split.user.add_balance(self.created_by, split_amount)

class Splitwise:
    def __init__(self):
        self.users = {}
        self.groups = {}
    
    def add_user(self, user_id, name, email, mobile_number):
        user = User(user_id, name, mobile_number, email)
        self.users[user_id] = user
    
    def add_group(self, group_id, name, users):
        group = Group(group_id, name, users)
        self.groups[group_id] = group
    
    def add_expense(self, user_id, group_id, expense_id, description, amount, expense_type, splits):
        user = self.users[user_id]
        group = self.groups[user_id]
        expense = Expense(expense_id, description, expense_type, amount, splits, user)
        group.add_expense(expense)
    
    def delete_expense(self, group_id, expense_id):
        group = self.groups[group_id]
        group.delete_expense(expense_id)
    
    def list_expense_with_friend(self, user_id, friend_id):
        user = self.users[user_id]
        friend = self.users[friend_id]
        expenses_with_friend = []
        for group in self.groups.values():
            for expense in group.expenses:
                if user in expense.involved_users and friend in expense.involved_users:
                    expenses_with_friend.append(expense)
        
        return expenses_with_friend
    
    def settle_expenses(self, user_id, group_id):
        group = self.groups[group_id]
        group.settle_expenses()

    def print_notifications(self):
        print("Priniting all notifications: ")
        for user in self.users.values():
            user.print_notifications()
        for group in self.groups.values():
            group.print_notifications()

splitwise = Splitwise()

user1 = User(1, "User1", "123456789", "user1@gmail.com")
user2 = User(2, 'User2', '987654321', 'user2@gmail.com')
user3 = User(3, 'User3', '123321123', 'user3@gmail.com')

splitwise.add_user(1, "User1", "123456789", "user1@gmail.com")
splitwise.add_user(2, 'User2', '987654321', 'user2@gmail.com')
splitwise.add_user(3, 'User3', '123321123', 'user3@gmail.com')

# create a group
splitwise.add_group(1, 'Friends', [splitwise.users[1], splitwise.users[2], splitwise.users[3]])

# add an expense to the group
splits = [Split(splitwise.users[1], 33.34), Split(splitwise.users[2], 33.34), Split(splitwise.users[3], 33.34)]

splitwise.add_expense(1, 1, 1, "Dinner", 100, "EQUAL", splits)

friend_expenses = splitwise.list_expense_with_friend(1, 2)
for expense in friend_expenses:
    print(f"Expense with User2: {expense.description} - {expense.amount}")

splitwise.settle_expenses(1, 1)
splitwise.print_notifications()

