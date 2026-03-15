# 🏥 Healthcare Planning Assistant Agent (AAI-02)

## 📌 Overview
This repository contains the source code for the "Healthcare Planning Assistant Agent", an advanced Agentic AI system that orchestrates complex medical tasks. 

Upon receiving a high-level goal (e.g., 'Treatment Options'), the single **Planner Agent** autonomously decomposes the objective into sequential, actionable steps. It utilizes a custom mock tool (`CheckResourceAvailabilityTool`) to validate the availability of standard hospital resources (e.g., doctors, rooms, equipment). Finally, it dynamically coordinates these variables to generate a detailed compilation of dependencies and an optimized execution schedule in a robust user interface.

### 👥 Team Project Information
- **Division**: D3
- **Group**: Placed BtechGroup07
- **Project No**: AAI-02
- **Subject**: Agentic AI

| # | Name | Enrollment No |
|---|---|---|
| 1 | CHETAN OSWAL | EN22CS301295 |
| 2 | IRYA PATNI | EN22CS301436 |
| 3 | UDAY DUBEY | EN22EL301058 |
| 4 | HIMANI JAISWAL | EN22CS301423 |

---

## 🛠️ Technologies
- **Python 3.10+**
- **CrewAI**: Advanced Multi-Agent / Reasoning Loop framework
- **LangChain**: Backbone components for LLM logic
- **Google Gemini API**: Native `gemini-2.5-flash` via `langchain-google-genai`
- **Streamlit**: Elegant, fast frontend for interaction

---

## 🚀 Setup & Installation Instructions

This project is built to be 100% implementable in one go. You will provide your API key securely using a `.env` file.

1. **Navigate to the Directory**:
   Ensure you are in the `Healthcare_Planner_Agent` root folder.

2. **Set up Environment Variables**:
   Open the `.env` file and replace `your_google_api_key_here` with your actual Google Gemini API key.

3. **Install Dependencies**:
   Install all required python modules leveraging pip.
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit Interface**:
   ```bash
   streamlit run app.py
   ```

5. **Using the App**:
   - Open your browser to the local URL (usually `http://localhost:8501`).
   - Enter your **Healthcare Goal** in the main text area.
   - Click "**Initialize Planning Sequence**".

---

## 📐 High Level Design (HLD)

1. **User Interface (Streamlit) (app.py)**
   - Operates as the user-facing interface component with a premium frontend.
   - Responsibilities: Loads environment variables securely, captures the human language query, instantiates UX elements (Spinners), and renders the returned Markdown string.

2. **Core Agent Backend (src/agent_backend.py)**
   - Acts as the core integration wrapper for dynamic execution logic.
   - Responsibilities: Compiles the Agent and Task objects into a sequential execution Crew using the API key from your `.env` file.

3. **Medical Planner Agent**
   - The primary reasoning LLM Node parameterized specifically with a system persona specialized in hospital triage and operational planning. Runs off `gemini-2.5-flash`.

4. **Resource Assessment Interface Tool**
   - Integrates natively via CrewAI's `tools=[...]` array. It allows the LLM to contextually query real-time mock data surrounding external systems.

## 📄 Low Level Design (LLD)

1. **Agent Definition (Planner)**
   - **Role**: `Medical Planning Coordinator`
   - **Goal Setup**: Orchestrate tasks and maintain strict dependencies. 
   - **Attributes**: `allow_delegation=False`, `verbose=True`, utilizes Google Gemini via `llm` prop.

2. **Task Parameters**
   - Implements multi-step logic requirements within `description`: (1) Goal Decomp (2) Resource ID (3) Validation Check (4) Scheduling.
   - Rejects the completion sequence until the rigid Markdown standard format outlined in the `expected_output` variable is matched.

3. **Custom CheckResourceAvailabilityTool (src/tools.py)**
   - Subclassed directly from `crewai.tools.BaseTool`.
   - `_run(self, resource_name: str)` matches predefined keywords ("Dr. Smith", "available") via a boolean string match returning either affirmative or negative resource capability for the LLM to adjust its schedule contextually.
