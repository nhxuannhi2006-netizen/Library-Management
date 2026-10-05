books = [
    {
        "id": 1,
        "title": "Harry Potter",
        "author": "J.K. Rowling",
        "available": True
    },
    {
        "id": 2,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "available": True
    },
    {
        "id": 3,
        "title": "1984",
        "author": "George Orwell",
        "available": False
    }
]

def display_books():
    print("\n===== LIBRARY BOOKS =====")
    if not books:
        print("No books in the library.")
        return
    for book in books:
        status = "Available" if book["available"] else "Borrowed"
        print(
            f'ID: {book["id"]} | '
            f'Title: {book["title"]} | '
            f'Author: {book["author"]} | '
            f'Status: {status}'
        )
        
def search_book(title):
    for book in books:
        if book["title"].lower() == title.lower():
            print("\nBook found!")
            print(f'Title: {book["title"]}')
            print(f'Author: {book["author"]}')
            print(
                "Status:",
                "Available" if book["available"] else "Borrowed"
            )
            return
    print("\nBook not found.")
    
def borrow_book(book_id):
    for book in books:
        if book["id"] == book_id:
            if book["available"]:
                book["available"] = False
                print("\nBook borrowed successfully!")
            else:
                print("\nThis book is already borrowed.")
            return
    print("\nBook ID not found.")
    
def return_book(book_id):
    for book in books:
        if book["id"] == book_id:
            if not book["available"]:
                book["available"] = True
                print("\nBook returned successfully!")
            else:
                print("\nThis book was not borrowed.")
            return 
    print("\nBook ID not found.")

def add_book(title, author):
    if books:
        new_id = max(book["id"] for book in books) + 1
    else:
        new_id = 1

    new_book = {
        "id": new_id,
        "title": title,
        "author": author,
        "available": True
    }
    books.append(new_book)
    print("\nBook added successfully!")
    print(f"New Book ID: {new_id}")

def remove_book(book_id):
    for book in books:
        if book["id"] == book_id:
            books.remove(book)
            print("\nBook deleted successfully!")
            return
    print("\nBook ID not found.")

while True:
    print("\n===== LIBRARY MANAGEMENT SYSTEM =====")
    print("1. Display Books")
    print("2. Search Book")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Add Book")
    print("6. Remove Book")
    print("7. Exit")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        display_books()
        
    elif choice == "2":
        title = input("Enter book title: ")
        search_book(title)
        
    elif choice == "3":
        try:
            book_id = int(input("Enter book ID: "))
            borrow_book(book_id)
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
        print("Goodbye!")
        break 
    else:
        print("Invalid choice. Please try again.")