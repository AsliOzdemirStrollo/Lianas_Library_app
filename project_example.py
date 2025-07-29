import streamlit as st
import library_app

valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_error" not in st.session_state:
    st.session_state.login_error = False

def login_page():
    st.title("Library Admin Login")

    # Custom CSS for colorful login page
    st.markdown(
        """
        <style>
        /* Background gradient */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            min-height: 100vh;
            padding: 50px 20px;
        }
        /* Center the form container */
        .css-1d391kg {  /* This class controls form container; may need adjustment if Streamlit updates */
            max-width: 400px;
            margin: auto;
            background: rgba(255, 255, 255, 0.1);
            padding: 30px 40px;
            border-radius: 15px;
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
            backdrop-filter: blur(8.5px);
            -webkit-backdrop-filter: blur(8.5px);
            border: 1px solid rgba(255, 255, 255, 0.18);
        }
        /* Style input fields */
        input[type="text"], input[type="password"] {
            background: rgba(255, 255, 255, 0.3) !important;
            color: white !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 10px 15px !important;
            font-size: 1rem !important;
            margin-bottom: 20px !important;
        }
        /* Style the login button */
        div.stButton > button {
            background: linear-gradient(90deg, #f7971e 0%, #ffd200 100%);
            color: #222 !important;
            font-weight: 700;
            font-size: 1.1rem;
            border-radius: 12px;
            padding: 10px 0;
            width: 100%;
            box-shadow: 0 4px 15px rgba(255, 210, 0, 0.4);
            transition: all 0.3s ease;
        }
        div.stButton > button:hover {
            filter: brightness(110%);
            cursor: pointer;
        }
        /* Error message styling */
        .stAlert {
            background-color: #ff4b4b !important;
            color: white !important;
            border-radius: 8px !important;
            padding: 10px !important;
            font-weight: 700 !important;
            margin-top: 10px !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_clicked = st.form_submit_button("Login")

        if login_clicked:
            if username == valid_username and password == valid_password:
                st.session_state.logged_in = True
                st.session_state.login_error = False
                st.rerun()
            else:
                st.session_state.login_error = True

    if st.session_state.login_error:
        st.error("Invalid username or password.")

# App logic
if not st.session_state.logged_in:
    login_page()
else:
    st.success(f"Welcome, {valid_username.capitalize()}!")
    library_app.main()
