import streamlit as st
from sqlalchemy import text
from example_con import engine
from datetime import date

def update_member():
    st.markdown("### 🔄 Update Member Information")

    with st.form("update_member_form"):
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email")
        mobile = st.text_input("Mobile")
        address = st.text_area("Address")
        social_media = st.text_input("Social Media (optional)")
        preference = st.selectbox("Preferred Contact Method", ["Email", "Mobile", "Address", "Social Media"])
        status = st.selectbox("Member Status", ["active", "inactive", "suspended"])
        submit = st.form_submit_button("Update Member")

    if submit:
        if not fname.strip() or not lname.strip() or not email.strip():
            st.warning("First name, last name, and email are required to identify the member.")
            return

        with engine.begin() as conn:  # handles connection + transaction
            result = conn.execute(text("""
                SELECT MemberID FROM Members 
                WHERE Member_FName = :fname AND Member_LName = :lname AND Email = :email
            """), {
                "fname": fname.strip(),
                "lname": lname.strip(),
                "email": email.strip()
            })
            member = result.fetchone()

            if not member:
                st.error("Member does not exist. Please add the member first.")
                return

            if preference == "Social Media" and not social_media.strip():
                st.warning("Social Media must be provided if selected as Preferred Contact Method.")
                return

            update_query = text("""
                UPDATE Members SET
                    Member_FName = :fname,
                    Member_LName = :lname,
                    Email = :email,
                    Mobile = :mobile,
                    Address = :address,
                    Social_Media = :social,
                    Preference = :preference,
                    Member_Status = :status
                WHERE MemberID = :member_id
            """)

            conn.execute(update_query, {
                "fname": fname.strip(),
                "lname": lname.strip(),
                "email": email.strip(),
                "mobile": mobile.strip(),
                "address": address.strip(),
                "social": social_media.strip() if social_media.strip() else "N/A",
                "preference": preference,
                "status": status,
                "member_id": member.MemberID
            })
            st.success("Member information successfully updated!")

def delete_member():
    st.markdown("### 🗑️ Delete Member")

    with st.form("delete_member_form"):
        fname = st.text_input("First Name")
        lname = st.text_input("Last Name")
        email = st.text_input("Email")
        submit = st.form_submit_button("Delete Member")

    if submit:
        if not fname.strip() or not lname.strip() or not email.strip():
            st.warning("Please fill in all fields.")
            return

        with engine.begin() as conn:  # Changed here to engine.begin()
            result = conn.execute(text("""
                SELECT * FROM Members 
                WHERE Member_FName = :fname AND Member_LName = :lname AND Email = :email
            """), {
                "fname": fname.strip(),
                "lname": lname.strip(),
                "email": email.strip()
            })
            member = result.fetchone()

            if not member:
                st.error("No matching member found.")
                return

            try:
                conn.execute(text("""
                    DELETE FROM Members 
                    WHERE Member_FName = :fname AND Member_LName = :lname AND Email = :email
                """), {
                    "fname": fname.strip(),
                    "lname": lname.strip(),
                    "email": email.strip()
                })
                st.success("Member deleted successfully.")
            except Exception as e:
                st.error(f"Error deleting member: {e}")


def delete_book():
    st.markdown("### 🗑️ Delete Book by ISBN")

    with st.form("delete_book_form"):
        isbn = st.text_input("Enter ISBN", placeholder="Required")
        find_clicked = st.form_submit_button("Find Book")

        if find_clicked:
            if not isbn.strip():
                st.warning("Please provide the ISBN to delete a book.")
                return

            try:
                with engine.begin() as conn:
                    # Find book
                    result = conn.execute(text("SELECT * FROM Books WHERE ISBN = :isbn"), {"isbn": isbn.strip()})
                    book = result.fetchone()

                    if not book:
                        st.error("No book found with the provided ISBN.")
                        st.session_state["book_to_delete"] = None
                        return

                    # Check for active loan
                    loan_check = conn.execute(text("""
                        SELECT * FROM Loans WHERE ISBN = :isbn AND Return_date IS NULL
                    """), {"isbn": isbn.strip()}).fetchone()

                    if loan_check:
                        st.warning("❌ Cannot delete the book because it is currently loaned out.")
                        st.session_state["book_to_delete"] = None
                        return

                    # Store book info in session state
                    st.session_state["book_to_delete"] = dict(book._mapping)

            except Exception as e:
                st.error(f"Error finding book: {e}")
                st.session_state["book_to_delete"] = None
                return

    # Outside the form — handles deletion after user confirmed
    if "book_to_delete" in st.session_state and st.session_state["book_to_delete"]:
        book = st.session_state["book_to_delete"]
        st.warning(f"⚠️ Are you sure you want to delete: **'{book['Title']}'** by {book['Author_FName']} {book['Author_LName']}?")

        confirm = st.checkbox("Yes, I want to delete this book.")
        if st.button("🗑️ Confirm Deletion"):
            if confirm:
                try:
                    with engine.begin() as conn:
                        conn.execute(text("DELETE FROM Books WHERE ISBN = :isbn"), {"isbn": book["ISBN"]})
                        st.success(f"✅ Book '{book['Title']}' has been deleted.")
                        st.session_state["book_to_delete"] = None  # Clear state
                except Exception as e:
                    st.error(f"Error deleting book: {e}")
            else:
                st.info("Please check the confirmation box before deletion.")





