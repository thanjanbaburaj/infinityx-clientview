import streamlit as st

st.title("Architecture (ClientView)")
st.markdown("Visualise Must / Should / Could priorities.")

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Must")
    st.write("- Essential life cover")
    st.write("- Core income protection")
    st.write("- Emergency fund")

with col2:
    st.subheader("Should")
    st.write("- Critical illness cover")
    st.write("- Education funding")
    st.write("- Retirement top-up")

with col3:
    st.subheader("Could")
    st.write("- Legacy planning")
    st.write("- Extra wealth accumulation")
    st.write("- Optional riders")

st.markdown("---")
st.caption("Use this visually while you speak; numbers live in your Console.")
