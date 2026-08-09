from datetime import datetime, timedelta
from config import (START_DATE, END_DATE, SIMULATION_DATE_FORMAT, RANDOM_SEED)
from business_rules import get_daily_ticket_volume
import random

from python.generate_tickets import start_date

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
    total_tickets = 0
    for current_date in simulation_days:
        day_name = get_day_name(current_date)
        ticket_count = get_daily_ticket_volume(day_name)
        total_tickets += ticket_count
        print(f"{current_date.strftime('%Y-%m-%d')} | " f"{day_name:<10} | " f"Tickets: {ticket_count}")

    print()
    print("--------------------------------")
    print(f"Simulation Days : {len(simulation_days):,}")
    print(f"Total Tickets   : {total_tickets:,}")
    print("--------------------------------")

# Main
if __name__ == "__main__":
    start_date, end_date = get_simulation_dates()
    run_simulation(start_date, end_date)