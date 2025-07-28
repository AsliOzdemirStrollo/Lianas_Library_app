import streamlit as st
from sqlalchemy import text
from example_con import engine
from datetime import date
import read

import pandas as pd


# ---------------- Generic DB Insert Function ----------------

def insert_db(table, query_dict):
    keys = [key for key, value in query_dict.items() if value != ""]
    values = [f":{key}" for key in keys]

    query = f"""
        INSERT INTO {table} ({", ".join(keys)})
        VALUES ({", ".join(values)});
    """
    with engine.connect() as connection:
        transaction = connection.begin()
        try:
            connection.execute(text(query), {k: query_dict[k] for k in keys})
            transaction.commit()
        except Exception as e:
            transaction.rollback()
            st.error(f"Database error: {e}")
            raise

# ---------------- Member Validation Helpers ----------------

def validate_member_name(name):
    if name.strip() == "":
        st.warning("Member name cannot be empty.")
        return False
    return True

def validate_member_email(email):
    if email and ("@" not in email or "." not in email):
        st.warning("Please enter a valid email address.")
        return False
    return True

# ------------------ CREATE MEMBER ------------------

def create_member():
    if "member_validated" not in st.session_state:
        st.session_state["member_validated"] = False

    submission = st.empty()

    if st.session_state["member_validated"]:
        with submission.container():
            st.success(f"Member '{st.session_state['message']}' was successfully added!")
            if st.button("Add another member"):
                st.session_state["member_validated"] = False
    else:
        with submission.container():
            st.markdown("### ➕ Add New Member")
            with st.form("create_member"):
                fname = st.text_input("First Name")
                lname = st.text_input("Last Name")
                mobile = st.text_input("Mobile")
                email = st.text_input("Email")
                address = st.text_area("Address")
                social_media = st.text_input("Social Media (optional)")
                preference = st.selectbox(
                    "Preferred Contact Method", 
                    ["Email", "Mobile", "Address", "Social Media"]
                )
                status = st.selectbox(
                    "Member Status", 
                    ["active", "inactive", "suspended"]
                )
                check_form = st.form_submit_button("Submit Member")

            if check_form:
                fname_valid = validate_member_name(fname)
                lname_valid = validate_member_name(lname)
                email_valid = validate_member_email(email)
                mobile_valid = mobile.strip() != ""
                address_valid = address.strip() != ""

                if not mobile_valid:
                    st.warning("Mobile cannot be empty.")
                if not address_valid:
                    st.warning("Address cannot be empty.")

                social_required = preference == "Social Media"
                social_valid = not social_required or (social_media.strip() != "")
                if social_required and not social_valid:
                    st.warning("Social Media must be provided if selected as Preferred Contact Method.")

                if fname_valid and lname_valid and email_valid and mobile_valid and address_valid and social_valid:
                    with engine.connect() as conn:
                        result = conn.execute(text("""
                            SELECT * FROM Members 
                            WHERE Member_FName = :fname AND Member_LName = :lname AND Email = :email
                        """), {
                            "fname": fname.strip(),
                            "lname": lname.strip(),
                            "email": email.strip()
                        })
                        existing = result.fetchone()
                        if existing:
                            st.error("A member with the same name and email already exists.")
                            return

                    query_dict = {
                        "Member_FName": fname.strip(),
                        "Member_LName": lname.strip(),
                        "Mobile": mobile.strip(),
                        "Email": email.strip(),
                        "Address": address.strip(),
                        "Preference": preference,
                        "Member_Status": status,
                        "Signup_Date": date.today().isoformat(),
                        "Social_Media": social_media.strip() if social_media.strip() != "" else "N/A"
                    }

                    insert_db("Members", query_dict)
                    st.session_state["message"] = f"{fname.strip()} {lname.strip()}"
                    st.session_state["member_validated"] = True

                    # Show success message immediately below the button without rerun:
                    st.success(f"Member '{st.session_state['message']}' was successfully added!")

                    # Prevent form from showing again on this run so message stays visible:
                    return

