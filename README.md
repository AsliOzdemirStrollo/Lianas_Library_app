# 📚 Liana's Library (SQLite Edition)

A **Streamlit web application** to help Liana — and anyone like her — manage books, members, and loans with ease. Built using **Python**, **SQLite**, and **Streamlit**, this app enables non-technical users to keep track of a personal or community book collection.

🔗 [Launch the App](https://asliozdemirstrollo-lianas-library-app-project-example-mfdbf0.streamlit.app/)  

---

## ✨ Features

- **Member Management**
  - Add, update, and delete members
  - View list of active, inactive, and suspended members
- **Book Management**
  - Add new books with full metadata
  - Prevent deletion of books with active loans
- **Loan Management**
  - Record new loans and return dates
  - Prevent multiple loans for the same book if not returned
- **Streamlined UI**
  - Sidebar navigation for actions
  - Form validation and feedback

---

## 🔐 Login Information

To try the app, use:

```plaintext
Username: liana
Password: LianaBooks_2025!
```

---

## 💼 Case Study: Liana’s Library

Liana is a voracious reader whose book collection rivals that of a small library. Her generosity in lending books is admirable—but problematic. Friends often forget to return them, leaving Liana frustrated and at a loss.

Over coffee one rainy afternoon, you propose a solution:  
> “If people are treating you like a library, why not *become* one?”

You promise to handle the tech part—a database, simple interface, and automated tracking. And that’s how this personal library management app was born: to bring order, accountability, and joy back to Liana’s reading life.

---

## 🧰 Tech Stack

| Component    | Technology     |
|--------------|----------------|
| UI           | Streamlit      |
| Backend      | Python         |
| Database     | SQLite         |
| Deployment   | Streamlit Cloud|

---

## 🛠️ Local Setup & Installation

### 1. Clone the repository

```bash
git clone https://github.com/AsliOzdemirStrollo/Lianas_Library_app.git
cd Lianas_Library_app
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # for macOS/Linux
# OR
venv\Scripts\activate     # for Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the initialization script

This will create the database and populate it with 20 members, 20 books, and 3 loan records.

```bash
python init_db.py
```

### 5. Launch the app

```bash
streamlit run project_example.py
```

---

## 📁 Project Structure

```
📁 Lianas_Library_app/
├── project_example.py         # Entry point with login logic
├── library_app.py             # Main app UI & routing
├── init_db.py                 # Script to create & populate database
├── db.py                      # SQLite connection helper
├── My_create.py               # Create functions
├── update_and_delete.py       # Update/Delete logic
├── read.py                    # Read/query logic
├── example_con.py             # SQLite connector
├── Lianas_Library_app.db      # SQLite database (populated)
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

---

## ✅ Status

The app is fully functional and deployed. All data (members, books, and loans) is available on load. It is intended for small-scale, personal, or educational use.

---

## 👤 Author

Made with ❤️ by [Asli Ozdemir Strollo](https://www.linkedin.com/in/asliozdemirstrollo/)  
GitHub: [@AsliOzdemirStrollo](https://github.com/AsliOzdemirStrollo)

