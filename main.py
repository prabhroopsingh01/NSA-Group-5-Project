"""
    Group project

    Emon, Manpreet, Prabhroop, Tehillah

    Pupose: Tracking peoples budget
"""
from datetime import datetime
import json



"""
  main function
  this function is main function of the program that calls every other function
"""
def main():
    is_running = True

    data_api = DataApi()

    data_api.fetch_data()

    categories = ["Food","Transportation","Entertainment","Bills","Other"]

    
    while is_running:
        try:
            # Displays menu
            display_menu()

            menu_choice_input = input("Select an option:")

            # checks value of menu choice and returns valid integer
            menu_choice = validate_menu_choice(menu_choice_input)

            if menu_choice == 1:
                print("\n\n\n=== Add Income ===")
                new_income = add_income()
                data_api.add_income(new_income)
                new_balance = get_current_balance(data_api.incomes, data_api.transactions)
                setattr(data_api, "current_balance",new_balance)
                print("\nIncome added successfully!\n")
                print(f"Current balance: ${new_balance}\n\n")
            elif menu_choice == 2:
                print("\n\n\n=== Add Expense ===")
                print("Select category:\n1. Food\n2. Transportation\n3. Entertainment\n4. Bills\n5. Other\n\n")
                new_expense = add_expense()
                data_api.add_transaction(new_expense)

                # update balance
                new_balance = get_current_balance(data_api.incomes, data_api.transactions)
                setattr(data_api, "current_balance",new_balance)

                # if budget targets have not been set, we save the data and make user set budget
                if len(data_api.targets) == 0:
                    raise Exception("We have saved your transaction but please Set your budget in Main menu.")
                
                remaining_budget = get_remaining_budget(new_expense.category,data_api.targets,data_api.transactions)
                print(f"Remaining {categories[new_expense.category - 1]} Budget:{remaining_budget}\n")
            elif menu_choice == 3:
                print("\n\n\n=== View Transactions ===")
                view_transactions(data_api.incomes,data_api.transactions)
            elif menu_choice == 4:
                print("\n\n\n=== Set Budget ===")
                budget_targets = set_budget()
                setattr(data_api,"targets",budget_targets)
            elif menu_choice == 5:
                # check if user has set budget
                if len(data_api.targets) == 0:
                    raise Exception("\nTo view this option menu option, you need to set your budget first.")
                
                print("\n\n\n=== Budget Summary ===")
                view_budget_summary(data_api.incomes,data_api.transactions,categories, data_api.targets, data_api.current_balance)
            elif menu_choice == 6:
                # check if user has set a budget
                if len(data_api.targets) == 0:
                    raise Exception("\nTo view this option menu option, you need to set your budget first.")
                
                print("\n\n\n=== Monthly Report ===")
                generate_report(data_api.incomes,data_api.transactions,categories, data_api.targets)
            elif menu_choice == 7:
                is_running = False
            else:
                print("Invalid input")

            if is_running:
                input("Press enter to continue")
                print("\n\n")
            else:
                data_api.save_data()
        except ValueError as e:
            print(f"{e}\n")
            input("Press enter to continue")
            print("\n===Restarting Program===\n\n")
        except Exception as e:
            print(f"{e}\n")
            input("Press enter to continue")
            print("\n===Restarting Program===\n\n")
    print("Thank you for using this program.")





"""
   display_menu
   prints out main menu
"""
def display_menu():
    print("Personal Budget Tracker\n1. Add Income\n2. Add Expense\n3. View All Transactions\n4. Set Budget\n5. View Budget Summary\n6. Generate Report\n7. Save and Exit\n")




"""
    validate_menu_choice
    makes sure user menu choice is validated
    returns an valid menu choice
    Manpreet wrote this function
"""
def validate_menu_choice(menu_choice):
    try:
        # casts menu choice from string to int
        result = int(menu_choice)

        # Checks if user picked a valid menu option
        if result < 1 or result > 7:

            #  Throws error if menu choice is not valid
            raise ValueError("Menu choice must be between 1 and 7.")

         # returns valid menu choice back to main function
        return result

    except ValueError as e:
         # prints out thwon error
         print(e)

         # throws error nack to main function
         raise ValueError("Invalid input! Please enter a number between 1 and 7.")



"""
    add_expense
    gets user input for expense and returns an expense dict
    returns an expense as a transaction object
"""
def add_expense():
    try:
        result = None
         # Get category input from user
        category = int(input("Enter category (1-5): "))

        # Check if category has valid values
        if category < 1 or category > 5:
            raise ValueError("Category must be between 1 and 5.")

        # Get description  input from user
        description = input("Enter expense description: ")

        # Check description length
        if len(description.strip()) < 3:
            raise ValueError("Description must be at least 3 characters long.")
        
        if description.isnumeric():
            raise ValueError("Description should not be a number")

        # Get amount input from user
        amount = float(input("Enter amount: $"))

        # check if amount is a none negative number or 0 
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")

        result = Transaction(description = description, amount = amount, category = category)

        return result
    except ValueError as e:
        print(f"Invalid input: {e}")
        raise ValueError("Failed to add expense due to invalid input.")
    except Exception as error:
        print(error)
        raise Exception(error)



