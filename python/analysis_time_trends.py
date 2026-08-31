import pandas as pd

#Load tickets dataset

tickets = pd.read_csv("../data/tickets_v3_full_simulation.csv",
                      parse_dates=["CreatedAt", "FirstResponseAt", "ResolvedAt"])

print("\nTIME-BASED ANALYSIS")
print("=" * 60)

#Create Month-Year column from ticket creation date
tickets["Months"] = tickets["CreatedAt"].dt.to_period("M")

#Monthly ticket Volume
monthly_ticket_volume = (tickets.groupby("Months").size().rename("TicketsCreated"))

print("\nMONTHLY TICKET VOLUME")
print("=" * 60)

print(monthly_ticket_volume)

#Convert Series into Dataframe
monthly_ticket_volume_df = (monthly_ticket_volume.reset_index())

#Calculate Month-over-Month percentage change
monthly_ticket_volume_df["MoM Growth %"] = (monthly_ticket_volume_df["TicketsCreated"].pct_change()
                                            * 100).round(2)

print("\nMONTH-OVER-MONTH TICKET GROWTH")
print("=" * 60)

print(monthly_ticket_volume_df)

#Identify busiest month
busiest_month = monthly_ticket_volume_df.loc[monthly_ticket_volume_df["TicketsCreated"].idxmax()]

#Identify slowest month
slowest_month = monthly_ticket_volume_df.loc[monthly_ticket_volume_df["TicketsCreated"].idxmin()]

print("\nBUSIEST MONTH")
print("=" * 60)

print(
    f"Month: {busiest_month['Months']}"
)
print(
    f"Tickets Created: {busiest_month['TicketsCreated']:,}"
)

print("\nSLOWEST MONTH")
print("=" * 60)

print(
    f"Month: {slowest_month['Months']}"
)
print(
    f"Tickets Created: {slowest_month['TicketsCreated']:,}"
)

#Monthly Resolution SLA Trend
monthly_resolution_sla = (tickets.groupby("Months")["SLAMet"].mean() * 100).round(2)

print("\nMONTHLY RESOLUTION SLA")
print("=" * 60)

print(monthly_resolution_sla)

# ==================================================
# BEST AND WORST RESOLUTION SLA MONTHS
# ==================================================

best_sla_month = monthly_resolution_sla.loc[
    monthly_resolution_sla.idxmax()
]

worst_sla_month = monthly_resolution_sla.loc[
    monthly_resolution_sla.idxmin()
]

print("\nBEST RESOLUTION SLA MONTH")
print("=" * 60)

print(
    f"Month: {monthly_resolution_sla.idxmax()}"
)
print(
    f"Resolution SLA: {best_sla_month:.2f}%"
)


print("\nWORST RESOLUTION SLA MONTH")
print("=" * 60)

print(
    f"Month: {monthly_resolution_sla.idxmin()}"
)
print(
    f"Resolution SLA: {worst_sla_month:.2f}%"
)

# ==================================================
# TICKET VOLUME VS RESOLUTION SLA
# ==================================================

#Merge monthly ticket volume and monthly SLA
monthly_performance = pd.concat([monthly_ticket_volume, monthly_resolution_sla], axis=1)

#Rename SLA column
monthly_performance = monthly_performance.rename(columns={"SLAMet": "ResolutionSLAPercentage"})

print("\nMONTHLY TICKET VOLUME VS RESOLUTION SLA")
print("=" * 60)

print(monthly_performance)

volume_sla_correlation = (monthly_performance["TicketsCreated"]
                          .corr(monthly_performance["ResolutionSLAPercentage"]))

print("\nTICKET VOLUME VS RESOLUTION SLA CORRELATION")
print("=" * 60)

print(
    f"Correlation: {volume_sla_correlation:.3f}"
)

# ==================================================
# MONTHLY FIRST RESPONSE SLA TREND
# ==================================================

monthly_first_response_sla = (
    tickets
    .groupby("Months")["FirstResponseSLAMet"]
    .mean()
    * 100
)

monthly_first_response_sla = (
    monthly_first_response_sla
    .round(2)
)

print("\nMONTHLY FIRST RESPONSE SLA")
print("=" * 60)

print(monthly_first_response_sla)

# MONTHLY SLA COMPARISON
monthly_sla_comparison = pd.concat([monthly_first_response_sla, monthly_resolution_sla], axis=1)

