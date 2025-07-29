import streamlit as st
from datetime import date
from db import get_connection  # Your DB connection function


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
                if fname.strip() == "" or lname.strip() == "" or mobile.strip() == "" or address.strip() == "":
                    st.warning("Please fill all required fields.")
                    return

                if email and ("@" not in email or "." not in email):
                    st.warning("Please enter a valid email address.")
                    return

                if preference == "Social Media" and social_media.strip() == "":
                    st.warning("Social Media must be provided if selected as Preferred Contact Method.")
                    return

                # Check for existing member
                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute(
                        """
                        SELECT * FROM Members
                        WHERE Member_FName = ? AND Member_LName = ? AND Email = ?
                        """,
                        (fname.strip(), lname.strip(), email.strip())
                    )
                    existing = cursor.fetchone()
                    if existing:
                        st.error("A member with the same name and email already exists.")
                        cursor.close()
                        conn.close()
                        return
                except Exception as e:
                    st.error(f"Database error: {e}")
                    return

                # Insert member
                try:
                    cursor.execute(
                        """
                        INSERT INTO Members 
                        (Member_FName, Member_LName, Mobile, Email, Address, Preference, Member_Status, Signup_Date, Social_Media)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            fname.strip(),
                            lname.strip(),
                            mobile.strip(),
                            email.strip(),
                            address.strip(),
                            preference,
                            status,
                            date.today().isoformat(),
                            social_media.strip() if social_media.strip() != "" else "N/A"
                        )
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()

                    st.session_state["message"] = f"{fname.strip()} {lname.strip()}"
                    st.session_state["member_validated"] = True
                    st.success(f"Member '{st.session_state['message']}' was successfully added!")
                except Exception as e:
                    st.error(f"Failed to add member: {e}")
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()


def create_book():
    if "book_validated" not in st.session_state:
        st.session_state["book_validated"] = False

    submission = st.empty()

    if st.session_state["book_validated"]:
        with submission.container():
            st.success(f"Book '{st.session_state['message']}' successfully added!")
            if st.button("Add another book"):
                st.session_state["book_validated"] = False
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

                if title.strip() == "":
                    st.warning("Title cannot be empty.")
                    return
                if not (isbn.isnumeric() and len(isbn) == 13):
                    st.warning("ISBN must be a 13-digit number.")
                    return

                try:
                    conn = get_connection()
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM Books WHERE ISBN = ?", (isbn.strip(),))
                    existing = cursor.fetchone()
                    if existing:
                        st.warning("A book with this ISBN already exists in the library.")
                        cursor.close()
                        conn.close()
                        return
                except Exception as e:
                    st.error(f"Database error: {e}")
                    return

                try:
                    cursor.execute(
                        """
                        INSERT INTO Books
                        (Title, Author_FName, Author_LName, Publisher, Publication_Year, Genre, ISBN)
                        VALUES (?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            title.strip(),
                            author_fname.strip(),
                            author_lname.strip(),
                            publisher.strip(),
                            publication_year,
                            genre.strip(),
                            isbn.strip()
                        )
                    )
                    conn.commit()
                    cursor.close()
                    conn.close()
                    st.success(f"Book '{title.strip()}' successfully added!")
                    st.session_state["message"] = title.strip()
                    st.session_state["book_validated"] = True
                except Exception as e:
                    st.error(f"Failed to add book: {e}")
                    if cursor:
                        cursor.close()
                    if conn:
                        conn.close()


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
                return

            try:
                conn = get_connection()
                cursor = conn.cursor()

                # Get Member ID
                cursor.execute(
                    """
                    SELECT MemberID FROM Members WHERE Member_FName = ? AND Member_LName = ?
                    """,
                    (member_fname.strip(), member_lname.strip())
                )
                member = cursor.fetchone()
                if not member:
                    st.error("Member not found.")
                    cursor.close()
                    conn.close()
                    return
                member_id = member[0]

                # Get Book ISBN
                cursor.execute(
                    "SELECT ISBN FROM Books WHERE Title = ?",
                    (book_title.strip(),)
                )
                book = cursor.fetchone()
                if not book:
                    st.error("Book not found.")
                    cursor.close()
                    conn.close()
                    return
                isbn = book[0]

                if returning:
                    # Find active loan for this member and book
                    cursor.execute(
                        """
                        SELECT LoanID FROM Loans
                        WHERE MemberID = ? AND ISBN = ? AND Return_date IS NULL
                        ORDER BY Borrow_date DESC LIMIT 1
                        """,
                        (member_id, isbn)
                    )
                    active_loan = cursor.fetchone()
                    if not active_loan:
                        st.error("No active loan found to return.")
                        cursor.close()
                        conn.close()
                        return
                    loan_id = active_loan[0]

                    # Update Return_date
                    cursor.execute(
                        """
                        UPDATE Loans SET Return_date = ? WHERE LoanID = ?
                        """,
                        (return_date.isoformat(), loan_id)
                    )
                    conn.commit()
                    st.success(f"✅ Returned '{book_title.strip()}' for {member_fname.strip()} {member_lname.strip()}")

                else:
                    # Check if book is already loaned out (Return_date IS NULL)
                    cursor.execute(
                        """
                        SELECT * FROM Loans WHERE ISBN = ? AND Return_date IS NULL
                        """,
                        (isbn,)
                    )
                    active_loan = cursor.fetchone()
                    if active_loan:
                        st.warning("This book is already loaned out.")
                        cursor.close()
                        conn.close()
                        return

                    # Insert new loan
                    cursor.execute(
                        """
                        INSERT INTO Loans (MemberID, ISBN, Borrow_date, Return_date)
                        VALUES (?, ?, ?, NULL)
                        """,
                        (member_id, isbn, borrow_date.isoformat())
                    )
                    conn.commit()
                    st.success(f"✅ Loan added: {member_fname.strip()} {member_lname.strip()} → '{book_title.strip()}'")

                cursor.close()
                conn.close()

            except Exception as e:
                st.error(f"Database error: {e}")
                try:
                    cursor.close()
                except:
                    pass
                try:
                    conn.close()
                except:
                    pass
