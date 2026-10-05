import sqlite3

connection = sqlite3.connect("library.db")
connection.execute("PRAGMA foreign_keys = ON")
cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    available INTEGER NOT NULL
)
""")
connection.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
)
""") 
connection.commit()

cursor.execute("""
CREATE TABLE IF NOT EXISTS borrow_records (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    book_id INTEGER NOT NULL, 
    borrow_date TEXT NOT NULL,
    return_date TEXT, 
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (book_id) REFERENCES books(id)
)
""")
connection.commit()

cursor.execute("SELECT COUNT(*) FROM books")
book_count = cursor.fetchone()[0]

if book_count == 0:
    cursor.execute("""
    INSERT INTO books (id, title, author, available)
    VALUES (?, ?, ?, ?)
    """, (1, "Harry Potter", "J.K. Rowling", 1))

    cursor.execute("""
    INSERT INTO books (id, title, author, available)
    VALUES (?, ?, ?, ?)
    """, (2, "The Great Gatsby", "F. Scott Fitzgerald", 1))

    cursor.execute("""
    INSERT INTO books (id, title, author, available)
    VALUES (?, ?, ?, ?)
    """, (3, "1984", "George Orwell", 0))

    connection.commit()
    
cursor.execute("SELECT COUNT(*) FROM users")
user_count = cursor.fetchone()[0]

if user_count == 0:
    cursor.execute("""
    INSERT INTO users (name)
    VALUES (?)
    """, ("Nhi Nguyen",))

    cursor.execute("""
    INSERT INTO users (name)
    VALUES (?)
    """, ("Alice Smith",))

    cursor.execute("""
    INSERT INTO users (name)
    VALUES (?)
    """, ("John Doe",))

    connection.commit()
    
def display_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    
    print("\n===== LIBRARY BOOKS =====")
    
    if not books:
        print("No books in the library.")
        return
    
    for book in books:
        status = "Available" if book[3] else "Borrowed"
        print(
            f"ID: {book[0]} | "
            f"Title: {book[1]} | "
            f"Author: {book[2]} | "
            f"Status: {status}"
        )
def display_users():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("\n===== LIBRARY USERS =====")
    if not users:
        print("No users found.")
        return 
    for user in users:
        print(
            f"ID: {user[0]} | "
            f"Name: {user[1]} | "
        )
def search_book(title):
    cursor.execute("""
    SELECT * FROM books
    WHERE title LIKE ?
    """, (f"%{title}%",))
    
    books = cursor.fetchall()
    
    if books: 
        print("\n===== SEARCH RESULTS =====")
        
        for book in books: 
            status = "Available" if book[3] else "Borrowed"
            print(
                f"ID: {book[0]} | "
                f"Title: {book[1]} | "
                f"Author: {book[2]} | "
                f"Status: {status}"
            )
    else:
        print("\nBook not found.")

def borrow_book(user_id, book_id):
    cursor.execute("""
    SELECT id 
    FROM users
    WHERE id = ?
    """, (user_id,))
    user = cursor.fetchone()
    if not user:
        print("\nUser ID not found.")
        return 
    
    cursor.execute("""
    UPDATE books
    SET available = 0
    WHERE id = ? AND available = 1
    """, (book_id,))
    
    if cursor.rowcount == 0:
        print("\nBook not found or already borrowed.")
        return 
    
    cursor.execute("""
    INSERT INTO borrow_records
    (user_id, book_id, borrow_date)
    VALUES (?, ?, DATE('now'))
    """, (user_id, book_id))
    
    connection.commit()
    
    print("\nBook borrowed successfully!")

def return_book(book_id):
    cursor.execute("""
    UPDATE books
    SET available = 1
    WHERE id = ? AND available = 0
    """, (book_id,))
    
    if cursor.rowcount == 0:
        print("\nBook not found or already available.")
        return 
    
    cursor.execute("""
    UPDATE borrow_records 
    SET return_date = DATE('now')
    WHERE book_id = ?
    AND return_date IS NULL
    """, (book_id,))
    connection.commit()
    print("\nBook returned successfully")
        
def add_book(title, author):
    cursor.execute("""
    INSERT INTO books (title, author, available)
    VALUES (?, ?, 1)
    """, (title, author))
    connection.commit()
    print("\nBook added successfully!")
    print(f"New Book ID: {cursor.lastrowid}")
    
def remove_book(book_id):
    cursor.execute("""
    SELECT id 
    FROM books
    WHERE id = ?
    """, (book_id,))
    book = cursor.fetchone()
    if not book: 
        print("\nBook ID not found.")
        return 
    
    cursor.execute("""
    SELECT id 
    FROM borrow_records 
    WHERE book_id = ? 
    """, (book_id,))
    
    record = cursor.fetchone()
    
    if record:
        print("\nThis book has borrowing records and cannot be deleted.")
        return 
    
    cursor.execute("""
    DELETE FROM books 
    WHERE id = ? 
    """, (book_id,))
    connection.commit()
    print("\nBook deleted successfully!")
    
def add_user(name):
    cursor.execute("""
    INSERT INTO users (name)
    VALUES (?)
    """, (name,))
    connection.commit()
    print("\nUser added successfully!")
    print(f"New User ID: {cursor.lastrowid}")
    
def display_borrow_records():
    cursor.execute("""
    SELECT
        borrow_records.id,
        users.name,
        books.title,
        borrow_records.borrow_date,
        borrow_records.return_date
    FROM borrow_records 
    JOIN users 
        ON borrow_records.user_id = users.id 
    JOIN books 
        ON borrow_records.book_id = books.id
    """)
    records = cursor.fetchall()
    print("\n===== BORROW RECORDS =====")
    
    if not records: 
        print("No borrowing records found.")
        return 
    for record in records:
        return_date = record[4] if record[4] else "Not returned"
        print(
            f"Record ID: {record[0]} | "
            f"User: {record[1]} | "
            f"Book: {record[2]} | "
            f"Borrowed: {record[3]} | "
            f"Returned: {return_date}"
        )
        
while True:
    print("\n ===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Display Books")
    print("2. Search Book")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Add Book")
    print("6. Delete Book")
    print("7. Display Users")
    print("8. Add User")
    print("9. Display Borrow Records")
    print("10. Exit")
    
    choice = input("Enter your choice: ")
    if choice == "1":
        display_books()
        
    elif choice == "2":
        title = input("Enter book title: ")
        search_book(title)
        
    elif choice == "3":
        try: 
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
            borrow_book(user_id, book_id)
            
        except ValueError:
            print("\nPlease enter a valid number.")
            
    elif choice == "4":
        try: 
            book_id = int(input("Enter book ID: "))
            return_book(book_id)
            
        except ValueError:
            print("\nPlease enter a valid number.") 
            
    elif choice == "5":
        title = input("Enter book title: ")
        author = input("Enter author: ")
        add_book(title, author)
    
    elif choice == "6":
        try:
            book_id = int(input("Enter book ID: "))
            remove_book(book_id)
            
        except ValueError:
            print("\nPlease enter a valid number.")
            
    elif choice == "7":
        display_users()
    
    elif choice == "8":
        name = input("Enter user name: ")
        add_user(name)
        
    elif choice == "9":
        display_borrow_records()
        
    elif choice == "10":
        print("\nGoodbye!")
        break 
    
    else:
        print("\nInvalid choice.Please try again.")
    
connection.close()