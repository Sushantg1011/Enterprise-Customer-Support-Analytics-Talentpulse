import pandas as pd
from pathlib import Path
from datetime import datetime
from ticket_generator import (generate_ticket, validate_ticket)
from id_generator import TicketIDGenerator

# Paths

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# Load Master Data

customers = pd.read_csv(DATA_DIR / "customers.csv")
categories = pd.read_csv(DATA_DIR / "categories.csv")
employees = pd.read_csv(DATA_DIR / "employees.csv")

# Test settings

TEST_TICKETS = 1000

test_date = datetime(2024,1,1)
ticket_id_generator = TicketIDGenerator()

#Generate test tickets
tickets = []

for _ in range(TEST_TICKETS):
    ticket = generate_ticket(test_date, customers, categories, employees, ticket_id_generator)
    tickets.append(ticket)


#Convert to Dataframe
df = pd.DataFrame(tickets)

#Validation

print()
print("INTEGRATION TEST")
print("-" * 45)
print(f"Test tickets: {len(df):,}")

#Duplicate Ticket IDs
duplicate_ids = df[df["TicketID"].duplicated()]
print(f"Duplicate Ticket IDs: {len(duplicate_ids):,}")

#Missing Values
missing_values = df.isna().sum()

print()
print("MISSING VALUES:")
print(missing_values)

#Invalid Customer IDs
invalid_customers = df[~df["CustomerID"].isin(customers["CustomerID"])]

#Invalid category IDs
invalid_categories = df[~df["CategoryID"].isin(categories["CategoryID"])]

print()
print(f"Invalid Customer IDs: {len(invalid_customers):,}")

#Invalid Employee IDs
invalid_employees = df[~df["EmployeeID"].isin(employees["EmployeeID"])]
print(f"Invalid Employee IDs: {len(invalid_employees):,}")

#Category + Department Validation
category_department = categories[["CategoryID", "DepartmentID"]]
df_check = df.merge(category_department, on="CategoryID", how="left", suffixes = ("", "_Expected"))

invalid_category_department = df_check[df_check["DepartmentID"] != df_check["DepartmentID_Expected"]]

print(f"Invalid Category-Department Assignments: {len(invalid_category_department):,}")

#Employee + Department Validation
employee_department = employees[["EmployeeID", "DepartmentID"]]
df_check = df.merge(employee_department, on="EmployeeID", how="left", suffixes = ("", "_Employee"))

invalid_employee_department = df_check[df_check["DepartmentID"] != df_check["DepartmentID_Employee"]]

print(f"Invalid Employee-Department Assignments: {len(invalid_employee_department):,}")

#Complexity validation
category_complexity = categories[["CategoryID", "Complexity"]]
df_check = df.merge(category_complexity, on="CategoryID", how="left", suffixes = ("", "_Expected"))

invalid_complexity = df_check[df_check["Complexity"] != df_check["Complexity_Expected"]]

print(f"Invalid Complexity Assignments: {len(invalid_complexity):,}")

#Priority validation
valid_priorities = ["Low", "Medium", "High", "Critical"]
invalid_priorities = df[~df["Priority"].isin(valid_priorities)]
print(f"Invalid Priorities: {len(invalid_priorities):,}")

#Response Duration validation
invalid_response_duration = df[df["FirstResponseHours"] <= 0]
print(f"Invalid Response Durations: {len(invalid_response_duration):,}")

#Resolution duration validation
invalid_resolution_duration = df[df["ResolutionHours"] <= 0]
print(f"Invalid Resolution Durations: {len(invalid_resolution_duration):,}")

#Timestamp Validation
invalid_timestamps = df[(df["FirstResponseAt"] <= df["CreatedAt"])
                        | (df["ResolvedAt"] <= df["CreatedAt"])
                        | (df["ResolvedAt"] < df["FirstResponseAt"])]
print(f"Invalid Timestamps Relationships: {len(invalid_timestamps):,}")

#SLA Validation
invalid_sla = df[df["SLAMet"] != (df["ResolutionHours"] <= df["SLAHours"])]
print(f"Invalid SLA Calculations: {len(invalid_sla):,}")

#Final validation
all_valid = (
    len(duplicate_ids) == 0
    and missing_values.sum() == 0
    and len(invalid_customers) == 0
    and len(invalid_categories) == 0
    and len(invalid_employees) == 0
    and len(invalid_category_department) == 0
    and len(invalid_employee_department) == 0
    and len(invalid_complexity) == 0
    and len(invalid_priorities) == 0
    and len(invalid_response_duration) == 0
    and len(invalid_resolution_duration) == 0
    and len(invalid_timestamps) == 0
    and len(invalid_sla) == 0
)

print()
print("=" * 45)

if all_valid:
    print("INTEGRATION TEST STATUS: PASS")
else:
    print("INTEGRATION TEST STATUS: FAIL")

# Save test dataset
test_output_path = DATA_DIR / "test_tickets.csv"

df.to_csv(test_output_path, index=False)
print(f"Test dataset saved to: {test_output_path}")
