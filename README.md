# 🚀 Travel Planner AI  
### Smart AI-Powered Itinerary Generator using MCP + LLM

---

## ❗ Problem Statement

Travel planning is often manual, time-consuming, and fragmented across multiple platforms. Users must search for destinations, estimate budgets, and manually create itineraries.

### Limitations of Existing Systems
- ❌ Lack personalization  
- ❌ Poor handling of natural language queries  
- ❌ Static, non-adaptive recommendations  

---

## 🎯 Goal

Build an intelligent system that:
- Understands natural language input  
- Extracts key travel parameters (destination, budget, duration)  
- Generates optimized, structured itineraries  
- Uses modular tool execution for reliability  
- Supports interactive refinement  

---

## 📖 Overview

**Travel Planner AI** converts user queries into **structured travel plans** using a hybrid architecture:

### 🔑 Core Architecture
- **LLM → Understanding + Response Formatting**
- **MCP → Tool Execution + Orchestration**

---

## 🌐 Live Demo

👉 https://huggingface.co/spaces/Harshitha-4/TRAVEL_ITERNARY  

---

## ⚙️ Workflow

```
User Input
   ↓
LLM (Extract intent & entities)
   ↓
MCP (Select & execute tools)
   ↓
Tool Outputs
   ↓
LLM (Format response)
   ↓
Final Output
```

---

## 💡 Features

- 🧠 Natural language trip planning  
- 📍 Destination, budget, duration extraction  
- 📅 Multi-day itinerary generation  
- 🔄 MCP-based modular execution  
- 💬 Interactive and flexible responses  
- ✂️ Output refinement (summary / detailed)  
- 🛡️ Fault-tolerant system  

---

## 🧠 MCP Architecture

MCP (Modular Command Protocol) acts as the execution engine:
- Tool selection  
- Execution routing  
- Failure handling  
- Response validation  

---

## 🔧 Tools

| Tool | Purpose |
|------|--------|
| 📅 itinerary.py | Generates day-wise itinerary |
| 📍 destination.py | Suggests places |
| 💰 budget.py | Handles cost estimation |
| 🌦️ weather.py | Fetches live weather data |
| 🖼️ images.py | Adds visual enhancement |

---

## ⚙️ Execution Strategy

```
LLM → Understand Input
        ↓
MCP → Execute Tools
        ↓
Validate Output
        ↓
Fallback (if needed)
        ↓
LLM → Format Response
```

---

## 🧪 Example

**Input:**
```
Plan a 3 day trip to Goa under 8000
```

**Output:**
```
Day 1: Baga Beach + Market  
Day 2: North Goa + Activities  
Day 3: South Goa + Departure  

Budget Tips:
- Use local transport  
- Stay in budget accommodations  
```

---

## ⚙️ Installation

```bash
git clone https://github.com/HarshithaNeella/Travel_Planner
cd Travel_Planner
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🔐 Environment Variables

Create a `.env` file:

```
GROQ_API_KEY=your_api_key
MCP_SERVER_URL=your_mcp_server_url
```

---

## ▶️ Run the Project

### Start MCP Server
```bash
cd mcp_server
python server.py
```

### Run Frontend
```bash
streamlit run app.py
```

---

## 💬 Example Queries

- Plan a 3 day trip to Goa under 8000  
- Suggest places to visit in Delhi  
- Goa → 8000 → 3 days  

---

## 🛠️ Tech Stack

- 🐍 Python  
- 🎨 Streamlit  
- 🤖 Groq LLM  
- 🔗 REST APIs  
- ⚙️ MCP Architecture  

---

## 📁 Project Structure

```
frontend/
 └── app.py

mcp_server/
 ├── server.py
 └── tools/

utils/
 └── llm.py
```

---

## ⚠️ Error Handling

- Tool failure → fallback to LLM  
- Missing input → follow-up questions  
- Invalid output → retry mechanism  

---

## 🚀 Future Improvements

- Async tool execution  
- Memory-based personalization  
- Better evaluation metrics  
- Smarter tool routing  

---

## 🧠 Key Insight

> Separating reasoning (LLM) from execution (MCP) makes the system more reliable, scalable, and production-ready compared to pure LLM-based systems.
