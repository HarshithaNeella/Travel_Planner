def estimate_days(destination: str, budget: int):
    avg_cost = 1500
    days = max(1, budget // avg_cost)
    return {"days": days}
