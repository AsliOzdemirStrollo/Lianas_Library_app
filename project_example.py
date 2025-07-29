import streamlit as st
import library_app

valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_error" not in st.session_state:
    st.session_state.login_error = False

# ✅ Move login check to the top-level block
if st.session_state.logged_in:
    st.success(f"Welcome, {valid_username.capitalize()}!")
    library_app.main()
    st.stop()

# ⬇️ Only runs if not logged in
st.title("Library Admin Login")

username = st.text_input("Username", key="login_username")
password = st.text_input("Password", type="password", key="login_password")
login_clicked = st.button("Login")

if login_clicked:
    if username == valid_username and password == valid_password:
        st.session_state.logged_in = True
        st.session_state.login_error = False
        st.stop()  # ✅ stop here, and app will rerun with logged_in=True
    else:
        st.session_state.login_error = True

if st.session_state.login_error:
    st.error("Invalid username or password.")
