import random
from config import DAILY_VOLUME, BUSINESS_HOURS, BUSINESS_HOURS_WEIGHT, SLA_MATRIX, CUSTOMER_TICKET_DEMAND_FACTOR

# Priority Distribution
PRIORITY_WEIGHTS = {"Low": 0.35,
                    "Medium":0.40,
                    "High":0.20,
                    "Critical":0.05
                    }


def get_daily_ticket_volume(day_name):
    """
        Returns the number of tickets to generate
        based on the day of the week.
        """
    min_value, max_value = DAILY_VOLUME[day_name]
    return random.randint(min_value, max_value)


def get_ticket_lifecycle():
    """
        Randomly selects a ticket lifecycle
        based on business probabilities.
        """
    lifecycles = [
        "Simple",
        "Waiting Customer",
        "Escalated",
        "Reopened",
    ]

    weights = [
        0.45,
        0.35,
        0.10,
        0.10,
    ]

    return random.choices(lifecycles,weights=weights,k=1)[0]

def get_ticket_time_block():
    return random.choices(BUSINESS_HOURS,weights=BUSINESS_HOURS_WEIGHT,k=1)[0]


def get_ticket_time():
    """
        Returns a random ticket arrival time
        within a business-hour block.
        """
    start_hour, end_hour = get_ticket_time_block()
    hour = random.randint(start_hour, end_hour - 1)
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return hour, minute, second

def get_ticket_priority():
    """
        Randomly selects ticket priority
        based on configured business probabilities.
        """
    priorities = list(PRIORITY_WEIGHTS.keys())
    weights = list(PRIORITY_WEIGHTS.values())

    return random.choices(priorities,weights=weights,k=1)[0]

def get_sla_hours(plan, priority):
    """
        Returns the SLA in hours based on
        customer plan and ticket priority.
        """
    return SLA_MATRIX[plan][priority]

def select_customer_by_demand(customers):
    """
        Selects a customer using plan-based
        ticket demand weighting.
        """
    weights = customers["Plan"].map(CUSTOMER_TICKET_DEMAND_FACTOR)
    return customers.sample(n=1, weights=weights).iloc[0]