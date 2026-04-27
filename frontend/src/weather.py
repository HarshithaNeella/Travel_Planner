"""
weather.py - Fetch live weather using Open-Meteo (free, no API key needed)
Geocoding via Open-Meteo geocoding API.
"""

import requests


WMO_CODES = {
    0: "Clear sky ☀️",
    1: "Mainly clear 🌤️", 2: "Partly cloudy ⛅", 3: "Overcast ☁️",
    45: "Foggy 🌫️", 48: "Icy fog 🌫️",
    51: "Light drizzle 🌦️", 53: "Moderate drizzle 🌦️", 55: "Dense drizzle 🌧️",
    61: "Slight rain 🌧️", 63: "Moderate rain 🌧️", 65: "Heavy rain 🌧️",
    71: "Slight snow 🌨️", 73: "Moderate snow 🌨️", 75: "Heavy snow ❄️",
    80: "Rain showers 🌦️", 81: "Moderate showers 🌧️", 82: "Violent showers ⛈️",
    95: "Thunderstorm ⛈️", 96: "Thunderstorm with hail ⛈️",
}


def _geocode(destination: str) -> tuple[float, float, str] | None:
    try:
        url = "https://geocoding-api.open-meteo.com/v1/search"
        params = {"name": destination, "count": 1, "language": "en", "format": "json"}
        resp = requests.get(url, params=params, timeout=6)
        results = resp.json().get("results", [])
        if results:
            r = results[0]
            return r["latitude"], r["longitude"], r.get("name", destination)
    except Exception:
        pass
    return None


def get_weather(destination: str) -> dict:
    """
    Fetch current weather for destination.
    Returns dict with: temperature, feels_like, condition, wind_speed, humidity,
                       weather_note, source
    """
    coords = _geocode(destination)
    if not coords:
        return {
            "destination": destination,
            "source": "unavailable",
            "weather_note": "Weather data unavailable for this destination.",
        }

    lat, lon, resolved_name = coords
    try:
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,apparent_temperature,weather_code,wind_speed_10m,relative_humidity_2m",
            "timezone": "auto",
        }
        resp = requests.get(url, params=params, timeout=6)
        data = resp.json()
        current = data.get("current", {})

        temp = current.get("temperature_2m")
        feels = current.get("apparent_temperature")
        wmo = current.get("weather_code", 0)
        wind = current.get("wind_speed_10m")
        humidity = current.get("relative_humidity_2m")
        condition = WMO_CODES.get(wmo, "Unknown")

        # Generate travel note
        if wmo in (0, 1, 2):
            note = f"🌤️ Weather is pleasant in {resolved_name} — great for sightseeing and outdoor activities."
        elif wmo in (61, 63, 65, 80, 81, 82):
            note = f"🌧️ Rain expected in {resolved_name} — carry an umbrella and plan a mix of indoor visits."
        elif wmo in (71, 73, 75):
            note = f"❄️ Snowfall in {resolved_name} — pack warm clothes and check road conditions."
        elif wmo == 95:
            note = f"⛈️ Thunderstorms in {resolved_name} — stay indoors during peak storm hours."
        elif temp and temp > 35:
            note = f"🥵 It's very hot in {resolved_name} ({temp}°C) — avoid midday sun and stay hydrated."
        else:
            note = f"Weather in {resolved_name}: {condition}, {temp}°C."

        return {
            "destination": resolved_name,
            "temperature_c": temp,
            "feels_like_c": feels,
            "condition": condition,
            "wind_kmh": wind,
            "humidity_pct": humidity,
            "weather_note": note,
            "source": "open-meteo",
        }
    except Exception as e:
        return {
            "destination": destination,
            "source": "error",
            "weather_note": "Could not fetch live weather. Plan for varied conditions.",
        }
