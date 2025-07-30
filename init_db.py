import sqlite3

conn = sqlite3.connect('Lianas_Library_app.db')
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

# ===== DROP OLD TABLES =====
cursor.execute("DROP TABLE IF EXISTS Loans;")
cursor.execute("DROP TABLE IF EXISTS Books;")
cursor.execute("DROP TABLE IF EXISTS Members;")

# ===== CREATE TABLES =====
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

# ===== INSERT MEMBERS (First 20) =====
members = [
    ("John", "Smith", "2023-01-15", "123 Maple St, Springfield", "555-1234", "john.smith@example.com", "@johnsmith", "Email", "active"),
    ("Emily", "Johnson", "2023-02-20", "456 Oak St, Shelbyville", "555-2345", "emily.johnson@example.com", "@emilyjohnson", "Mobile", "active"),
    ("Michael", "Brown", "2023-03-05", "789 Pine St, Capital City", "555-3456", "michael.brown@example.com", "@michaelbrown", "Address", "inactive"),
    ("Sarah", "Williams", "2023-04-10", "101 Elm St, Ogdenville", "555-4567", "sarah.williams@example.com", "@sarahwilliams", "Social Media", "active"),
    ("David", "Jones", "2023-05-12", "202 Birch St, North Haverbrook", "555-5678", "david.jones@example.com", "@davidjones", "Email", "suspended"),
    ("Laura", "Miller", "2023-06-18", "303 Cedar St, Springfield", "555-6789", "laura.miller@example.com", "@lauramiller", "Mobile", "active"),
    ("Robert", "Davis", "2023-07-21", "404 Walnut St, Shelbyville", "555-7890", "robert.davis@example.com", "@robertdavis", "Address", "active"),
    ("Jessica", "Garcia", "2023-08-14", "505 Chestnut St, Capital City", "555-8901", "jessica.garcia@example.com", "@jessicagarcia", "Social Media", "inactive"),
    ("James", "Rodriguez", "2023-09-09", "606 Ash St, Ogdenville", "555-9012", "james.rodriguez@example.com", "@jamesrodriguez", "Email", "active"),
    ("Anna", "Wilson", "2023-10-02", "707 Hickory St, North Haverbrook", "555-0123", "anna.wilson@example.com", "@annawilson", "Mobile", "suspended"),
    ("William", "Martinez", "2023-01-25", "808 Poplar St, Springfield", "555-1111", "william.martinez@example.com", "@williammartinez", "Address", "active"),
    ("Olivia", "Anderson", "2023-02-28", "909 Fir St, Shelbyville", "555-2222", "olivia.anderson@example.com", "@oliviaanderson", "Social Media", "active"),
    ("Joseph", "Taylor", "2023-03-15", "111 Spruce St, Capital City", "555-3333", "joseph.taylor@example.com", "@josephtaylor", "Email", "inactive"),
    ("Emma", "Thomas", "2023-04-22", "222 Cypress St, Ogdenville", "555-4444", "emma.thomas@example.com", "@emmathomas", "Mobile", "active"),
    ("Charles", "Hernandez", "2023-05-30", "333 Redwood St, North Haverbrook", "555-5555", "charles.hernandez@example.com", "@charleshernandez", "Address", "suspended"),
    ("Sophia", "Moore", "2023-06-25", "444 Beech St, Springfield", "555-6666", "sophia.moore@example.com", "@sophiamoore", "Social Media", "active"),
    ("Thomas", "Martin", "2023-07-13", "555 Magnolia St, Shelbyville", "555-7777", "thomas.martin@example.com", "@thomasmartin", "Email", "active"),
    ("Isabella", "Jackson", "2023-08-17", "666 Dogwood St, Capital City", "555-8888", "isabella.jackson@example.com", "@isabellajackson", "Mobile", "inactive"),
    ("Daniel", "Thompson", "2023-09-20", "777 Sycamore St, Ogdenville", "555-9999", "daniel.thompson@example.com", "@danielthompson", "Address", "active"),
    ("Mia", "White", "2023-10-05", "888 Willow St, North Haverbrook", "555-0000", "mia.white@example.com", "@miawhite", "Social Media", "suspended")
]

cursor.executemany('''
INSERT INTO Members (Member_FName, Member_LName, Signup_Date, Address, Mobile, Email, Social_Media, Preference, Member_Status)
VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
''', members)

# ===== INSERT BOOKS (First 20) =====
books = [
    ("9780141439600", "Pride and Prejudice", "Jane", "Austen", "Penguin", 2002, "Romance"),
    ("9780140449266", "The Aeneid", "Virgil", "Virgil", "Penguin", 2003, "Epic"),
    ("9780385472579", "The Things They Carried", "Tim", "O'Brien", "Mariner", 2009, "War"),
    ("9780553212419", "Dracula", "Bram", "Stoker", "Bantam", 1986, "Horror"),
    ("9780451524935", "1984", "George", "Orwell", "Signet Classic", 1990, "Dystopian"),
    ("9780743273565", "The Great Gatsby", "F. Scott", "Fitzgerald", "Scribner", 2004, "Classic"),
    ("9780486415864", "Meditations", "Marcus", "Aurelius", "Dover", 2002, "Philosophy"),
    ("9780679783268", "Crime and Punishment", "Fyodor", "Dostoevsky", "Vintage", 1993, "Classic"),
    ("9780060850524", "Brave New World", "Aldous", "Huxley", "Harper Perennial", 2006, "Sci-Fi"),
    ("9780141182575", "The Trial", "Franz", "Kafka", "Penguin", 2000, "Classic"),
    ("9780307474278", "The Road", "Cormac", "McCarthy", "Vintage", 2007, "Post-Apocalyptic"),
    ("9780812981605", "Unbroken", "Laura", "Hillenbrand", "Random House", 2010, "Biography"),
    ("9780679734529", "Slaughterhouse-Five", "Kurt", "Vonnegut", "Dell", 1991, "Satire"),
    ("9780143039433", "The Kite Runner", "Khaled", "Hosseini", "Riverhead", 2004, "Fiction"),
    ("9781400079988", "A Thousand Splendid Suns", "Khaled", "Hosseini", "Riverhead", 2008, "Fiction"),
    ("9780316769532", "Franny and Zooey", "J.D.", "Salinger", "Back Bay", 2001, "Fiction"),
    ("9780743482745", "Hamlet", "William", "Shakespeare", "Folger", 2003, "Tragedy"),
    ("9780061122415", "The Alchemist", "Paulo", "Coelho", "HarperOne", 1998, "Fiction"),
    ("9780375703768", "Beloved", "Toni", "Morrison", "Vintage", 2004, "Historical"),
    ("9780140177398", "Of Mice and Men", "John", "Steinbeck", "Penguin", 1993, "Fiction")
]

cursor.executemany('''
INSERT INTO Books (ISBN, Title, Author_FName, Author_LName, Publisher, Publication_Year, Genre)
VALUES (?, ?, ?, ?, ?, ?, ?);
''', books)

# ===== INSERT 3 LOANS =====
loans = [
    (1, "9780141439600", "2025-07-15", None),
    (2, "9780385472579", "2025-07-20", "2025-07-28"),
    (3, "9780743273565", "2025-07-25", None)
]

cursor.executemany('''
INSERT INTO Loans (MemberID, ISBN, Borrow_date, Return_date)
VALUES (?, ?, ?, ?);
''', loans)

# ===== SAVE AND CLOSE =====
conn.commit()
conn.close()

print("Database initialized with real members, books, and loans.")
