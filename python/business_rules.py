import random
import numpy as np
from config import (DAILY_VOLUME, BUSINESS_HOURS, BUSINESS_HOURS_WEIGHT, SLA_MATRIX,
                    CUSTOMER_TICKET_DEMAND_FACTOR, PRIORITY_FACTOR, PLAN_FACTOR,
                    EXPERIENCE_FACTOR, LIFECYCLE_FACTOR, RESOLUTION_VARIATION_MIN,
                    RESOLUTION_VARIATION_MAX, BUSINESS_RESOLUTION_HOURS, RANDOM_SEED)

rng = np.random.default_rng(RANDOM_SEED)

def reset_random_generator():
    global rng
    rng = np.random.default_rng(RANDOM_SEED)

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


def get_ticket_lifecycle(priority, complexity):
    """
    Selects a ticket lifecycle based on
    ticket priority and complexity.
    """
    # Easy + Low/Medium
    if complexity == "Easy" and priority in ["Low", "Medium"]:
        lifecycles = [
            "Simple",
            "Waiting Customer",
            "Escalated",
            "Reopened",
        ]

        weights = [
            0.60,
            0.30,
            0.05,
            0.05,
        ]
    #Easy + High/Critical
    elif complexity == "Easy" and priority in ["High", "Critical"]:
        lifecycles = [
            "Simple",
            "Waiting Customer",
            "Escalated",
            "Reopened",
        ]

        weights = [
            0.45,
            0.30,
            0.15,
            0.10,
        ]
    #Medium + Low/Medium
    elif complexity == "Medium" and priority in ["Low", "Medium"]:
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
     #Medium + High/Critical
    elif complexity == "Medium" and priority in ["High", "Critical"]:
        lifecycles = [
            "Simple",
            "Waiting Customer",
            "Escalated",
            "Reopened",
        ]

        weights = [
            0.35,
            0.35,
            0.20,
            0.10,
        ]
    #Hard + Low/Medium
    elif complexity == "Hard" and priority in ["Low", "Medium"]:
        lifecycles = [
            "Simple",
            "Waiting Customer",
            "Escalated",
            "Reopened",
        ]

        weights = [
            0.35,
            0.35,
            0.15,
            0.15,
        ]
    #Hard + High/Critical
    else:
        lifecycles = [
            "Simple",
            "Waiting Customer",
            "Escalated",
            "Reopened",
        ]

        weights = [
            0.25,
            0.30,
            0.25,
            0.20,
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
    return customers.sample(n=1, weights=weights, random_state=rng).iloc[0]

def get_first_response_hours(sla_hours, priority):
    """
    Generates the first response duration.

    Most tickets receive a response within SLA.
    A controlled percentage of tickets breach SLA
    based on priority.
    """
    breach_probability = {
        "Critical": 0.10,
        "High": 0.08,
        "Medium": 0.05,
        "Low": 0.03
    }
    breach = random.random() < breach_probability[priority]

    if breach:
        response_factor = random.uniform(1.05, 1.50)
    else:
        response_factor = random.uniform(0.10, 0.95)

    return round(sla_hours * response_factor, 4)

def get_experience_level(experience_years):
    """
        Converts employee experience in years
        into an experience category.
        """
    if experience_years <= 3:
        return "Junior"
    elif experience_years <= 7:
        return "Mid"
    else:
        return "Senior"

def get_resolution_hours(complexity, priority, plan, experience_level, lifecycle):
    """
        Calculates the estimated resolution time
        using multiple business factors.
        """
    priority_factor = PRIORITY_FACTOR[priority]
    plan_factor = PLAN_FACTOR[plan]
    experience_factor = EXPERIENCE_FACTOR[experience_level]
    lifecycle_factor = LIFECYCLE_FACTOR[lifecycle]

    variation = random.uniform(RESOLUTION_VARIATION_MIN, RESOLUTION_VARIATION_MAX)

    resolution_hours = (BUSINESS_RESOLUTION_HOURS[complexity]
                        * priority_factor
                        * plan_factor
                        * experience_factor
                        * lifecycle_factor
                        * variation)
    return resolution_hours
