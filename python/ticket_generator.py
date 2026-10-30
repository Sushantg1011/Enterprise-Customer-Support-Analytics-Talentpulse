import pandas as pd
from datetime import datetime, timedelta
from id_generator import TicketIDGenerator
import business_rules
from business_rules import (get_ticket_time, get_ticket_priority,
                            get_sla_hours, select_customer_by_demand,
                            get_ticket_lifecycle, get_first_response_hours,
                            get_resolution_hours, get_experience_level)



def generate_ticket_created_at(simulation_date):
    """
        Generates a ticket creation timestamp
        for a specific simulation date.
        """
    hour, minute, second = get_ticket_time()
    return datetime(simulation_date.year, simulation_date.month,
                    simulation_date.day, hour, minute, second)


def select_customer(customers):
    """
    Selects one customer using
    plan-based ticket demand.
    """
    return select_customer_by_demand(customers)


def select_category(categories):
    """
        Selects one support category
        from the category master data.
        """
    return categories.sample(n=1, random_state=business_rules.rng).iloc[0]

def select_employee(category, employees):
    """
        Selects an employee from the department
        responsible for the selected category.
        """
    department_id = category['DepartmentID']
    eligible_employees = employees[employees['DepartmentID'] == department_id]
    return eligible_employees.sample(n=1, random_state=business_rules.rng).iloc[0]

ticket_id_generator = TicketIDGenerator()

def generate_ticket(simulation_date, customers, categories, employees, ticket_id_generator):
    """
        Generates one complete support ticket.
        """

    #Ticket creation time

    created_at = generate_ticket_created_at(simulation_date)

    #customer
    customer = select_customer(customers)

    #category
    category = select_category(categories)

    #employee
    employee = select_employee(category, employees)

    experience_years = employee["ExperienceYears"]
    experience_level = get_experience_level(experience_years)

    #priority
    priority = get_ticket_priority()

    #lifecycle
    lifecycle = get_ticket_lifecycle(priority,category['Complexity'])

    #SLA Hours
    sla_hours = get_sla_hours(customer['Plan'], priority)

    first_response_hours = get_first_response_hours(sla_hours,priority)
    first_response_sla_met = first_response_hours <= sla_hours
    first_response_at = created_at + timedelta(hours=first_response_hours)

    resolution_hours = get_resolution_hours(complexity=category["Complexity"],
                                            priority=priority, plan=customer["Plan"],
                                            experience_level=experience_level, lifecycle=lifecycle)
    resolution_hours = max(first_response_hours, resolution_hours)
    resolved_at = created_at + timedelta(hours=resolution_hours)

    sla_met = resolution_hours <= sla_hours


    #Build Ticket
    ticket = {
        "TicketID": ticket_id_generator.next_id(),
        "CreatedAt": created_at,

        "FirstResponseAt": first_response_at,
        "FirstResponseHours": first_response_hours,
        "FirstResponseSLAMet": first_response_sla_met,

        "ResolvedAt": resolved_at,
        "ResolutionHours": resolution_hours,

        "CustomerID": customer['CustomerID'],

        "CategoryID": category["CategoryID"],
        "DepartmentID": category['DepartmentID'],

        "EmployeeID": employee['EmployeeID'],
        "ExperienceLevel": experience_level,

        "Priority": priority,

        "SLAHours": sla_hours,
        "SLAMet": sla_met,

        "Complexity": category['Complexity'],

        "Lifecycle": lifecycle,
    }
    return ticket

def validate_ticket(ticket, customers, categories, employees):
    """
        Validates a generated ticket against
        master data and business rules.

        Returns:
            True  -> ticket is valid
            False -> ticket is invalid
        """
    #Customer Validation
    customer_exists = (ticket['CustomerID'] in customers['CustomerID'].values)
    if not customer_exists:
        return False

    #Category Validation
    category_exists = (ticket['CategoryID'] in categories['CategoryID'].values)
    if not category_exists:
        return False

    #Employee Validation
    employee_exists = (ticket['EmployeeID'] in employees['EmployeeID'].values)
    if not employee_exists:
        return False

    # Get category information
    category = categories[categories['CategoryID'] == ticket['CategoryID']].iloc[0]

    # Department validation
    if ticket['DepartmentID'] != category['DepartmentID']:
        return False

    # Employee department validation
    employee = employees[employees['EmployeeID'] == ticket['EmployeeID']].iloc[0]

    if employee['DepartmentID'] != ticket['DepartmentID']:
        return False

    # Complexity validation
    if ticket['Complexity'] != category['Complexity']:
        return False

    # SLA validation
    customer = customers[customers['CustomerID'] == ticket['CustomerID']].iloc[0]

    expected_sla = get_sla_hours(customer['Plan'], ticket['Priority'])

    if ticket['SLAHours'] != expected_sla:
        return False

    if ticket["FirstResponseHours"] <= 0:
        return False

    if ticket["ResolutionHours"] <=0:
        return False

    if ticket["FirstResponseAt"] <= ticket["CreatedAt"]:
        return False

    if ticket["ResolvedAt"] <= ticket["CreatedAt"]:
        return False
    if ticket["ResolvedAt"] < ticket["FirstResponseAt"]:
        return False

    calculated_response_hours = (ticket["FirstResponseAt"] -
                                 ticket["CreatedAt"]).total_seconds() / 3600
    if abs(calculated_response_hours - ticket["FirstResponseHours"]) > 0.0001:
        return False
    return True


#test
if __name__ == "__main__":
    customers = pd.read_csv('../data/customers.csv')
    categories = pd.read_csv('../data/categories.csv')
    employees = pd.read_csv('../data/employees.csv')

    test_date = datetime(2024, 1, 1)

    ticket = generate_ticket(test_date, customers, categories, employees, ticket_id_generator)

    print("\n Generated Ticket")
    print("-----------------")

    for key, value in ticket.items():
        print(f"{key:<15}: {value}")


    is_valid = validate_ticket(ticket, customers, categories, employees)

    print()
    print("Ticket Validation")
    print("-----------------")
    print(f"Valid tickets: {is_valid}")

    print()

    response_duration = (
            ticket["FirstResponseAt"] - ticket["CreatedAt"]
    )
    print(f"Calculated response duration: {response_duration}")
