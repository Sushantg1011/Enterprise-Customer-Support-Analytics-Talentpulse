
import random
from pathlib import Path

import pandas as pd

import business_rules
import ticket_generator
from config import RANDOM_SEED


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

customers = pd.read_csv(DATA_DIR / "customers.csv")
categories = pd.read_csv(DATA_DIR / "categories.csv")
employees = pd.read_csv(DATA_DIR / "employees.csv")


def get_selection_sequence():
    # Reset both random-number generators
    random.seed(RANDOM_SEED)
    business_rules.reset_random_generator()

    selections = []

    for _ in range(10):
        customer = business_rules.select_customer_by_demand(customers)
        category = ticket_generator.select_category(categories)
        employee = ticket_generator.select_employee(category, employees)

        selections.append((
            customer["CustomerID"],
            category["CategoryID"],
            employee["EmployeeID"]
        ))

    return selections


first_run = get_selection_sequence()
second_run = get_selection_sequence()

print("First run:")
print(first_run)

print("\nSecond run:")
print(second_run)

print("\nReproducibility test:", "PASS" if first_run == second_run else "FAIL")
