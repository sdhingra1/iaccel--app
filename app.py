"""
HOW TO RUN THIS APP
-------------------
1. Ensure you have added your secrets in `.streamlit/secrets.toml` (local)
   or the Streamlit Cloud Dashboard (Cloud).
2. Run: python3 -m streamlit run app.py
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURATION ---
st.set_page_config(page_title="iAccel USA - Strategic Assessment", page_icon="🚀", layout="wide")

# --- GOOGLE SHEETS SETUP ---
# expected_headers defines the order of columns in your Google Sheet
EXPECTED_HEADERS = [
    "Timestamp", "Company", "Website", "Founder", "Email", "LinkedIn", "Industry",
    "Problem", "Solution", "Competitors", "Differentiation", "Clients", "Scope",
    "Capital Raised", "Investors", "ARR 2025", "TAM",
    "Proj 2026", "Proj 2027", "Proj 2028",
    "Services", "Fund Ask", "Deck Link"
]

def get_google_sheet_data():
    """Connects to Google Sheets and returns the worksheet object."""
    # Define the scope
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Load credentials from Streamlit Secrets
    try:
        # Check if secrets exist before trying to access them
        if "gcp_service_account" not in st.secrets:
            st.error("Secrets not found. Please set up your .streamlit/secrets.toml or Cloud Secrets.")
            return None

        s_info = st.secrets["gcp_service_account"]
        credentials = Credentials.from_service_account_info(
            s_info, scopes=scopes
        )
        gc = gspread.authorize(credentials)
        
        # Open the Google Sheet by URL
        sh = gc.open_by_url(st.secrets["private_sheet_url"])
        worksheet = sh.sheet1
        return worksheet
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# --- CUSTOM STYLING ---
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { background-color: #004e92; color: white; border-radius: 5px; width: 100%; font-weight: bold; }
    h1 { color: #004e92; text-align: center; }
    h3 { color: #004e92; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://via.placeholder.com/300x100?text=iAccel+USA", use_container_width=True)
    st.title("About iAccel USA")
    st.info("Bridging India & The US for high-growth startups.")
    st.markdown("---")
    
    # ADMIN SECTION
    st.write("### 🔒 Internal Access")
    if st.checkbox("Admin Login"):
        pwd = st.text_input("Enter Password", type="password")
        if pwd == "admin123":
            ws = get_google_sheet_data()
            if ws:
