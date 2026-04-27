"""
budget.py - Estimate number of days from a given budget
"""


def estimate_days_from_budget(budget: int, destination: str = "") -> dict:
    """
    Given a total budget (INR) and destination, estimate feasible trip duration.
    Returns a dict with: suggested_days, daily_budget, note
    """
    # Rough daily cost tiers (INR) based on destination type
    dest_lower = destination.lower()

    if any(k in dest_lower for k in ["dubai", "paris", "london", "new york", "singapore", "tokyo"]):
        daily_cost = 8000
        tier = "international luxury"
    elif any(k in dest_lower for k in ["bali", "bangkok", "nepal", "sri lanka", "vietnam"]):
        daily_cost = 4000
        tier = "international budget"
    elif any(k in dest_lower for k in ["goa", "kerala", "rajasthan", "manali", "shimla", "ooty"]):
        daily_cost = 2500
        tier = "domestic popular"
    else:
        daily_cost = 2000
        tier = "domestic standard"

    suggested_days = max(1, budget // daily_cost)
    daily_budget = budget // max(suggested_days, 1)

    return {
        "suggested_days": suggested_days,
        "daily_budget": daily_budget,
        "cost_tier": tier,
        "note": (
            f"With ₹{budget:,} for {destination or 'this destination'}, "
            f"a comfortable {suggested_days}-day trip is feasible "
            f"(~₹{daily_budget:,}/day, {tier} tier)."
        ),
    }