# ------------------ CREATE BOOK ------------------

def create_book():
    if "book_validated" not in st.session_state:
        st.session_state["book_validated"] = False

    submission = st.empty()

    if st.session_state["book_validated"]:
        with submission.container():
            st.success(f"Book '{st.session_state['message']}' successfully added!")
            if st.button("Add another book"):
                st.session_state["book_validated"] = False
                # No rerun, state reset only
    else:
        with submission.container():
            st.markdown("### 📖 Add New Book to Library")
            with st.form("create_book"):
                title = st.text_input("Title")
                author_fname = st.text_input("Author First Name")
                author_lname = st.text_input("Author Last Name")
                publisher = st.text_input("Publisher")
                publication_year_str = st.text_input("Publication Year (YYYY)")
                genre = st.text_input("Genre")
                isbn = st.text_input("ISBN (13 digits)")
                check_form = st.form_submit_button("Submit Book")

            if check_form:
                if publication_year_str.strip() == "":
                    st.warning("Publication Year cannot be empty.")
                    return
                if not (publication_year_str.isdigit() and 1000 <= int(publication_year_str) <= 9999):
                    st.warning("Publication Year must be a 4-digit number between 1000 and 9999.")
                    return

                publication_year = int(publication_year_str)

                title_valid = title.strip() != ""
                isbn_valid = isbn.isnumeric() and len(isbn) == 13

                if not title_valid:
                    st.warning("Title cannot be empty.")
                if not isbn_valid:
                    st.warning("ISBN must be a 13-digit number.")

                if title_valid and isbn_valid:
                    with engine.connect() as conn:
                        result = conn.execute(text("SELECT * FROM Books WHERE ISBN = :isbn"), {"isbn": isbn.strip()})
                        existing = result.fetchone()
                        if existing:
                            st.warning("A book with this ISBN already exists in the library.")
                            return

                    book = {
                        "Title": title.strip(),
                        "Author_FName": author_fname.strip(),
                        "Author_LName": author_lname.strip(),
                        "Publisher": publisher.strip(),
                        "Publication_Year": publication_year,
                        "Genre": genre.strip(),
                        "ISBN": isbn.strip()
                    }
                    insert_db("Books", book)
                    st.success(f"Book '{title.strip()}' successfully added!")
                    # Optional: also update session state if needed later
                    st.session_state["message"] = title.strip()
                    st.session_state["book_validated"] = True


# ------------------ CREATE LOAN ------------------

def create_loan():
    st.markdown("### ➕ Add New Loan / Return Book")

    with st.form("create_loan"):
        member_fname = st.text_input("Member First Name")
        member_lname = st.text_input("Member Last Name")
        book_title = st.text_input("Book Title")
        borrow_date = st.date_input("Borrow Date", date.today())
        returning = st.checkbox("Returning book?")
        return_date = st.date_input("Return Date", date.today()) if returning else None

        submit_loan = st.form_submit_button("Submit")

        if submit_loan:
            if not member_fname.strip() or not member_lname.strip() or not book_title.strip():
                st.warning("Please fill in all fields.")
            else:
                with engine.connect() as conn:
                    # Get Member
                    member_res = conn.execute(text("""
                        SELECT MemberID FROM Members
                        WHERE Member_FName = :fname AND Member_LName = :lname
                    """), {"fname": member_fname.strip(), "lname": member_lname.strip()})
                    member = member_res.fetchone()
                    if not member:
                        st.error("Member not found.")
                        return
                    member_id = member.MemberID

                    # Get Book
                    book_res = conn.execute(text("""
                        SELECT ISBN FROM Books WHERE Title = :title
                    """), {"title": book_title.strip()})
                    book = book_res.fetchone()
                    if not book:
                        st.error("Book not found.")
                        return
                    isbn = book.ISBN

                    if returning:
                        active_loan = conn.execute(text("""
                            SELECT LoanID FROM Loans
                            WHERE MemberID = :member_id AND ISBN = :isbn AND Return_date IS NULL
                            ORDER BY Borrow_date DESC LIMIT 1
                        """), {"member_id": member_id, "isbn": isbn}).fetchone()

                        if not active_loan:
                            st.error("No active loan found to return.")
                            return

                        try:
                            conn.execute(text("""
                                UPDATE Loans SET Return_date = :return_date WHERE LoanID = :loan_id
                            """), {"return_date": return_date.isoformat(), "loan_id": active_loan.LoanID})
                            st.success(f"✅ Returned '{book_title.strip()}' for {member_fname.strip()} {member_lname.strip()}")
                        except Exception as e:
                            st.error(f"Failed to return loan: {e}")
                    else:
                        active_loan = conn.execute(text("""
                            SELECT * FROM Loans WHERE ISBN = :isbn AND Return_date IS NULL
                        """), {"isbn": isbn}).fetchone()
                        if active_loan:
                            st.warning("This book is already loaned out.")
                            return

                        try:
                            insert_db("Loans", {
                                "MemberID": member_id,
                                "ISBN": isbn,
                                "Borrow_date": borrow_date.isoformat(),
                                "Return_date": None
                            })
                            st.success(f"✅ Loan added: {member_fname.strip()} {member_lname.strip()} → '{book_title.strip()}'")
                        except Exception as e:
                            st.error(f"Failed to create loan: {e}")



