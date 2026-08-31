import pandas as pd

tickets = pd.read_csv("../data/tickets_v3_full_simulation.csv",
                      parse_dates=["CreatedAt","FirstResponseAt","ResolvedAt"])
customers = pd.read_csv("../data/customers.csv")

print("\nCUSTOMER ANALYSIS")
print("=" * 60)

tickets_with_plan = tickets.merge(customers[["CustomerID","Plan"]], on="CustomerID", how="left")

plan_ticket_volume = tickets_with_plan.groupby("Plan").size().rename("TicketsCreated")

print("\nTICKET VOLUME BY CUSTOMER PLAN")
print("=" * 60)

print(plan_ticket_volume)

# TICKET VOLUME PERCENTAGE BY CUSTOMER PLAN
plan_ticket_volume_percentage = (plan_ticket_volume.div(plan_ticket_volume.sum())
                                 .mul(100).round(2))

print("\nTICKET VOLUME SHARE BY CUSTOMER PLAN")
print("=" * 60)

print(plan_ticket_volume_percentage)

# ==================================================
# CUSTOMER PLAN PERFORMANCE SUMMARY
# ==================================================

plan_performance = (
    tickets_with_plan
    .groupby("Plan")
    .agg(
        TicketsCreated=("TicketID", "count"),
        AvgFirstResponseHours=("FirstResponseHours", "mean"),
        AvgResolutionHours=("ResolutionHours", "mean"),
        FirstResponseSLA=("FirstResponseSLAMet", "mean"),
        ResolutionSLA=("SLAMet", "mean")
    )
)

# Calculate ticket share
plan_performance["TicketShare"] = (
    plan_performance["TicketsCreated"]
    .div(plan_performance["TicketsCreated"].sum())
    .mul(100)
)

# Convert SLA proportions to percentages
plan_performance["FirstResponseSLA"] = (
    plan_performance["FirstResponseSLA"]
    .mul(100)
)

plan_performance["ResolutionSLA"] = (
    plan_performance["ResolutionSLA"]
    .mul(100)
)

# Round numerical values
plan_performance = plan_performance.round(2)

print("\nCUSTOMER PLAN PERFORMANCE SUMMARY")
print("=" * 60)

print(plan_performance.to_string())

# CUSTOMER-LEVEL TICKET VOLUME
customer_ticket_volume = (tickets_with_plan.groupby("CustomerID")
                          .agg(TicketsCreated=("TicketID", "count"),
                               Plan=("Plan", "first")).reset_index()
                          .sort_values("TicketsCreated", ascending=False))

print("\nTOP 10 CUSTOMERS BY TICKET VOLUME")
print("=" * 60)

print(
    customer_ticket_volume
    .head(10)
)
# ==================================================
# CUSTOMER-LEVEL PERFORMANCE
# ==================================================

customer_performance = (
    tickets_with_plan
    .groupby(["CustomerID", "Plan"])
    .agg(
        TicketsCreated=("TicketID", "count"),
        AvgFirstResponseHours=("FirstResponseHours", "mean"),
        AvgResolutionHours=("ResolutionHours", "mean"),
        FirstResponseSLA=("FirstResponseSLAMet", "mean"),
        ResolutionSLA=("SLAMet", "mean")
    )
    .reset_index()
)

# Convert SLA proportions to percentages
customer_performance["FirstResponseSLA"] = (
    customer_performance["FirstResponseSLA"]
    .mul(100)
)

customer_performance["ResolutionSLA"] = (
    customer_performance["ResolutionSLA"]
    .mul(100)
)

# Round numerical values
customer_performance = customer_performance.round(2)


print("\nCUSTOMER PERFORMANCE SUMMARY")
print("=" * 60)

print(customer_performance.head(10).to_string())

# ==================================================
# TOP 10 HIGH-VOLUME CUSTOMER PERFORMANCE
# ==================================================

top_10_customer_performance = (
    customer_performance
    .sort_values(
        "TicketsCreated",
        ascending=False
    )
    .head(10)
)

print("\nTOP 10 CUSTOMERS - PERFORMANCE")
print("=" * 60)

print(top_10_customer_performance.to_string())

# ==================================================
# TOP 10 CUSTOMER AVERAGE PERFORMANCE
# ==================================================

top_10_customer_summary = (
    top_10_customer_performance[
        [
            "TicketsCreated",
            "AvgFirstResponseHours",
            "AvgResolutionHours",
            "FirstResponseSLA",
            "ResolutionSLA"
        ]
    ]
    .mean()
    .round(2)
)

print("\nTOP 10 HIGH-VOLUME CUSTOMER AVERAGE PERFORMANCE")
print("=" * 60)

print(top_10_customer_summary)

# ==================================================
# HIGH-VOLUME VS OVERALL CUSTOMER PERFORMANCE
# ==================================================

overall_customer_summary = (
    customer_performance[
        [
            "TicketsCreated",
            "AvgFirstResponseHours",
            "AvgResolutionHours",
            "FirstResponseSLA",
            "ResolutionSLA"
        ]
    ]
    .mean()
    .round(2)
)

customer_comparison = pd.DataFrame({
    "Overall Customer Average": overall_customer_summary,
    "Top 10 High-Volume Average": top_10_customer_summary
})

print("\nHIGH-VOLUME VS OVERALL CUSTOMER PERFORMANCE")
print("=" * 60)

print(customer_comparison)

customer_comparison["Difference"] = (
    customer_comparison["Top 10 High-Volume Average"]
    - customer_comparison["Overall Customer Average"]
).round(2)

print("\nHIGH-VOLUME CUSTOMER PERFORMANCE DIFFERENCE")
print("=" * 60)

print(customer_comparison)

# HIGH-VOLUME LOW-SLA CUSTOMERS

high_volume_low_sla = ((customer_performance[(customer_performance["TicketsCreated"] >=50)
                                            &(customer_performance["ResolutionSLA"] < 70)])
                       .sort_values(["ResolutionSLA", "TicketsCreated"], ascending=[True, False]))

print("\nHIGH-VOLUME CUSTOMERS WITH LOW RESOLUTION SLA")
print("=" * 60)

print(high_volume_low_sla.to_string())

