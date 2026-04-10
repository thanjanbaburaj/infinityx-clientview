import streamlit as st
from utils.sheets_clientview import load_sheet

SPREADSHEET_NAME = "Infinity-X Backend"
TAB_FACT_FIND = "Financial_Fact_Find"

st.title("Gap Engine (ClientView)")
st.markdown("Explore risks and shortfalls based on the fact-find.")

client_id = st.text_input("Client ID")

if client_id:
    records = load_sheet("Financial_Fact_Find")
    row = next((r for r in records if str(r.get("ClientID", "")) == client_id), None)

    if not row:
        st.warning("No fact-find data found for this Client ID.")
    else:
        st.subheader("Current Snapshot")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Income: {row.get('Income', '')}")
            st.write(f"Expenses: {row.get('Expenses', '')}")
            st.write(f"Assets: {row.get('Assets', '')}")
        with col2:
            st.write(f"Liabilities: {row.get('Liabilities', '')}")
            st.write(f"Dependents: {row.get('Dependents', '')}")
            st.write(f"Retirement Age: {row.get('RetirementAge', '')}")

        st.subheader("Gap Conversation")
        st.markdown("""
- What happens if income stops?
- How long can current assets sustain the family?
- Are major goals (education, retirement) fully funded?
""")
        st.text_area("Talking points (not saved):")
else:
    st.info("Enter a Client ID to load gap context.")
