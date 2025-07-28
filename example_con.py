import streamlit as st
from sqlalchemy import create_engine

schema = "Lianas_Library"
port = 3306

# Get sensitive info from Streamlit secrets
host = st.secrets["DB_HOST"]
user = st.secrets["DB_USER"]
password = st.secrets["DB_PASS"]

# Create SQLAlchemy engine string dynamically
module_string = f'mysql+pymysql://{user}:{password}@{host}:{port}/{schema}'
engine = create_engine(module_string)