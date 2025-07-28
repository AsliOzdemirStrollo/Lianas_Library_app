import streamlit as st
import library_app  # This is your actual app code, assuming it defines a main() function

# import project_example  # your library app code, assumed as a module or script with a main() function

# --- CSS to fix input colors ---
st.markdown("""
<style>
input[type="text"], input[type="password"] {
    background-color: white !important;
    color: black !important;
}
</style>
""", unsafe_allow_html=True)

# --- LOGIN CREDENTIALS ---
valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

# --- SESSION STATE SETUP ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN PAGE ---
def login_page():
    st.title("Library Admin Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password", placeholder="")
    login_clicked = st.button("Login")

    if login_clicked:
        if username == valid_username and password == valid_password:
            st.session_state.logged_in = True
        else:
            st.error("Invalid username or password.")

# --- MAIN APP WRAPPER ---
def main_app():
    library_app.main()  # Call your real app

# --- PAGE ROUTING ---
if not st.session_state.logged_in:
    login_page()
else:
    st.success(f"Welcome, {valid_username.capitalize()}!")
    main_app()
