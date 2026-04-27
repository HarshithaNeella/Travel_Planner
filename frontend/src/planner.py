"""
planner.py - Smart Travel Planner Agent
Intent order (critical):
  1. suggestion
  2. elaborate
  3. summarize
  4. planning
  5. other / partial state continuation
"""

import json
import requests

from src.memory import TravelMemory
from  src.llm import call_llm, safe_understand_query, resolve_destination

MCP_BASE = "http://localhost:8000"


# ── MCP helpers ───────────────────────────────────────────────────────────────

def _post(endpoint: str, payload: dict) -> dict:
    try:
        resp = requests.post(f"{MCP_BASE}{endpoint}", json=payload, timeout=12)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return {"error": str(e)}


def mcp_places(destination: str, days: int) -> dict:
    return _post("/tools/itinerary", {"destination": destination, "days": days})

def mcp_destination(destination: str) -> dict:
    return _post("/tools/destination", {"destination": destination})

def mcp_weather(destination: str) -> dict:
    return _post("/tools/weather", {"destination": destination})

def mcp_image(destination: str) -> dict:
    return _post("/tools/image", {"destination": destination})

def mcp_budget(budget: int, destination: str) -> dict:
    return _post("/tools/budget", {"budget": budget, "destination": destination})


# ── Place extraction helper ───────────────────────────────────────────────────

def _extract_places(data: dict) -> tuple[list, list]:
    """
    Robustly extract attractions and restaurants from MCP response.
    MCP may return any shape:
      { "attractions": [...], "restaurants": [...] }
      { "places": [...] }
      { "attractions": [...] }   <- partial
      { "restaurants": [...] }   <- partial
    Rules:
    - Prefer "attractions"; fall back to "places" if attractions empty.
    - restaurants always from "restaurants" key.
    - Never raise on partial data.
    """
    attractions = data.get("attractions") or []
    restaurants = data.get("restaurants") or []

    if not attractions:
        attractions = data.get("places") or []

    return attractions, restaurants


def _has_usable_data(attractions: list, restaurants: list) -> bool:
    """Only fail when BOTH lists are completely empty."""
    return bool(attractions) or bool(restaurants)


# ── Itinerary builder ─────────────────────────────────────────────────────
  

  


