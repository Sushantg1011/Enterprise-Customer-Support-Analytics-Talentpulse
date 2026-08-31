import pandas as pd
import random
from business_rules import get_experience_level, get_resolution_hours

#reproducibility
random.seed(42)

#test data
complexities = ["Easy", "Medium", "Hard"]
priorities = ["Low", "Medium", "High", "Critical"]
plans = ["Basic", "Professional", "Enterprise"]
experience_years = [2, 5, 10]
lifecycles = ["Simple", "Waiting Customer", "Escalated", "Reopened"]

#Generate test records
results = []

for _ in range(1000):
    complexity = random.choice(complexities)
    priority = random.choice(priorities)
    plan = random.choice(plans)
    years = random.choice(experience_years)
    experience_level = get_experience_level(years)
    lifecycle = random.choice(lifecycles)
    resolution_hours = get_resolution_hours(complexity, priority, plan,
                                            experience_level, lifecycle)
    results.append({"Complexity": complexity, "Priority": priority, "Plan": plan,
                    "ExperienceYears": years, "ExperienceLevel": experience_level,
                    "Lifecycle": lifecycle, "ResolutionHours": resolution_hours})

#Convert to DataFrame
df = pd.DataFrame(results)

#Basic Validation
print()
print("RESOLUTION ENGINE VALIDATION")
print("-" * 45)
print(f"Test records: {len(df):,}")

#Check Negative/Zero values
invalid_duration = df[df["ResolutionHours"] <= 0]
print(f"Invalid Resolution Duration: {len(invalid_duration):,}")

#Overall Average
print()
print("AVERAGE RESOLUTION HOURS")
print("-" * 45)
print(round(df["ResolutionHours"].mean(),2))

#Resolution by complexity
print()
print("RESOLUTION BY COMPLEXITY")
print("-" * 45)
print(df.groupby("Complexity")["ResolutionHours"].mean().round(2))

#Resolution by Priority
print()
print("RESOLUTION BY PRIORITY")
print("-" * 45)
print(df.groupby("Priority")["ResolutionHours"].mean().round(2))

#Resolution by Experience
print()
print("RESOLUTION BY EXPERIENCE")
print("-" * 45)
print(df.groupby("ExperienceLevel")["ResolutionHours"].mean().round(2))

#Resolution by Plan
print()
print("RESOLUTION BY CUSTOMER PLAN")
print("-" * 45)
print(df.groupby("Plan")["ResolutionHours"].mean().round(2))

#Resolution by Lifecycle
print()
print("RESOLUTION BY LIFECYCLE")
print("-" * 45)
print(df.groupby("Lifecycle")["ResolutionHours"].mean().round(2))

#Final validation
print()
print("=" * 45)
if len(invalid_duration) == 0:
    print("RESOLUTION ENGINE STATUS: PASS")
else:
    print("RESOLUTION ENGINE STATUS: FAIL")

