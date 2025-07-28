import streamlit as st
import project_example  # your library app code, assumed as a module or script with a main() function

# --- CSS to fix input colors ---
st.markdown("""
<style>
input[type="text"], input[type="password"] {
    background-color: white !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# --- LOGIN CODE ---
valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("Library Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password", placeholder="")
    login_clicked = st.button("Login")

    if login_clicked:
        if username == valid_username and password == valid_password:
            st.session_state.logged_in = True
            st.experimental_rerun()  # Reload to show main app immediately
        else:
            st.error("Invalid username or password.")

def main_app():
    # Call your actual library app code here:
    # If your project_example.py has a function main() that runs the app:
    project_example.main()
    
    # Or if not modularized, you can inline the project_example.py code here instead

# Show either login page or main app based on login state
if not st.session_state.logged_in:
    login_page()
else:
    st.success(f"Welcome, {valid_username.capitalize()}!")
    main_app()
