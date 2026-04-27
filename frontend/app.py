"""
app.py - Smart Travel Planner — Streamlit Chat UI
Run: streamlit run app.py
"""

import streamlit as st
from memory import TravelMemory
from planner import handle_message
from dotenv import load_dotenv

import sys
import os

sys.path.append(os.path.dirname(__file__))
load_dotenv()

# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Smart Travel Planner ✈️",
    page_icon="✈️",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600&family=Playfair+Display:wght@700&display=swap');

    html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }

    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 0.5rem 0;
    }
    .subtitle {
        text-align: center;
        color: #666;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .state-badge {
        display: inline-block;
        background: #e8f4fd;
        border: 1px solid #bee3f8;
        color: #2b6cb0;
        border-radius: 20px;
        padding: 3px 12px;
        font-size: 0.8rem;
        margin: 2px;
    }
    .stChatMessage [data-testid="stMarkdownContainer"] {
        font-size: 0.95rem;
        line-height: 1.6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown('<div class="main-title">✈️ Smart Travel Planner</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Plan your perfect trip — just chat naturally!</div>',
    unsafe_allow_html=True,
)

# ── Session state ─────────────────────────────────────────────────────────────

if "memory" not in st.session_state:
    st.session_state.memory = TravelMemory()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Hi! I'm your Smart Travel Planner.\n\n"
                "Tell me where you want to go and I'll build a complete day-by-day itinerary "
                "with real places, live weather, and a budget breakdown.\n\n"
                "You can say things like:\n"
                "- *\"Plan a 5-day trip to Goa for 2 people with ₹20,000\"*\n"
                "- *\"I want to visit Manali\"*\n"
                "- *\"Suggest some hill stations\"*"
            ),
        }
    ]

memory: TravelMemory = st.session_state.memory

# ── Sidebar: current planning state ──────────────────────────────────────────

with st.sidebar:
    st.markdown("### 🗺️ Trip Planning Status")
    state = memory.get_state()
    fields = {
        "destination": ("📍 Destination", state.get("destination")),
        "days": ("📅 Days", state.get("days")),
        "budget": ("💰 Budget", f"₹{state['budget']:,}" if state.get("budget") else None),
        "members": ("👥 Travellers", state.get("members")),
    }

    for key, (label, val) in fields.items():
        if val:
            st.success(f"{label}: **{val}**")
        else:
            st.info(f"{label}: *not set*")

    st.divider()
    if st.button("🔄 Start New Trip", use_container_width=True):
        memory.reset_state()
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "✨ Ready for a new trip! Where would you like to go?",
            }
        ]
        st.rerun()

    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "👋 Hi! I'm your Smart Travel Planner. Where would you like to go?"
            }
        ]
        st.session_state.memory = TravelMemory()
        st.rerun()

    if memory.get_plan():
        if st.button("📋 Show Last Plan", use_container_width=True):
            last_plan = memory.get_plan()
            st.session_state.messages.append(
                {"role": "assistant", "content": f"**Your last plan:**\n\n{last_plan}"}
            )
            st.rerun()

    st.divider()
    st.markdown("**💡 Quick tips:**")
    st.markdown("- Say *'elaborate'* for more details\n- Say *'suggest places'* for recommendations\n- Budget: 10k, ₹50000, 2 lakh")

# ── Chat history ──────────────────────────────────────────────────────────────

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input ────────────────────────────────────────────────────────────────

if prompt := st.chat_input("Where do you want to go? Or ask anything travel-related…"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("Planning your trip…"):
            response = handle_message(prompt, memory)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
    st.rerun()
