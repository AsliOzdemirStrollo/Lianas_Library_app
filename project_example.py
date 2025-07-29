import streamlit as st
from sql_auth_functions import verify_password  # Make sure this is defined

st.set_page_config(page_title="Liana's Library", page_icon="📚")

# Session state setup
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'user_role' not in st.session_state:
    st.session_state.user_role = None

# Login page
def login_page():
    st.title("🔐 Liana's Library Login")
    st.markdown("Please enter your credentials to access the library management system.")

    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if username and password:
                is_valid, role = verify_password(username, password)
                if is_valid:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.user_role = role
                    st.success(f"Welcome, {username}! You are logged in as {role}.")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")
            else:
                st.warning("Please enter both username and password.")

# Logout button
def logout_button():
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.session_state.user_role = None
        st.rerun()

# Main logic
if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.write(f"Logged in as: **{st.session_state.username}** ({st.session_state.user_role})")
    logout_button()

    # Navigation to other pages (adjust paths as needed)
    overview_page1 = st.Page("p1_overview.py", title="Library Overview", icon=":books:")
    datainput_page2 = st.Page("p2_datainput.py", title="Data Input", icon=":pencil:")

    pg = st.navigation([overview_page1, datainput_page2])
    pg.run()
