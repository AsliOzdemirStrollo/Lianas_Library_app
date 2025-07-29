import streamlit as st
import random
import library_app

def generate_star_shadows(n, max_x=2000, max_y=2000):
    """Generates a string of multiple box-shadows for stars."""
    shadows = []
    for _ in range(n):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        shadows.append(f"{x}px {y}px #FFF")
    return ", ".join(shadows)

# Generate star shadows for layers
shadows_small = generate_star_shadows(700)
shadows_medium = generate_star_shadows(200)
shadows_big = generate_star_shadows(100)

# Inject CSS for starry background and form styling
st.markdown(f"""
<style>
  /* Reset */
  * {{
    margin: 0;
    padding: 0;
    box-sizing: border-box !important;
  }}

  html, body, .stApp {{
    height: 100%;
    background: radial-gradient(ellipse at bottom, #E0F7FF 0%, #B3E5FC 100%);
    overflow: hidden;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #03396c;
    position: relative;
  }}

  /* Star layers */
  #stars, #stars2, #stars3 {{
    position: fixed;
    top: 0; left: 0;
    width: 1px; height: 1px;
    background: transparent;
    pointer-events: none;
    z-index: 0;
  }}

  #stars {{
    box-shadow: {shadows_small};
    animation: animStar 60s linear infinite;
  }}
  #stars:after {{
    content: "";
    position: absolute;
    top: 2000px;
    width: 1px; height: 1px;
    background: transparent;
    box-shadow: {shadows_small};
  }}

  #stars2 {{
    width: 2px; height: 2px;
    box-shadow: {shadows_medium};
    animation: animStar 100s linear infinite;
  }}
  #stars2:after {{
    content: "";
    position: absolute;
    top: 2000px;
    width: 2px; height: 2px;
    background: transparent;
    box-shadow: {shadows_medium};
  }}

  #stars3 {{
    width: 3px; height: 3px;
    box-shadow: {shadows_big};
    animation: animStar 140s linear infinite;
  }}
  #stars3:after {{
    content: "";
    position: absolute;
    top: 2000px;
    width: 3px; height: 3px;
    background: transparent;
    box-shadow: {shadows_big};
  }}

  @keyframes animStar {{
    from {{ transform: translateY(0); }}
    to {{ transform: translateY(-2000px); }}
  }}

  /* Form container on top */
  .css-1d391kg {{
    position: relative !important;
    z-index: 10 !important;
    max-width: 420px !important;
    margin: auto !important;
    background: rgba(255, 255, 255, 0.85) !important;
    padding: 30px 40px !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    backdrop-filter: blur(10px);
    color: #03396c !important;
  }}

  /* Inputs */
  input[type="text"], input[type="password"] {{
    background: rgba(255, 255, 255, 0.9) !important;
    color: #03396c !important;
    border: 1.8px solid #90CAF9 !important;
    border-radius: 10px !important;
    padding: 12px 15px !important;
    font-size: 1.1rem !important;
    line-height: 1.4 !important;
    vertical-align: middle !important;
    box-shadow: inset 0 1px 3px rgb(0 0 0 / 0.1);
    transition: border-color 0.3s ease;
  }}
  input[type="text"]:focus, input[type="password"]:focus {{
    border-color: #42A5F5 !important;
    outline: none !important;
    box-shadow: 0 0 8px #42A5F5 !important;
  }}

  /* Button */
  div.stButton > button {{
    background: linear-gradient(90deg, #42A5F5 0%, #1E88E5 100%) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1.2rem !important;
    border-radius: 15px !important;
    padding: 14px 0 !important;
    width: 100% !important;
    box-shadow: 0 6px 15px rgba(30, 136, 229, 0.6) !important;
    border: none !important;
    cursor: pointer !important;
    transition: background 0.3s ease !important;
  }}
  div.stButton > button:hover {{
    background: linear-gradient(90deg, #1E88E5 0%, #1565C0 100%) !important;
  }}

  /* Error */
  .stAlert {{
    background-color: #FFCDD2 !important;
    color: #B71C1C !important;
    border-radius: 10px !important;
    padding: 12px !important;
    font-weight: 700 !important;
    margin-top: 12px !important;
    text-align: center !important;
  }}
</style>
""", unsafe_allow_html=True)

# Inject stars divs for the animation
st.markdown("""
<div id='stars'></div>
<div id='stars2'></div>
<div id='stars3'></div>
""", unsafe_allow_html=True)

valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_error" not in st.session_state:
    st.session_state.login_error = False

def login_page():
    st.title("Library Admin Login")

    with st.form("login_form"):
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        login_clicked = st.form_submit_button("Login")

        if login_clicked:
            if username == valid_username and password == valid_password:
                st.session_state.logged_in = True
                st.session_state.login_error = False
                st.experimental_rerun()  # rerun app on login success
            else:
                st.session_state.login_error = True

    if st.session_state.login_error:
        st.error("Invalid username or password.")

# Main app logic
if not st.session_state.logged_in:
    login_page()
else:
    st.success(f"Welcome, {valid_username.capitalize()}!")
    library_app.main()