"""
    add_income
    adds the user income and returns a dict
"""
def add_income():
    result = None
    try:
        description = input("Enter income description: ")
        # Check description length
        if len(description.strip()) < 3:
            raise ValueError("Description must be at least 3 characters long.")
        
        if description.isnumeric():
            raise ValueError("Description should not be a number")


        amount = float(input("Enter amount: $"))

        # check if amount is a none negative number or 0 
        if amount <= 0:
            raise ValueError("Amount must be greater than 0.")
        

        # zero will be set as default value of category for transaction
        result = Transaction(description, amount)
        return result
    except ValueError as error:
        print(f"Invalid input: {error}")
        raise ValueError("Failed to add income due to invalid input.")
    except Exception as error:
        print(error)
        raise Exception(error)
    
        


"""
    get_current_balance
    recalculates current balance and returns it as float
"""
def get_current_balance(income_list, expenses):

    result = 0.0 # initial result value

    # add all income amounts
    for income in income_list:
        result += income.amount

    # add all expense amounts
    for expense in expenses:
        result -= expense.amount

    # returns current balance based off expenses and income
    return result



"""
    view_transactions
    display transcations
"""
def view_transactions(incomes, transactions):
    print("\n\nIncome:")
    print("_______________________________________________________________________________")
    print(f"| Date.                     | Description.           |Amount.       ")
    print("_______________________________________________________________________________")
    for income in incomes:
        print(income)
    print("_______________________________________________________________________________\n\n\n")
    print("Expenses:")
    print("_______________________________________________________________________________")
    print(f"| Date.                     | Description.           |Amount.       ")
    print("____________________________________________________________________________")
    for transaction in transactions:
        print(transaction)
    print("_______________________________________________________________________________\n\n\n")

"""
    set_budget
    sets budget for expense categories
    returns a list of budget targets respectively
"""
def set_budget():
    # categories for budget
    categories = ["Food","Transportation","Entertainment","Bills","Other"]
     
    # Result to be returned back to main function
    result = []
    try:

        # Prompts user to enter budget for each caegory 
        for category in categories:

            # waits for user input and it takes in as a float
            user_input = float(input(f"Set {category} budget: $"))

            # if user input is 0 or less than 0 is not a valid input for budget target
            if  user_input <= 0:

                # Raises Exception for in valid category input
                raise Exception(f"{category} budget value should be above 0")

            # adds user budget target to result list
            result.append(user_input)

        # returns users budget targets res
        return result
    
    except ValueError:
        # Raises error back to main function
        raise ValueError("Budget targets all need to be numbers")
    except Exception as error:
         # Raises error back to main function
        raise Exception(error)



"""
    get_remanining_budget
"""
def get_remaining_budget(category, budget_targets,transactions):

    total_expense =  sum([i.amount for i in transactions if i.category == category ])

    return budget_targets[category - 1] - total_expense


"""
    view_budget_summary
    create and output budget summary
"""
def view_budget_summary(incomes, transactions, categories, targets, current_balance):
    total_income = sum([i.amount for i in incomes])
    total_expenses = sum([i.amount for i in transactions])
    total_budget = sum([i for i in targets])
    difference = total_budget - total_expenses
    under_budget = False

    if difference > 0:
        under_budget = True

    n = len(categories) + 1
    print(f"INCOME:\nTotal Income: ${total_income}\n")
    print("EXPENSES BY CATEGORY:")
    for i in range(1, n):
        category = categories[i - 1]
        budget_target = targets[i - 1]
        category_spent = sum([j.amount for j in transactions if j.category == i])
        budget_used = round((category_spent/budget_target) * 100,2)
        print(f"{category}: ${category_spent} / ${budget_target}   ({budget_used}% used)")

    print(f"\nTotal Expenses:{total_expenses}\nCurrent Balance:{current_balance}\nTotal Budget:{total_budget}\nOver/Under budget:{difference} ", end="")

    if under_budget:
        print("(Under Budget)\n\n")
    else:
        print("(Over budget)\n\n")

    

