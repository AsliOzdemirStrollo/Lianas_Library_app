import pandas as pd
from db import get_connection  # use your sqlite connection function

def return_df(query, params=None):
    with get_connection() as conn:
        cur = conn.cursor()
        if params:
            cur.execute(query, params)
        else:
            cur.execute(query)
        # fetch all rows and columns names for DataFrame
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
    return pd.DataFrame(rows, columns=columns)

def read_books():
    query = "SELECT * FROM books;"
    return return_df(query)

def read_members():
    query = "SELECT * FROM members;"
    return return_df(query)

def read_loans_raw():
    query = "SELECT * FROM loans;"
    return return_df(query)

def read_loans():
    loans_df = read_loans_raw()
    books_df = read_books()
    members_df = read_members()

    # Merge loans with books on ISBN to get Title
    merged_df = loans_df.merge(books_df[['ISBN', 'Title']], on='ISBN', how='left')

    # Merge with members on MemberID to get first and last names
    merged_df = merged_df.merge(
        members_df[['MemberID', 'Member_FName', 'Member_LName']],
        on='MemberID', how='left'
    )

    result_df = merged_df[['Title', 'Member_FName', 'Member_LName', 'Borrow_date', 'Return_date']]
    result_df = result_df.sort_values(by='Borrow_date', ascending=True).reset_index(drop=True)

    return result_df

def read_available_books_from_loans():
    books_df = read_books()
    loans_df = read_loans_raw()

    active_loans = loans_df[loans_df['Return_date'].isnull()]
    loaned_isbns = active_loans['ISBN'].unique()

    available_books_df = books_df[~books_df['ISBN'].isin(loaned_isbns)].reset_index(drop=True)
    return available_books_df

def read_active_loans():
    query = """
        SELECT l.LoanID, m.Member_FName, m.Member_LName, b.Title, l.Borrow_date
        FROM loans l
        JOIN members m ON l.MemberID = m.MemberID
        JOIN books b ON l.ISBN = b.ISBN
        WHERE l.Return_date IS NULL
        ORDER BY l.Borrow_date;
    """
    return return_df(query)

def get_book_loan_status_by_title(title):
    with get_connection() as conn:
        cur = conn.cursor()
        # Check if book exists (case-insensitive)
        cur.execute("SELECT * FROM books WHERE LOWER(Title) = LOWER(?)", (title,))
        book_result = cur.fetchone()

        if not book_result:
            return {"status": "not_found"}

        columns = [desc[0] for desc in cur.description]
        book_data = dict(zip(columns, book_result))
        isbn = book_data['ISBN']

        # Check if book is currently loaned
        cur.execute("""
            SELECT l.Borrow_date, m.Member_FName, m.Member_LName
            FROM loans l
            JOIN members m ON l.MemberID = m.MemberID
            WHERE l.ISBN = ? AND l.Return_date IS NULL
            ORDER BY l.Borrow_date DESC LIMIT 1
        """, (isbn,))
        loan_result = cur.fetchone()

        if loan_result:
            return {
                "status": "loaned",
                "book": book_data,
                "borrow_date": loan_result[0],
                "borrowed_by": f"{loan_result[1]} {loan_result[2]}"
            }
        else:
            return {
                "status": "available",
                "book": book_data
            }

def get_member_by_name(first_name, last_name):
    query = """
        SELECT * FROM members 
        WHERE LOWER(Member_FName) = LOWER(?) 
          AND LOWER(Member_LName) = LOWER(?);
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, (first_name, last_name))
        result = cur.fetchone()
        if result:
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, result))
        else:
            return None

def get_member_loans_by_id(member_id):
    query = """
        SELECT b.Title, l.Borrow_date, l.Return_date
        FROM loans l
        JOIN books b ON l.ISBN = b.ISBN
        WHERE l.MemberID = ?
        ORDER BY l.Borrow_date;
    """
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, (member_id,))
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        return pd.DataFrame(rows, columns=columns)
