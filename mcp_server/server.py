from fastapi import FastAPI
from pydantic import BaseModel

from mcp_server.tools.destination import get_destination_info
from mcp_server.tools.itinerary import generate_plan
from mcp_server.tools.images import get_image

app = FastAPI()


class ToolRequest(BaseModel):
    tool: str
    args: dict


@app.get("/")
def home():
    return {"status": "MCP server running"}


@app.post("/tool")
def run_tool(req: ToolRequest):

    if req.tool == "destination_info":
        return get_destination_info(req.args.get("destination"))

    elif req.tool == "generate_plan":
        return generate_plan(
            destination=req.args.get("destination"),
            budget=req.args.get("budget"),
            days=req.args.get("days")
        )

    elif req.tool == "get_image":
        return get_image(req.args.get("destination"))

    return {"error": "Unknown tool"}
