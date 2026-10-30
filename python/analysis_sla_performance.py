import pandas as pd
from business_rules import get_experience_level

tickets = pd.read_csv("../data/tickets_v3_full_simulation.csv",
                      parse_dates=["CreatedAt", "FirstResponseAt", "ResolvedAt"])
customers = pd.read_csv("../data/customers.csv")
employees = pd.read_csv("../data/employees.csv")

print("\nSLA PERFORMANCE ANALYSIS")
print("=" * 50)

# Resolution SLA Performance by Priority
print("\nRESOLUTION SLA BY PRIORITY")
print("=" * 50)

resolution_sla_by_priority = (
    tickets.groupby("Priority")["SLAMet"]
    .mean()
    .mul(100)
    .sort_values()
)

print(resolution_sla_by_priority.round(2))

print("\nRESOLUTION SLA BY COMPLEXITY")
print("=" * 50)

resolution_sla_by_complexity = (
    tickets.groupby("Complexity")["SLAMet"]
    .mean()
    .mul(100)
    .sort_values()
)

print(resolution_sla_by_complexity.round(2))

print("\nRESOLUTION SLA BY CUSTOMER PLAN")
print("=" * 50)

# Merge customer plan with tickets
tickets_with_plan = tickets.merge(
    customers[["CustomerID", "Plan"]],
    on="CustomerID",
    how="left"
)

resolution_sla_by_plan = (
    tickets_with_plan.groupby("Plan")["SLAMet"]
    .mean()
    .mul(100)
    .sort_values()
)

print(resolution_sla_by_plan.round(2))

print("\nRESOLUTION SLA BY LIFECYCLE")
print("=" * 50)

resolution_sla_by_lifecycle = (
    tickets.groupby("Lifecycle")["SLAMet"]
    .mean()
    .mul(100)
    .sort_values()
)

print(resolution_sla_by_lifecycle.round(2))

print("\nFIRST RESPONSE SLA BY PRIORITY")
print("=" * 50)

first_response_sla_by_priority = (
    tickets.groupby("Priority")["FirstResponseSLAMet"]
    .mean()
    .mul(100)
    .sort_values()
)

print(first_response_sla_by_priority.round(2))

print("\nFIRST RESPONSE SLA BY CUSTOMER PLAN")
print("=" * 50)

first_response_sla_by_plan = (
    tickets_with_plan.groupby("Plan")["FirstResponseSLAMet"]
    .mean()
    .mul(100)
    .sort_values()
)

print(first_response_sla_by_plan.round(2))

print("\nFIRST RESPONSE SLA BY COMPLEXITY")
print("=" * 50)

first_response_sla_by_complexity = (
    tickets.groupby("Complexity")["FirstResponseSLAMet"]
    .mean()
    .mul(100)
    .sort_values()
)

print(first_response_sla_by_complexity.round(2))

print("\nFIRST RESPONSE SLA BY LIFECYCLE")
print("=" * 50)

first_response_sla_by_lifecycle = (
    tickets.groupby("Lifecycle")["FirstResponseSLAMet"]
    .mean()
    .mul(100)
    .sort_values()
)

print(first_response_sla_by_lifecycle.round(2))

print("\nSLA GAP BY PRIORITY")
print("=" * 50)

sla_gap_by_priority = pd.DataFrame({
    "First Response SLA %": (
        tickets.groupby("Priority")["FirstResponseSLAMet"]
        .mean()
        .mul(100)
    ),

    "Resolution SLA %": (
        tickets.groupby("Priority")["SLAMet"]
        .mean()
        .mul(100)
    )
})

sla_gap_by_priority["SLA Gap (Percentage Points)"] = (
        sla_gap_by_priority["First Response SLA %"]
        - sla_gap_by_priority["Resolution SLA %"]
)

print(sla_gap_by_priority.round(2))

print("\nSLA GAP BY COMPLEXITY")
print("=" * 50)

sla_gap_by_complexity = pd.DataFrame({
    "First Response SLA %": (
        tickets.groupby("Complexity")["FirstResponseSLAMet"]
        .mean()
        .mul(100)
    ),

    "Resolution SLA %": (
        tickets.groupby("Complexity")["SLAMet"]
        .mean()
        .mul(100)
    )
})

sla_gap_by_complexity["SLA Gap (Percentage Points)"] = (
    sla_gap_by_complexity["First Response SLA %"]
    - sla_gap_by_complexity["Resolution SLA %"]
)

