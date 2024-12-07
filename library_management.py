import mysql.connector
from datetime import datetime, timedelta


conn = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="Nanapu@123",  
    database="library_db"
)
cursor = conn.cursor()


def issue_book():
    member_id = int(input("Enter Member ID: "))
    book_id = int(input("Enter Book ID: "))
    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=14)
    

    cursor.execute("SELECT available FROM books WHERE book_id = %s", (book_id,))
    book = cursor.fetchone()
    if not book or not book[0]:
        print("Book not available.")
        return

    
    cursor.execute("INSERT INTO transactions (member_id, book_id, issue_date, due_date) VALUES (%s, %s, %s, %s)",
                   (member_id, book_id, issue_date, due_date))
    cursor.execute("UPDATE books SET available = FALSE WHERE book_id = %s", (book_id,))
    conn.commit()
    print("Book issued successfully!")

def return_book():
    transaction_id = int(input("Enter Transaction ID: "))
    return_date = datetime.now()
    
    cursor.execute("SELECT book_id FROM transactions WHERE transaction_id = %s", (transaction_id,))
    book_id = cursor.fetchone()
    if not book_id:
        print("Transaction not found.")
        return
    book_id = book_id[0]

    cursor.execute("UPDATE transactions SET return_date = %s WHERE transaction_id = %s",
                   (return_date, transaction_id))
    cursor.execute("UPDATE books SET available = TRUE WHERE book_id = %s", (book_id,))
    conn.commit()
    print("Book returned successfully!")

def list_books():
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("\nBooks in Library:")
    for book in books:
        status = "Available" if book[3] else "Issued"
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {status}")

def main():
    while True:
        print("\n--- Library Management System ---")
        print("1. Issue Book")
        print("2. Return Book")
        print("3. List Books")
        print("4. Exit")
        choice = int(input("Enter your choice: "))
        if choice == 1:
            issue_book()
        elif choice == 2:
            return_book()
        elif choice == 3:
            list_books()
        elif choice == 4:
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
