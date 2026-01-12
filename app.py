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
EXPECTED_HEADERS = [
    "Timestamp", "Company", "Website", "Founder", "Email", "LinkedIn", "Industry",
    "Problem", "Solution", "Competitors", "Differentiation", "Clients", "Scope",
    "Capital Raised", "Investors", "ARR 2025", "TAM",
    "Proj 2026", "Proj 2027", "Proj 2028",
    "Services", "Fund Ask", "Deck Link"
]

def get_google_sheet_data():
    """Connects to Google Sheets and returns the worksheet object."""
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive"
    ]
    
    try:
        # Check if the main section exists
        if "gcp_service_account" not in st.secrets:
            st.error("Secrets Error: [gcp_service_account] section not found.")
            return None

        # Convert Streamlit Secrets object to a standard Python dictionary
        s_info = dict(st.secrets["gcp_service_account"])

        # --- CRITICAL KEY FIX ---
        if "private_key" in s_info:
            pk = s_info["private_key"]
            
            # 1. Clean whitespace
            pk = pk.strip()
            
            # 2. Check for missing headers (Common copy-paste error)
            if not pk.startswith("-----BEGIN PRIVATE KEY-----"):
                st.error("Secrets Error: The 'private_key' is missing the '-----BEGIN PRIVATE KEY-----' header.")
                st.info("Tip: Make sure you copied the ENTIRE key from the JSON file, including the dashes.")
                return None
                
            if not pk.endswith("-----END PRIVATE KEY-----"):
                st.error("Secrets Error: The 'private_key' is missing the '-----END PRIVATE KEY-----' footer.")
                return None

            # 3. Fix Newlines: Convert literal "\n" strings to actual newlines
            # This handles both double-escaped (\\n) and single-escaped (\n) issues
            pk = pk.replace("\\n", "\n")
            
            s_info["private_key"] = pk
        else:
            st.error("Secrets Error: 'private_key' field is missing from secrets.")
            return None

        credentials = Credentials.from_service_account_info(s_info, scopes=scopes)
        gc = gspread.authorize(credentials)
        
        # Check for Sheet URL
        if "private_sheet_url" not in st.secrets:
            st.error("Secrets Error: 'private_sheet_url' is missing.")
            return None
            
        sh = gc.open_by_url(st.secrets["private_sheet_url"])
        return sh.sheet1

    except ValueError as ve:
        # This specific error usually comes from the key format
        st.error(f"Certificate Error: {ve}")
        st.info("Troubleshooting: Ensure your private_key in secrets has no extra spaces or quote marks breaking the string.")
        return None
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
    is_admin = st.checkbox("Admin Login")
    
    if is_admin:
        pwd = st.text_input("Enter Password", type="password")
        if pwd == "admin123":
            ws = get_google_sheet_data()
            if ws:
                # Simplified logic to avoid indentation errors
                try:
                    data = ws.get_all_records()
                    df = pd.DataFrame(data)
                    st.write(f"Total Applications: {len(df)}")
                    st.dataframe(df)
                except Exception as e:
                    st.warning("No data found or empty sheet.")
        elif pwd:
            st.error("Incorrect Password")

# --- MAIN FORM ---
st.title("🚀 iAccel USA | Strategic Assessment")
st.markdown("**Confidential Intake Form**")

with st.form("application_form"):
    st.markdown("### 1. Company Snapshot")
    c1, c2, c3 = st.columns(3)
    with c1:
        company_name = st.text_input("Startup Name*")
        founder_name = st.text_input("Founder Name*")
    with c2:
        website = st.text_input("Website URL*")
        linkedin = st.text_input("Founder LinkedIn*")
    with c3:
        email = st.text_input("Email Address*")
        industry = st.selectbox("Industry*", ["SaaS", "Fintech", "Healthtech", "Deeptech", "AI/ML", "E-commerce", "Other"])

    st.markdown("### 2. Product & Market Position")
    pm1, pm2 = st.columns(2)
    with pm1:
        problem_statement = st.text_area("Problem Statement*", height=100)
    with pm2:
        solution_desc = st.text_area("Solution Description*", height=100)

    cc1, cc2 = st.columns(2)
    with cc1:
        competitors = st.text_area("Top Competitors*", help="List 3-5 key competitors.")
        differentiation = st.text_area("USP / Differentiation*", help="How do you win?")
    with cc2:
        current_clients = st.text_area("Key Clients*", help="List top 5-10 customers.")
        scope = st.radio("Geographic Scope*", ["Global", "India Only", "US Only", "Other"], horizontal=True)

    st.markdown("### 3. Financial Health (USD)")
    f1, f2, f3 = st.columns(3)
    with f1:
        capital_raised = st.text_input("Total Capital Raised*", placeholder="$2M")
        investors = st.text_area("Current Investors*")
    with f2:
        arr_2025 = st.text_input("ARR 2025*", placeholder="$500k")
        tam = st.text_input("TAM*", placeholder="$10B")
    with f3:
        proj_2026 = st.text_input("Proj 2026")
        proj_2027 = st.text_input("Proj 2027")
        proj_2028 = st.text_input("Proj 2028")

    st.markdown("### 4. Collaboration")
    services = st.multiselect("Services Needed*", ["US Market Access", "Fundraising", "Operations"])
    fund_ask = st.text_input("Fundraising Ask (if applicable)") if "Fundraising" in str(services) else ""
    deck_link = st.text_input("Pitch Deck Link (URL)")

    submitted = st.form_submit_button("Submit Assessment")

    if submitted:
        if not all([company_name, email, arr_2025, capital_raised]):
            st.error("Please fill in required fields (*).")
        else:
            # Prepare row data
            row_data = [
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                company_name, website, founder_name, email, linkedin, industry,
                problem_statement, solution_desc, competitors, differentiation, current_clients, scope,
                capital_raised, investors, arr_2025, tam,
                proj_2026, proj_2027, proj_2028,
                ", ".join(services), fund_ask, deck_link
            ]
            
            # Send to Google Sheets
            ws = get_google_sheet_data()
            if ws:
                try:
                    # If sheet is empty, add headers first
                    if len(ws.get_all_values()) == 0:
                        ws.append_row(EXPECTED_HEADERS)
                    
                    ws.append_row(row_data)
                    st.success("✅ Application Received & Saved to Cloud Database.")
                    st.balloons()
                except Exception as e:
                    st.error(f"Error saving to Google Sheets: {e}")