print(sla_gap_by_complexity.round(2))

print("\nSLA GAP BY CUSTOMER PLAN")
print("=" * 50)

sla_gap_by_plan = pd.DataFrame({
    "First Response SLA %": (
        tickets_with_plan.groupby("Plan")["FirstResponseSLAMet"]
        .mean()
        .mul(100)
    ),

    "Resolution SLA %": (
        tickets_with_plan.groupby("Plan")["SLAMet"]
        .mean()
        .mul(100)
    )
})

sla_gap_by_plan["SLA Gap (Percentage Points)"] = (
    sla_gap_by_plan["First Response SLA %"]
    - sla_gap_by_plan["Resolution SLA %"]
)

print(sla_gap_by_plan.round(2).to_string())

print("\nSLA GAP BY LIFECYCLE")
print("=" * 50)

sla_gap_by_lifecycle = pd.DataFrame({
    "First Response SLA %": (
        tickets.groupby("Lifecycle")["FirstResponseSLAMet"]
        .mean()
        .mul(100)
    ),

    "Resolution SLA %": (
        tickets.groupby("Lifecycle")["SLAMet"]
        .mean()
        .mul(100)
    )
})

sla_gap_by_lifecycle["SLA Gap (Percentage Points)"] = (
    sla_gap_by_lifecycle["First Response SLA %"]
    - sla_gap_by_lifecycle["Resolution SLA %"]
)

print(sla_gap_by_lifecycle.round(2).to_string())

print("\nRESOLUTION SLA BY PRIORITY AND COMPLEXITY")
print("=" * 50)

resolution_sla_priority_complexity = (
    tickets.groupby(["Priority", "Complexity"])["SLAMet"]
    .mean()
    .mul(100)
    .round(2)
    .unstack()
)

print(resolution_sla_priority_complexity.to_string())

# RESOLUTION SLA BY CUSTOMER PLAN AND PRIORITY

print("\nRESOLUTION SLA BY CUSTOMER PLAN AND PRIORITY")
print("=" * 50)

resolution_sla_plan_priority = (
    tickets_with_plan
    .groupby(["Plan", "Priority"])["SLAMet"]
    .mean()
    .mul(100)
    .unstack()
    .round(2)
)

print(resolution_sla_plan_priority)

# RESOLUTION SLA BY EXPERIENCE LEVEL AND COMPLEXITY

print("\nRESOLUTION SLA BY EXPERIENCE LEVEL AND COMPLEXITY")
print("=" * 50)

resolution_sla_experience_complexity = (
    tickets
    .groupby(["ExperienceLevel", "Complexity"])["SLAMet"]
    .mean()
    .mul(100)
    .unstack()
    .round(2)
)

print(resolution_sla_experience_complexity)

# AVERAGE RESOLUTION TIME BY EXPERIENCE LEVEL AND COMPLEXITY

print("\nAVERAGE RESOLUTION TIME BY EXPERIENCE LEVEL AND COMPLEXITY")
print("=" * 50)

average_resolution_experience_complexity = (
    tickets
    .groupby(["ExperienceLevel", "Complexity"])["ResolutionHours"]
    .mean()
    .unstack()
    .round(2)
)

print(average_resolution_experience_complexity)

print("\nEMPLOYEE PERFORMANCE SUMMARY")
print("=" * 50)

employee_performance = (tickets.groupby("EmployeeID")
                        .agg(TicketsHandled=("TicketID", "count"),
                             AvgFirstResponseHours=("FirstResponseHours", "mean"),
                             AvgResolutionHours=("ResolutionHours", "mean"),
                             ResolutionSLAPercentage=("SLAMet", "mean"),
                             FirstResponseSLAPercentage=("FirstResponseSLAMet", "mean"),))

# Convert SLA rates into percentages

employee_performance["ResolutionSLAPercentage"] = (employee_performance["ResolutionSLAPercentage"]
                                                   * 100).round(2)
employee_performance["FirstResponseSLAPercentage"] = (employee_performance["FirstResponseSLAPercentage"]
                                                      * 100).round(2)

#Round time columns
employee_performance["AvgFirstResponseHours"] = (employee_performance["AvgFirstResponseHours"]).round(2)
employee_performance["AvgResolutionHours"] = (employee_performance["AvgResolutionHours"]).round(2)

