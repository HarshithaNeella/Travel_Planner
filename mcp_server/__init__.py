from fastapi import FastAPI

from mcp_server.tools.destination import get_destination_info
from mcp_server.tools.budget import estimate_days
from mcp_server.tools.itinerary import generate_plan

app = FastAPI()


@app.post("/tool")
def run_tool(payload: dict):
    tool = payload.get("tool")
    args = payload.get("args", {})

    if tool == "get_destination_info":
        return get_destination_info(**args)

    elif tool == "estimate_days":
        return estimate_days(**args)

    elif tool == "generate_plan":
        return generate_plan(**args)

    return {"error": "Invalid tool"}