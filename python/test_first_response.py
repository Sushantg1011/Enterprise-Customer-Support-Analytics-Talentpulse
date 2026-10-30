import pandas as pd
from pathlib import Path

from ticket_generator import (generate_ticket)
from id_generator import TicketIDGenerator

# Paths

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

#Load Master Data

customers = pd.read_csv(DATA_DIR / "customers.csv")
categories = pd.read_csv(DATA_DIR / "categories.csv")
employees = pd.read_csv(DATA_DIR / "employees.csv")

#Generate test tickets

test_tickets = []

ticket_id_generator = TicketIDGenerator()
test_date = pd.Timestamp("2020-01-10").to_pydatetime()

for _ in range(1000):
    ticket = generate_ticket(test_date, customers, categories, employees, ticket_id_generator)
    test_tickets.append(ticket)

#Convert to Dataframe

df = pd.DataFrame(test_tickets)

# print("\n GENERATED TICKET COLUMNS")
# print("-" * 45)
# print(df.columns.tolist())

print()
print("FIRST RESPONSE VALIDATION")
print("=" * 40)

print(f"Test Tickets: {len(df):,}")

#1. Check positive response time
invalid_duration = df[df["FirstResponseHours"] <= 0]
print(f"Invalid Response Duration: {len(invalid_duration):,}")

#2. Check timestamp order
invalid_timestamp = df[df["FirstResponseAt"] <= df["CreatedAt"]]
print(f"Invalid Response Timestamps: {len(invalid_timestamp):,}")

#3. Check response against SLA
invalid_sla_response = df[df["FirstResponseHours"] > df["SLAHours"]]
print(f"Response Time > SLA: {len(invalid_sla_response):,}")

#4. Average Response Time
print()
print("AVERAGE FIRST RESPONSE HOURS")
print("=" * 45)
print(df["FirstResponseHours"].mean())

#5. Response Time by priority
print()
print("Average Response Time by Priority")
print("=" * 45)

print(df.groupby("Priority")["FirstResponseHours"].mean().round(2))

#6. Response time by complexity
print()
print("Average Response Time by Complexity")
print("=" * 45)

print(df.groupby("Complexity")["FirstResponseHours"].mean().round(2))

# Final Result
total_errors = (
    len(invalid_duration)
    + len(invalid_timestamp)
    + len(invalid_sla_response)
)

print()
print("-" * 45)
if total_errors == 0:
    print("FIRST RESPONSE STATUS: PASS")
else:
    print(f"FIRST RESPONSE STATUS: FAIL({total_errors} errors)")
