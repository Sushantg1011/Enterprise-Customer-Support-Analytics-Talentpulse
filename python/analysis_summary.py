import pandas as pd


# ==================================================
# LOAD DATASETS
# ==================================================

tickets = pd.read_csv(
    "../data/tickets_v3_full_simulation.csv",
    parse_dates=[
        "CreatedAt",
        "FirstResponseAt",
        "ResolvedAt"
    ]
)

customers = pd.read_csv("../data/customers.csv")
employees = pd.read_csv("../data/employees.csv")
categories = pd.read_csv("../data/categories.csv")


print("\nEXECUTIVE SUPPORT ANALYTICS SUMMARY")
print("=" * 60)

print("\nDATASET LOADED SUCCESSFULLY")

#Dataset KPIs
total_tickets = tickets["TicketID"].nunique()
total_customers = tickets["CustomerID"].nunique()
total_employees = tickets["EmployeeID"].nunique()
total_categories = tickets["CategoryID"].nunique()

print("\nDATASET OVERVIEW")
print("=" * 60)

print(f"Total Tickets: {total_tickets:,}")
print(f"Unique Customers: {total_customers:,}")
print(f"Unique Employees: {total_employees:,}")
print(f"Unique Categories: {total_categories:,}")

# ANALYSIS PERIOD
start_date = tickets["CreatedAt"].min()
end_date = tickets["CreatedAt"].max()

print("\nANALYSIS PERIOD")
print("=" * 60)

print(f"Start Date: {start_date}")
print(f"End Date: {end_date}")

# OVERALL SUPPORT PERFORMANCE
avg_first_response = tickets["FirstResponseHours"].mean()
avg_resolution = tickets["ResolutionHours"].mean()

first_response_sla = tickets["FirstResponseSLAMet"].mean() * 100
resolution_sla = tickets["SLAMet"].mean() * 100

print("\nOVERALL SUPPORT PERFORMANCE")
print("=" * 60)

print(f"Average First Response Time: {avg_first_response:.2f} hours")
print(f"Average Resolution Time: {avg_resolution:.2f} hours")
print(f"First Response SLA: {first_response_sla:.2f}%")
print(f"Resolution SLA: {resolution_sla:.2f}%")

# KEY SLA FINDINGS
resolution_sla_by_priority = (tickets.groupby("Priority")["SLAMet"].mean().mul(100).round(2))
resolution_sla_by_complexity = (tickets.groupby("Complexity")["SLAMet"].mean().mul(100).round(2))

resolution_sla_by_lifecycle = (
    tickets
    .groupby("Lifecycle")["SLAMet"]
    .mean()
    .mul(100)
    .round(2)
)

print("\nRESOLUTION SLA BY PRIORITY")
print("=" * 60)
print(resolution_sla_by_priority)

print("\nRESOLUTION SLA BY COMPLEXITY")
print("=" * 60)
print(resolution_sla_by_complexity)

print("\nRESOLUTION SLA BY LIFECYCLE")
print("=" * 60)
print(resolution_sla_by_lifecycle)

# ==================================================
# CUSTOMER PLAN SLA
# ==================================================

resolution_sla_by_plan = (
    tickets
    .merge(
        customers[["CustomerID", "Plan"]],
        on="CustomerID",
        how="left"
    )
    .groupby("Plan")["SLAMet"]
    .mean()
    .mul(100)
    .round(2)
)

print("\nRESOLUTION SLA BY CUSTOMER PLAN")
print("=" * 60)
print(resolution_sla_by_plan)


# ==================================================
# EXPERIENCE LEVEL SLA
# ==================================================

resolution_sla_by_experience = (
    tickets
    .groupby("ExperienceLevel")["SLAMet"]
    .mean()
    .mul(100)
    .round(2)
)

print("\nRESOLUTION SLA BY EXPERIENCE LEVEL")
print("=" * 60)

print(resolution_sla_by_experience)

# ==================================================
# TIME-BASED ANALYSIS
# ==================================================

tickets["Month"] = tickets["CreatedAt"].dt.to_period("M")

monthly_ticket_volume = (
    tickets
    .groupby("Month")["TicketID"]
    .count()
)

monthly_resolution_sla = (
    tickets
    .groupby("Month")["SLAMet"]
    .mean()
    .mul(100)
)

busiest_month = monthly_ticket_volume.idxmax()
busiest_month_tickets = monthly_ticket_volume.max()

slowest_month = monthly_ticket_volume.idxmin()
slowest_month_tickets = monthly_ticket_volume.min()

best_sla_month = monthly_resolution_sla.idxmax()
best_sla_value = monthly_resolution_sla.max()

worst_sla_month = monthly_resolution_sla.idxmin()
worst_sla_value = monthly_resolution_sla.min()


print("\nTIME-BASED ANALYSIS")
print("=" * 60)

print(
    f"Busiest Month: {busiest_month} "
    f"({busiest_month_tickets:,} tickets)"
)

print(
    f"Slowest Month: {slowest_month} "
    f"({slowest_month_tickets:,} tickets)"
)

print(
    f"Best Resolution SLA Month: {best_sla_month} "
    f"({best_sla_value:.2f}%)"
)

print(
    f"Worst Resolution SLA Month: {worst_sla_month} "
    f"({worst_sla_value:.2f}%)"
)

# ==================================================
# YEARLY SUPPORT PERFORMANCE
# ==================================================

tickets["Year"] = tickets["CreatedAt"].dt.year

yearly_performance = (
    tickets
    .groupby("Year")
    .agg(
        TicketsCreated=("TicketID", "count"),
        AvgFirstResponseHours=("FirstResponseHours", "mean"),
        AvgResolutionHours=("ResolutionHours", "mean"),
        FirstResponseSLA=("FirstResponseSLAMet", "mean"),
        ResolutionSLA=("SLAMet", "mean")
    )
)

# Convert SLA values to percentages
yearly_performance["FirstResponseSLA"] = (
    yearly_performance["FirstResponseSLA"] * 100
)

yearly_performance["ResolutionSLA"] = (
    yearly_performance["ResolutionSLA"] * 100
)

yearly_performance = yearly_performance.round(2)

print("\nYEARLY SUPPORT PERFORMANCE")
print("=" * 60)

print(yearly_performance.to_string())

# ==================================================
# EXECUTIVE FINDINGS
# ==================================================

print("\nEXECUTIVE FINDINGS")
print("=" * 60)

print(
    f"1. Resolution SLA is {resolution_sla:.2f}%, "
    f"significantly lower than First Response SLA of "
    f"{first_response_sla:.2f}%."
)

worst_priority = resolution_sla_by_priority.idxmin()
worst_priority_sla = resolution_sla_by_priority.min()

print(
    f"2. {worst_priority} priority has the lowest "
    f"Resolution SLA at {worst_priority_sla:.2f}%."
)

worst_complexity = resolution_sla_by_complexity.idxmin()
worst_complexity_sla = resolution_sla_by_complexity.min()

print(
    f"3. {worst_complexity} complexity has the lowest "
    f"Resolution SLA at {worst_complexity_sla:.2f}%."
)

worst_lifecycle = resolution_sla_by_lifecycle.idxmin()
worst_lifecycle_sla = resolution_sla_by_lifecycle.min()

print(
    f"4. {worst_lifecycle} lifecycle has the lowest "
    f"Resolution SLA at {worst_lifecycle_sla:.2f}%."
)

worst_plan = resolution_sla_by_plan.idxmin()
worst_plan_sla = resolution_sla_by_plan.min()

print(
    f"5. {worst_plan} customers have the lowest "
    f"Resolution SLA at {worst_plan_sla:.2f}%."
)

worst_experience = resolution_sla_by_experience.idxmin()
worst_experience_sla = resolution_sla_by_experience.min()

print(
    f"6. {worst_experience} employees have the lowest "
    f"Resolution SLA at {worst_experience_sla:.2f}%."
)

print(
    f"7. The busiest month was {busiest_month} "
    f"with {busiest_month_tickets:,} tickets."
)

print(
    f"8. The worst Resolution SLA month was {worst_sla_month} "
    f"at {worst_sla_value:.2f}%."
)

tickets_v3 = pd.read_csv("../data/tickets_v3_full_simulation.csv")

print("COLUMNS:")
print(tickets_v3.columns.tolist())

print("\nDATA TYPES:")
print(tickets_v3.dtypes)

print("\nSHAPE:")
print(tickets_v3.shape)

print("\nFIRST 5 ROWS:")
print(tickets_v3.head())
