import streamlit as st
import library_app

import streamlit as st
st.write("Streamlit version:", st.__version__)

valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_error" not in st.session_state:
    st.session_state.login_error = False
if "login_triggered" not in st.session_state:
    st.session_state.login_triggered = False  # flag to trigger rerun

def login_page():
    st.title("Library Admin Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_clicked = st.button("Login")

    if login_clicked:
        if username == valid_username and password == valid_password:
            st.session_state.logged_in = True
            st.session_state.login_error = False
            st.session_state.login_triggered = True  # set rerun flag
        else:
            st.session_state.login_error = True

    if st.session_state.login_error:
        st.error("Invalid username or password.")

# Main logic
if not st.session_state.logged_in:
    login_page()
else:
    st.success(f"Welcome, {valid_username.capitalize()}!")
    library_app.main()

# AFTER everything else — do rerun if login just triggered
if st.session_state.get("login_triggered", False):
    st.session_state.login_triggered = False
    st.experimental_rerun()
