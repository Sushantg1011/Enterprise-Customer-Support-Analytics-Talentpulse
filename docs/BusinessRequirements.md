# Business Requirements Document (BRD)

## TalentPulse Analytics — Enterprise Recruitment Support Analytics Platform

## 1. Problem Statement

Support managers at the fictional HR SaaS company rely on manually prepared Excel reports to review support operations. This process can delay access to performance information and make it difficult to identify operational issues promptly.

Key challenges include:

- Limited visibility into support performance and ticket trends.
- Delayed identification of SLA breaches.
- Difficulty monitoring workload across departments.
- Limited visibility into ticket priority and lifecycle distribution.
- Time-consuming preparation and review of operational reports.
- Difficulty comparing service performance across customer plans and reporting periods.

This project simulates a support analytics environment and demonstrates how business intelligence can help address these challenges.

## 2. Project Objective

Build an end-to-end Business Intelligence platform that uses Python, SQL Server, and Power BI to generate, validate, analyze, and visualize enterprise customer support data.

The platform aims to provide interactive operational reporting and help stakeholders identify trends, monitor SLA performance, and understand ticket distribution.

The current project uses synthetic data generated through configurable business rules. It does not connect to a live customer support system.

## 3. Stakeholders

The intended stakeholders are:

- **CEO:** High-level visibility into support performance and service delivery.
- **Support Director:** Overview of SLA compliance, ticket trends, and operational performance.
- **Operations Manager:** Monitoring of ticket volume, SLA breaches, and department workload.
- **Team Leads:** Visibility into assigned workload, ticket priorities, and lifecycle patterns.
- **Support Agents:** Potential future use of workload and resolution insights to support operational improvement.

These stakeholders represent the intended audience for the analytics platform.

## 4. Business Requirements

### BR-01: Ticket Volume Monitoring

The platform shall provide visibility into total ticket volume and trends over time.

### BR-02: SLA Performance Monitoring

The platform shall report the number and percentage of tickets meeting or breaching SLA targets.

### BR-03: Priority Analysis

The platform shall allow stakeholders to analyze ticket volume by priority, including Critical, High, Medium, and Low.

### BR-04: Department Workload Analysis

The platform shall provide ticket distribution by department to support workload analysis.

### BR-05: Customer Plan Analysis

The platform shall provide visibility into ticket volume across customer plans: Basic, Professional, and Enterprise.

### BR-06: Ticket Lifecycle Analysis

The platform shall support analysis of ticket lifecycle classifications, including Simple, Waiting Customer, Escalated, and Reopened.

### BR-07: Ticket-Level Investigation

The platform shall provide access to ticket-level details to support investigation of individual records.

### BR-08: Interactive Reporting

The Power BI report shall provide filters for relevant dimensions, including date, department, employee, category, customer, and priority.

### BR-09: Data Quality

The data-generation workflow shall validate ticket identifiers, required values, timestamps, master-data references, and relevant business-rule assignments.

### BR-10: Repeatable Simulation

The Python simulation shall support repeatable data generation when run with the same configuration, source data, and execution sequence.

## 5. Current Solution

The implemented solution consists of three primary layers.

### 5.1 Python Simulation and Validation

Python generates synthetic ticket data using configurable rules covering:

- Daily ticket volume and weekday patterns.
- Customer plan-based demand weighting.
- Ticket priority.
- Category and department assignment.
- Employee selection and experience.
- SLA targets.
- First-response and resolution durations.
- Ticket lifecycle classifications.

The validation script checks data quality before the dataset is used for analysis.

### 5.2 SQL Server and SQL Analysis

SQL Server stores the ticket data and associated master data.

SQL scripts support data exploration, aggregation, joins, subqueries, CTEs, window functions, and operational analysis.

### 5.3 Power BI Reporting

The interactive Power BI report contains four pages:

1. Executive Overview
2. Ticket Analysis
3. SLA Performance
4. Ticket Details

The report provides an overview of ticket volume, SLA performance, priority distribution, department workload, customer plan distribution, lifecycle patterns, and ticket-level details.

## 6. Baseline Success Metrics

The following figures represent the current full-dataset baseline.

| Metric | Baseline |
|---|---:|
| Total tickets | 31,818 |
| Tickets meeting SLA | 23,421 |
| Tickets breaching SLA | 8,397 |
| SLA compliance | 73.61% |
| SLA breach rate | 26.39% |
| Critical tickets | 1,616 |

These values have been reconciled between the Executive Overview in Power BI and the SQL Server database.

## 7. Expected Business Outcomes

The platform is intended to help stakeholders:

- Identify SLA performance trends.
- Understand where ticket volume is concentrated.
- Compare workload across departments.
- Investigate priority and lifecycle distributions.
- Reduce reliance on manually assembled reporting.
- Make more informed operational decisions using consistent metrics.

These are intended benefits. Actual reductions in backlog, resolution time, or SLA breaches have not been demonstrated by the current synthetic-data project.

## 8. Scope

### In Scope

- Synthetic ticket and master-data generation.
- Configurable business rules.
- Data-quality validation.
- SQL Server storage and SQL-based analysis.
- Interactive Power BI reporting.
- Reconciliation of headline KPIs.
- Documentation of the simulation and analytics workflow.

### Out of Scope for the Current Version

- Integration with a live support ticketing system.
- Automated near-real-time ingestion of production tickets.
- A live operational alerting system.
- Direct measurement of customer satisfaction (CSAT).
- A detailed ticket-status event history table.
- Proven reductions in operational backlog or resolution time.
- Production deployment and user access management.

## 9. Assumptions and Limitations

- The company and its support operations are fictional.
- The dataset is synthetic and generated by configured business rules.
- SLA compliance reflects the simulation's defined rules and generated outcomes.
- The current report analyzes the available ticket fields and master data.
- The current dataset does not establish actual customer satisfaction or real-world operational improvements.
- The current simulation period is January 1, 2024, through December 31, 2025, based on ticket creation dates.
- Response and resolution timestamps may extend beyond the ticket creation period.

## 10. Future Enhancements

Potential future improvements include:

- Integrating live ticket data.
- Introducing automated refresh and alerting.
- Creating a detailed ticket lifecycle event-history table.
- Measuring time spent in individual ticket statuses.
- Adding customer satisfaction data.
- Developing workload forecasting and trend analysis.
- Evaluating operational changes against defined baseline metrics.

## 11. Acceptance Criteria

The current project can be considered functionally complete when:

- The Python simulation generates the configured ticket dataset.
- The implemented data-quality checks pass.
- SQL analysis scripts have been reviewed against their intended purpose.
- Power BI headline KPIs reconcile with SQL Server.
- Report pages and filters work as intended.
- Project documentation accurately distinguishes implemented features from planned enhancements.
- Setup and execution instructions are documented for another person to follow.

## 12. Project Success Definition

Success for the current project means delivering a documented, repeatable analytics workflow that demonstrates synthetic data generation, data validation, SQL analysis, and interactive Power BI reporting.

Operational improvements such as reducing actual SLA breaches, backlog, or resolution time would require additional real-world data and evaluation beyond the current project scope.