# ------------------ RETURN LOAN ------------------


def return_loan():
    st.markdown("### Return a Loan")

    # Load all loans, filter active ones (no Return_date)
    loans_df = read.read_loans()
    active_loans_df = loans_df[loans_df["Return_date"].isna()]

    if active_loans_df.empty:
        st.info("No active loans to return.")
        return

    # Create a unique temporary LoanID based on row index
    active_loans_df = active_loans_df.reset_index(drop=True)
    active_loans_df["TempLoanID"] = active_loans_df.index

    # Build display labels for each loan
    loan_options = [
        (
            row["TempLoanID"],
            f'ID {row["TempLoanID"]} - "{row["Title"]}" borrowed by {row["Member_FName"]} {row["Member_LName"]} on {row["Borrow_date"]}'
        )
        for _, row in active_loans_df.iterrows()
    ]

    loan_ids = [opt[0] for opt in loan_options]
    loan_labels = [opt[1] for opt in loan_options]

    # Add placeholder to the top of the dropdown
    placeholder_option = "🔁 Select a loan to return"
    loan_labels_with_placeholder = [placeholder_option] + loan_labels

    selected_label = st.selectbox("Select loan to return:", loan_labels_with_placeholder)

    if selected_label != placeholder_option:
        selected_index = loan_labels.index(selected_label)
        selected_temp_loan_id = loan_ids[selected_index]

        if st.button("Return Selected Loan"):
            selected_loan = active_loans_df.loc[active_loans_df["TempLoanID"] == selected_temp_loan_id].iloc[0]

            member_fname = selected_loan["Member_FName"]
            member_lname = selected_loan["Member_LName"]
            book_title = selected_loan["Title"]
            borrow_date = selected_loan["Borrow_date"]

            # Update the loan's Return_date
            update_return_date_in_db(member_fname, member_lname, book_title, borrow_date)

            st.success(f'✅ Loan for "{book_title}" borrowed by {member_fname} {member_lname} has been returned.')
    else:
        st.info("Please select a loan to return.")


def update_return_date_in_db(member_fname, member_lname, book_title, borrow_date):
    import example_con
    from example_con import engine
    from sqlalchemy import text
    import datetime

    today = datetime.date.today()

    query = """
    UPDATE Loans L
    JOIN Members M ON L.MemberID = M.MemberID
    JOIN Books B ON L.ISBN = B.ISBN
    SET L.Return_date = :today
    WHERE M.Member_FName = :member_fname
      AND M.Member_LName = :member_lname
      AND B.Title = :book_title
      AND L.Borrow_date = :borrow_date
      AND L.Return_date IS NULL
    """

    with engine.connect() as conn:
        conn.execute(text(query), {
            "today": today,
            "member_fname": member_fname,
            "member_lname": member_lname,
            "book_title": book_title,
            "borrow_date": borrow_date
        })
        conn.commit()



