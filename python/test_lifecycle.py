import pandas as pd
from business_rules import get_ticket_lifecycle


NUMBER_OF_TESTS = 10000

results = []

for _ in range(NUMBER_OF_TESTS):
    # Randomly create test conditions
    priority = pd.Series(["Low","Medium","High","Critical"]).sample(n=1).iloc[0]

    complexity = pd.Series(["Easy", "Medium", "Hard"]).sample(n=1).iloc[0]

    lifecycle = get_ticket_lifecycle(priority, complexity)

    results.append({
        "Priority": priority,
        "Complexity": complexity,
        "Lifecycle": lifecycle,
    })

df = pd.DataFrame(results)

# Overall Lifecycle Distribution

print("\nOVERALL LIFECYCLE DISTRIBUTION")
print("-" * 40)
print(df["Lifecycle"].value_counts(normalize=True).mul(100).round(2))

# Lifecycle by Complexity
print("\nLIFECYCLE BY COMPLEXITY")
print("-" * 40)
print(pd.crosstab(df["Complexity"], df["Lifecycle"], normalize="index").mul(100).round(2))

# Lifecycle by Priority
print("\nLIFECYCLE BY PRIORITY")
print("-" * 40)
print(pd.crosstab(df["Priority"], df["Lifecycle"], normalize="index").mul(100).round(2))

# Hard + Critical
print("\nHARD + CRITICAL")
print("-" * 40)
hard_critical = df[(df["Complexity"] == "Hard") & (df["Priority"] == "Critical")]
print(hard_critical["Lifecycle"].value_counts(normalize=True).mul(100).round(2))

# Easy + Low
print("\nEASY + LOW")
print("-" * 40)
easy_low = df[(df["Complexity"] == "Easy") & (df["Priority"] == "Low")]
print(easy_low["Lifecycle"].value_counts(normalize=True).mul(100).round(2))