"""
    generate_report
    generates a report of the user's spending 
    and prints out the ouput
"""
def generate_report(incomes, transactions, categories, targets):
    n = len(categories) + 1
    total_income = sum([i.amount for i in incomes])
    total_expenses = sum([i.amount for i in transactions])
    net_income = total_income - total_expenses
    savings_rating = round((net_income/total_income) * 100,2)

    total_spending = {}

    category_budget_used = {}


    for i in range(1, n):
        category = categories[i - 1]
        budget_target = targets[i - 1]
        category_spent = sum([j.amount for j in transactions if j.category == i])
        budget_used = round((category_spent/budget_target) * 100,2)
        category_budget_used[category]= budget_used

    for i in range(1,n):
        category = categories[i - 1]
        total_spending[category] = sum([j.amount for j in transactions if j.category == i])

    categories_totals_list = sorted(total_spending.items(),key = get_expense_val, reverse = True)[0:3]

   
    over_eighty_percent_usage = [{i:category_budget_used[i] } for i in category_budget_used if category_budget_used[i]>80]

    print(f"SUMMARY:\n- Total Income: ${total_income}\n- Total Expenses: ${total_expenses}\n", end="")
    print(f"- Net Income: ${net_income}\n- Savings Rate: {savings_rating}%\n\n")

    print(f"TOP SPENDING CATEGORIES:")
   

    num = 1
   
    for spending_category in categories_totals_list:
        percent_expense = round((spending_category[1]/total_expenses) * 100,2)
        print(f"{num}. {spending_category[0]}: ${spending_category[1]}({percent_expense}%)")
        num += 1

    print(f"\nBudget Status:\n- Categories over 80%: ", end = "")

    if len(over_eighty_percent_usage) == 0:
        print(":) You dont have anything over 80%. Muy Perfecto!!")
    for budget_item in over_eighty_percent_usage:
        for category in budget_item:
            print(f"{category} ({budget_item[category]}%)", end=", ")

    print("\n\n---End of Report---\n\n")



"""
    get_expense_val
    used as key in sorting dictionary so that we can sort the values by value
"""    
def get_expense_val(tuple):
    return tuple[1]




    




"""
    DataApi
    Talks to the json file and if it is not there it creates it and it store current
    data in instance variables
"""
class DataApi:
    def __init__(self):
        self.file_name = "data.json"
        self.incomes = []
        self.transactions = []
        self.targets = []
        self.monthly_budget = 0
        self.current_balance = 0


    """
        add_transaction
        add user expense transaction to list
    """
    def add_transaction(self, transaction):
        self.transactions.append(transaction)


    """
        add_income
        adds the users new income to income instance variable list
    """
    def add_income(self, income):
        self.incomes.append(income)


    """
        set_values
        receives a dictionary of the data in data.json
        and stores it as instance variables
    """
    def set_values(self,data_dict):
        try:
            self.monthly_budget = data_dict["monthlyBudget"]
            self.current_balance = data_dict["currentBalance"]
            self.targets = data_dict["targets"]
            for transaction_dict in data_dict["transactions"]:
                description = transaction_dict["description"]
                amount = transaction_dict["amount"]
                date = transaction_dict["date"]
                category = transaction_dict["category"]
                self.transactions.append(Transaction(description,amount, category, date))

            for transaction_dict in data_dict["income"]:
                description = transaction_dict["description"]
                amount = transaction_dict["amount"]
                date = transaction_dict["date"]
                category = transaction_dict["category"]
                self.incomes.append(Transaction(description,amount, category, date))
        except KeyError as error:
            print(error)
            raise Exception("JSON file is corrupted. Please delete data.json.")
        except Exception:
            raise Exception("JSON file is corrupted. Please delete data.json.")


    """
        fetch_data
        reads data from data.json or creates file if it doesnt exist
    """
    def fetch_data(self):
        try:
            with open("data.json","r") as file:
                content = file.read()
                json_str = content
                json_dict = json.loads(json_str)
                self.set_values(json_dict)
                file.close()
        except FileNotFoundError as error:
            print("data.json was not found")
            print("Created data.json file for you :). Dont worry.")
            proto_file = {
            "income": [],
            "transactions":[],
            "monthlyBudget":0,
            "currentBalance":0,
            "targets":[]
            }
            with open("data.json", "w") as file:
                json_str = json.dumps(proto_file, indent=4)
                file.write(json_str)
                result = proto_file
                file.close()
        except Exception as error:
            raise Exception(error)
       

    """
        save_data
        saves the data in instance variables as dictionary then makes
        it a json string then puts the string in data.json
    """
    def save_data(self):
        try:
            income_json_dict = [i.to_dict() for i in self.incomes]
            transaction_json_dict = [ i.to_dict() for i in self.transactions]
            proto_file = {
            "income": income_json_dict,
            "transactions":transaction_json_dict,
            "monthlyBudget":self.monthly_budget,
            "currentBalance":self.current_balance,
            "targets":self.targets
            }

            json_str = json.dumps(proto_file)
            with open("data.json", "w") as file:
                file.write(json_str)
                file.close()
        except Exception:
            raise Exception("Failed to save data")



class Transaction:
    def __init__(self ,description, amount, category = 0, date = str(datetime.now())):
        self.description =  description
        self.amount = amount
        self.category = category
        self.date = date

    def to_dict(self):
        return {"description": self.description, "amount": self.amount,"date":self.date, "category": self.category}
    

    def __str__(self):
        count = 18 - len(self.description)
        return f" {self.date} | {self.description}{" "* count}  | ${self.amount}"

if __name__ == "__main__":
    main()
