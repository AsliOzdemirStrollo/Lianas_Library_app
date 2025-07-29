import streamlit as st
import library_app

# Read credentials from secrets
valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

# Initialize session state variables
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_error" not in st.session_state:
    st.session_state.login_error = False
if "login_attempted" not in st.session_state:
    st.session_state.login_attempted = False

# ✅ Successful login → set flag, re-run
if st.session_state.login_attempted and st.session_state.logged_in:
    st.session_state.login_attempted = False  # reset flag
    st.success(f"Welcome, {valid_username.capitalize()}!")
    library_app.main()
    st.stop()

# ⬇️ Login form (only shows if not logged in)
st.title("Library Admin Login")

username = st.text_input("Username")
password = st.text_input("Password", type="password")
login_clicked = st.button("Login")

if login_clicked:
    if username == valid_username and password == valid_password:
        st.session_state.logged_in = True
        st.session_state.login_attempted = True  # trigger rerun logic
        st.session_state.login_error = False
        st.experimental_rerun()  # Use if working; if not, rely on rerun by Streamlit itself
    else:
        st.session_state.login_error = True

if st.session_state.login_error:
    st.error("Invalid username or password.")
