import streamlit as st
from utils.sheets_clientview import append_row

SPREADSHEET_NAME = "Infinity-X Backend"
TAB_FACT_FIND = "Financial_Fact_Find"

st.title("Fact-Find (ClientView)")

st.markdown("This is a guided, client-friendly fact-find.")

col1, col2 = st.columns(2)
with col1:
    client_id = st.text_input("Client ID")
    name = st.text_input("Full Name")
    income = st.number_input("Monthly Income", min_value=0.0, step=1000.0)
    expenses = st.number_input("Monthly Expenses", min_value=0.0, step=500.0)
    assets = st.number_input("Total Assets", min_value=0.0, step=10000.0)
with col2:
    liabilities = st.number_input("Total Liabilities", min_value=0.0, step=10000.0)
    dependents = st.number_input("Number of Dependents", min_value=0, step=1)
    catalyst = st.text_input("Main reason for reviewing now (catalyst)")
    retirement_age = st.number_input("Target Retirement Age", min_value=40, max_value=80, step=1)
    education_goal = st.text_input("Education / major life goals")

if st.button("Save Fact-Find"):
    if not client_id:
        st.error("Client ID is required.")
    else:
        row = [
            client_id,
            income,
            expenses,
            assets,
            liabilities,
            dependents,
            catalyst,
            "",  # CoverLife
            "",  # CoverCI
            "",  # CoverDisability
            retirement_age,
            education_goal,
            "",  # LastUpdated (optional, can be filled by Apps Script later)
        ]
        append_row(SPREADSHEET_NAME, TAB_FACT_FIND, row)
        st.success("Fact-Find saved.")