def _build_itinerary(state: dict) -> str:
    # Unpack all fields first to prevent mid-function NameError
    original_destination = state["destination"]
    days    = state["days"]
    budget  = state["budget"]
    members = state["members"]

    # Step 1: resolve vague destination to a specific city
    resolved = resolve_destination(original_destination)

    # Step 2: fetch places for resolved destination
    places_data = mcp_places(resolved, days)

    # Step 3: extract with flexible fallback
    attractions = places_data.get("attractions") or []
    restaurants = places_data.get("restaurants") or []

    if not attractions:
        attractions = places_data.get("places") or []

    # Step 4: if resolved yielded nothing, retry with original destination
    destination = resolved
    note = ""

    if not attractions and not restaurants:
        destination = original_destination
        places_data = mcp_places(destination, days)

        attractions = places_data.get("attractions") or []
        restaurants = places_data.get("restaurants") or []

        if not attractions:
            attractions = places_data.get("places") or []
    else:
        if original_destination.strip().lower() != resolved.strip().lower():
            note = (
                f"📍 Interpreting **'{original_destination}'** as "
                f"**'{resolved}'** for better planning.\n\n"
            )

    # Step 5: ONLY fail if BOTH are empty after all attempts
    
    if not attractions and not restaurants:
        print("[DEBUG] No real data → using LLM fallback")
    
        return call_llm(
            f"""
    Create a {days}-day travel itinerary for {destination}.
    
    Details:
    - Destination: {destination}
    - Duration: {days} days
    - Budget: ₹{budget}
    - Travellers: {members}
    
    Focus on:
    - history, culture, food
    - temples, landmarks, local markets, street food
    
    Generate a realistic itinerary even without external data.
    """,
            system=f"""
    You are a travel planner.
    
    STRICT RULES:
    - ONLY talk about {destination}
    - DO NOT suggest other cities or countries
    - Generate realistic local places
    """,
            temperature=0.6,
        )
    # Step 6: fetch supporting data
    dest_info    = mcp_destination(destination)
    weather_data = mcp_weather(destination)
    image_data   = mcp_image(destination)

    weather_note      = weather_data.get("weather_note", "")
    weather_temp      = weather_data.get("temperature_c")
    weather_condition = weather_data.get("condition", "")

    highlights  = dest_info.get("highlights", [])
    best_season = dest_info.get("best_season", "")
    tip         = dest_info.get("tip", "")

    image_url  = image_data.get("url")
    image_line = f"\n📍 **Photo**: [{destination}]({image_url})" if image_url else ""

    # Step 7: combine ALL places for LLM context
    all_places = attractions + restaurants

    max_places      = days * 2 + 2
    max_restaurants = max(days, 3)

    places_text = "\n".join(
        f"- {p['name']} ({p.get('category', 'attraction')})"
        f"{': ' + p['address'] if p.get('address') else ''}"
        for p in all_places[:max_places]
    ) or f"- Popular spots in {destination}"

    restaurants_text = "\n".join(
        f"- {r['name']}" for r in restaurants[:max_restaurants]
    ) or f"- Local restaurants in {destination}"

    # Step 8: LLM formats everything into itinerary
    system_prompt = f"""
        You are an expert travel planner. Create a detailed, realistic day-by-day itinerary. 
        Format EXACTLY as specified. Be specific. 
        Use the real places provided. If fewer places than needed, 
        add 'free exploration' or 'local market visit' slots.
        STRICT RULES:
        - ONLY talk about the given destination: {destination}
        - DO NOT suggest other countries or cities
        - If real data is missing, generate a realistic itinerary for {destination}
        - Stay relevant to user intent (history, culture, food)
        
        User destination: {destination}
        """
    

    user_prompt = f"""Create a complete {days}-day travel itinerary for {destination}.
TRIP DETAILS:
- Destination: {destination}
- Duration: {days} days
- Total Budget: ₹{budget:,} for {members} person(s) = ₹{budget // members:,} per person
- Group: {members} traveller(s)
REAL PLACES TO USE:
{places_text}
Restaurants / Food:
{restaurants_text}
DESTINATION INFO:
- Highlights: {', '.join(highlights) if highlights else 'local culture, sightseeing'}
- Best season: {best_season or 'year-round'}
- Local tip: {tip or 'Explore local markets and street food.'}
WEATHER TODAY:
{weather_note}
{f'Temperature: {weather_temp}°C, {weather_condition}' if weather_temp else ''}
REQUIRED OUTPUT FORMAT:
Start with a 2-line intro about {destination}.
Then for EACH day (Day 1 to Day {days}):
**Day X – [Theme Title]**
| Time | Activity | Est. Cost (₹) |
|------|----------|--------------|
| Morning | ... | ₹XXX |
| Afternoon | ... | ₹XXX |
| Evening | ... | ₹XXX |
| Dinner | [restaurant name] | ₹XXX |
After all days:
**📊 Budget Summary**
| Category | Estimated Cost (₹) |
|----------|-------------------|
| Accommodation ({days} nights) | ₹X,XXX |
| Food & Dining | ₹X,XXX |
| Activities & Entry | ₹X,XXX |
| Transport | ₹X,XXX |
| Miscellaneous | ₹X,XXX |
| **Total** | **₹X,XXX** |
Budget per person: ₹{budget // members:,}
Total budget: ₹{budget:,}
**🌤️ Weather Note**
{weather_note}
**💡 Pro Tips**
- {tip or 'Research local transport options before arrival.'}
- [2 more relevant tips]
RULES:
- Total cost MUST NOT exceed ₹{budget:,}
- Use real places listed above; if fewer than needed, add free exploration slots
- Each day MUST be distinct and realistic
- All costs must add up correctly
"""

    itinerary = call_llm(user_prompt, system=system_prompt, temperature=0.6)

    if image_line:
        itinerary = image_line + "\n\n" + itinerary

    return note + itinerary
