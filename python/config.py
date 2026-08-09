# Simulation period

START_DATE = "2024-01-01"
END_DATE = "2025-12-31"
SIMULATION_DATE_FORMAT = "%Y-%m-%d"


RANDOM_SEED = 42

# Monday Login spike

MONDAY_LOGIN_MULTIPLIER = 1.50

RESOLUTION_VARIATION_MIN = 0.60
RESOLUTION_VARIATION_MAX = 1.40

# Agent Experience Factor
EXPERIENCE_FACTOR = {
    "Junior": 1.40,
    "Mid": 1.00,
    "Senior": 0.60
}

# Customer Plan Factors
PLAN_FACTOR = {
    "Basic": 1.20,
    "Professional": 1.00,
    "Enterprise": 0.75
}

SLA_MATRIX = {
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

BUSINESS_HOURS = [
        (9, 10),
        (10, 12),
        (12, 13),
        (13, 16),
        (16, 18)
    ]

DAILY_VOLUME = {
        "Monday": (60,80),
        "Tuesday": (50,60),
        "Wednesday": (50,60),
        "Thursday": (50,60),
        "Friday": (40,50),
        "Saturday": (10,20),
        "Sunday": (5,15)
    }

BUSINESS_HOURS_WEIGHT = [
        0.25,
        0.35,
        0.10,
        0.20,
        0.10
    ]