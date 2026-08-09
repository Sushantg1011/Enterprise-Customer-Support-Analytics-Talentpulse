import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path
from config import *

random.seed(RANDOM_SEED)

# --------------------------------
# Paths
# --------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

# --------------------------------
# Load dimension tables
# --------------------------------
customers = pd.read_csv(DATA_DIR / "customers.csv")
employees = pd.read_csv(DATA_DIR / "employees.csv")
categories = pd.read_csv(DATA_DIR / "categories.csv")

# --------------------------------
# Settings
# --------------------------------

base_resolution_hours = {
    "Easy": 4,
    "Medium": 10,
    "Hard": 20
}

NUMBER_OF_TICKETS = 1000

start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31, 23, 59, 59)

priorities = ["Low", "Medium", "High", "Critical"]

priority_weights = [0.35, 0.40, 0.20, 0.05]

sla_matrix = {
    "Basic": {
        "Low": 72,
        "Medium": 48,
        "High": 24,
        "Critical": 8
    },
    "Professional": {
        "Low": 48,
        "Medium": 24,
        "High": 12,
        "Critical": 4
    },
    "Enterprise": {
        "Low": 24,
        "Medium": 12,
        "High": 6,
        "Critical": 2
    }
}

complexity_factor = {
    "Easy": 0.75,
    "Medium": 1.00,
    "Hard": 1.30
}

# --------------------------------
# Helper: random datetime
# --------------------------------
def random_datetime(start, end):
    seconds = int((end - start).total_seconds())
    return start + timedelta(seconds=random.randint(0, seconds))


# --------------------------------
# Generate tickets
# --------------------------------
tickets = []

for ticket_id in range(1, NUMBER_OF_TICKETS + 1):

    customer = customers.sample(n=1).iloc[0]

    # Select the ticket category first
    category = categories.sample(n=1).iloc[0]

    # Find which department handles this category
    department_id = category["DepartmentID"]

    complexity = category["Complexity"]
    complexity_multiplier = complexity_factor[complexity]

    # Keep only employees belonging to that department
    eligible_employees = employees[
        employees["DepartmentID"] == department_id
        ]

    # Assign one employee from the correct department
    employee = eligible_employees.sample(n=1).iloc[0]

    priority = random.choices(
        priorities,
        weights=priority_weights,
        k=1
    )[0]

    created_at = random_datetime(start_date, end_date)

    plan = customer["Plan"]

    sla_hours = sla_matrix[plan][priority]

    # Higher priority / better plans generally receive faster responses
    response_factor = random.uniform(0.05, 1.20)

    first_response_hours = max(
        0.05,
        sla_hours * response_factor
    )

    first_response_at = created_at + timedelta(
        hours=first_response_hours
    )

    # Resolution takes longer than first response
    base_hours = base_resolution_hours[complexity]

    resolution_variation = random.uniform(RESOLUTION_VARIATION_MIN, RESOLUTION_VARIATION_MAX)

    resolution_hours = base_hours * resolution_variation

    resolution_hours = max(
        first_response_hours,
        resolution_hours
    )

    resolved_at = created_at + timedelta(
        hours=resolution_hours
    )

    sla_met = resolution_hours <= sla_hours

    # CSAT tends to be better when SLA is met
    if sla_met:
        csat = random.choices(
            [3, 4, 5],
            weights=[0.15, 0.35, 0.50],
            k=1
        )[0]
    else:
        csat = random.choices(
            [1, 2, 3, 4],
            weights=[0.25, 0.35, 0.30, 0.10],
            k=1
        )[0]

    tickets.append({
        "TicketID": ticket_id,
        "CustomerID": customer["CustomerID"],
        "EmployeeID": employee["EmployeeID"],
        "DepartmentID": department_id,
        "CategoryID": category["CategoryID"],
        "Complexity": complexity,
        "Priority": priority,
        "CreatedAt": created_at,
        "FirstResponseAt": first_response_at,
        "ResolvedAt": resolved_at,
        "SLAHours": sla_hours,
        "SLAMet": sla_met,
        "CSAT": csat
    })

# --------------------------------
# Save FactTickets
# --------------------------------
df_tickets = pd.DataFrame(tickets)

df_tickets.to_csv(
    DATA_DIR / "tickets.csv",
    index=False
)

print()
print("SLA Results:")
print(df_tickets["SLAMet"].value_counts())

print()
print("SLA Results (%):")
print(
    df_tickets["SLAMet"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print()
print("SLA by Priority:")
print(
    df_tickets.groupby("Priority")["SLAMet"]
    .agg(["count", "mean"])
)