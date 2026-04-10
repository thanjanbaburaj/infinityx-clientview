import streamlit as st

st.set_page_config(
    page_title="Infinity-X ClientView",
    page_icon="💠",
    layout="wide"
)

def check_password():
    def verify():
        if st.session_state["password"] == st.secrets["CLIENTVIEW_PASSWORD"]:
            st.session_state["auth"] = True
        else:
            st.session_state["auth"] = False

    if "auth" not in st.session_state:
        st.text_input("Password", type="password", on_change=verify, key="password")
        st.stop()

    if not st.session_state["auth"]:
        st.text_input("Password", type="password", on_change=verify, key="password")
        st.error("Incorrect password.")
        st.stop()

check_password()

st.title("Infinity-X ClientView")
st.write("Use the sidebar to navigate the review journey.")
