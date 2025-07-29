import streamlit as st
import library_app

# Load credentials from Streamlit secrets
valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_error" not in st.session_state:
    st.session_state.login_error = False

def login_page():
    st.title("📚 Library Admin Login")

    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    login_clicked = st.button("Login")

    if login_clicked:
        # Debug prints
        st.write(f"Entered username: '{username}', password: '{password}'")  
        st.write(f"Valid username: '{valid_username}', password: '{valid_password}'")  

        # Normalize inputs
        entered_user = username.strip().lower()
        entered_pass = password.strip()
        valid_user = valid_username.strip().lower()
        valid_pass = valid_password.strip()

        if entered_user == valid_user and entered_pass == valid_pass:
            st.session_state.logged_in = True
            st.session_state.login_error = False
            st.rerun()  # <-- Use st.rerun() here
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
