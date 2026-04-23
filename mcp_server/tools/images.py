import requests
import os
from dotenv import load_dotenv

load_dotenv()

UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")


def get_image(destination):
    try:
        url = "https://api.unsplash.com/search/photos"

        params = {
            "query": destination,
            "per_page": 1
        }

        headers = {
            "Authorization": f"Client-ID {UNSPLASH_KEY}"
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        if data.get("results"):
            image_url = data["results"][0]["urls"]["regular"]
            return {"image": image_url}

        return {"image": None}

    except:
        return {"image": None}
