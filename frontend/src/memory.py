"""
memory.py - Stores conversation history and latest travel plan
"""

from typing import Optional

from src.itinerary import get_places_for_itinerary


class TravelMemory:
    def __init__(self):
        self._history: list[dict] = []
        self._latest_plan: Optional[str] = None
        self._state: dict = {}

    # ── History ──────────────────────────────────────────────────────────────

    def add_message(self, role: str, content: str):
        """Append a message to the conversation history."""
        self._history.append({"role": role, "content": content})

    def get_history(self) -> list[dict]:
        """Return the full conversation history."""
        return list(self._history)

    def clear_history(self):
        self._history.clear()

    # ── Plan ─────────────────────────────────────────────────────────────────

    def save_plan(self, plan: str):
        """Persist the latest generated itinerary."""
        self._latest_plan = plan

    def get_plan(self) -> Optional[str]:
        """Retrieve the latest itinerary (None if none yet)."""
        return self._latest_plan

    # ── Planning State ────────────────────────────────────────────────────────

    def get_state(self) -> dict:
        return dict(self._state)

    def update_state(self, **kwargs):
        """Merge new key-value pairs into the planning state."""
        self._state.update({k: v for k, v in kwargs.items() if v is not None})

    def reset_state(self):
        self._state.clear()

    def is_planning_complete(self) -> bool:
        """True when all four required fields are present."""
        required = {"destination", "days", "budget", "members"}
        return required.issubset(self._state.keys())

    def missing_fields(self) -> list[str]:
        required = ["destination", "days", "budget", "members"]
        return [f for f in required if f not in self._state]
    def set_last_itinerary(self, itinerary: str):
        self._state["last_itinerary"] = itinerary


    def get_last_itinerary(self) -> str:
        return self._state.get("last_itinerary", "")
