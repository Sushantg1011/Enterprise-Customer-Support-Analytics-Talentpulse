import pandas as pd
from business_rules import get_sla_hours

#Load datasets
tickets = pd.read_csv("../data/tickets_v3_full_simulation.csv",
                      parse_dates=["CreatedAt", "FirstResponseAt", "ResolvedAt"])

customers = pd.read_csv("../data/customers.csv")
categories = pd.read_csv("../data/categories.csv")
employees = pd.read_csv("../data/employees.csv")

print("\nFULL DATASET VALIDATION")
print("=" * 50)

print(f"Total Tickets: {len(tickets):,}")
print(f"Unique Ticket IDs: {tickets['TicketID'].nunique():,}")

print("\nMISSING VALUES")
print("=" * 50)
print(tickets.isnull().sum())

duplicate_ticket_ids = (
    tickets["TicketID"].duplicated().sum()
)

print(f"Duplicate Ticket IDs: {duplicate_ticket_ids:,}")

print("\nMASTER DATA VALIDATION")
print("=" * 50)

#Customer Validation
invalid_customers = ~tickets["CustomerID"].isin(customers["CustomerID"])
print(f"Invalid Customer IDs: {invalid_customers.sum():,}")

#Employee Validation
invalid_employees = ~tickets["EmployeeID"].isin(employees["EmployeeID"])
print(f"Invalid Employee IDs: {invalid_employees.sum():,}")

#Category Validation
invalid_categories = ~tickets["CategoryID"].isin(categories["CategoryID"])
print(f"Invalid Category IDs: {invalid_categories.sum():,}")

#Category - Department Validation
category_department = categories[["CategoryID", "DepartmentID"]].rename(
    columns={"DepartmentID": "ExpectedDepartmentID"})

category_check = tickets.merge(category_department, on="CategoryID", how="left")

invalid_category_department = (
    category_check["DepartmentID"] != category_check["ExpectedDepartmentID"]).sum()

print(f"Invalid Category-Department IDs: {invalid_category_department:,}")

#Employee - Department Validation
employee_department = employees[["EmployeeID", "DepartmentID"]].rename(
    columns={"DepartmentID": "EmployeeDepartmentID"}
)

employee_check = tickets.merge(employee_department, on="EmployeeID", how="left")
invalid_employee_department = (
    employee_check["DepartmentID"] != employee_check["EmployeeDepartmentID"]).sum()
print(f"Invalid Employee-Department IDs: {invalid_employee_department:,}")

#Complexity Validation
category_complexity = categories[["CategoryID","Complexity"]].rename(
    columns={"Complexity": "ExpectedComplexity"})
complexity_check = tickets.merge(category_complexity, on="CategoryID", how="left")

invalid_complexity = (complexity_check["Complexity"] != complexity_check["ExpectedComplexity"]).sum()
print(f"Invalid Complexity: {invalid_complexity:,}")

print("\nTIMESTAMPS AND DURATION VALIDATION")
print("=" * 50)

# First response Duration validation
calculated_response_hours = (tickets["FirstResponseAt"] - tickets["CreatedAt"]
                             ).dt.total_seconds() / 3600

invalid_response_duration = ((calculated_response_hours - tickets["FirstResponseHours"]).abs()
                             > 0.001).sum()
print(f"Invalid Response Duration: {invalid_response_duration:,}")

#Resolution Duration Validation
calculated_resolution_hours = (tickets["ResolvedAt"] - tickets["CreatedAt"]
                               ).dt.total_seconds() / 3600
invalid_resolution_duration = ((calculated_resolution_hours - tickets["ResolutionHours"]).abs()
                               > 0.001).sum()
print(f"Invalid Resolution Duration: {invalid_resolution_duration:,}")

#Timestamp Relationship Validation
invalid_first_response_timestamp = (
    tickets["FirstResponseAt"] < tickets["CreatedAt"]
    ).sum()

invalid_resolved_timestamp = (
    tickets["ResolvedAt"] < tickets["CreatedAt"]
).sum()

invalid_response_after_resolution = (
    tickets["FirstResponseAt"] > tickets["ResolvedAt"]
).sum()

print(
    f"First Response Before CreatedAt: "
    f"{invalid_first_response_timestamp:,}"
)

print(
    f"Resolved Before CreatedAt: "
    f"{invalid_resolved_timestamp:,}"
)

print(
    f"First Response After Resolution: "
    f"{invalid_response_after_resolution:,}"
)

print("\nSLA HOURS VALIDATION")
print("=" * 50)

#Merge customer plan into tickets
sla_validation = tickets.merge(
    customers[["CustomerID", "Plan"]],
    on="CustomerID",
    how="left"
)

#Calculate expected SLA Hours
sla_validation["ExpectedSLAHours"] = sla_validation.apply(
    lambda row: get_sla_hours(
        row["Plan"],
        row["Priority"]),
    axis=1
)

#Identify invalid SLA Hours
invalid_sla_hours = (
    sla_validation["SLAHours"] != sla_validation["ExpectedSLAHours"]
).sum()

#Calculate expected SLA Status
sla_validation["ExpectedSLAMet"] = (sla_validation["ResolutionHours"]
                                    <= sla_validation["SLAHours"])

#Identify incorrect SLA status
invalid_sla_status = (sla_validation["SLAMet"] != sla_validation["ExpectedSLAMet"]).sum()


print(f"Invalid SLA Hours: {invalid_sla_hours:,}")
print(f"Invalid SLA Status: {invalid_sla_status:,}")

#First response SLA Validation
print("\nFIRST RESPONSE SLA VALIDATION")
print("=" * 50)

#Calculate expected first response SLA status
tickets["ExpectedFirstResponseSLAMet"] = (tickets["FirstResponseHours"]
                                          <= tickets["SLAHours"])

#Count invalid first response SLA status
invalid_first_response_sla = (tickets["FirstResponseSLAMet"]
                                != tickets["ExpectedFirstResponseSLAMet"]).sum()

print(f"Invalid First Response SLA Status: {invalid_first_response_sla:,}")

# Final Validation Summary

total_errors = (
    duplicate_ticket_ids
    + invalid_customers.sum()
    + invalid_employees.sum()
    + invalid_categories.sum()
    + invalid_category_department
    + invalid_employee_department
    + invalid_complexity
    + invalid_response_duration
    + invalid_resolution_duration
    + invalid_first_response_timestamp
    + invalid_resolved_timestamp
    + invalid_response_after_resolution
    + invalid_sla_hours
    + invalid_sla_status
    + invalid_first_response_sla
)

print("\nFINAL VALIDATION STATUS")
print("=" * 50)

if total_errors == 0:
    print("FULL DATASET VALIDATION STATUS: PASS")
else:
    print("FULL DATASET VALIDATION STATUS: FAIL")
    print(f"Total Validation Errors: {total_errors:,}")