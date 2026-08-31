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