import streamlit as st
import library_app

valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_error" not in st.session_state:
    st.session_state.login_error = False
if "rerun_needed" not in st.session_state:
    st.session_state.rerun_needed = False

def login_page():
    st.title("Library Admin Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_clicked = st.button("Login")

    if login_clicked:
    if username == valid_username and password == valid_password:
        st.session_state.logged_in = True
        st.session_state.login_error = False
        st.stop()  # <-- replace rerun with stop here
    else:
        st.session_state.login_error = True


    if st.session_state.login_error:
        st.error("Invalid username or password.")

if not st.session_state.logged_in:
    login_page()
else:
    st.success(f"Welcome, {valid_username.capitalize()}!")
    library_app.main()

# Outside login_page(), do the rerun check
if st.session_state.get("rerun_needed"):
    st.session_state.rerun_needed = False
    st.experimental_rerun()
