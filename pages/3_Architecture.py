import streamlit as st

st.title("Architecture (ClientView)")
st.markdown("Show the Must / Should / Could structure of their protection & savings.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Must")
    st.write("- Essential life cover")
    st.write("- Core income protection")
    st.write("- Minimum emergency fund")

with col2:
    st.subheader("Should")
    st.write("- Critical illness cover")
    st.write("- Education funding")
    st.write("- Retirement top-up")

with col3:
    st.subheader("Could")
    st.write("- Legacy planning")
    st.write("- Wealth accumulation extras")
    st.write("- Optional riders / enhancements")

st.markdown("---")
st.write("Use this visually while you speak. The actual numbers can come from your Console / backend.")
