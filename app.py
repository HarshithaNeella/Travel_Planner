import streamlit as st
import re
from agent.planner import agent

st.set_page_config(page_title="WanderWise AI")

st.title("✈️ WanderWise AI")
st.subheader("Smart Travel Planner")

# ---------- SESSION STATE ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "state" not in st.session_state:
    st.session_state.state = {}

# ---------- CLEAR ----------
if st.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.session_state.state = {}
    st.rerun()

# ---------- DISPLAY ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- INPUT ----------
user_input = st.chat_input("Plan your trip...")

if user_input:

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # ---------- HANDLE FOLLOW-UP ----------
    if "pending" in st.session_state.state:
        key = st.session_state.state["pending"]

        if key == "budget":
            nums = re.findall(r'\d+', user_input)
            if nums:
                st.session_state.state["budget"] = int(nums[0])
                del st.session_state.state["pending"]
                response = "📅 How many days?"
            else:
                response = "⚠️ Please enter budget in numbers"

        elif key == "days":
            nums = re.findall(r'\d+', user_input)
            if nums:
                st.session_state.state["days"] = int(nums[0])
                del st.session_state.state["pending"]
                response = agent("", st.session_state.state)
            else:
                response = "⚠️ Please enter valid number of days"

        elif key == "destination":
            st.session_state.state["destination"] = user_input
            del st.session_state.state["pending"]
            response = "💰 What is your budget?"

        else:
            response = agent(user_input, st.session_state.state)

    else:
        response = agent(user_input, st.session_state.state)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })

    st.rerun()