import streamlit as st

st.title("Blueprint (ClientView)")
st.markdown("High-level summary of where they are and what the next steps could be.")

st.markdown("""
Use this page at the end of the meeting to summarise:

- Current position
- Key risks / gaps
- Agreed priorities
- Next steps
""")

summary_points = st.text_area("Type or refine the live summary here (not saved):")

st.info("You can copy this text into WhatsApp or email after the meeting.")
