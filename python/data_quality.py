import pandas as pd
from pathlib import Path

# Patch

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data"

#Load Data

tickets = pd.read_csv(DATA_PATH / "tickets_v2_demand_weighted.csv")
customers = pd.read_csv(DATA_PATH / "customers.csv")
categories = pd.read_csv(DATA_PATH / "categories.csv")
employees = pd.read_csv(DATA_PATH / "employees.csv")

print()
print("DATA QUALITY CHECK")
print("==================")

# 1. Row count
print(f"Total tickets: {len(tickets):,}")

# 2.Ticket ID Uniqueness

duplicate_ids = tickets[tickets["TicketID"].duplicated()]
print(f"Duplicate Ticket IDs: {len(duplicate_ids):,}")

#3. Missing Values

missing_values = tickets.isnull().sum()
print("Missing Values:")
print(missing_values[missing_values > 0])

#4. Customer Validation

invalid_customers = tickets[~tickets["CustomerID"].isin(customers["CustomerID"])]
print(f"Invalid Customer IDs: {len(invalid_customers):,}")

# 5. Category Validation
invalid_categories = tickets[~tickets["CategoryID"].isin(categories["CategoryID"])]
print(f"Invalid Category IDs: {len(invalid_categories):,}")

# 6. Employee Validatation
invalid_employees = tickets[~tickets["EmployeeID"].isin(employees["EmployeeID"])]
print(f"Invalid Employee IDs: {len(invalid_employees):,}")

#7. Department Validation
ticket_category_check = tickets.merge(categories[["CategoryID", "DepartmentID"]], on="CategoryID",
                                      how="left", suffixes=("_Ticket", "_Category"))
invalid_departments = ticket_category_check[ticket_category_check["DepartmentID_Ticket"] !=
                                           ticket_category_check["DepartmentID_Category"]]
print(f"Invalid Category-Department Assignments: {len(invalid_departments):,}")

#8. Employee-Department Validation
ticket_employee_check = tickets.merge(employees[["EmployeeID", "DepartmentID"]], on="EmployeeID",
                                      how="left", suffixes=("_Ticket", "_Employee"))
invalid_employee_departments = ticket_employee_check[ticket_employee_check["DepartmentID_Ticket"] !=
                                           ticket_employee_check["DepartmentID_Employee"]]
print(f"Invalid Employee-Department Assignments: {len(invalid_employee_departments):,}")

#9. Complexity Validation
ticket_complexity_check = tickets.merge(categories[["CategoryID", "Complexity"]], on="CategoryID",
                                      how="left", suffixes=("_Ticket", "_Category"))
invalid_complexity = ticket_complexity_check[ticket_complexity_check["Complexity_Ticket"] !=
                                           ticket_complexity_check["Complexity_Category"]]
print(f"Invalid Complexity Assignments: {len(invalid_complexity):,}")

#10. Priority validation
valid_priorities = ["Low", "Medium", "High", "Critical"]

invalid_priorities = tickets[~tickets["Priority"].isin(valid_priorities)]
print(f"Invalid Priorities: {len(invalid_priorities):,}")

#Final result
total_errors = (
    len(duplicate_ids)
    + len(invalid_customers)
    + len(invalid_categories)
    + len(invalid_employees)
    + len(invalid_departments)
    + len(invalid_employee_departments)
    + len(invalid_complexity)
    + len(invalid_priorities)
)
print()
print("==================")

if total_errors == 0:
    print("DATA QUALITY STATUS: PASS")
else:
    print(f"DATA QUALITY STATUS: FAIL {total_errors} errors")
