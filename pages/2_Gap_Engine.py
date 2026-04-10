import streamlit as st
from utils.sheets_clientview import load_sheet_as_df

SPREADSHEET_NAME = "Infinity-X Backend"
TAB_FACT_FIND = "Financial_Fact_Find"

st.title("Gap Engine (ClientView)")
st.markdown("Quickly explore protection and planning gaps based on the fact-find.")

client_id = st.text_input("Client ID")

if client_id:
    df = load_sheet_as_df(SPREADSHEET_NAME, TAB_FACT_FIND)
    row = df[df["ClientID"] == client_id] if not df.empty else None

    if row is None or row.empty:
        st.warning("No fact-find data found for this Client ID yet.")
    else:
        r = row.iloc[0]
        st.subheader("Current Snapshot")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"Income: {r.get('Income', '')}")
            st.write(f"Expenses: {r.get('Expenses', '')}")
            st.write(f"Assets: {r.get('Assets', '')}")
        with col2:
            st.write(f"Liabilities: {r.get('Liabilities', '')}")
            st.write(f"Dependents: {r.get('Dependents', '')}")
            st.write(f"Retirement Age: {r.get('RetirementAge', '')}")

        st.subheader("Gap Narrative")
        st.write("Use this section live with the client to talk through:")
        st.markdown("""
        - What happens if income stops?
        - How long can current assets sustain the family?
        - Are major goals (education, retirement) fully funded?
        """)

        notes = st.text_area("Talking points / notes (for you, not saved here)")
else:
    st.info("Enter a Client ID to load gap context.")
