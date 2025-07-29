import sqlite3

conn = sqlite3.connect('Lianas_Library_app.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# Members table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Members (
    MemberID INTEGER PRIMARY KEY AUTOINCREMENT,
    Member_FName TEXT NOT NULL,
    Member_LName TEXT NOT NULL,
    Signup_Date TEXT NOT NULL,
    Address TEXT NOT NULL,
    Mobile TEXT NOT NULL,
    Email TEXT NOT NULL UNIQUE,
    Social_Media TEXT NOT NULL,
    Preference TEXT NOT NULL CHECK (Preference IN ('Email', 'Mobile', 'Address', 'Social Media')),
    Member_Status TEXT NOT NULL CHECK (Member_Status IN ('active', 'inactive', 'suspended'))
);
''')

# Books table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Books (
    ISBN TEXT PRIMARY KEY,
    Title TEXT NOT NULL,
    Author_FName TEXT NOT NULL,
    Author_LName TEXT NOT NULL,
    Publisher TEXT NOT NULL,
    Publication_Year INTEGER,
    Genre TEXT NOT NULL
);
''')

# Loans table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Loans (
    LoanID INTEGER PRIMARY KEY AUTOINCREMENT,
    MemberID INTEGER NOT NULL,
    ISBN TEXT NOT NULL,
    Borrow_date TEXT NOT NULL,
    Return_date TEXT DEFAULT NULL,
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (ISBN) REFERENCES Books(ISBN)
);
''')

conn.commit()
conn.close()

print("SQLite database and tables created!")

