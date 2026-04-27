"""
server.py - FastAPI MCP backend
Exposes all travel tools as REST endpoints.
Run with: uvicorn server:app --host 0.0.0.0 --port 8000 --reload
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from src.budget import estimate_days_from_budget
from src.destination import get_destination_info
from src.itinerary import get_places_for_itinerary
from src.images import get_destination_image
from src.weather import get_weather
from src.planner import _build_itinerary
app = FastAPI(title="Smart Travel Planner MCP", version="1.0.0")


# ── Request models ────────────────────────────────────────────────────────────

class BudgetRequest(BaseModel):
    budget: int
    destination: Optional[str] = ""

class DestinationRequest(BaseModel):
    destination: str

class ItineraryRequest(BaseModel):
    destination: str
    days: int

class ImageRequest(BaseModel):
    destination: str

class WeatherRequest(BaseModel):
    destination: str


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "service": "Smart Travel Planner MCP"}


@app.post("/tools/budget")
def tool_budget(req: BudgetRequest):
    try:
        return estimate_days_from_budget(req.budget, req.destination)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/destination")
def tool_destination(req: DestinationRequest):
    try:
        return get_destination_info(req.destination)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/itinerary")
def tool_itinerary(req: ItineraryRequest):
    try:
        return get_places_for_itinerary(req.destination, req.days)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/image")
def tool_image(req: ImageRequest):
    try:
        return get_destination_image(req.destination)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/tools/weather")
def tool_weather(req: WeatherRequest):
    try:
        return get_weather(req.destination)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Composite endpoint ────────────────────────────────────────────────────────

class PlanRequest(BaseModel):
    destination: str
    days: int
    budget: int
    members: int

@app.post("/tools/plan_data")
def tool_plan_data(req: PlanRequest):
    """Fetch all data needed for a plan in one call."""
    try:
        places_data = get_places_for_itinerary(req.destination, req.days)
        dest_info = get_destination_info(req.destination)
        weather_data = get_weather(req.destination)
        image_data = get_destination_image(req.destination)
        budget_data = estimate_days_from_budget(req.budget, req.destination)
        return {
            "places": places_data,
            "destination": dest_info,
            "weather": weather_data,
            "image": image_data,
            "budget": budget_data,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
