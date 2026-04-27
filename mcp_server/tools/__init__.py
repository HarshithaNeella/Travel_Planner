from fastapi import FastAPI

from mcp_server.tools.destination import get_destination_info
from mcp_server.tools.budget import estimate_days_from_budget
from mcp_server.tools.itinerary import get_places_for_itinerary

app = FastAPI()


@app.post("/tool")
def run_tool(payload: dict):
    tool = payload.get("tool")
    args = payload.get("args", {})

    if tool == "get_destination_info":
        return get_destination_info(**args)

    elif tool == "estimate_days_from_budget":
        return estimate_days(**args)

    elif tool == "get_places_for_itinerary":
        return generate_plan(**args)

    return {"error": "Invalid tool"}
