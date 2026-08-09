from faker import Faker
import pandas as pd
import random
import os


fake = Faker()

# ----------------------------
# Create folders
# ----------------------------
os.makedirs("../data", exist_ok=True)

# ----------------------------
# Departments
# ----------------------------
departments = [
    "Technical Support",
    "Billing Support",
    "Recruitment Support",
    "Product Support",
    "API Support"
]

df_departments = pd.DataFrame({
    "DepartmentID": range(1, len(departments)+1),
    "DepartmentName": departments
})

# ----------------------------
# Employees
# ----------------------------
employees = []

for emp_id in range(1, 61):
    employees.append({
        "EmployeeID": emp_id,
        "EmployeeName": fake.name(),
        "DepartmentID": random.randint(1, 5),
        "ExperienceYears": random.randint(1, 12)
    })

df_employees = pd.DataFrame(employees)

# ----------------------------
# Customers
# ----------------------------
plans = ["Basic", "Professional", "Enterprise"]

industries = [
    "IT",
    "Healthcare",
    "Retail",
    "Banking",
    "Education",
    "Manufacturing"
]

customers = []

for cust_id in range(1, 501):
    customers.append({
        "CustomerID": cust_id,
        "CustomerName": fake.company(),
        "Industry": random.choice(industries),
        "Country": fake.country(),
        "Plan": random.choice(plans)
    })

df_customers = pd.DataFrame(customers)

# ----------------------------
# Categories
# ----------------------------
categories = [
    (1, "Login Issues", "Easy", 1),
    (2, "Job Posting Failure", "Medium", 3),
    (3, "Resume Parsing", "Hard", 3),
    (4, "Billing", "Medium", 2),
    (5, "Interview Scheduling", "Medium", 3),
    (6, "API Error", "Hard", 5),
    (7, "Email Notification", "Easy", 1),
    (8, "Candidate Import", "Medium", 3),
    (9, "Performance Issue", "Hard", 1),
    (10, "Feature Request", "Hard", 4)
]

df_categories = pd.DataFrame(
    categories,
    columns=[
        "CategoryID",
        "CategoryName",
        "Complexity",
        "DepartmentID"
    ]
)

# ----------------------------
# Save Files
# ----------------------------
df_departments.to_csv("../data/departments.csv", index=False)
df_employees.to_csv("../data/employees.csv", index=False)
df_customers.to_csv("../data/customers.csv", index=False)
df_categories.to_csv("../data/categories.csv", index=False)

print("✅ Master data generated successfully!")