print(employee_performance.to_string())

print("\nTOP 10 EMPLOYEES BY RESOLUTION SLA")
print("=" * 50)

top_10_employees = (
    employee_performance
    .sort_values(
        by="ResolutionSLAPercentage",
        ascending=False
    )
    .head(10).index.tolist()
)

print(top_10_employees)

print("\nBOTTOM 10 EMPLOYEES BY RESOLUTION SLA")
print("=" * 50)

bottom_10_employees = (
    employee_performance
    .sort_values(
        by="ResolutionSLAPercentage",
        ascending=True
    )
    .head(10).index.tolist()
)

print(bottom_10_employees)

employee_columns = employees[
    ["EmployeeID", "ExperienceYears"]
]

employee_analysis = tickets.merge(
    employee_columns,
    on="EmployeeID",
    how="left"
)

employee_analysis["ExperienceLevel"] = (
    employee_analysis["ExperienceYears"]
    .apply(get_experience_level)
)

experience_sla = (
    employee_analysis
    .groupby("ExperienceLevel")["SLAMet"]
    .mean()
    .mul(100)
    .round(2)
)

print("\nRESOLUTION SLA BY EXPERIENCE LEVEL")
print("=" * 50)
print(experience_sla)


#Add Performance Group
employee_analysis["PerformanceGroup"] = "Other"

employee_analysis.loc[employee_analysis["EmployeeID"].isin(top_10_employees), "PerformanceGroup"]\
    = "Top 10"

employee_analysis.loc[employee_analysis["EmployeeID"].isin(bottom_10_employees),"PerformanceGroup"] \
    = "Bottom 10"

print(employee_analysis)

complexity_distribution = (
    employee_analysis[employee_analysis["PerformanceGroup"].isin(["Top 10", "Bottom 10"])]
    .groupby(["PerformanceGroup", "Complexity"]).size().
    groupby(level=0).transform(lambda x: x / x.sum() * 100).round(2).unstack()
)

print("\nCOMPLEXITY DISTRIBUTION: TOP 10 VS BOTTOM 10")
print("=" * 60)
print(complexity_distribution)

# Experience level distribution for Top 10 vs Bottom 10

experience_distribution = (
    employee_analysis[
        employee_analysis["PerformanceGroup"].isin(["Top 10", "Bottom 10"])
    ]
    .groupby(["PerformanceGroup", "ExperienceLevel"])
    .size()
    .groupby(level=0)
    .transform(lambda x: x / x.sum() * 100)
    .round(2)
    .unstack()
)

print("\nEXPERIENCE LEVEL DISTRIBUTION: TOP 10 VS BOTTOM 10")
print("=" * 60)
print(experience_distribution)

# Calculate the average Resolution SLA for each experience level

experience_benchmark = (
    employee_analysis
    .groupby("ExperienceLevel")["SLAMet"]
    .mean()
    .mul(100)
    .round(2)
)

print("\nEXPERIENCE LEVEL PERFORMANCE BENCHMARK")
print("=" * 60)
print(experience_benchmark)

employee_performance_with_level = (
    employee_performance
    .reset_index()
    .merge(
        employees[["EmployeeID", "ExperienceYears"]],
        on="EmployeeID",
        how="left"
    )
)

def get_experience_level(years):
    if years <=2:
        return "Junior"
    elif years <= 5:
        return "Mid"
    else:
        return "Senior"

employee_performance_with_level["ExperienceLevel"] = (
    employee_performance_with_level["ExperienceYears"]
    .apply(get_experience_level)
)

employee_performance_with_level["ExperienceBenchmarkSLA"] = (
    employee_performance_with_level["ExperienceLevel"].map(experience_benchmark)
)

employee_performance_with_level["SLA Difference vs Benchmark"] = (
    employee_performance_with_level["ResolutionSLAPercentage"]
    - employee_performance_with_level["ExperienceBenchmarkSLA"]
).round(2)

print("\nEMPLOYEE PERFORMANCE VS EXPERIENCE BENCHMARK")
print("=" * 60)

print(
    employee_performance_with_level[
        [
            "EmployeeID",
            "ExperienceLevel",
            "TicketsHandled",
            "ResolutionSLAPercentage",
            "ExperienceBenchmarkSLA",
            "SLA Difference vs Benchmark"
        ]
    ].to_string()
)

