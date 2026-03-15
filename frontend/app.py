import streamlit as st
import traceback
import sys
import os
from dotenv import load_dotenv

# Ensure 'backend' is in path and import backend module
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from backend.agent_backend import run_healthcare_planner

# Load environment variables from .env file
load_dotenv()

# Configure basic page layout
st.set_page_config(
    page_title="Healthcare Planner Agent - AAI-02",
    page_icon="🏥",
    layout="wide"
)

# Hide Streamlit Deploy Button and Top Menu
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Theme & Layout Configuration
# ---------------------------------------------------------

# Use columns to place the theme toggle on the right
col_title, col_theme = st.columns([10, 2])

with col_title:
    st.markdown("<div class='main-title'>Healthcare Planning Assistant <span style='font-size:0.5em'>Agent</span></div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Autonomous task orchestration & resource validation via Agentic multi-step reasoning.</div>", unsafe_allow_html=True)

with col_theme:
    st.markdown("<br>", unsafe_allow_html=True)
    theme = st.selectbox("UI Theme", ["Dark", "Light"], label_visibility="collapsed")

if theme == "Dark":
    theme_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
        .stApp { background-color: #0e1117; color: #f0f2f6; }
        h1, h2, h3 { color: #e0e6ed !important; font-weight: 600 !important; letter-spacing: -0.02em; }
        .main-title { font-size: 2.8rem; background: -webkit-linear-gradient(45deg, #4f46e5, #0ea5e9); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; margin-bottom: 0px; }
        .subtitle { color: #94a3b8; font-size: 1.1rem; margin-top: 5px; margin-bottom: 30px; }
        .stTextArea textarea { background-color: #1e2530 !important; color: #f8fafc !important; border: 1px solid #334155 !important; border-radius: 8px !important; padding: 12px !important; font-size: 1rem !important; transition: all 0.3s ease; }
        .stTextArea textarea:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important; }
        .stButton>button { background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%) !important; color: white !important; border: none !important; border-radius: 8px !important; padding: 0.75rem 1.5rem !important; font-size: 1.1rem !important; font-weight: 600 !important; transition: all 0.3s ease !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important; }
        .stButton>button:hover { transform: translateY(-2px) !important; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important; }
        hr { border-color: #334155 !important; margin: 2rem 0 !important; }
        .result-container { background-color: #1e293b; padding: 30px; border-radius: 12px; border: 1px solid #334155; margin-top: 15px; }
    </style>
    """
else:
    theme_css = """
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
        .stApp { background-color: #f8fafc; color: #0f172a; }
        h1, h2, h3 { color: #1e293b !important; font-weight: 600 !important; letter-spacing: -0.02em; }
        .main-title { font-size: 2.8rem; background: -webkit-linear-gradient(45deg, #3b82f6, #0284c7); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700; margin-bottom: 0px; }
        .subtitle { color: #475569; font-size: 1.1rem; margin-top: 5px; margin-bottom: 30px; }
        .stTextArea textarea { background-color: #ffffff !important; color: #0f172a !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; padding: 12px !important; font-size: 1rem !important; transition: all 0.3s ease; }
        .stTextArea textarea:focus { border-color: #3b82f6 !important; box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2) !important; }
        .stButton>button { background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%) !important; color: white !important; border: none !important; border-radius: 8px !important; padding: 0.75rem 1.5rem !important; font-size: 1.1rem !important; font-weight: 600 !important; transition: all 0.3s ease !important; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06) !important; }
        .stButton>button:hover { transform: translateY(-2px) !important; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05) !important; }
        hr { border-color: #e2e8f0 !important; margin: 2rem 0 !important; }
        .result-container { background-color: #ffffff; padding: 30px; border-radius: 12px; border: 1px solid #cbd5e1; margin-top: 15px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); }
    </style>
    """

st.markdown(theme_css, unsafe_allow_html=True)
st.markdown("---")

# Agent Input Section
st.markdown("### 🎯 Define Primary Healthcare Objective")

example_goal = "Schedule a complete cardiac evaluation for a new patient, including initial consultation, ECG, echocardiogram, and follow-up review."

user_goal = st.text_area(
    "Orchestration Prompt",
    height=140,
    placeholder=f"e.g., {example_goal}",
    label_visibility="collapsed"
)

# Helper Row
st.caption("💡 The agent will autonomously decompose this goal, check constraints, and allocate resources via mock tools.")

st.markdown("<br>", unsafe_allow_html=True)

# Action Area Layout (Center Button)
_, btn_col, _ = st.columns([1, 2, 1])
with btn_col:
    run_agent = st.button("🚀 Initialize Planning Sequence", use_container_width=True)

# ---------------------------------------------------------
# Execution & Results
# ---------------------------------------------------------
if run_agent:
    api_key = os.getenv("GOOGLE_API_KEY")
    
    if not api_key:
        st.error("❌ Authentication Error: Google API Key not found. Please set GOOGLE_API_KEY in the .env file.")
    elif not user_goal.strip():
        st.warning("⚠️ Input Required: Please define a healthcare objective for the agent.")
    else:
        # Progress UI
        st.markdown("---")
        st.markdown("### 🔄 Agentic Execution Log")
        
        status_container = st.empty()
        
        with st.spinner("🧠 Medical Planner Agent is reasoning and querying tool subroutines..."):
            try:
                # Add a simulated log structure for professional feel before calling backend
                status_container.info("Step 1: Contextualizing Objective & Assessing Resource Feasibility...")
                
                # Invoke the CrewAI backend function
                plan_result_markdown = run_healthcare_planner(api_key, user_goal)
                
                status_container.empty() # Clear intermediate log
                
                # Success Banner
                st.success("✅ Workflow Complete. Resources validated. Schedule Optimized.")
                
                # Output Presentation
                st.markdown("---")
                
                st.markdown("### 📋 Generated Execution Schedule")
                
                # Wrap the result in a nice styled container
                st.markdown(f"""
                <div class='result-container'>
                    {plan_result_markdown}
                </div>
                """, unsafe_allow_html=True)
                
            except Exception as e:
                status_container.empty()
                st.error("🚨 Critical Error encountered during agent execution.")
                with st.expander("View Stack Trace"):
                    st.code(traceback.format_exc(), language="python")

st.markdown("<br><br><p style='text-align: center; color: #64748b; font-size: 0.85em;'>Architected for Datagami Agentic AI Assessment</p>", unsafe_allow_html=True)
