import pandas as pd
from pathlib import Path
from datetime import datetime

from ticket_generator import generate_ticket
from id_generator import TicketIDGenerator
from business_rules import get_experience_level


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


# Load master data
customers = pd.read_csv(DATA_DIR / "customers.csv")
categories = pd.read_csv(DATA_DIR / "categories.csv")
employees = pd.read_csv(DATA_DIR / "employees.csv")


# Create ticket ID generator
ticket_id_generator = TicketIDGenerator()


# Test date
test_date = datetime(2024, 1, 1)


# Generate test tickets
tickets = []

for _ in range(10000):
    ticket = generate_ticket(
        test_date,
        customers,
        categories,
        employees,
        ticket_id_generator
    )

    tickets.append(ticket)


# Convert list of tickets into a DataFrame
df = pd.DataFrame(tickets)


print()
print("RESOLUTION BEHAVIOR PROFILE")
print("=" * 45)

print(f"Total Tickets: {len(df):,}")

print()
print("RESOLUTION BY COMPLEXITY")
print("-" * 45)

resolution_by_complexity = (
    df.groupby("Complexity")["ResolutionHours"]
    .mean()
    .round(2)
)

print(resolution_by_complexity)

print()
print("RESOLUTION BY PRIORITY")
print("-" * 45)

resolution_by_priority = (
    df.groupby("Priority")["ResolutionHours"]
    .mean()
    .round(2)
)

print(resolution_by_priority)

#Add employee experience level to the ticket data
##Create ExperienceLevel from ExperienceYears
employees = employees.copy()

employees["ExperienceLevel"] = employees["ExperienceYears"].apply(get_experience_level)

employee_experience = employees[["EmployeeID", "ExperienceLevel"]]

df_with_experience = df.merge(employee_experience, on="EmployeeID", how="left")

print()
print("RESOLUTION BY EXPERIENCE LEVEL")
print("-" * 45)

resolution_by_experience = (
    df_with_experience
    .groupby("ExperienceLevel")["ResolutionHours"]
    .mean()
    .round(2)
)

print(resolution_by_experience)


# Select customer information
customer_plan = customers[
    ["CustomerID", "Plan"]
]


# Merge customer plan with ticket data
df_with_plan = df.merge(
    customer_plan,
    on="CustomerID",
    how="left"
)


print()
print("RESOLUTION BY CUSTOMER PLAN")
print("-" * 45)


resolution_by_plan = (
    df_with_plan
    .groupby("Plan")["ResolutionHours"]
    .mean()
    .round(2)
)


print(resolution_by_plan)

print()
print("RESOLUTION BY LIFECYCLE")
print("-" * 45)

resolution_by_lifecycle = (
    df.groupby("Lifecycle")["ResolutionHours"]
    .mean()
    .round(2)
)

print(resolution_by_lifecycle)

# Merge customer and employee information
df_full = (
    df
    .merge(
        customers[["CustomerID", "Plan"]],
        on="CustomerID",
        how="left"
    )
    .merge(
        employees[["EmployeeID", "ExperienceLevel"]],
        on="EmployeeID",
        how="left"
    )
)

print(df_full)

fastest_scenario = df_full[
    (df_full["Complexity"] == "Easy")
    & (df_full["Priority"] == "Critical")
    & (df_full["Plan"] == "Enterprise")
    & (df_full["ExperienceLevel"] == "Senior")
    & (df_full["Lifecycle"] == "Simple")
]

slowest_scenario = df_full[
    (df_full["Complexity"] == "Hard")
    & (df_full["Priority"] == "Low")
    & (df_full["Plan"] == "Basic")
    & (df_full["ExperienceLevel"] == "Junior")
    & (df_full["Lifecycle"] == "Escalated")
]

print()
print("EXTREME SCENARIO COMPARISON")
print("-" * 45)

print(f"Fastest Scenario Ticket Count: {len(fastest_scenario)}")
print(f"Slowest Scenario Ticket Count: {len(slowest_scenario)}")

fastest_resolution = (
    fastest_scenario["ResolutionHours"]
    .mean()
    .round(2)
)

slowest_resolution = (
    slowest_scenario["ResolutionHours"]
    .mean()
    .round(2)
)

print()
print("AVERAGE RESOLUTION TIME")
print("-" * 45)

print(f"Fastest Scenario: {fastest_resolution} hours")
print(f"Slowest Scenario: {slowest_resolution} hours")

print()
print("EXTREME SCENARIO VALIDATION")
print("-" * 45)

if fastest_resolution < slowest_resolution:
    print("STATUS: PASS")
    print("Fastest scenario resolves quicker than slowest scenario.")
else:
    print("STATUS: FAIL")
    print("Unexpected resolution behavior detected.")

