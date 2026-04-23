import requests
import os
from dotenv import load_dotenv
from utils.llm import call_llm

load_dotenv()

GEODB_KEY = os.getenv("GEODB_API_KEY")
GEODB_HOST = os.getenv("GEODB_HOST")


def get_destination_info(destination):

    # 🔥 STEP 1: TRY API FIRST
    try:
        url = f"https://{GEODB_HOST}/v1/geo/cities"
        headers = {
            "X-RapidAPI-Key": GEODB_KEY,
            "X-RapidAPI-Host": GEODB_HOST
        }

        params = {
            "namePrefix": destination,
            "limit": 1
        }

        res = requests.get(url, headers=headers, params=params)
        data = res.json()

        if data.get("data"):
            city = data["data"][0]

            return {
                "info": f"""
📍 Destination: {destination}

🌍 Country: {city.get('country')}
🏙️ Region: {city.get('region')}
👥 Population: {city.get('population')}

💡 Tip: Popular tourist destination.
"""
            }

    except:
        pass  # fallback below

    # 🔥 STEP 2: FALLBACK TO LLM
    try:
        prompt = f"""
Give short travel info about {destination}

Include:
- Overview
- Best time
- Budget
- Type

Keep it short and structured.
"""

        response = call_llm(prompt)

        return {"info": response}

    except:
        return {"info": f"Basic info about {destination} not available."}