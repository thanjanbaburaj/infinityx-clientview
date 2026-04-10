import streamlit as st

st.title("Blueprint (ClientView)")
st.markdown("Summarise the review and agreed next steps.")

st.markdown("""
Use this at the end of the meeting to summarise:
- Current position
- Key risks / gaps
- Agreed priorities
- Next steps
""")

summary = st.text_area("Live summary (not saved):")
st.info("You can copy this text into WhatsApp or email after the meeting.")
