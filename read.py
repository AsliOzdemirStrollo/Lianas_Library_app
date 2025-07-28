import pandas as pd
from sqlalchemy import text
from example_con import engine


def return_df(query):
    with engine.connect() as connection:
        response = connection.execute(text(query))
    
    response_df = pd.DataFrame(response.tuples())
    return response_df

def read_books():
    query = """
        SELECT * 
        FROM books;
    """
    books_df = return_df(query)
    return books_df

# st.dataframe(read_books())

def read_members():
    query = """
        SELECT * 
        FROM members;
    """
    members_df = return_df(query)
    return members_df

# st.dataframe(read_members())

def read_loans():
    query = """
        SELECT * 
        FROM loans;
    """
    loans_df = return_df(query)
    
    # Now join in Python with read_books() and read_members() to get Title and Member names
    
    # Read books and members dataframes
    books_df = read_books()
    members_df = read_members()

    # Merge loans with books on ISBN to get Title
    merged_df = loans_df.merge(books_df[['ISBN', 'Title']], on='ISBN', how='left')

    # Merge with members on MemberID to get first and last names
    merged_df = merged_df.merge(
        members_df[['MemberID', 'Member_FName', 'Member_LName']], 
        on='MemberID', how='left'
    )

    # Select columns and order by Borrow_date ascending
    result_df = merged_df[['Title', 'Member_FName', 'Member_LName', 'Borrow_date', 'Return_date']]

    # Sort by Borrow_date
    result_df = result_df.sort_values(by='Borrow_date', ascending=True).reset_index(drop=True)

    return result_df



# st.dataframe(read_loans())

def read_available_books_from_loans():
    # Step 1: Read all books and loans
    books_df = read_books()
    loans_df = read_loans_raw()  # raw loans with no joins
    
    # Step 2: Filter out books that are currently loaned (Return_date is NULL)
    active_loans = loans_df[loans_df['Return_date'].isnull()]
    loaned_isbns = active_loans['ISBN'].unique()

    # Step 3: Keep only books not currently loaned
    available_books_df = books_df[~books_df['ISBN'].isin(loaned_isbns)].reset_index(drop=True)
    
    return available_books_df
def read_loans_raw():
    query = "SELECT * FROM loans;"
    return return_df(query)



#read active loans

def read_active_loans():
    query = """
        SELECT l.LoanID, m.Member_FName, m.Member_LName, b.Title, l.Borrow_date
        FROM loans l
        JOIN members m ON l.MemberID = m.MemberID
        JOIN books b ON l.ISBN = b.ISBN
        WHERE l.Return_date IS NULL
        ORDER BY l.Borrow_date
    """
    return return_df(query)


#Track a Book by Title

def get_book_loan_status_by_title(title):
    with engine.connect() as connection:
        # First, check if book exists
        book_query = text("""
            SELECT * FROM Books WHERE LOWER(Title) = LOWER(:title)
        """)
        book_result = connection.execute(book_query, {"title": title}).fetchone()

        if not book_result:
            return {"status": "not_found"}

        isbn = book_result[0]  # ISBN is first column
        book_data = dict(zip(book_result.keys(), book_result))

        # Check if book is currently loaned
        loan_query = text("""
            SELECT l.Borrow_date, m.Member_FName, m.Member_LName
            FROM Loans l
            JOIN Members m ON l.MemberID = m.MemberID
            WHERE l.ISBN = :isbn AND l.Return_date IS NULL
            ORDER BY l.Borrow_date DESC LIMIT 1;
        """)
        loan_result = connection.execute(loan_query, {"isbn": isbn}).fetchone()

        if loan_result:
            return {
                "status": "loaned",
                "book": book_data,
                "borrow_date": loan_result["Borrow_date"],
                "borrowed_by": f"{loan_result['Member_FName']} {loan_result['Member_LName']}"
            }
        else:
            return {
                "status": "available",
                "book": book_data
            }
            
# Member search

def get_member_by_name(first_name, last_name):
    query = text("""
        SELECT * FROM Members 
        WHERE LOWER(Member_FName) = LOWER(:first_name) 
          AND LOWER(Member_LName) = LOWER(:last_name)
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"first_name": first_name, "last_name": last_name}).fetchone()
        return dict(result._mapping) if result else None  # <-- fixed here



def get_member_loans_by_id(member_id):
    query = text("""
        SELECT b.Title, l.Borrow_date, l.Return_date
        FROM Loans l
        JOIN Books b ON l.ISBN = b.ISBN
        WHERE l.MemberID = :member_id
        ORDER BY l.Borrow_date
    """)
    with engine.connect() as conn:
        result = conn.execute(query, {"member_id": member_id})
        rows = result.fetchall()
        df = pd.DataFrame([dict(row._mapping) for row in rows])  # 💡 proper conversion
        return df







