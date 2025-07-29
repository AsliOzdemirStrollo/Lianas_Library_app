import streamlit as st
import pandas as pd
from db import get_connection  # or your existing connection import

import read
from My_create import create_member, create_book, create_loan, return_loan
from update_and_delete import update_member, delete_member, delete_book


def main():
    # ================== PAGE CONFIG & STYLES ==================
    st.set_page_config(page_title="Liana's Library", layout="wide")

    st.markdown("""
    <style>
    /* Shrink all sidebar elements */
    [data-testid="stSidebar"] * {
        font-size: 13px !important;
    }

    /* Shrink headers */
    [data-testid="stSidebar"] h2 {
        font-size: 16px !important;
        font-weight: 700;
        margin: 0.5rem 0 0.25rem 0;
        color: #4A4A4A;
    }
    [data-testid="stSidebar"] h3 {
        font-size: 14px !important;
        font-weight: 600;
        margin: 0.25rem 0 0 0;
    }

    /* Reduce selectbox height and spacing */
    section[data-testid="stSidebar"] .stSelectbox > div {
        padding-top: 2px !important;
        padding-bottom: 2px !important;
        margin-bottom: 4px !important;
    }
    section[data-testid="stSidebar"] label {
        font-size: 0px;
    }

    /* Tighten spacing between widgets */
    section[data-testid="stSidebar"] > div > div {
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }

    /* Make all text inputs white */
    input[type="text"], input[type="email"], input[type="tel"], input[type="date"], input[type="number"] {
        background-color: white !important;
        color: black !important;
    }

    /* Make all selectboxes white */
    .css-13cymwt-control, .css-1n76uvr-control, .stSelectbox > div, .stSelectbox div[data-baseweb="select"] {
        background-color: white !important;
        color: black !important;
    }

    /* Ensure all dropdown options are white */
    [data-baseweb="select"] div[role="option"], [data-baseweb="select"] div[role="listbox"] {
        background-color: white !important;
        color: black !important;
    }

    /* Selected value styling */
    div[data-baseweb="select"] > div {
        background-color: white !important;
        color: black !important;
        border-radius: 4px;
    }
    div[data-baseweb="select"] div[role="combobox"] {
        background-color: white !important;
        color: black !important;
    }

    /* Optional: textarea too */
    textarea {
        background-color: white !important;
        color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # ================== SIDEBAR ==================
    st.sidebar.markdown("## 📚 Library Actions")

    # Add actions
    st.sidebar.markdown("### ➕ Add")
    add_action = st.sidebar.selectbox(
        "Add Options",
        options=["-- Select an action --", "Add Member", "Add Book", "Add Loan"],
        key="add_action",
        label_visibility="collapsed"
    )

    # Delete actions
    st.sidebar.markdown("### 🗑️ Delete")
    delete_action = st.sidebar.selectbox(
        "Delete Options",
        options=["-- Select an action --", "Delete Member", "Delete Book"],
        key="delete_action",
        label_visibility="collapsed"
    )

    # Other actions
    st.sidebar.markdown("### ⚙️ Other")
    other_action = st.sidebar.selectbox(
        "Other Options",
        options=["-- Select an action --", "Update Member", "Return Loan"],
        key="other_action",
        label_visibility="collapsed"
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📈 Overviews")
    overview = st.sidebar.selectbox(
        "Select overview:",
        options=[
            "-- Select an action --",
            "📄 Loan History",
            "📖 Browse your books",
            "🢑 Find your members",
            "🔍 Search book status",
            "🔎 Search member"
        ],
        key="overview",
        label_visibility="collapsed"
    )

    if overview != "-- Select an action --":
        num_rows = st.sidebar.slider("How many rows to display?", 5, 50, 10, 5)
    else:
        num_rows = 10

    # ================== MAIN HEADER ==================
    st.markdown("<h1 style='text-align: center; color: #6C3483;'>📚 Welcome to Liana's Library</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #5D6D7E;'>So Your Books Always Find Their Way Back</h3>", unsafe_allow_html=True)

    # ================== THEME COLOR PICKER CENTERED BELOW HEADERS ==================
    if "page_color" not in st.session_state:
        st.session_state["page_color"] = "#F0F2F6"  # default color

    cols = st.columns([1, 2, 1])  # 3 columns, middle one wider
    with cols[1]:
        color_choice = st.color_picker(
            "🎨 Choose your page background color",
            st.session_state["page_color"],
            key="page_color_picker"
        )
        st.session_state["page_color"] = color_choice

    # ================== APPLY BACKGROUND COLOR ==================
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {st.session_state["page_color"]} !important;
        }}
        /* Make main content and sidebar backgrounds transparent so color shows through */
        .css-18e3th9, .css-1d391kg {{
            background-color: transparent !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    # ================== DEFAULT EMPTY STATE ==================
    if all([
        add_action == "-- Select an action --", 
        delete_action == "-- Select an action --", 
        other_action == "-- Select an action --", 
        overview == "-- Select an action --"
    ]):
        st.markdown(
            """
            <div style='text-align: center; color: #8B0000; margin-top: 3em;'>
                <h4>Please choose an action or overview from the sidebar.</h4>
                <div style='font-size: 48px;'>&larr;</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # ================== ACTIONS ==================
    add_funcs = {
    "Add Member": create_member,
    "Add Book": create_book,
    "Add Loan": create_loan
    }

    if add_action in add_funcs:
        add_funcs[add_action]()

    delete_funcs = {
        "Delete Member": delete_member,
        "Delete Book": delete_book
    }
    if delete_action in delete_funcs:
        delete_funcs[delete_action]()

    other_funcs = {
        "Update Member": update_member,
        "Return Loan": return_loan
    }
    if other_action in other_funcs:
        other_funcs[other_action]()

    # ================== OVERVIEWS ==================
    if overview == "📄 Loan History":
        st.markdown("### 📄 Loan History")
        filter_option = st.radio(
            "Filter loans by status:",
            options=["All Loans", "Loaned", "Returned"],
            index=0,
            horizontal=True,
            key="loan_filter"
        )
        loans_df = read.read_loans()
        if filter_option == "Loaned":
            filtered_df = loans_df[loans_df["Return_date"].isna()]
        elif filter_option == "Returned":
            filtered_df = loans_df[loans_df["Return_date"].notna()]
        else:
            filtered_df = loans_df
        display_df = filtered_df.rename(columns={
            'Member_FName': 'Member Name',
            'Member_LName': 'Member Last Name',
            'Borrow_date': 'Borrow Date',
            'Return_date': 'Return Date'
        })
        st.dataframe(display_df.head(num_rows))

    elif overview == "📖 Browse your books":
        st.markdown("### 📖 Library Catalog")
        only_available = st.checkbox("✅ Show only books available to loan")
        books_df = read.read_available_books_from_loans() if only_available else read.read_books()

        # Rename columns only for display
        display_df = books_df.rename(columns={
            'Author_FName': 'Author Name',
            'Author_LName': 'Author Last Name',
            'Publication_Year': 'Publication year'
        })

        st.dataframe(display_df.head(num_rows))

    elif overview == "🢑 Find your members":
        st.markdown("### 🢑 Member Directory")
        members_df = read.read_members()

        # Rename columns for display only
        display_df = members_df.rename(columns={
            'Member_FName': 'Member First Name',
            'Member_LName': 'Member Last Name',
            'Signup_Date': 'Signup Date',
            'Social_Media': 'Social Media'
        })

        st.dataframe(display_df.head(num_rows))

    elif overview == "🔍 Search book status":
        st.markdown("### 🔍 Check Book Loan Status")
        title_query = st.text_input("Enter book title:")
        if title_query:
            # Search books by title (case-insensitive contains)
            books_df = read.read_books()
            matches = books_df[books_df['Title'].str.contains(title_query, case=False, na=False)]
            if matches.empty:
                st.info("No books found with that title.")
            else:
                # For each match, show book info and loan status
                for idx, row in matches.iterrows():
                    st.markdown(f"**Title:** {row['Title']}")
                    st.markdown(f"Author: {row['Author_FName']} {row['Author_LName']}")
                    st.markdown(f"Published: {row['Publication_Year']}")
                    # Check if currently loaned out
                    loans_df = read.read_loans()
                    currently_loaned = loans_df[
                        (loans_df['Book_ID'] == row['Book_ID']) & (loans_df['Return_date'].isna())
                    ]
                    if currently_loaned.empty:
                        st.success("Status: Available")
                    else:
                        st.error("Status: Currently loaned out")
                    st.markdown("---")

    elif overview == "🔎 Search member":
        st.markdown("### 🔎 Search Member Information")
        member_name_query = st.text_input("Enter member first or last name:")
        if member_name_query:
            members_df = read.read_members()
            matches = members_df[
                members_df['Member_FName'].str.contains(member_name_query, case=False, na=False) |
                members_df['Member_LName'].str.contains(member_name_query, case=False, na=False)
            ]
            if matches.empty:
                st.info("No members found with that name.")
            else:
                display_df = matches.rename(columns={
                    'Member_FName': 'Member First Name',
                    'Member_LName': 'Member Last Name',
                    'Signup_Date': 'Signup Date',
                    'Social_Media': 'Social Media'
                })
                st.dataframe(display_df.head(num_rows))

if __name__ == "__main__":
    main()
