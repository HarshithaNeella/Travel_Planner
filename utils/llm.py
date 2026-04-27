""
llm.py - Groq LLM wrapper (llama-3.1-8b-instant)
"""

import os
import json
import re
from dotenv import load_dotenv

load_dotenv()

from groq import Groq

_client = Groq(api_key=os.environ.get("GROQ_API_KEY", ""))

MODEL = "llama-3.1-8b-instant"


def call_llm(prompt: str, system: str = "", temperature: float = 0.7) -> str:
    """Call Groq and return the assistant text. Falls back gracefully on error."""
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    try:
        response = _client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=temperature,
            max_tokens=2048,
        )
        return response.choices[0].message.content or ""
    except Exception as e:
        return f"[LLM Error: {e}]"


def resolve_destination(destination: str) -> str:
    """Convert vague destinations (country/region) into a specific city."""
    prompt = f"""
Convert the following travel destination into a specific city suitable for itinerary planning.

Rules:
- If it's a country → return a major tourist city
- If it's a region → return a popular city in that region
- If already a city → return as is
- Return ONLY the city name (no explanation)

Examples:
South Korea → Seoul
USA → New York
South India → Bangalore
Rajasthan → Jaipur
Andhra Pradesh → Visakhapatnam

Destination: {destination}
"""
    result = call_llm(prompt, temperature=0)
    return result.strip()


def safe_understand_query(user_input: str, current_state: dict) -> dict:
    """
    Use the LLM to extract planning fields from user input.

    Returns a dict with any of:
      destination, days, budget, members, intent

    intent values:
      'planning' | 'elaborate' | 'summarize' | 'suggestion' | 'other'
    """
    system = """You are a travel planning assistant. Extract structured information from user input.
Return ONLY valid JSON (no markdown, no explanation) with these keys (include only what you can extract):
- destination: string (city/country name)
- days: integer (number of days; convert "1 week"→7, "2 weeks"→14, "10 days"→10)
- budget: integer (total INR; convert "10k"→10000, "2 lakh"→200000, "₹5000"→5000, "5k"→5000)
- members: integer (number of travellers; convert "solo"→1, "couple"→2, "family of 4"→4)
- intent: one of ["planning","elaborate","summarize","suggestion","other"]

Rules:
- intent="planning" if user mentions trip/travel/plan/visit/tour/vacation with specific parameters
- intent="elaborate" if user says elaborate/more details/expand/detail
- intent="summarize" if user says summarize/summary/overview/brief/recap/shorten/condense
- intent="suggestion" if:
    - user asks suggest/recommend/nearby/hangout without a specific plan
    - user asks "is it okay", "should I go", "is it good time"
    - user asks about weather suitability or best time
    - user asks for recommendations without specifying full trip details
- intent="other" for greetings, thanks, or unrelated questions
- Do NOT mix up numbers — days and budget and members are different fields
- If you cannot determine a value, omit that key entirely

IMPORTANT:
- DO NOT treat "visit" alone as planning
- DO NOT convert vague time phrases like "next month" into days
- If unsure between planning and suggestion, prefer "suggestion"
"""
    state_hint = f"Current known state: {json.dumps(current_state)}"
    prompt = f"{state_hint}\n\nUser said: {user_input}"

    raw = call_llm(prompt, system=system, temperature=0.1)

    # Strip markdown fences if present
    raw = re.sub(r"```json|```", "", raw).strip()

    try:
        data = json.loads(raw)
    except Exception:
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            try:
                data = json.loads(match.group())
            except Exception:
                data = {}
        else:
            data = {}

    # Coerce types safely
    result = {}
    if "destination" in data and isinstance(data["destination"], str):
        result["destination"] = data["destination"].strip().title()
    if "days" in data:
        try:
            result["days"] = int(data["days"])
        except (ValueError, TypeError):
            pass
    if "budget" in data:
        try:
            result["budget"] = int(data["budget"])
        except (ValueError, TypeError):
            pass
    if "members" in data:
        try:
            result["members"] = int(data["members"])
        except (ValueError, TypeError):
            pass
    if "intent" in data:
        result["intent"] = str(data["intent"])

    # Guard: prevent days being silently overwritten by members
    if "members" in result and "days" in result:
        if result["members"] == result["days"]:
            result.pop("days", None)

    return result
