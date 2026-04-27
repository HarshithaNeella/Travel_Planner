import requests
import os

"""
itinerary.py - Fetch real places using Geoapify Places API
"""

import os
import requests
from dotenv import load_dotenv
load_dotenv()

POPULAR_DESTINATIONS = {
    "goa": "Baga Beach Goa",
    "south goa": "Colva Beach Goa",
    "north goa": "Baga Beach Goa",
    "andhra pradesh": "Visakhapatnam",
    "south india": "Bangalore",
}

GEOAPIFY_KEY = os.environ.get("GEOAPIFY_API_KEY", "")

CATEGORY_MAP = {
    "attraction": "tourism.attraction",
    "restaurant": "catering.restaurant",
    "hotel": "accommodation.hotel",
    "shopping": "commercial.shopping_mall",
    "park": "leisure.park",
    "museum": "tourism.attraction.museum",
    "beach": "beach",
    "temple": "religion",
}


def _geocode(destination: str) -> tuple[float, float] | None:
    """Get lat/lon for a destination name."""
    try:
        print(f"[DEBUG] Geocoding destination: {destination}")
        url = "https://api.geoapify.com/v1/geocode/search"
        search_query = POPULAR_DESTINATIONS.get(destination.lower(), destination)

        print(f"[DEBUG] Using search query: {search_query}")

        params = {
            "text": search_query,
            "limit": 1,
            "apiKey": GEOAPIFY_KEY
        }
        resp = requests.get(url, params=params, timeout=8)
        data = resp.json()
        feat = data.get("features", [])
        if feat:
            lon, lat = feat[0]["geometry"]["coordinates"]
            return lat, lon
    except Exception:
        pass
    return None


def _fetch_places(lat: float, lon: float, category: str, limit: int = 5) -> list[dict]:
    """Fetch places of a given category near lat/lon."""
    try:
        print(f"[DEBUG] Fetching {category} near {lat},{lon}")
        url = "https://api.geoapify.com/v2/places"
        params = {
            "categories": CATEGORY_MAP.get(category, "tourism.attraction"),
            "filter": f"circle:{lon},{lat},5000",
            "limit": limit,
            "apiKey": GEOAPIFY_KEY,
        }
        resp = requests.get(url, params=params, timeout=8)
        data = resp.json()
        places = []
        for feat in data.get("features", []):
            props = feat.get("properties", {})
            name = props.get("name") or props.get("address_line1", "")
            if name:
                places.append({
                    "name": name,
                    "category": category,
                    "address": props.get("formatted", ""),
                    "city": props.get("city", ""),
                })
        print(f"[DEBUG] Found {len(places)} {category}")
        return places
    except Exception:
        print("[DEBUG] Places ERROR:", str())
        return []


def get_places_for_itinerary(destination: str, days: int) -> dict:
    """
    Fetch attractions, restaurants for each day of the trip.
    Returns dict with: places (list), days, destination, source
    """
    print(f"[DEBUG] get_places_for_itinerary called for: {destination}")

    coords = _geocode(destination)

    if not coords or not GEOAPIFY_KEY:
        # Fallback: generic place names so the trip still generates
        return {
            "destination": destination,
            "days": days,
            "source": "fallback",
            "places": [
                {"name": f"Popular Attraction {i+1} in {destination}", "category": "attraction", "address": ""}
                for i in range(days * 2)
            ],
        }

    lat, lon = coords
    attractions = _fetch_places(lat, lon, "attraction", limit=min(days * 2, 10))
    restaurants = _fetch_places(lat, lon, "restaurant", limit=min(days, 5))

    all_places = attractions + restaurants
    print("[DEBUG] Returning REAL Geoapify data ✅")
    return {
        "destination": destination,
        "days": days,
        "source": "geoapify",
        "coordinates": {"lat": lat, "lon": lon},
        "attractions": attractions,
        "restaurants": restaurants,
        "places": all_places,
    }