print("\nEXPERIENCE AND COMPLEXITY PERFORMANCE BENCHMARK")
print("=" * 60)

experience_complexity_benchmark = (
    employee_analysis
    .groupby(["ExperienceLevel", "Complexity"])["SLAMet"]
    .mean()
    .mul(100)
    .round(2)
    .unstack()
)

print(experience_complexity_benchmark)

print("\nEMPLOYEE PERFORMANCE BY EXPERIENCE LEVEL AND COMPLEXITY")
print("=" * 60)

employee_complexity_performance = (
    employee_analysis
    .groupby(
        ["EmployeeID", "ExperienceLevel", "Complexity"]
    )
    .agg(
        TicketsHandled=("TicketID", "count"),
        ResolutionSLAPercentage=("SLAMet", "mean")
    )
    .reset_index()
)

# Convert SLA to percentage
employee_complexity_performance["ResolutionSLAPercentage"] = (
    employee_complexity_performance["ResolutionSLAPercentage"]
    * 100
).round(2)

print(employee_complexity_performance.head(15).to_string())

# Convert benchmark table into a DataFrame

benchmark_lookup = (
    experience_complexity_benchmark
    .stack()
    .reset_index(name="ExperienceComplexityBenchmark")
)

print("\nEXPERIENCE + COMPLEXITY BENCHMARK LOOKUP")
print("=" * 60)
print(benchmark_lookup)

employee_complexity_performance = (
    employee_complexity_performance
    .merge(
        benchmark_lookup,
        on=["ExperienceLevel", "Complexity"],
        how="left"
    )
)

employee_complexity_performance["PerformanceDifference"] = (
    employee_complexity_performance["ResolutionSLAPercentage"]
    - employee_complexity_performance["ExperienceComplexityBenchmark"]
).round(2)

print("\nEMPLOYEE PERFORMANCE VS EXPERIENCE + COMPLEXITY BENCHMARK")
print("=" * 60)

print(employee_complexity_performance.head(20).to_string())

print("\nWEIGHTED ADJUSTED EMPLOYEE PERFORMANCE")
print("=" * 60)

weighted_employee_performance = (
    employee_complexity_performance.groupby(["EmployeeID", "ExperienceLevel"])
    .apply(lambda group: pd.Series({
        "TicketsHandled": group["TicketsHandled"].sum(),
        "WeightedPerformanceDifference": ((group["PerformanceDifference"] * group["TicketsHandled"])
        .sum() / group["TicketsHandled"].sum())
    })).reset_index()
)

weighted_employee_performance["WeightedPerformanceDifference"] = (
    weighted_employee_performance["WeightedPerformanceDifference"].round(2)
)

print(weighted_employee_performance)

adjusted_ranking = (weighted_employee_performance.sort_values("WeightedPerformanceDifference",
        ascending=False
    )
)

print("\nTOP 10 EMPLOYEES BY ADJUSTED PERFORMANCE")
print("=" * 60)

print(adjusted_ranking.head(10))

print("\nBOTTOM 10 EMPLOYEES BY ADJUSTED PERFORMANCE")
print("=" * 60)

print(adjusted_ranking.tail(10))

# ==================================================
# RAW VS ADJUSTED EMPLOYEE PERFORMANCE RANKING
# ==================================================

raw_employee_ranking = (employee_performance.reset_index().sort_values("ResolutionSLAPercentage",
        ascending=False).reset_index(drop=True))

raw_employee_ranking["RawSLARank"] = (raw_employee_ranking.index + 1)

adjusted_rank = (adjusted_ranking.reset_index(drop=True).copy())

adjusted_rank["AdjustedPerformanceRank"] = (adjusted_rank.index + 1)

ranking_comparison = (raw_employee_ranking[["EmployeeID", "ResolutionSLAPercentage", "RawSLARank"]]
    .merge(adjusted_rank[["EmployeeID", "WeightedPerformanceDifference", "AdjustedPerformanceRank"]],
        on="EmployeeID",how="inner"))

ranking_comparison["RankChange"] = (ranking_comparison["RawSLARank"]
                                    - ranking_comparison["AdjustedPerformanceRank"])

print("\nRAW SLA RANK VS ADJUSTED PERFORMANCE RANK")
print("=" * 60)

print(
    ranking_comparison
    .sort_values("RankChange", ascending=False).to_string()
)
