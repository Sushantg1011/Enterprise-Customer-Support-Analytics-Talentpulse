# Simulation Versions

## V1 — Baseline

- Random customer selection
- Random category selection
- Random priority based on configured weights
- SLA based on customer plan + priority
- 31,903 tickets
- Used as baseline dataset

## V2 — Demand Weighted

- Customer selection weighted by customer plan
- Basic demand factor: 0.80
- Professional demand factor: 1.00
- Enterprise demand factor: 1.30
- Enterprise customers generate approximately 45% of tickets
- Used as improved business simulation

## V3 — Full Business Simulation

- Simulates daily ticket generation from January 1, 2024, to December 31, 2025.
- Daily ticket volume varies by weekday, with lower volumes on weekends.
- Customer selection is weighted by plan: Basic (0.80), Professional (1.00), and Enterprise (1.30).
- Ticket priorities follow configured probabilities: Low (35%), Medium (40%), High (20%), and Critical (5%).
- Ticket creation times are generated within configured business-hour blocks.
- Ticket categories determine the responsible department and eligible employee pool.
- Ticket creation dates fall within the simulation period; response and resolution timestamps may extend beyond the period end.
- Employee experience is classified as Junior, Mid, or Senior based on years of experience.
- SLA targets depend on customer plan and ticket priority.
- First-response times use priority-specific breach probabilities and response-time factors.
- Resolution times incorporate ticket complexity, priority, customer plan, employee experience, lifecycle, and random variation.
- Ticket lifecycles include Simple, Waiting Customer, Escalated, and Reopened, with probabilities influenced by priority and complexity.
- Generated tickets are validated against master data and business rules before being saved.
- Output dataset: tickets_v3_full_simulation.csv
- Generated dataset contains 31,818 tickets.
- Used as the full business-rule-driven simulation dataset for analytics.