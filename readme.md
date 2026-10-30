# TalentPulse Analytics

## Enterprise Recruitment Support Analytics Platform

## 📌 Project Overview

TalentPulse Analytics is an end-to-end Business Intelligence project that simulates the support operations of a fictional HR SaaS company.

The project demonstrates how Python, SQL Server, and Power BI can work together to generate, validate, analyze, and visualize enterprise customer support ticket data.

Rather than relying on a publicly available dataset, the project uses synthetic operational data generated through configurable business rules. These rules model customer plans, ticket priorities, service-level agreements (SLAs), ticket complexity, employee experience, and ticket lifecycle behavior.

The objective is to transform simulated operational data into meaningful business insights that support data-driven decision-making.

## 🎯 Business Problem

Customer support managers need visibility into operational performance to understand whether service targets are being met, workloads are distributed effectively, and tickets are being resolved efficiently.

This project addresses business questions related to:

- SLA compliance and breach rates
- Ticket volume and trends
- Ticket priority and complexity
- Department workload distribution
- Customer plan-based ticket demand
- Employee assignment and experience
- Ticket lifecycle distribution
- First-response and resolution performance

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Synthetic data generation, business rules, and data-quality validation |
| Pandas | Data manipulation and CSV processing |
| SQL Server | Relational data storage and SQL-based analysis |
| SQL | Data exploration, joins, aggregations, CTEs, subqueries, and window functions |
| Power BI Desktop | Interactive reporting, KPI monitoring, and visual analysis |
| Power Query | Data loading and transformation |
| Git and GitHub | Version control and portfolio sharing |

## 📊 Dataset Overview

The V3 simulation generates **31,818 support tickets** across 731 calendar days.

- Simulation period: January 1, 2024 – December 31, 2025
- Ticket records: 31,818
- Ticket fields: 17
- Customer master: 500 customers
- Employee master: 60 employees
- Category master: 10 categories
- Department master: 5 departments

The generated ticket dataset is stored in `data/tickets_v3_full_simulation.csv`.

The project also maintains customer, employee, category, and other supporting master data.

## ⚙️ Simulation Engine

The Python simulation generates tickets day by day using configurable business rules.

The simulation includes:

- Daily ticket volumes that vary by weekday
- Lower ticket volumes on weekends
- Customer selection weighted by customer plan
- Priority assignment using configured probabilities
- Ticket creation timestamps within configured business-hour blocks
- Category-based department assignment
- Employee selection from the responsible department
- Employee experience classification
- SLA targets based on customer plan and priority
- First-response and resolution duration calculations
- Ticket lifecycle selection based on priority and complexity
- Ticket ID generation and ticket validation

### Customer Demand Weighting

Customer selection uses plan-based demand factors:

| Customer plan | Demand factor |
|---|---:|
| Basic | 0.80 |
| Professional | 1.00 |
| Enterprise | 1.30 |

These factors influence the relative probability of selecting customers during ticket generation.

### Ticket Priority Distribution

The configured priority probabilities are:

| Priority | Probability |
|---|---:|
| Low | 35% |
| Medium | 40% |
| High | 20% |
| Critical | 5% |

These are generation settings, not a guarantee that the realized dataset will match those percentages exactly.

### Ticket Lifecycle

The simulation supports the following lifecycle classifications:

- Simple
- Waiting Customer
- Escalated
- Reopened

Lifecycle probabilities vary according to ticket priority and complexity.

### Reproducibility

The simulation uses a configured random seed to support reproducible data generation. Python's random generator and a shared NumPy random-number generator control the random operations.

A repeatability test confirmed that two generated V3 datasets matched across all 31,818 rows and 17 columns under the tested configuration.

## 🧹 Data Quality and Validation

The project includes a Python data-quality script to validate the generated dataset.

Implemented checks include:

- Duplicate ticket IDs
- Missing values
- Invalid ticket creation timestamps
- Ticket creation dates outside the simulation period
- Invalid timestamp sequences
- Invalid customer, category, and employee references
- Category-to-department consistency
- Employee-to-department consistency
- Complexity and priority validation

The latest recorded validation result was **PASS**, with zero errors reported by the implemented checks.

## 🗄️ SQL Server Database

The project stores its operational data in a SQL Server database named `EnterpriseCustomerSupport`.

The current database contains these six tables:

- `dbo.Tickets`
- `dbo.Customers`
- `dbo.Employees`
- `dbo.Departments`
- `dbo.Categories`
- `dbo.Statuses`

The SQL scripts cover foundational database exploration and setup, along with analytical SQL concepts.

### SQL Concepts Practised

- SELECT, WHERE, ORDER BY, and TOP
- Aggregate functions and GROUP BY
- INNER JOIN and other join patterns
- Self-joins for learning hierarchical relationships
- CASE expressions
- Common Table Expressions (CTEs)
- Subqueries and correlated subqueries
- EXISTS and NOT EXISTS
- Window functions, including LAG, LEAD, and ranking functions
- Running totals and comparative analysis
- UNION ALL, INTERSECT, and EXCEPT

Some queries are retained as learning exercises and may require hypothetical columns or a different schema from the current database.

## 📈 Power BI Dashboard

The project includes a four-page interactive Power BI report.

### 1. Executive Overview

Provides a high-level view of ticket volume, SLA performance, priority distribution, ticket lifecycle, department workload, customer plan distribution, and recent tickets.

### 2. Ticket Analysis

Supports analysis of ticket patterns and operational distributions.

### 3. SLA Performance

Focuses on SLA compliance, breaches, and service performance.

### 4. Ticket Details

Provides a detailed view of individual ticket records.

The report includes filters for dimensions such as department, employee, category, customer, priority, and date.

### Executive Overview — Validated KPIs

The following baseline figures have been independently checked against SQL Server:

| KPI | Result |
|---|---:|
| Total tickets | 31,818 |
| SLA met | 23,421 |
| SLA breached | 8,397 |
| SLA compliance | 73.61% |
| SLA breach rate | 26.39% |
| Critical tickets | 1,616 |

These values represent the full-dataset baseline and can change when report filters are applied.

## 📁 Project Structure

The project is organized into Python scripts, data files, SQL scripts, documentation, and Power BI assets.

```text
Enterprise-Customer-Support-Analytics/
│
├── data/
│   ├── customers.csv
│   ├── categories.csv
│   ├── employees.csv
│   └── tickets_v3_full_simulation.csv
│
├── docs/
│   └── simulation_versions.md
│
├── powerbi/
│   └── Power BI report and related assets
│
├── python/
│   ├── config.py
│   ├── business_rules.py
│   ├── ticket_generator.py
│   ├── simulation.py
│   ├── data_quality.py
│   └── other Python modules
│
├── sql/
│   ├── database setup scripts
│   └── SQL analysis scripts
│
└── readme.md
```

*The tree highlights the main project areas. Verify individual filenames against the current repository before publishing.*

## 🚀 Running the Python Simulation

1. Clone or download the repository.
2. Create and activate a Python virtual environment.
3. Install the required Python dependencies.
4. Confirm that the master data files are available in the `data/` directory.
5. Run the simulation from the `python/` directory:

```bash
python simulation.py
```

The simulation writes the generated tickets to `data/tickets_v3_full_simulation.csv`.

**Warning:** Running the simulation overwrites that output file. Back up any dataset you want to preserve before regenerating it.

To run the implemented data-quality checks:

```bash
python data_quality.py
```

## 🔮 Future Enhancements

The following are potential extensions, not claims about the current implementation:

- Implement a detailed `TicketHistory` event table
- Analyze time spent in each ticket status
- Track agent handoffs and escalation paths
- Add customer satisfaction scores
- Incorporate holidays and special-event demand patterns
- Introduce more advanced workload forecasting
- Add deeper process bottleneck and lifecycle analysis

## 📌 Current Project Status

- [x] Synthetic master data generation
- [x] Configurable ticket simulation
- [x] Customer plan-based demand weighting
- [x] Priority, SLA, and lifecycle business rules
- [x] Ticket validation and data-quality checks
- [x] Reproducibility test
- [x] SQL Server database and analytical SQL scripts
- [x] Four-page Power BI dashboard
- [x] Executive Overview KPI reconciliation with SQL Server
- [x] Simulation version documentation
- [ ] Final README and repository review
- [ ] Final portfolio packaging and end-to-end handoff

## 🎯 Project Objective

This project demonstrates practical skills in synthetic data generation, Python, SQL, data validation, data modeling, Power BI reporting, and translating operational data into business insights.

It is designed as a hands-on analytics portfolio project that combines data engineering, SQL analysis, and Business Intelligence reporting in one end-to-end workflow.