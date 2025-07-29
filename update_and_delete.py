import streamlit as st
from db import get_connection  # or from example_con import get_connection
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

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT MemberID FROM Members 
                WHERE Member_FName = ? AND Member_LName = ? AND Email = ?
            """, (fname.strip(), lname.strip(), email.strip()))
            member = cursor.fetchone()

            if not member:
                st.error("Member does not exist. Please add the member first.")
                cursor.close()
                conn.close()
                return

            if preference == "Social Media" and not social_media.strip():
                st.warning("Social Media must be provided if selected as Preferred Contact Method.")
                cursor.close()
                conn.close()
                return

            cursor.execute("""
                UPDATE Members SET
                    Member_FName = ?,
                    Member_LName = ?,
                    Email = ?,
                    Mobile = ?,
                    Address = ?,
                    Social_Media = ?,
                    Preference = ?,
                    Member_Status = ?
                WHERE MemberID = ?
            """, (
                fname.strip(),
                lname.strip(),
                email.strip(),
                mobile.strip(),
                address.strip(),
                social_media.strip() if social_media.strip() else "N/A",
                preference,
                status,
                member[0]
            ))

            conn.commit()
            cursor.close()
            conn.close()
            st.success("Member information successfully updated!")

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

        try:
            conn = get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM Members 
                WHERE Member_FName = ? AND Member_LName = ? AND Email = ?
            """, (fname.strip(), lname.strip(), email.strip()))
            member = cursor.fetchone()

            if not member:
                st.error("No matching member found.")
                cursor.close()
                conn.close()
                return

            cursor.execute("""
                DELETE FROM Members 
                WHERE Member_FName = ? AND Member_LName = ? AND Email = ?
            """, (fname.strip(), lname.strip(), email.strip()))

            conn.commit()
            cursor.close()
            conn.close()
            st.success("Member deleted successfully.")

        except Exception as e:
            st.error(f"Error deleting member: {e}")
            try:
                cursor.close()
            except:
                pass
            try:
                conn.close()
            except:
                pass


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
                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("SELECT * FROM Books WHERE ISBN = ?", (isbn.strip(),))
                book = cursor.fetchone()

                if not book:
                    st.error("No book found with the provided ISBN.")
                    st.session_state["book_to_delete"] = None
                    cursor.close()
                    conn.close()
                    return

                cursor.execute("""
                    SELECT * FROM Loans WHERE ISBN = ? AND Return_date IS NULL
                """, (isbn.strip(),))
                loan_check = cursor.fetchone()

                if loan_check:
                    st.warning("❌ Cannot delete the book because it is currently loaned out.")
                    st.session_state["book_to_delete"] = None
                    cursor.close()
                    conn.close()
                    return

                # Store book info in session state (convert tuple to dict for easy access)
                columns = [col[0] for col in cursor.description]
                book_dict = dict(zip(columns, book))
                st.session_state["book_to_delete"] = book_dict

                cursor.close()
                conn.close()

            except Exception as e:
                st.error(f"Error finding book: {e}")
                st.session_state["book_to_delete"] = None
                try:
                    cursor.close()
                except:
                    pass
                try:
                    conn.close()
                except:
                    pass
                return

    # Outside the form — handles deletion after user confirmed
    if "book_to_delete" in st.session_state and st.session_state["book_to_delete"]:
        book = st.session_state["book_to_delete"]
        st.warning(f"⚠️ Are you sure you want to delete: **'{book['Title']}'** by {book['Author_FName']} {book['Author_LName']}?")

        confirm = st.checkbox("Yes, I want to delete this book.")
        if st.button("🗑️ Confirm Deletion"):
            if confirm:
                try:
                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute("DELETE FROM Books WHERE ISBN = ?", (book["ISBN"],))
                    conn.commit()

                    st.success(f"✅ Book '{book['Title']}' has been deleted.")
                    st.session_state["book_to_delete"] = None

                    cursor.close()
                    conn.close()

                except Exception as e:
                    st.error(f"Error deleting book: {e}")
                    try:
                        cursor.close()
                    except:
                        pass
                    try:
                        conn.close()
                    except:
                        pass
            else:
                st.info("Please check the confirmation box before deletion.")
