import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.budget = 0.0

    # Method to set monthly budget
    def set_budget(self):
        budget = float(input("Enter your monthly budget: $"))
        self.budget = budget
        print(f"Budget set to ${self.budget:.2f}")

    # Method to add an expense entry
    def add_expense(self):
        amount = float(input("Enter expense amount: $"))
        category = input("Enter expense category (e.g., Food, Transport, Bills): ")
        description = input("Enter a short description: ")
        expense = {
            "amount": amount,
            "category": category,
            "description": description,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.expenses.append(expense)
        print("Expense added successfully.")

    # Method to display expenses by category
    def display_expenses(self):
        print("\nExpenses by Category:")
        spending_by_category = self.get_spending_by_category()
        for category, total in spending_by_category.items():
            print(f"{category}: ${total:.2f}")

    # Calculate total expenses for the month
    def calculate_total_expenses(self):
        return sum(expense["amount"] for expense in self.expenses)

    # Display current budget status
    def display_budget_status(self):
        total_spent = self.calculate_total_expenses()
        remaining_budget = self.budget - total_spent
        over_budget = total_spent > self.budget
        print("\nBudget Status:")
        print(f"Total Budget: ${self.budget:.2f}")
        print(f"Total Spent: ${total_spent:.2f}")
        print(f"Remaining Budget: ${remaining_budget:.2f}")
        print("Warning: Over Budget!" if over_budget else "Within Budget")

    # Get spending breakdown by category
    def get_spending_by_category(self):
        spending = {}
        for expense in self.expenses:
            category = expense["category"]
            spending[category] = spending.get(category, 0) + expense["amount"]
        return spending

    # Save expenses to a JSON file
    def save_expenses(self, filename="expenses.json"):
        with open(filename, 'w') as file:
            json.dump({
                "budget": self.budget,
                "expenses": self.expenses
            }, file, indent=4)
        print("Expenses saved successfully.")

    # Load expenses from a JSON file
    def load_expenses(self, filename="expenses.json"):
        try:
            with open(filename, 'r') as file:
                data = json.load(file)
                self.budget = data.get("budget", 0.0)
                self.expenses = data.get("expenses", [])
            print("Expenses loaded successfully.")
        except FileNotFoundError:
            print("No saved expenses found. Starting fresh.")

    # Main menu for interaction
    def menu(self):
        while True:
            print("\n===== Expense Tracker Menu =====")
            print("1. Set Monthly Budget")
            print("2. Add Expense")
            print("3. View Expenses by Category")
            print("4. View Budget Status")
            print("5. Save Expenses to File")
            print("6. Load Expenses from File")
            print("7. Exit")
            
            choice = input("Choose an option: ")
            if choice == "1":
                self.set_budget()
            elif choice == "2":
                self.add_expense()
            elif choice == "3":
                self.display_expenses()
            elif choice == "4":
                self.display_budget_status()
            elif choice == "5":
                self.save_expenses()
            elif choice == "6":
                self.load_expenses()
            elif choice == "7":
                print("Exiting the Expense Tracker. Goodbye!")
                break
            else:
                print("Invalid option. Please try again.")

# Example usage
if __name__ == "__main__":
    tracker = ExpenseTracker()
    tracker.menu()
