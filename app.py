import streamlit as st

st.set_page_config(
    page_title="Infinity-X ClientView",
    page_icon="💠",
    layout="wide"
)

def check_password():
    def password_entered():
        if st.session_state["password"] == st.secrets.get("CLIENTVIEW_PASSWORD", ""):
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.stop()
    elif not st.session_state["password_correct"]:
        st.text_input("Password", type="password", on_change=password_entered, key="password")
        st.error("Incorrect password.")
        st.stop()

check_password()

st.title("Infinity-X ClientView")
st.write("Use the sidebar to navigate the client-facing modules.")
