import pandas as pd
from pathlib import Path

#Paths

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

#Load test tickets
tickets = pd.read_csv(DATA_DIR / "test_tickets.csv")

#Basic profile
print()
print("TICKET BEHAVIOR PROFILE")
print("=" * 45)

print(f"Total tickets: {len(tickets):,}")
print(f"Unique Customers: {tickets['CustomerID'].nunique():,}")
print(f"Unique Employees: {tickets['EmployeeID'].nunique():,}")
print(f"Unique Categories: {tickets['CategoryID'].nunique():,}")

# Priority Distribution
print()
print("PRIORITY DISTRIBUTION")
print("-" * 45)
priority_distribution = (tickets["Priority"].value_counts())
print(priority_distribution)

# Priority Distribution (%)
print()
print("PRIORITY DISTRIBUTION (%)")
print("-" * 45)
priority_percentage = (tickets["Priority"].value_counts(normalize=True).mul(100).round(2))
print(priority_percentage)

#Priority: Expected vs Actual
expected_priority = {
    "Low": 35,
    "Medium": 40,
    "High": 20,
    "Critical": 5,
}

actual_priority = (tickets["Priority"].value_counts(normalize=True).mul(100))

priority_comparison = pd.DataFrame({
    "Expected": pd.Series(expected_priority),
    "Actual": actual_priority
})

priority_comparison["Difference"] = (
    priority_comparison["Actual"]
    - priority_comparison["Expected"]
)

priority_comparison["Difference"] = priority_comparison["Difference"].round(2)

print()
print("PRIORITY: EXPECTED VS ACTUAL")
print("-" * 45)
print(priority_comparison)

# Lifecycle Distribution
print()
print("LIFECYCLE DISTRIBUTION")
print("-" * 45)

lifecycle_distribution = (tickets["Lifecycle"].value_counts())
print(lifecycle_distribution)

print()
print("LIFECYCLE DISTRIBUTION (%)")
print("-" * 45)

lifecycle_percentage = (tickets["Lifecycle"].value_counts(normalize=True).mul(100).round(2))
print(lifecycle_percentage)

# Lifecycle by complexity
print()
print("LIFECYCLE BY COMPLEXITY")
print("-" * 45)

lifecycle_by_complexity = pd.crosstab(tickets["Complexity"], tickets["Lifecycle"],
                                      normalize="index").mul(100).round(2)
print(lifecycle_by_complexity)

# Lifecycle by Priority
print()
print("LIFECYCLE BY PRIORITY")
print("-" * 45)

lifecycle_by_priority = pd.crosstab(tickets["Priority"], tickets["Lifecycle"],
                                      normalize="index").mul(100).round(2)
print(lifecycle_by_priority)

#Hard + Critical
hard_critical = tickets[(tickets["Complexity"] == "Hard") & (tickets["Priority"] == "Critical")]

print()
print("HARD + CRITICAL")
print("-" * 45)

print(hard_critical["Lifecycle"].value_counts(normalize=True).mul(100).round(2))


# --------------------------------
# Easy + Low
# --------------------------------

easy_low = tickets[
    (tickets["Complexity"] == "Easy") &
    (tickets["Priority"] == "Low")
]

print()
print("EASY + LOW")
print("-" * 45)

print(
    easy_low["Lifecycle"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(f"Hard + Critical Tickets: {len(hard_critical)}")
print(f"Easy + Low Tickets: {len(easy_low)}")
