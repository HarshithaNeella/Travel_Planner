import requests
import os


def get_coordinates(city):
    url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text": city,
        "apiKey": os.getenv("GEOAPIFY_API_KEY")
    }

    res = requests.get(url, params=params)
    data = res.json()

    if data.get("features"):
        coords = data["features"][0]["geometry"]["coordinates"]
        return coords[1], coords[0]

    return None, None


def generate_plan(destination=None, budget=None, days=None):

    lat, lon = get_coordinates(destination)

    if not lat:
        return {"plan": f"❌ Could not find location for {destination}"}

    url = "https://api.geoapify.com/v2/places"

    params = {
        "categories": "tourism.sights",
        "filter": f"circle:{lon},{lat},5000",
        "limit": 15,
        "apiKey": os.getenv("GEOAPIFY_API_KEY")
    }

    res = requests.get(url, params=params)
    data = res.json()

    # ✅ CLEAN FILTER
    places = list(set([
        p["properties"].get("name")
        for p in data.get("features", [])
        if p["properties"].get("name")
        and len(p["properties"].get("name")) > 3
    ]))

    if not places:
        return {"plan": f"⚠️ No places found for {destination}"}

    # ✅ RAW SIMPLE PLAN (LLM WILL FIX THIS)
    plan = f"{destination.title()} trip places:\n"

    for i, place in enumerate(places[:days * 3]):
        plan += f"{i+1}. {place}\n"

    return {"plan": plan}
