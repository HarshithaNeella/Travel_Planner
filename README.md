# 🚀 Travel Planner AI  
### Smart AI-Powered Itinerary Generator using MCP + LLM
---

## ❗ Problem Statement

Travel planning is often manual, time-consuming, and fragmented across multiple platforms.  
Users must search for destinations, estimate budgets, and manually create itineraries.

Existing solutions either:
- Lack personalization  
- Do not handle natural language input effectively  
- Rely entirely on static recommendations  

### 🎯 Goal

Build an intelligent system that:
- Understands natural language queries  
- Extracts key travel parameters (destination, budget, duration)  
- Generates structured, optimized travel itineraries  
- Provides flexible interaction with refinement capabilities  

---

## 📖 Overview

**Travel Planner AI** is an intelligent system that converts natural language input into structured, budget-aware travel itineraries.

### 🎯 Purpose
To automate travel planning using a **hybrid architecture combining MCP (tool execution)** and **LLM (reasoning + formatting)**.


## 🌐 Live Demo

👉 https://huggingface.co/spaces/Harshitha-4/TRAVEL_ITERNARY

### ⚙️ Approach
- 🧩 Parser extracts structured data  
- 🗂️ State manager maintains conversation flow  
- 🛠️ MCP executes tools for reliable outputs  
- 🤖 LLM formats and handles fallback  

---
## 💡 Features

- 🧠 Natural language trip planning  
- 📍 Destination, budget, and days extraction  
- 📅 Multi-day itinerary generation  
- 🔄 MCP + LLM hybrid execution  
- 💬 Stateful conversation handling  
- ✂️ Output refinement (short, summary, precise)  

---

## 🏗️ Architecture

The system follows a **tool-first execution model**:

1. Parse user input  
2. Store extracted data in state  
3. Call MCP tools for structured execution  
4. Use LLM for formatting or fallback  
5. Return final itinerary
---

## 🔄 Component-Level Workflow
  
<img width="1945" height="619" alt="Travel_workflow" src="https://github.com/user-attachments/assets/a34a975d-e340-4853-9c33-c846f689aea5" />

🧠 MCP Layer

The system uses MCP (Modular Command Protocol) for structured execution instead of relying solely on LLMs.

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
