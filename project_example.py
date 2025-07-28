import streamlit as st
import project_example  # or import library_app

valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("Library Admin Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_clicked = st.button("Login")

    if login_clicked:
        if username == valid_username and password == valid_password:
            st.session_state.logged_in = True
            # No st.experimental_rerun here, just rely on session_state rerun
        else:
            st.error("Invalid username or password.")

if not st.session_state.logged_in:
    login_page()
else:
    st.success(f"Welcome, {valid_username.capitalize()}!")
    project_example.main()  # run your library app here
