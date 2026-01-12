"""
HOW TO RUN THIS APP
-------------------
1. Open your Terminal.
2. Navigate to the folder where this file is saved (e.g., cd Desktop).
3. Run the following command:
   python3 -m streamlit run app.py
"""

import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- APP CONFIGURATION ---
st.set_page_config(
    page_title="iAccel USA - Comprehensive Intake",
    page_icon="🚀",
    layout="wide"  # Changed to 'wide' to accommodate more data fields
)

# --- CUSTOM STYLING (CSS) ---
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button {
        background-color: #004e92; color: white; border-radius: 5px; width: 100%; font-weight: bold;
    }
    .stButton>button:hover { background-color: #003366; color: white; }
    h1 { color: #004e92; text-align: center; }
    h3 { color: #004e92; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
    .stAlert { border-left: 5px solid #004e92; }
    </style>
    """, unsafe_allow_html=True)

# --- FILE PATH ---
# We use v2 to avoid conflicts with your previous simple CSV
DATA_FILE = "iaccel_leads_v2.csv"

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://via.placeholder.com/300x100?text=iAccel+USA", use_container_width=True)
    st.title("About iAccel USA")
    st.info("""
    **Bridging India & The US**
    We help high-growth Indian startups succeed in the American market.
    """)
    
    st.markdown("---")
    st.write("### 🔒 Internal Access")
    admin_login = st.checkbox("Admin Login")
    if admin_login:
        password = st.text_input("Enter Password", type="password")
        if password == "admin123":
            if os.path.exists(DATA_FILE):
                df = pd.read_csv(DATA_FILE)
                st.write(f"Total Applications: {len(df)}")
                st.dataframe(df)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button("Download CSV", csv, DATA_FILE, "text/csv")
            else:
                st.warning("No data found yet.")
        elif password:
            st.error("Incorrect Password")

# --- MAIN APP ---
st.title("🚀 iAccel USA | Strategic Assessment")
st.markdown("**Confidential Intake Form** | Please provide detailed metrics to help us assess the fit.")

with st.form("application_form"):
    
    # --- 1. THE BASICS ---
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

    # --- 2. PRODUCT & MARKET ---
    st.markdown("### 2. Product & Market Position")
    
    pm1, pm2 = st.columns(2)
    with pm1:
        problem_statement = st.text_area("Problem Statement (What pain point do you solve?)*", height=100)
    with pm2:
        solution_desc = st.text_area("Solution/Product Description*", height=100)

    # Competition & Clients
    st.markdown("**Competition & Clients**")
    cc1, cc2 = st.columns(2)
    with cc1:
        competitors = st.text_area("Who are your top Competitors?*", help="List 3-5 key competitors.")
        differentiation = st.text_area("What is your USP / Differentiation?*", help="How do you win against them?")
    with cc2:
        current_clients = st.text_area("Key Clients / Logos*", help="List your top 5-10 current customers.")
        scope = st.radio("Geographic Scope of Product*", ["Global", "India Only", "US Only", "Other"], horizontal=True)

    # --- 3. FINANCIAL DEEP DIVE ---
    st.markdown("### 3. Financial Health & Projections")
    st.info("Please provide values in **USD**.")
    
    f1, f2, f3 = st.columns(3)
    with f1:
        capital_raised = st.text_input("Total Capital Raised to Date (USD)*", placeholder="e.g. $2M")
        investors = st.text_area("Current Investors*", help="Who has invested so far? (VCs, Angels, etc.)")
    with f2:
        arr_2025 = st.text_input("Current ARR / 2025 Run Rate (USD)*", placeholder="e.g. $500k")
        tam = st.text_input("Total Addressable Market (TAM)*", placeholder="e.g. $10B")
    with f3:
        # Projections
        proj_2026 = st.text_input("Revenue Projection 2026", placeholder="e.g. $1.5M")
        proj_2027 = st.text_input("Revenue Projection 2027", placeholder="e.g. $4M")
        proj_2028 = st.text_input("Revenue Projection 2028", placeholder="e.g. $10M")

    # --- 4. IACCEL FIT ---
    st.markdown("### 4. Collaboration & Goals")
    
    services = st.multiselect("Services Needed*", ["US Market Access", "Fundraising (Debt/Equity)", "Operations Support"])
    
    # Logic for fundraising details
    fund_ask = ""
    if "Fundraising (Debt/Equity)" in services:
        fund_ask = st.text_input("If fundraising, how much are you looking to raise in this round? (USD)")

    deck_link = st.text_input("Pitch Deck Link (URL)", help="Link to DocSend, Google Drive, or Dropbox.")

    st.markdown("---")
    submitted = st.form_submit_button("Submit Strategic Assessment")

    if submitted:
        if not company_name or not email or not arr_2025 or not capital_raised:
            st.error("Please fill in all required fields marked with (*).")
        else:
            # Data Structure
            new_data = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Company": company_name,
                "Website": website,
                "Founder": founder_name,
                "Email": email,
                "LinkedIn": linkedin,
                "Industry": industry,
                # Strategic Info
                "Problem": problem_statement,
                "Solution": solution_desc,
                "Competitors": competitors,
                "Differentiation": differentiation,
                "Clients": current_clients,
                "Scope": scope,
                # Financials
                "Capital Raised": capital_raised,
                "Investors": investors,
                "ARR 2025": arr_2025,
                "TAM": tam,
                "Proj 2026": proj_2026,
                "Proj 2027": proj_2027,
                "Proj 2028": proj_2028,
                # Fit
                "Services": ", ".join(services),
                "Fund Ask": fund_ask,
                "Deck Link": deck_link
            }
            
            # Save Logic
            try:
                file_exists = os.path.exists(DATA_FILE)
                df = pd.DataFrame([new_data])
                df.to_csv(DATA_FILE, mode='a', header=not file_exists, index=False)
                st.success("✅ Application Received. Our investment committee will review your data.")
                st.balloons()
            except Exception as e:
                st.error(f"Error saving data: {e}")