monthly_sla_comparison.columns = ["FirstResponseSLA", "ResolutionSLA"]

# Calculate the monthly SLA gap
monthly_sla_comparison["SLA Gap"] = (monthly_sla_comparison["FirstResponseSLA"]
                                    - monthly_sla_comparison["ResolutionSLA"]).round(2)

print("\nMONTHLY FIRST RESPONSE VS RESOLUTION SLA")
print("=" * 60)

print(monthly_sla_comparison)

#Largest and smallest sla gap
largest_sla_gap = monthly_sla_comparison.loc[monthly_sla_comparison["SLA Gap"].idxmax()]

smallest_sla_gap = monthly_sla_comparison.loc[monthly_sla_comparison["SLA Gap"].idxmin()]

print("\nLARGEST MONTHLY SLA GAP")
print("=" * 60)

print(f"Month: {monthly_sla_comparison['SLA Gap'].idxmax()}")
print(f"Gap: {largest_sla_gap['SLA Gap']:.2f} percentage points")

print("\nSMALLEST MONTHLY SLA GAP")
print("=" * 60)

print(f"Month: {monthly_sla_comparison['SLA Gap'].idxmin()}")
print(f"Gap: {smallest_sla_gap['SLA Gap']:.2f} percentage points")

# MONTHLY AVERAGE RESOLUTION TIME
monthly_resolution_time = (tickets.groupby("Months")["ResolutionHours"].mean().round(2))

print("\nMONTHLY AVERAGE RESOLUTION TIME")
print("=" * 60)

print(monthly_resolution_time)

# ==================================================
# FASTEST AND SLOWEST RESOLUTION MONTHS
# ==================================================

fastest_resolution_month = monthly_resolution_time.loc[
    monthly_resolution_time.idxmin()
]

slowest_resolution_month = monthly_resolution_time.loc[
    monthly_resolution_time.idxmax()
]

print("\nFASTEST RESOLUTION MONTH")
print("=" * 60)

print(f"Month: {monthly_resolution_time.idxmin()}")
print(f"Average Resolution Time: {fastest_resolution_month:.2f} hours")

print("\nSLOWEST RESOLUTION MONTH")
print("=" * 60)

print(f"Month: {monthly_resolution_time.idxmax()}")
print(f"Average Resolution Time: {slowest_resolution_month:.2f} hours")

# RESOLUTION TIME VS RESOLUTION SLA
monthly_resolution_analysis = pd.concat([monthly_resolution_time, monthly_resolution_sla], axis=1)

monthly_resolution_analysis.columns = ["AverageResolutionHours", "ResolutionSLA"]

print("\nMONTHLY RESOLUTION TIME VS RESOLUTION SLA")
print("=" * 60)

print(monthly_resolution_analysis)

# Calculate correlation
resolution_time_sla_correlation = (monthly_resolution_analysis["AverageResolutionHours"]
                                   .corr(monthly_resolution_analysis["ResolutionSLA"]))

print("\nRESOLUTION TIME VS RESOLUTION SLA CORRELATION")
print("=" * 60)

print(
    f"Correlation: {resolution_time_sla_correlation:.3f}"
)


# YEARLY SUPPORT PERFORMANCE
tickets["Year"] = tickets["CreatedAt"].dt.year

yearly_performance = (tickets.groupby("Year").agg(TicketsCreated=("TicketID", "count"),
                                                  AvgFirstResponseHours=("FirstResponseHours", "mean"),
                                                  AvgResolutionHours=("ResolutionHours", "mean"),
                                                  FirstResponseSLA=("FirstResponseSLAMet", "mean"),
                                                  ResolutionSLA=("SLAMet", "mean")))

# Convert SLA values to percentages
yearly_performance["FirstResponseSLA"] = (
    yearly_performance["FirstResponseSLA"] * 100
).round(2)

yearly_performance["ResolutionSLA"] = (
    yearly_performance["ResolutionSLA"] * 100
).round(2)

yearly_performance["AvgFirstResponseHours"] = (
    yearly_performance["AvgFirstResponseHours"].round(2)
)

yearly_performance["AvgResolutionHours"] = (
    yearly_performance["AvgResolutionHours"].round(2)
)

print("\nYEARLY SUPPORT PERFORMANCE")
print("=" * 60)

print(yearly_performance.to_string())
