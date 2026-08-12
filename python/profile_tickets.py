import pandas as pd
from pathlib import Path

from python.business_rules import select_customer_by_demand

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data"

tickets = pd.read_csv(DATA_PATH / "tickets_v2_demand_weighted.csv")
customers = pd.read_csv(DATA_PATH / "customers.csv")

print("\nTICKET PROFILE")
print("=" * 40)

print(f"Total Tickets : {len(tickets):,}")

print(f"Unique Customers: {tickets['CustomerID'].nunique():,}")
print(f"Unique Employees: {tickets['EmployeeID'].nunique():,}")
print(f"Unique Categories: {tickets['CategoryID'].nunique():,}")

print("\nPRIORITY DISTRIBUTION")
print("-" * 40)

print(tickets['Priority'].value_counts(normalize=True).mul(100).round(2))

print("\nCOMPLEXITY DISTRIBUTION")
print("-" * 40)

print(tickets["Complexity"].value_counts())

print("\nTickets by Department")
print("-" * 40)

print(tickets["DepartmentID"].value_counts().sort_index())

print("\nCustomer Plan Distribution")
print("-" * 40)

print(customers["Plan"].value_counts())

print("\nCustomer Plan Distribution (%)")

print(customers["Plan"].value_counts(normalize=True).mul(100).round(2))

customer_plan = customers[["CustomerID", "Plan"]]

ticket_plan = tickets.merge(customer_plan, on="CustomerID", how="left")

print("\nTicket Distribution by Customer Plan")
print("=" * 45)

print(ticket_plan["Plan"].value_counts(normalize=True).mul(100).round(2))
