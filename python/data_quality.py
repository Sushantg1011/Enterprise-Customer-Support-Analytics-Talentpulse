import pandas as pd
from pathlib import Path

# Patch

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data"

#Load Data

tickets = pd.read_csv(DATA_PATH / "tickets_v3_full_simulation.csv")
customers = pd.read_csv(DATA_PATH / "customers.csv")
categories = pd.read_csv(DATA_PATH / "categories.csv")
employees = pd.read_csv(DATA_PATH / "employees.csv")

print()
print("DATA QUALITY CHECK")
print("==================")

# Row count
print(f"Total tickets: {len(tickets):,}")

# Ticket ID Uniqueness

duplicate_ids = tickets[tickets["TicketID"].duplicated()]
print(f"Duplicate Ticket IDs: {len(duplicate_ids):,}")

# Missing Values

missing_values = tickets.isnull().sum()
total_missing_values = missing_values.sum()
print("Missing Values:")
print(missing_values[missing_values > 0])

# Date Validation
tickets["CreatedAt"] = pd.to_datetime(tickets["CreatedAt"], errors="coerce")

invalid_created_dates = tickets["CreatedAt"].isna().sum()

outside_range = (
    (tickets["CreatedAt"] < "2024-01-01")
    | (tickets["CreatedAt"] >= "2026-01-01")
)

outside_simulation_period = outside_range.sum()

print(f"Invalid CreatedAt values: {invalid_created_dates:,}")
print(f"Tickets outside simulation period: {outside_simulation_period:,}")

# Timestamp sequence validation
invalid_response_sequence = (tickets["FirstResponseAt"] < tickets["CreatedAt"]).sum()
invalid_resolution_sequence = (tickets["ResolvedAt"] < tickets["CreatedAt"]).sum()
invalid_resolution_response_sequence = (tickets["ResolvedAt"] < tickets["FirstResponseAt"]).sum()

print(f"First response before creation: {invalid_response_sequence:,}")
print(f"Response before creation: {invalid_resolution_sequence:,}")
print(f"Resolution before response: {invalid_resolution_response_sequence:,}")

# Customer Validation

invalid_customers = tickets[~tickets["CustomerID"].isin(customers["CustomerID"])]
print(f"Invalid Customer IDs: {len(invalid_customers):,}")

# Category Validation
invalid_categories = tickets[~tickets["CategoryID"].isin(categories["CategoryID"])]
print(f"Invalid Category IDs: {len(invalid_categories):,}")

# Employee Validatation
invalid_employees = tickets[~tickets["EmployeeID"].isin(employees["EmployeeID"])]
print(f"Invalid Employee IDs: {len(invalid_employees):,}")

# Department Validation
ticket_category_check = tickets.merge(categories[["CategoryID", "DepartmentID"]], on="CategoryID",
                                      how="left", suffixes=("_Ticket", "_Category"))
invalid_departments = ticket_category_check[ticket_category_check["DepartmentID_Ticket"] !=
                                           ticket_category_check["DepartmentID_Category"]]
print(f"Invalid Category-Department Assignments: {len(invalid_departments):,}")

# Employee-Department Validation
ticket_employee_check = tickets.merge(employees[["EmployeeID", "DepartmentID"]], on="EmployeeID",
                                      how="left", suffixes=("_Ticket", "_Employee"))
invalid_employee_departments = ticket_employee_check[ticket_employee_check["DepartmentID_Ticket"] !=
                                           ticket_employee_check["DepartmentID_Employee"]]
print(f"Invalid Employee-Department Assignments: {len(invalid_employee_departments):,}")

# Complexity Validation
ticket_complexity_check = tickets.merge(categories[["CategoryID", "Complexity"]], on="CategoryID",
                                      how="left", suffixes=("_Ticket", "_Category"))
invalid_complexity = ticket_complexity_check[ticket_complexity_check["Complexity_Ticket"] !=
                                           ticket_complexity_check["Complexity_Category"]]
print(f"Invalid Complexity Assignments: {len(invalid_complexity):,}")

# Priority validation
valid_priorities = ["Low", "Medium", "High", "Critical"]

invalid_priorities = tickets[~tickets["Priority"].isin(valid_priorities)]
print(f"Invalid Priorities: {len(invalid_priorities):,}")

master_data_errors = 0

for df, id_column in [(customers, "CustomerID"),
                      (categories, "CategoryID"),
                      (employees, "EmployeeID"),]:
    master_data_errors += df[id_column].duplicated().sum()
    master_data_errors += df[id_column].isna().sum().sum()

print(f"Total master-data errors: {master_data_errors:,}")

#Final result
total_errors = (
    len(duplicate_ids)
    + total_missing_values
    + invalid_created_dates
    + outside_simulation_period
    + invalid_response_sequence
    + invalid_resolution_sequence
    + invalid_resolution_response_sequence
    + len(invalid_customers)
    + len(invalid_categories)
    + len(invalid_employees)
    + len(invalid_departments)
    + len(invalid_employee_departments)
    + len(invalid_complexity)
    + len(invalid_priorities)
    + master_data_errors
)
print()
print("==================")

if total_errors == 0:
    print("DATA QUALITY STATUS: PASS")
else:
    print(f"DATA QUALITY STATUS: FAIL {total_errors} errors")

