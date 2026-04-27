"""
images.py - Fetch destination image from Unsplash API
"""

import os
import requests

UNSPLASH_ACCESS_KEY = os.environ.get("UNSPLASH_ACCESS_KEY", "")


def get_destination_image(destination: str) -> dict:
    """
    Fetch a representative image URL for a destination from Unsplash.
    Returns dict with: url, alt_text, photographer, source
    """
    if not UNSPLASH_ACCESS_KEY:
        return {
            "url": None,
            "alt_text": destination,
            "photographer": "",
            "source": "unavailable",
            "note": "Set UNSPLASH_ACCESS_KEY environment variable to enable images.",
        }

    try:
        query = f"{destination} travel landscape"
        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "per_page": 1,
            "orientation": "landscape",
            "client_id": UNSPLASH_ACCESS_KEY,
        }
        resp = requests.get(url, params=params, timeout=8)
        data = resp.json()
        results = data.get("results", [])
        if results:
            photo = results[0]
            return {
                "url": photo["urls"]["regular"],
                "alt_text": photo.get("alt_description") or destination,
                "photographer": photo.get("user", {}).get("name", ""),
                "source": "unsplash",
            }
    except Exception as e:
        pass

    return {
        "url": None,
        "alt_text": destination,
        "photographer": "",
        "source": "error",
    }
