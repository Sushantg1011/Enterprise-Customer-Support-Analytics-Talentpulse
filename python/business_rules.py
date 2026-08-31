import random
from config import DAILY_VOLUME, BUSINESS_HOURS, BUSINESS_HOURS_WEIGHT


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