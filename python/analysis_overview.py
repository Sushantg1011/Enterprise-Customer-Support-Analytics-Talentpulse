import pandas as pd

tickets = pd.read_csv("../data/tickets_v3_full_simulation.csv",
                      parse_dates=["CreatedAt", "FirstResponseAt", "ResolvedAt"])

print("\nDATASET OVERVIEW")
print("=" * 50)

print(f"Total Tickets: {len(tickets):,}")
print(f"Unique Customers: {tickets['CustomerID'].nunique():,}")
print(f"Unique Employees: {tickets['EmployeeID'].nunique():,}")
print(f"Unique Categories: {tickets['CategoryID'].nunique():,}")

print("\nDATE RANGE")
print("=" * 50)

print(f"Start Date: {tickets['CreatedAt'].min()}")
print(f"End Date: {tickets['CreatedAt'].max()}")

# Priority Distribution
print("\nPRIORITY DISTRIBUTION")
print("=" * 50)

priority_distribution = tickets["Priority"].value_counts()

print(priority_distribution)


print("\nPRIORITY DISTRIBUTION (%)")
print("=" * 50)

priority_distribution_percent = (
    tickets["Priority"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(priority_distribution_percent)

# Complexity Distribution
print("\nCOMPLEXITY DISTRIBUTION")
print("=" * 50)

complexity_distribution = tickets["Complexity"].value_counts()

print(complexity_distribution)


print("\nCOMPLEXITY DISTRIBUTION (%)")
print("=" * 50)

complexity_distribution_percent = (
    tickets["Complexity"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(complexity_distribution_percent)

# Lifecycle Distribution
print("\nLIFECYCLE DISTRIBUTION")
print("=" * 50)

lifecycle_distribution = tickets["Lifecycle"].value_counts()

print(lifecycle_distribution)


print("\nLIFECYCLE DISTRIBUTION (%)")
print("=" * 50)

lifecycle_distribution_percent = (
    tickets["Lifecycle"]
    .value_counts(normalize=True)
    .mul(100)
    .round(2)
)

print(lifecycle_distribution_percent)

# Overall Support Performance
print("\nOVERALL SUPPORT PERFORMANCE")
print("=" * 50)

print(
    f"Average First Response Time: "
    f"{tickets['FirstResponseHours'].mean():.2f} hours"
)

print(
    f"Average Resolution Time: "
    f"{tickets['ResolutionHours'].mean():.2f} hours"
)

print(
    f"Resolution SLA Met: "
    f"{tickets['SLAMet'].mean() * 100:.2f}%"
)

print(
    f"First Response SLA Met: "
    f"{tickets['FirstResponseSLAMet'].mean() * 100:.2f}%"
)

