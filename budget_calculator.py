# budget_calculator.py - Personal Finance Calculator
# Starter code for e002-exercise-python-intro

"""
Personal Finance Calculator
---------------------------
This program helps users understand their monthly budget by collecting
income and expense information and displaying a formatted summary.

Complete the TODO sections below to finish the program.
"""

print("=" * 44)
print("       PERSONAL FINANCE CALCULATOR")
print("=" * 44)
print()

# =============================================================================
# DONE: Task 1 - Collect User Information
# =============================================================================
# Get the user's name
name: str = input("Enter your name: ")
if name == "":
    name = "Anonymous"

# Get monthly income (as a float)
# Remember to convert the input to a float!
monthlyIncome: float = float(input("Enter your monthly income (num): "))
if monthlyIncome < 0:
    print("It is no longer income. Please enter a positive value.")
    exit()


# Get expenses for at least 4 categories:
# - rent: Rent/Housing
# - utilities: Utilities (electric, water, internet)
# - food: Food/Groceries
# - transportation: Transportation (gas, public transit)

# store expenses as collection to easily iterate over categories
expenses: dict = {
    "Rent/Housing": 0,
    "Utilities": 0,
    "Food/Groceries": 0,
    "Transportation": 0
}
for expense in expenses.keys():
    expenses[expense] = float(input(f"How much do you pay for {expense} each month (num)? "))

for expense in expenses.keys():
    if expenses[expense] < 0:
        expenses[expense] = 0



# =============================================================================
# DONE: Task 2 - Perform Calculations
# =============================================================================
# Calculate total expenses
totalMonthlyExpenses: float = sum(expenses.values())


# Calculate remaining balance (income - expenses)
remainingBalance: float = monthlyIncome - totalMonthlyExpenses


# Calculate savings rate as a percentage
# Formula: (balance / income) * 100
savingsRate: float = (remainingBalance / monthlyIncome) * 100 


# Determine financial status
# - If balance > 0: status = "in the green"
# - If balance < 0: status = "in the red"
# - If balance == 0: status = "breaking even"

# assign financialStatus variable to proper status depending on user's remaining balance
financialStatus: str = ""
if remainingBalance > 0:
    financialStatus = "in the green"
elif remainingBalance < 0:
    financialStatus = "in the red"
else:
    financialStatus = "breaking even"


# =============================================================================
# DONE: Task 3 - Display Results
# =============================================================================
# Create a formatted budget report
# Use f-strings for formatting
# Dollar amounts should show 2 decimal places: f"${amount:.2f}"
# Percentages should show 1 decimal place: f"{rate:.1f}%"

# Example structure:

# report f string template
report_str = f"""============================================
       MONTHLY BUDGET REPORT
============================================
Name: {name}
Monthly Income: ${monthlyIncome:.2f}

EXPENSES:
  - Rent/Housing:    ${expenses['Rent/Housing']:.2f}
  - Utilities:       ${expenses['Utilities']:.2f}
  - Food/Groceries:  ${expenses['Food/Groceries']:.2f}
  - Transportation:  ${expenses['Transportation']:.2f}
--------------------------------------------
Total Expenses:      ${totalMonthlyExpenses:.2f}
Remaining Balance:   ${remainingBalance:.2f}
Savings Rate:        {savingsRate:.1f}%

Status: You are {financialStatus}!
============================================
"""

print(report_str)

# =============================================================================
# DONE: Task 4 - Add Validation (Optional Enhancement)
# =============================================================================
# Add these validations before calculations:
# - If name is empty, use "Anonymous"
# - If income is <= 0, print error and exit
# - If any expense is negative, treat as 0


# =============================================================================
# STRETCH GOAL: Category Percentages
# =============================================================================
# Add a section showing what percentage each expense is of total income
# Example: print(f"  - Rent/Housing:    {(rent/income)*100:.1f}% of income")

# start category report string
category_percentages_report: str = f"CATEGORY PERCENTAGES\n"

# programatically add each line in report for each expense category
for category, expense in expenses.items():
    category_percentages_report += f"  - {category+":":<16} {(expense/monthlyIncome)*100:.1f}% of income\n"
category_percentages_report += "============================================"

print(category_percentages_report)