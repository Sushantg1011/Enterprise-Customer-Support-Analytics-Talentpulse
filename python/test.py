from business_rules import get_resolution_hours

hard_ticket = get_resolution_hours("Hard", "Critical", "Enterprise",
                             "Senior", "Escalated")


easy_ticket = get_resolution_hours(
    "Easy",
    "Low",
    "Basic",
    "Junior",
    "Simple"
)

print("Easy/Low/Basic/Junior/Simple:", round(easy_ticket, 2))
print("Hard/Critical/Enterprise/Senior/Escalated:", round(hard_ticket, 2))