# ── Follow-up question prompts ────────────────────────────────────────────────

QUESTIONS = {
    "destination": "🗺️ Where would you like to travel? (e.g., Goa, Manali, Bali, Paris)",
    "days":        "📅 How many days are you planning? (e.g., 5 days, 1 week)",
    "budget":      "💰 What's your total budget? (e.g., ₹15,000 / 50k / 2 lakh)",
    "members":     "👥 How many people are travelling? (e.g., solo, 2 people, family of 4)",
}


def _next_question(missing: list[str]) -> str:
    return QUESTIONS.get(missing[0], "Could you tell me more?")


def _state_summary(state: dict) -> str:
    """Human-readable summary of what we already know."""
    known = {k: v for k, v in state.items() if k in ("destination", "days", "budget", "members")}
    if not known:
        return ""
    parts = []
    for k, v in known.items():
        parts.append(f"budget: ₹{v:,}" if k == "budget" else f"{k}: {v}")
    return "Got it! So far I have: " + ", ".join(parts) + ".\n\n"


# ── Main entry point ──────────────────────────────────────────────────────────

def handle_message(user_input: str, memory: TravelMemory) -> str:
    """
    Process one user message and return the assistant response.
    ALWAYS saves both user + assistant messages to memory before returning.
    """
    memory.add_message("user", user_input)
    state = memory.get_state()

    extracted = safe_understand_query(user_input, state)
    intent = extracted.pop("intent", "other")

    # ════════════════════════════════════════════════════════════════════
    # INTENT ORDER: suggestion → elaborate → summarize → planning → other
    # ════════════════════════════════════════════════════════════════════

    # ── 1. Suggestion ─────────────────────────────────────────────────────────
    state =memory.get_state()
    
    if intent == "suggestion" :
        if state.get("destination"):
            intent="planning"
        else:
            response = call_llm(
                user_input,
                system=(
                    "You are a helpful travel assistant. Answer questions about places, "
                    "travel tips, and suggestions. Give practical advice based on season, "
                    " Suggest destinations based on user interests"
                    " Provide 3–5 relevant options"
                    "Keep it practical and concise"
                    "weather, and safety. If a destination is not ideal, suggest alternatives. "
                    "Be concise and friendly."
                    
                ),
            )
            memory.add_message("assistant", response)
            return response

    # ── 2. Elaborate ──────────────────────────────────────────────────────────
    if intent == "elaborate":
        existing_plan = memory.get_plan()
        if existing_plan:
            prompt = (
                f"The user wants more details about this travel plan:\n\n{existing_plan}\n\n"
                f"Their request: {user_input}\n\n"
                "Expand with more specific details, local insights, and tips. "
                "Keep the same structure but add meaningful depth."
            )
            response = call_llm(
                prompt,
                system="You are an expert travel planner. Expand the itinerary with richer details.",
                temperature=0.65,
            )
        else:
            response = (
                "I don't have a saved plan to elaborate on yet. "
                "Let me help you create one — where would you like to go?"
            )
        memory.add_message("assistant", response)
        return response

    # ── 3. Summarize ──────────────────────────────────────────────────────────
    if intent == "summarize":
        existing_plan = memory.get_plan()
        if not existing_plan:
            response = (
                "I don't have a travel plan to summarize yet. "
                "Would you like me to plan a trip? Just tell me your destination, "
                "duration, budget, and group size."
            )
        else:
            prompt = (
                "Summarize the following travel itinerary in 5–8 bullet points. "
                "Cover: destination, duration, key highlights per day, total budget, "
                "and one important tip.\n\n"
                f"Plan:\n{existing_plan}"
            )
            response = call_llm(
                prompt,
                system=(
                    "You are a concise travel assistant. "
                    "Produce a clean, easy-to-read bullet-point summary. "
                    "Do not repeat the full itinerary — only the key highlights."
                ),
                temperature=0.4,
            )
            if not response or response.startswith("[LLM Error"):
                response = "Sorry, I couldn't generate a summary right now. Please try again."
        memory.add_message("assistant", response)
        return response

    # ── 4. Planning ───────────────────────────────────────────────────────────
    if intent == "planning":
        memory.update_state(_planning_active=True)

        for field in ("destination", "days", "budget", "members"):
            if field in extracted:
                memory.update_state(**{field: extracted[field]})

        state = memory.get_state()
        missing = memory.missing_fields()

        if missing:
            response = _state_summary(state) + _next_question(missing)
            memory.add_message("assistant", response)
            return response

        # All 4 fields ready → build itinerary
        response_prefix = (
            f"✈️ Perfect! Planning your **{state['days']}-day trip to {state['destination']}** "
            f"for **{state['members']} traveller(s)** "
            f"with a budget of **₹{state['budget']:,}**.\n\n"
            "⏳ Fetching real-time places, weather, and building your itinerary…\n\n"
        )

        try:
            itinerary = _build_itinerary(state)
        except Exception:
            itinerary = call_llm(
                f"Create a {state['days']}-day travel itinerary for {state['destination']} "
                f"for {state['members']} person(s) with total budget ₹{state['budget']:,}. "
                "Include day-by-day plan with activities, food, costs in table format.",
                system="You are an expert travel planner.",
                temperature=0.65,
            )

        full_response = response_prefix + itinerary
        memory.save_plan(full_response)
        memory.reset_state()

        memory.add_message("assistant", full_response)
        return full_response

    # ── 5. Other / mid-planning continuation ──────────────────────────────────
    if state.get("_planning_active") or any(
        k in state for k in ("destination", "days", "budget", "members")
    ):
        for field in ("destination", "days", "budget", "members"):
            if field in extracted:
                memory.update_state(**{field: extracted[field]})

        state = memory.get_state()
        missing = memory.missing_fields()

        if missing:
            response = _next_question(missing)
            memory.add_message("assistant", response)
            return response

        # All fields filled after extraction
        response_prefix = (
            f"✈️ Great, I have everything! Planning your "
            f"**{state['days']}-day trip to {state['destination']}** "
            f"for **{state['members']} traveller(s)** "
            f"with budget **₹{state['budget']:,}**.\n\n"
            "⏳ Building your itinerary…\n\n"
        )
        try:
            itinerary = _build_itinerary(state)
        except Exception:
            itinerary = call_llm(
                f"Create a {state['days']}-day travel itinerary for {state['destination']} "
                f"for {state['members']} person(s) with total budget ₹{state['budget']:,}. "
                "Include day-by-day plan with activities, food, costs in table format.",
                system="You are an expert travel planner.",
                temperature=0.65,
            )

        full_response = response_prefix + itinerary
        memory.save_plan(full_response)
        memory.reset_state()

        memory.add_message("assistant", full_response)
        return full_response

    # ── 6. General question ───────────────────────────────────────────────────
    history = memory.get_history()[-6:]
    history_text = "\n".join(
        f"{m['role'].title()}: {m['content']}" for m in history[:-1]
    )
    destination = memory.get_state().get("destination") or "not specified"

    response = call_llm(
        f"Conversation so far:\n{history_text}\n\nUser: {user_input}",
        system=f"""
You are a Smart Travel Planner assistant.
- If a destination is already set ({destination}), ONLY talk about that location
- Do NOT suggest other countries or cities
- Stay relevant to user's context
- If user is planning a trip, ask for missing details:
  destination, days, budget, number of travellers
- If no destination is set, you may suggest travel ideas
- Be helpful, conversational, and guide the user step-by-step
""",
)
    
    memory.add_message("assistant", response)
    return response
