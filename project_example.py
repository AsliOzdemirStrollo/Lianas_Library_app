import streamlit as st
import random
import library_app

def generate_star_shadows(n, max_x=2000, max_y=2000, size=1):
    """Generates box-shadows for stars."""
    shadows = []
    for _ in range(n):
        x = random.randint(0, max_x)
        y = random.randint(0, max_y)
        shadows.append(f"{x}px {y}px #FFF")
    return ", ".join(shadows)

# Larger and more visible stars
shadows_small = generate_star_shadows(300, size=2)
shadows_medium = generate_star_shadows(150, size=3)
shadows_big = generate_star_shadows(60, size=4)

# Inject CSS
st.markdown(f"""
<style>
  html, body, .stApp {{
    height: 100%;
    background: radial-gradient(ellipse at bottom, #E0F7FF 0%, #B3E5FC 100%);
    overflow: hidden;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    color: #03396c;
    position: relative;
  }}

  #stars, #stars2, #stars3 {{
    position: fixed;
    top: 0; left: 0;
    width: 2px; height: 2px;
    background: transparent;
    pointer-events: none;
    z-index: 0;
  }}

  #stars {{
    box-shadow: {shadows_small};
    animation: animStar 80s linear infinite;
  }}
  #stars:after {{
    content: "";
    position: absolute;
    top: 2000px;
    width: 2px; height: 2px;
    box-shadow: {shadows_small};
  }}

  #stars2 {{
    width: 3px; height: 3px;
    box-shadow: {shadows_medium};
    animation: animStar 120s linear infinite;
  }}
  #stars2:after {{
    content: "";
    position: absolute;
    top: 2000px;
    width: 3px; height: 3px;
    box-shadow: {shadows_medium};
  }}

  #stars3 {{
    width: 4px; height: 4px;
    box-shadow: {shadows_big};
    animation: animStar 160s linear infinite;
  }}
  #stars3:after {{
    content: "";
    position: absolute;
    top: 2000px;
    width: 4px; height: 4px;
    box-shadow: {shadows_big};
  }}

  @keyframes animStar {{
    from {{ transform: translateY(0); }}
    to {{ transform: translateY(-2000px); }}
  }}

  /* Centering login box */
  .login-container {{
    background: rgba(255, 255, 255, 0.9);
    padding: 40px 30px;
    max-width: 400px;
    margin: 100px auto;
    border-radius: 20px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    position: relative;
    z-index: 1;
    text-align: center;
  }}

  .login-container h1 {{
    margin-bottom: 25px;
    color: #01579B;
  }}

  .stTextInput input {{
    background: white;
    color: #03396c;
    padding: 12px 16px;
    border: 2px solid #81D4FA;
    border-radius: 10px;
    font-size: 1rem;
  }}

  .stTextInput input:focus {{
    border-color: #0288D1;
    outline: none;
    box-shadow: 0 0 5px #0288D1;
  }}

  div.stButton > button {{
    background: linear-gradient(90deg, #29B6F6, #0288D1);
    color: white;
    font-weight: bold;
    font-size: 1.1rem;
    border-radius: 10px;
    padding: 12px;
    width: 100%;
    border: none;
    box-shadow: 0 5px 12px rgba(0,0,0,0.15);
    margin-top: 20px;
  }}

  div.stButton > button:hover {{
    background: linear-gradient(90deg, #0288D1, #0277BD);
  }}

  .stAlert {{
    background-color: #FFCDD2;
    color: #B71C1C;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
    text-align: center;
  }}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div id='stars'></div>
<div id='stars2'></div>
<div id='stars3'></div>
""", unsafe_allow_html=True)

# App secrets (replace these in Streamlit Cloud secrets)
valid_username = st.secrets["APP_USERNAME"]
valid_password = st.secrets["APP_PASSWORD"]

# Initialize state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "login_error" not in st.session_state:
    st.session_state.login_error = False

# Login form
def login_page():
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    st.markdown("<h1>Library Admin Login</h1>", unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_clicked = st.form_submit_button("Login")

        if login_clicked:
            if username == valid_username and password == valid_password:
                st.session_state.logged_in = True
                st.session_state.login_error = False
                st.rerun()
            else:
                st.session_state.login_error = True

    st.markdown('</div>', unsafe_allow_html=True)

    if st.session_state.login_error:
        st.error("Invalid username or password.")

# App logic
if not st.session_state.logged_in:
    login_page()
else:
    st.success(f"Welcome, {valid_username.capitalize()}!")
    library_app.main()
