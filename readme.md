# TalentPulse Analytics

## Enterprise Recruitment Support Analytics Platform

## 📌 Project Overview

TalentPulse Analytics is an end-to-end Business Intelligence project that simulates the support operations of a fictional HR SaaS company.

The project demonstrates how Python, SQL, and Power BI can be used together to generate, model, analyze, and visualize enterprise support ticket data.

Instead of using publicly available datasets, this project generates realistic operational data using business rules that mimic real-world support environments.

---

## 🎯 Business Problem

Support managers need visibility into:

- SLA compliance
- Agent performance
- Ticket backlog
- Customer satisfaction
- Resolution trends
- Department workload

The goal of this project is to build an analytics platform that enables better operational decision-making.

---

## 🛠 Tech Stack

- Python
- Pandas
- SQLite (later SQL Server)
- SQL
- Power BI
- Git & GitHub

---

## 🧩 Simulation Assumptions

The synthetic dataset is generated using configurable business rules rather than random values.

Current simulation includes:

- Ticket priorities
- Customer SLA plans
- Ticket complexity
- Department ownership
- Employee assignment
- Agent experience factors
- Customer plan factors
- Weekly ticket volume patterns
- Monday login issue spikes

---

## 🏗️ Data Model Design

The project follows a dimensional model with additional event-based tracking.

### Core Tables

- FactTickets
- DimCustomer
- DimEmployee
- DimDepartment
- DimCategory
- DimPriority
- DimDate

### Event Tracking

A separate `TicketHistory` table will capture every ticket lifecycle event (Created, Assigned, In Progress, Waiting for Customer, Resolved, Closed).

This design enables advanced analytics such as:

- Time spent in each status
- Reopened ticket analysis
- Agent handoffs
- Process bottleneck analysis
- SLA stage-level monitoring

---

## 🔄 Ticket Lifecycle

Each ticket progresses through multiple operational stages.

Typical lifecycle:

Created → Assigned → In Progress → Waiting for Customer → Resolved → Closed

Some tickets may also:

- Escalate to another team
- Be reopened after resolution
- Return to "In Progress" after customer response

A separate TicketHistory table stores every status transition, enabling stage-level performance analysis.

---

## 🎫 Ticket Lifecycle Simulation

The project simulates multiple ticket lifecycles instead of assuming every ticket follows the same process.

Current lifecycle scenarios include:

- Standard Resolution
- Waiting for Customer
- Escalation
- Reopened Tickets

This enables process mining, bottleneck analysis, and stage-level SLA reporting.

---

## 📈 Simulation Philosophy

The synthetic data is not generated using independent random values.

Instead, business entities influence one another through predefined relationships.

Examples:

- Customer Plan → SLA
- Ticket Category → Department
- Ticket Complexity → Resolution Time
- Ticket Priority → SLA Compliance
- Lifecycle → Ticket History

This approach creates realistic operational data that supports meaningful analytics.

---

## ⚙️ Simulation Engine

The project uses a configurable simulation engine rather than generating random records.

The simulation is based on business rules such as:

- Daily ticket volume
- Weekly workload patterns
- Ticket lifecycle probabilities
- Customer SLA plans
- Agent experience
- Ticket complexity

This approach produces realistic operational datasets suitable for enterprise analytics.

---

## 🧠 Business Rule Engine

Business behavior is encapsulated into reusable Python functions.

Current rule modules include:

- Daily ticket volume
- Ticket lifecycle selection

Future rules will include:

- Category distribution
- Priority assignment
- Agent assignment
- Customer plan behavior
- Business hours
- Holiday effects

---

## 🗓️ Daily Simulation Engine

The simulator models business operations day by day instead of generating tickets in a single batch.

Benefits:

- Weekly workload patterns
- Weekend ticket reduction
- Holiday effects
- Month-end activity
- Time-series analysis in Power BI

---

### Simulation Workflow

1. Generate simulation dates.
2. Identify the weekday.
3. Apply business rules.
4. Generate daily ticket volume.
5. Create tickets.
6. Generate ticket history.

---

## 🆔 Identifier Strategy

Every ticket receives a globally unique TicketID.

This design prevents duplicate identifiers across simulation days and supports reliable relationships between FactTickets and FactTicketHistory.

Future entities such as TicketHistory will also use unique identifiers linked through foreign keys.

---

## 🚧 Current Progress

- [x] Project Setup
- [x] Master Data Generation
- [x] Customer Dimension
- [x] Employee Dimension
- [x] Department Dimension
- [x] Category Dimension
- [x] Ticket Generation
- [x] Category → Department Assignment
- [ ] Agent Experience Simulation
- [ ] Ticket Generation Engine
- [ ] SQL Database
- [ ] Power BI Dashboard
- [ ] Documentation