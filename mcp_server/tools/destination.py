"""
destination.py - Provides static enriched destination info
"""

DESTINATION_DATA = {
    "goa": {
        "country": "India",
        "region": "West Coast",
        "highlights": ["beaches", "Portuguese architecture", "nightlife", "seafood", "water sports"],
        "best_season": "November to February",
        "currency": "INR",
        "language": "Konkani, English, Hindi",
        "timezone": "IST (UTC+5:30)",
        "tip": "Hire a scooter for easy beach-hopping. North Goa is lively; South Goa is serene.",
    },
    "kerala": {
        "country": "India",
        "region": "South India",
        "highlights": ["backwaters", "houseboats", "spice plantations", "Ayurveda", "hill stations"],
        "best_season": "October to March",
        "currency": "INR",
        "language": "Malayalam, English",
        "timezone": "IST (UTC+5:30)",
        "tip": "Book a houseboat in Alleppey for an unforgettable backwater experience.",
    },
    "rajasthan": {
        "country": "India",
        "region": "North India",
        "highlights": ["forts", "palaces", "desert safari", "folk music", "handicrafts"],
        "best_season": "October to March",
        "currency": "INR",
        "language": "Hindi, Rajasthani",
        "timezone": "IST (UTC+5:30)",
        "tip": "Combine Jaipur, Jodhpur, and Udaipur for the Golden Triangle experience.",
    },
    "manali": {
        "country": "India",
        "region": "Himachal Pradesh",
        "highlights": ["snow peaks", "adventure sports", "Rohtang Pass", "Old Manali cafes", "trekking"],
        "best_season": "March to June, October to December",
        "currency": "INR",
        "language": "Hindi, Pahari",
        "timezone": "IST (UTC+5:30)",
        "tip": "Carry warm layers even in summer. Roads to Rohtang close in heavy snow.",
    },
    "bali": {
        "country": "Indonesia",
        "region": "Southeast Asia",
        "highlights": ["temples", "rice terraces", "surf beaches", "wellness retreats", "nightlife"],
        "best_season": "April to October",
        "currency": "IDR (Indian cards work at ATMs)",
        "language": "Balinese, Indonesian, English",
        "timezone": "WITA (UTC+8)",
        "tip": "Ubud for culture and nature; Seminyak for nightlife; Nusa Penida for adventure.",
    },
    "paris": {
        "country": "France",
        "region": "Western Europe",
        "highlights": ["Eiffel Tower", "Louvre", "Seine cruises", "cuisine", "fashion"],
        "best_season": "April to June, September to November",
        "currency": "EUR",
        "language": "French, English widely spoken",
        "timezone": "CET (UTC+1)",
        "tip": "Get a Paris Museum Pass for skip-the-line access to top attractions.",
    },
    "dubai": {
        "country": "UAE",
        "region": "Middle East",
        "highlights": ["Burj Khalifa", "desert safari", "luxury malls", "dhow cruise", "gold souk"],
        "best_season": "November to March",
        "currency": "AED",
        "language": "Arabic, English",
        "timezone": "GST (UTC+4)",
        "tip": "Dubai Pass covers many attractions. Avoid summer (May–Sep) — extreme heat.",
    },
    "singapore": {
        "country": "Singapore",
        "region": "Southeast Asia",
        "highlights": ["Gardens by the Bay", "Marina Bay Sands", "hawker centres", "Sentosa", "shopping"],
        "best_season": "February to April",
        "currency": "SGD",
        "language": "English, Mandarin, Malay, Tamil",
        "timezone": "SGT (UTC+8)",
        "tip": "Grab an EZ-Link card for MRT travel. Street food at hawker centres is incredible and cheap.",
    },
}


def get_destination_info(destination: str) -> dict:
    """
    Return enriched info for a destination.
    Falls back to a generic response for unknown destinations.
    """
    key = destination.lower().strip()
    for k, v in DESTINATION_DATA.items():
        if k in key or key in k:
            return {"destination": destination, **v, "found": True}

    # Generic fallback
    return {
        "destination": destination,
        "country": "Unknown",
        "highlights": ["local culture", "cuisine", "sightseeing", "shopping", "nature"],
        "best_season": "Year-round (check local calendar)",
        "currency": "Local currency",
        "language": "Local language",
        "timezone": "Check local timezone",
        "tip": f"Research visa requirements and local customs before visiting {destination}.",
        "found": False,
    }