# ----- File upload

def upload_books_from_csv():
    st.markdown("### 📂 Upload Books via CSV")

    uploaded_file = st.file_uploader(
        "Choose a CSV file with columns: ISBN, Title, Author_FName, Author_LName, Publisher, Publication_Year, Genre",
        type=["csv"]
    )

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)

            required_columns = ["ISBN", "Title", "Author_FName", "Author_LName", "Publisher", "Publication_Year", "Genre"]
            missing_cols = [col for col in required_columns if col not in df.columns]
            if missing_cols:
                st.error(f"CSV is missing required columns: {', '.join(missing_cols)}")
                return

            # ✅ FIXED: Clean and trim all values as strings (to prevent .str error)
            for col in required_columns:
                df[col] = df[col].fillna("").astype(str).str.strip()

            # Validate ISBN: must be numeric and 13 digits
            df['ISBN_valid'] = df['ISBN'].str.isnumeric() & (df['ISBN'].str.len() == 13)
            invalid_isbn_rows = df[~df['ISBN_valid']]

            # Validate Publication_Year: 4-digit numeric between 1000 and 9999
            df['Publication_Year_valid'] = df['Publication_Year'].apply(
                lambda x: str(x).isdigit() and 1000 <= int(x) <= 9999
            )
            invalid_year_rows = df[~df['Publication_Year_valid']]

            if not invalid_isbn_rows.empty:
                st.warning(f"Skipped {len(invalid_isbn_rows)} rows with invalid ISBN (must be 13-digit numeric).")

            if not invalid_year_rows.empty:
                st.warning(f"Skipped {len(invalid_year_rows)} rows with invalid Publication Year (must be 4-digit year).")

            # Filter only valid rows
            valid_rows = df[df['ISBN_valid'] & df['Publication_Year_valid']]

            if valid_rows.empty:
                st.info("No valid rows to insert after validation.")
                return

            # Check duplicates in DB by ISBN
            isbns = valid_rows['ISBN'].tolist()
            with engine.connect() as conn:
                query = text("SELECT ISBN FROM Books WHERE ISBN IN :isbns")
                existing_books = conn.execute(query, {"isbns": tuple(isbns)}).fetchall()
                existing_isbns = set(row.ISBN for row in existing_books)

            # Filter out existing ISBNs
            new_books = valid_rows[~valid_rows['ISBN'].isin(existing_isbns)]

            if new_books.empty:
                st.info("No new books to add; all ISBNs already exist in the database.")
                return

            # Insert new books
            inserted_count = 0
            for _, row in new_books.iterrows():
                book_data = {
                    "ISBN": row["ISBN"],
                    "Title": row["Title"],
                    "Author_FName": row["Author_FName"],
                    "Author_LName": row["Author_LName"],
                    "Publisher": row["Publisher"],
                    "Publication_Year": int(row["Publication_Year"]),
                    "Genre": row["Genre"]
                }
                try:
                    insert_db("Books", book_data)
                    inserted_count += 1
                except Exception as e:
                    st.error(f"Failed to insert book '{row['Title']}': {e}")

            st.success(f"Inserted {inserted_count} new books into the library.")

            if existing_isbns:
                st.info(f"Skipped {len(existing_isbns)} books due to duplicate ISBNs already in the database.")

        except Exception as e:
            st.error(f"Failed to process CSV: {e}")

def add_book_section():
    create_book()           # Your full existing Add Book form remains unchanged
    st.markdown("---")      # Divider line to separate visually
    st.markdown("Or upload books via CSV:")  
    upload_books_from_csv() # CSV upload option appears below the form








