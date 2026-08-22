import pandas as pd
from datetime import datetime

from ticket_generator import generate_ticket
from id_generator import TicketIDGenerator

customers = pd.read_csv("../data/customers.csv")
categories = pd.read_csv("../data/categories.csv")
employees = pd.read_csv("../data/employees.csv")

ticket_id_generator = TicketIDGenerator()

test_date = datetime(2024, 1, 1)

tickets = []

for _ in range(1000):
    ticket = generate_ticket(simulation_date=test_date, customers=customers,
                             categories=categories, employees=employees,
                             ticket_id_generator=ticket_id_generator)
    tickets.append(ticket)

df = pd.DataFrame(tickets)

print()
print("FIRST RESPONSE BY PRIORITY")
print("-" * 45)
print(df.groupby("Priority")["FirstResponseHours"].mean().sort_values().round(2))

print()
print("FIRST RESPONSE BY CUSTOMER PLAN")
print("-" * 45)

customer_plan = customers[["CustomerID", "Plan"]]

df_with_plan = df.merge(customer_plan, on="CustomerID", how="left")

print(df_with_plan.groupby("Plan")["FirstResponseHours"].mean().sort_values().round(2))

# Critical + Enterprise

critical_enterprise = df_with_plan[(df_with_plan["Priority"] == "Critical") &
                                   (df_with_plan["Plan"] == "Enterprise")]

print()
print("CRITICAL + ENTERPRISE")
print("-" * 45)

print(f"Ticket Count: {len(critical_enterprise)}")
print(f"Average First Response Hours: {critical_enterprise['FirstResponseHours'].mean():.2f}")

#Low + Basic
low_basic = df_with_plan[(df_with_plan["Priority"] == "Low") & (df_with_plan["Plan"] == "Basic")]

print()
print("LOW + BASIC")
print("-" * 45)
print(f"Ticket Count: {len(low_basic)}")
print(f"Average First Response Hours: {low_basic['FirstResponseHours'].mean():.2f}")

#First Response SLA Performance
df_with_plan["FirstResponseSLAMet"] = (df_with_plan["FirstResponseHours"]
    <= df_with_plan["SLAHours"])

print()
print("FIRST RESPONSE SLA PERFORMANCE")
print("-" * 45)
print(df_with_plan["FirstResponseSLAMet"].value_counts())

#First Response SLA Performance (%)
print()
print("FIRST RESPONSE SLA PERFORMANCE (%)")
print("-" * 45)

print(df_with_plan["FirstResponseSLAMet"].value_counts(normalize=True).mul(100).round(2))

#SLA performance by Priority
print()
print("FIRST RESPONSE SLA BY PRIORITY")
print("-" * 45)

priority_sla = df_with_plan.groupby("Priority")["FirstResponseSLAMet"].mean().mul(100).round(2)
print(priority_sla)

#First Response SLA by Customer Plan
print()
print("FIRST RESPONSE SLA BY CUSTOMER PLAN")
print("-" * 45)

plan_sla = (
    df_with_plan
    .groupby("Plan")["FirstResponseSLAMet"]
    .mean()
    .mul(100)
    .round(2)
)

print(plan_sla)
