import random
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from config import (START_DATE, END_DATE, SIMULATION_DATE_FORMAT, RANDOM_SEED)
from business_rules import get_daily_ticket_volume
from ticket_generator import (generate_ticket, validate_ticket)
from id_generator import TicketIDGenerator


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

customers = pd.read_csv(DATA_DIR / "customers.csv")
categories = pd.read_csv(DATA_DIR / "categories.csv")
employees = pd.read_csv(DATA_DIR / "employees.csv")

# Reproducible simulation
random.seed(RANDOM_SEED)

# convert configuration dates
def get_simulation_dates():
    """
        Converts the start and end dates from config.py
        into Python datetime objects.
        """
    start_date = datetime.strptime(START_DATE, SIMULATION_DATE_FORMAT)
    end_date = datetime.strptime(END_DATE, SIMULATION_DATE_FORMAT)
    return start_date, end_date

# Generate every simulation day
def generate_simulation_days(start_date, end_date):
    """
        Returns every date between the
        simulation start and end dates.
        """
    current_date  = start_date
    simulation_days  = []
    while current_date  <= end_date:
        simulation_days.append(current_date)
        current_date += timedelta(days=1)
    return simulation_days


# Get weekday name
def get_day_name(date):
    """
        Returns the weekday name.
        """
    return date.strftime("%A")

# Run simulation
def run_simulation(start_date, end_date):
    simulation_days = generate_simulation_days(start_date, end_date)
    ticket_id_generator = TicketIDGenerator()

    all_tickets = []
    for current_date in simulation_days:
        day_name = get_day_name(current_date)
        ticket_count = get_daily_ticket_volume(day_name)
        print(f"{current_date.strftime('%Y-%m-%d')} | " f"{day_name:<10} | " f"Tickets: {ticket_count}")

        for _ in range(ticket_count):
            ticket = generate_ticket(current_date, customers, categories, employees, ticket_id_generator)
            is_valid = validate_ticket(ticket, customers, categories, employees)
            if not is_valid:
                raise ValueError(f"Invalid ticket generated: {ticket['TicketID']}")
            all_tickets.append(ticket)

    return all_tickets

#     print()
#     print("--------------------------------")
#     print(f"Simulation Days : {len(simulation_days):,}")
#     print(f"Total Tickets   : {total_tickets:,}")
#     print("--------------------------------")
#
# Main
if __name__ == "__main__":
    start_date, end_date = get_simulation_dates()
    tickets = run_simulation(start_date, end_date)
    df_tickets = pd.DataFrame(tickets)

    output_path = DATA_DIR / "tickets_v3_full_simulation.csv"
    df_tickets.to_csv(output_path, index=False)

    print()
    print("--------------------------------")
    print(f"Simulation Days: {(end_date - start_date).days + 1:,}")
    print(f"Total tickets: {len(df_tickets):,}")
    print(f"Output File: {output_path}")
    print("--------------------------------")


# print("\nSample Ticket Times:")
#
# for _ in range(10):
#     hour, minute, second = get_ticket_time()
#
#     print(
#         f"{hour:02d}:{minute:02d}:{second:02d}"
#     )