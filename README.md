🚀 Travel Planner AI
Smart AI-Powered Itinerary Generator using MCP + LLM
---
❗ Problem Statement

Travel planning is often manual, time-consuming, and fragmented across multiple platforms. Users must:

Search destinations separately
Estimate budgets manually
Plan itineraries without guidance
Limitations of Existing Systems
❌ Lack personalization
❌ Poor natural language understanding
❌ Static, non-adaptive recommendations
---

🎯 Goal

Build an intelligent system that:

Understands natural language queries
Extracts structured travel parameters
Generates optimized itineraries
Uses modular tools for reliable execution
Supports interactive refinement
---

📖 Overview

Travel Planner AI converts free-text user queries into structured, budget-aware travel plans using a hybrid architecture:

🔑 Core Idea
LLM → Understanding + Response Formatting
MCP → Tool Execution + Orchestration
---
🌐 Live Demo

👉 https://huggingface.co/spaces/Harshitha-4/TRAVEL_ITERNARY
---

⚙️ Approach
🧠 LLM extracts intent and entities
🗂️ State manager maintains conversation context
⚙️ MCP orchestrates tool execution
🔄 Fallback ensures robustness
✨ LLM formats final response
---
💡 Features
🧠 Natural language trip planning
📍 Extracts destination, budget, duration
📅 Multi-day itinerary generation
🔄 MCP-based modular execution
💬 Stateful multi-turn interaction
✂️ Output refinement (summary / detailed)
🛡️ Fault-tolerant execution 

---
🏗️ Architecture

The system follows a tool-first orchestration model:

🔄 Workflow
User provides input
LLM extracts structured data
MCP selects & executes tools
Tool outputs are aggregated
LLM formats final response


## 🔄 Component-Level Workflow
  
<img width="1945" height="619" alt="Travel_workflow" src="https://github.com/user-attachments/assets/a34a975d-e340-4853-9c33-c846f689aea5" />

🧠 MCP Layer

MCP (Modular Command Protocol) enables:

Tool selection
Execution routing
Failure handling
Modular scalability

🔧 Tools Used

Tool	Purpose

📅 generate_plan	Creates itinerary

📍 destination_info	Provides location insights

💰 budget	Handles cost logic

🖼️ images	(Optional) visual enhancement

⚙️ Execution Strategy

Call MCP tool

Validate response

If invalid → fallback to LLM

Format output

🧪 Sample Input & Output
Input
Plan a 3 day trip to Goa under 8000
Output
Day 1:
- Arrival & Baga Beach
- Evening market visit

Day 2:
- North Goa (Fort Aguada, Calangute)
- Water activities

Day 3:
- South Goa (Colva Beach)
- Departure

Budget Tips:
- Use local transport
- Stay in budget hostels

⚙️ Installation
1. Clone Repository
git clone https://github.com/HarshithaNeella/Travel_Planner/edit/main/README.md
cd Travel_Planner
2. Create Virtual Environment
python -m venv venv
venv\Scripts\activate
3. Install Dependencies
pip install -r requirements.txt
4. Setup Environment Variables
---
Create .env file:

GROQ_API_KEY=your_api_key

MCP_SERVER_URL=your_mcp_server_url
---
▶️ Usage

Run MCP Server
      
cd mcp_server

python server.py

Run Frontend

streamlit run app.py

Example Queries

Plan a 3 day trip to Goa under 8000

Suggest places to visit in Delhi

Goa → 8000 → 3 days


---

🛠️ Tech Stack

🐍 Python

🎨 Streamlit

🤖 Groq LLM

🔗 REST APIs

⚙️ MCP Architecture
---
📁 Project Structure

Travel_Planner/
│

├── agent/             # Core agent logic

├── mcp_server/        # MCP backend (tools)

├── utils/             # LLM integration

├── app.py             # Streamlit UI

├── requirements.txt

└── runtime.txt
---
⚠️ Error Handling

If MCP fails → fallback to LLM

If input incomplete → ask follow-up

If refinement requested → reprocess output

This ensures robust and reliable responses.
