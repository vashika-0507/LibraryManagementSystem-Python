# Library Management System
# CM1601 Coursework

import csv
import os

# file names
bookfile = "book.csv"
studentfile = "student.csv"
transactionfile = "transactions.csv"


# load data
def load_books():
    books = []
    if os.path.exists(bookfile):
        with open(bookfile, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:  # skip empty lines
                    books.append(row)
    return books


def load_students():
    students = []
    if os.path.exists(studentfile):
        with open(studentfile, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    students.append(row)
    return students


def load_transactions():
    transactions = []
    if os.path.exists(transactionfile):
        with open(transactionfile, "r") as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    transactions.append(row)
    return transactions


# save data
def save_books(books):
    with open(bookfile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(books)


def save_students(students):
    with open(studentfile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(students)


def save_transactions(transactions):
    with open(transactionfile, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(transactions)


# main menu
def main_menu():
    while True:
        print("   LIBRARY MANAGEMENT SYSTEM")
        print("-" * 40)
        print("1. Add Book")
        print("2. Edit / Update Book")
        print("3. Search Book")
        print("4. View All Books")
        print("5. Add Student")
        print("6. Issue Book")
        print("7. Return Book")
        print("8. View Trend Graph")
        print("9. Exit")

        choice = input("Select option: ").strip()

        if choice == "1":
            add_book()
        elif choice == "2":
            edit_book()
        elif choice == "3":
            search_book()
        elif choice == "4":
            view_books()
        elif choice == "5":
            add_student()
        elif choice == "6":
            issue_book()
        elif choice == "7":
            return_book()
        elif choice == "8":
            trend_graph()
        elif choice == "9":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")


# functions
# validations
def validate_book_id(book_id):
    # Must be exactly 4 characters: 2 letters then 2 digits
    if len(book_id) != 4:
        return False
    if not book_id[:2].isalpha():
        return False
    if not book_id[2:].isdigit():
        return False
    return True

def validate_isbn(isbn):
    # Must be exactly 13 digits
    if len(isbn) != 13 or not isbn.isdigit():
        return False
    # Check digit validation (official ISBN-13 algorithm)
    total = 0
    for i in range(12):
        digit = int(isbn[i])
        if i % 2 == 0:
            total += digit
        else:
            total += digit * 3
    check = (10 - (total % 10)) % 10
    return check == int(isbn[12])

def validate_title(title):
    # Letters and spaces only, max 20 characters
    if len(title) > 20:
        return False
    if not all(c.isalpha() or c.isspace() for c in title):
        return False
    return True

def validate_price(price_str):
    # Must be a valid number with up to 2 decimal places
    try:
        val = float(price_str)
        if val < 0:
            return False
        # Check it has at most 2 decimal places
        parts = price_str.split(".")
        if len(parts) == 2 and len(parts[1]) > 2:
            return False
        return True
    except ValueError:
        return False

# add book
def add_book():
    print("\nAdd Book")
    books = load_books()

    # Book id
    while True:
        book_id = input("Enter Book ID: ").strip().upper()
        if not validate_book_id(book_id):
            print("Invalid Book ID! Must be 2 letters followed by 2 digits.")
            continue
        # Check if ID already exists
        if any(b[0].upper() == book_id for b in books):
            print("This Book ID already exists. Please use a different ID.")
            continue
        break

    # ISBN
    while True:
        isbn = input("Enter ISBN: ").strip()
        if not validate_isbn(isbn):
            print("Invalid ISBN-13! Must be exactly 13 digits with a valid check digit.")
            continue
        break

    # Title
    while True:
        title = input("Enter Title: ").strip()
        if not validate_title(title):
            print("Invalid Title! Letters and spaces only, maximum 20 characters.")
            continue
        break

    # Author
    author = input("Enter Author Name: ").strip()

    # Copies
    while True:
        copies_str = input("Enter number of copies: ").strip()
        if not copies_str.isdigit() or int(copies_str) < 1 or int(copies_str) > 2:
            print("Invalid! Copies must be 1 or 2.")
            continue
        copies = int(copies_str)
        break

    # Price
    while True:
        price_str = input("Enter Price : ").strip()
        if not validate_price(price_str):
            print("Invalid price! Enter a positive number with up to 2 decimal places.")
            continue
        price = float(price_str)
        break

    # Available is automatically set to copies when adding
    available = copies

    # Save the new book
    books.append([book_id, title, isbn, author, copies, available, f"{price:.2f}"])
    save_books(books)

    print(f"\nBook '{title}' added successfully!")

#edit book
def edit_book():
    print("\nEDIT / UPDATE BOOK")
    books = load_books()

    if not books:
        print("No books found in the library.")
        return

    # First show all books so user knows what exists
    view_books()

    # Ask which book to edit
    book_id = input("\nEnter the Book ID you want to edit: ").strip().upper()

    # Find the book
    book_index = None
    for i, b in enumerate(books):
        if b[0].upper() == book_id:
            book_index = i
            break

    if book_index is None:
        print(f"Book ID '{book_id}' not found.")
        return

    book = books[book_index]
    print(f"\nEditing Book: {book[1]} (ID: {book[0]})")
    print("Press ENTER to keep the current value.\n")

    #  Edit ISBN-13
    while True:
        new_isbn = input(f"ISBN-13 (current: {book[2]}): ").strip()
        if new_isbn == "":
            new_isbn = book[2]  # keep old value
            break
        if not validate_isbn(new_isbn):
            print("Invalid ISBN-13! Must be 13 digits with valid check digit.")
            continue
        break

    # Edit Title
    while True:
        new_title = input(f"Title (current: {book[1]}): ").strip()
        if new_title == "":
            new_title = book[1]  # keep old value
            break
        if not validate_title(new_title):
            print("Invalid Title! Letters and spaces only, max 20 characters.")
            continue
        break

    # Edit Author
    new_author = input(f"Author (current: {book[3]}): ").strip()
    if new_author == "":
        new_author = book[3]  # keep old value

    # Edit Copies
    while True:
        new_copies_str = input(f"Copies (current: {book[4]}, max 2): ").strip()
        if new_copies_str == "":
            new_copies = int(book[4])  # keep old value
            break
        if not new_copies_str.isdigit() or int(new_copies_str) < 1 or int(new_copies_str) > 2:
            print("Invalid! Copies must be 1 or 2.")
            continue
        new_copies = int(new_copies_str)
        break

    # Edit Price
    while True:
        new_price_str = input(f"Price (current: {book[6]}): ").strip()
        if new_price_str == "":
            new_price_str = book[6]  # keep old value
            break
        if not validate_price(new_price_str):
            print("Invalid price! Enter a positive number with up to 2 decimal places.")
            continue
        break

    # Recalculate available
    # Available should not go below 0 or above new copies
    currently_issued = int(book[4]) - int(book[5])  # copies - available = how many are out
    new_available = new_copies - currently_issued
    if new_available < 0:
        new_available = 0
    if new_available > new_copies:
        new_available = new_copies

    # Update the book in the list
    books[book_index] = [
        book[0],           # ID stays the same
        new_title,
        new_isbn,
        new_author,
        new_copies,
        new_available,
        f"{float(new_price_str):.2f}"
    ]

    save_books(books)
    print(f"\nBook '{new_title}' updated successfully!")
# View books
def view_books():

    print("\nALL BOOKS")
    books = load_books()
    print(books)

    if not books:
        print("No books found in the library.")
        return

    # Print header
    print(f"{'ID':<6} {'Title':<22} {'ISBN-13':<15} {'Author':<20} {'Copies':<8} {'Available':<10} {'Price':<8}")
    print("-" * 95)

    # Print each book
    for b in books:
        # b[0]=id, b[1]=title, b[2]=isbn, b[3]=author, b[4]=copies, b[5]=available, b[6]=price
        print(f"{b[0]:<6} {b[1]:<22} {b[2]:<15} {b[3]:<20} {b[4]:<8} {b[5]:<10} {b[6]:<8}")

    print("-" * 95)
    print(f"Total books: {len(books)}")


# search
def search_book():
    print("\nSEARCH BOOK")
    print("Search by:")
    print("1. Book ID")
    print("2. Title")
    print("3. Author")

    choice = input("Select option: ").strip()

    books = load_books()

    if not books:
        print("No books found in the library.")
        return

    results = []

    if choice == "1":
        search_term = input("Enter Book ID: ").strip().upper()
        results = [b for b in books if b[0].upper() == search_term]

    elif choice == "2":
        search_term = input("Enter Title : ").strip().lower()
        results = [b for b in books if search_term in b[1].lower()]

    elif choice == "3":
        search_term = input("Enter Author: ").strip().lower()
        results = [b for b in books if search_term in b[3].lower()]

    else:
        print("Invalid option.")
        return

    # Show results
    if not results:
        print("No matching books found.")
        return

    print(f"\n{len(results)} result(s) found:")
    print(f"{'ID':<6} {'Title':<22} {'ISBN-13':<15} {'Author':<20} {'Copies':<8} {'Available':<10} {'Price':<8}")
    print("-" * 95)

    for b in results:
        print(f"{b[0]:<6} {b[1]:<22} {b[2]:<15} {b[3]:<20} {b[4]:<8} {b[5]:<10} {b[6]:<8}")

    print("-" * 95)

#student records
#validate student id
def validate_student_id(student_id):
    # Must be exactly 8 digits
    if len(student_id) != 8:
        return False
    if not student_id.isdigit():
        return False
    return True

#validate student name
def validate_student_name(name):
    # Letters only, max 10 characters
    if len(name) > 10:
        return False
    if not name.isalpha():
        return False
    return True

# ADD STUDENT
def add_student():
    print("\nADD STUDENT")
    students = load_students()
    #Student ID
    while True:
        student_id = input("Enter Student ID : ").strip()
        if not validate_student_id(student_id):
            print("Invalid Student ID! Must be exactly 8 digits.")
            continue
        # Check if ID already exists
        if any(s[0] == student_id for s in students):
            print("This Student ID already exists. Please use a different ID.")
            continue
        break

    # First Name
    while True:
        first_name = input("Enter First Name: ").strip()
        if not validate_student_name(first_name):
            print("Invalid Name! Letters only, maximum 10 characters.")
            continue
        break

    # Save the new student
    students.append([student_id, first_name])
    save_students(students)

    print(f"\nStudent '{first_name}' (ID: {student_id}) added successfully!")


# VIEW ALL STUDENTS
def view_students():
    print("\n ALL STUDENTS ")
    students = load_students()

    if not students:
        print("No students found.")
        return

    print(f"{'Student ID':<12} {'First Name':<12}")
    print("-" * 26)

    for s in students:
        print(f"{s[0]:<12} {s[1]:<12}")

    print("-" * 26)
    print(f"Total students: {len(students)}")


# ---- VALIDATE DATE ----

def validate_date(date_str):
    # Date must follow DD/MM/YYYY pattern
    parts = date_str.split("/")
    if len(parts) != 3:
        return False
    day, month, year = parts

    # Each part must be digits
    if not day.isdigit() or not month.isdigit() or not year.isdigit():
        return False

    # Check lengths
    if len(day) != 2 or len(month) != 2 or len(year) != 4:
        return False

    day = int(day)
    month = int(month)
    year = int(year)

    # Check valid ranges
    if month < 1 or month > 12:
        return False
    if day < 1 or day > 31:
        return False
    if year < 2000 or year > 2100:
        return False

    return True


#ISSUE BOOK
def issue_book():
    print("\nISSUE BOOK")
    books = load_books()
    students = load_students()
    transactions = load_transactions()

    # Show available books and students for reference
    view_books()
    view_students()

    # Book ID
    while True:
        book_id = input("\nEnter Book ID to issue: ").strip().upper()

        # Check book exists
        book_index = None
        for i, b in enumerate(books):
            if b[0].upper() == book_id:
                book_index = i
                break

        if book_index is None:
            print(f"Invalid Book ID! '{book_id}' does not exist.")
            continue
        break

    book = books[book_index]

    # Check availability
    if int(book[5]) <= 0:
        print(f"Sorry! No available copies of '{book[1]}'. All copies are issued.")
        return

    # --- Student ID ---
    while True:
        student_id = input("Enter Student ID: ").strip()

        # Check student exists
        student_exists = any(s[0] == student_id for s in students)
        if not student_exists:
            print(f"Invalid Student ID! '{student_id}' does not exist.")
            continue
        break

    # Check if this student already has this book issued
    # Look in transactions for type 1 (issued) with no matching return (type 2)
    issued_to_student = False
    for t in transactions:
        # t[0]=date, t[1]=book_id, t[2]=student_id, t[3]=type
        if t[1].upper() == book_id and t[2] == student_id and t[3] == "1":
            # Check if this was already returned
            already_returned = any(
                r[1].upper() == book_id and r[2] == student_id and r[3] == "2"
                for r in transactions
            )
            if not already_returned:
                issued_to_student = True
                break

    if issued_to_student:
        print(f"Cannot issue! Student '{student_id}' already has a copy of '{book[1]}'.")
        return

    # --- Date ---
    while True:
        date_str = input("Enter Issue Date (DD/MM/YYYY): ").strip()
        if not validate_date(date_str):
            print("Invalid date! Please use DD/MM/YYYY format e.g. 15/04/2026")
            continue
        break

    # Update book availability (reduce by 1)
    books[book_index][5] = int(book[5]) - 1
    save_books(books)

    # Save transaction (type 1 = issued)
    transactions.append([date_str, book_id, student_id, "1"])
    save_transactions(transactions)

    print(f"\nSuccess! Book '{book[1]}' issued to Student '{student_id}' on {date_str}")
    print(f"Remaining copies available: {books[book_index][5]}")

#RETURN BOOK
def return_book():
    print("\nRETURN BOOK")

    books = load_books()
    students = load_students()
    transactions = load_transactions()

    # Show books and students for reference
    view_books()
    view_students()

    # --- Book ID ---
    while True:
        book_id = input("\nEnter Book ID to return: ").strip().upper()

        # Check book exists
        book_index = None
        for i, b in enumerate(books):
            if b[0].upper() == book_id:
                book_index = i
                break

        if book_index is None:
            print(f"Invalid Book ID! '{book_id}' does not exist.")
            continue
        break

    book = books[book_index]

    # Student ID
    while True:
        student_id = input("Enter Student ID: ").strip()

        # Check student exists
        student_exists = any(s[0] == student_id for s in students)
        if not student_exists:
            print(f"Invalid Student ID! '{student_id}' does not exist.")
            continue
        break

    # Check if book was actually issued to this student
    # Find the most recent transaction for this book + student
    was_issued = False
    was_returned = False

    for t in transactions:
        # t[0]=date, t[1]=book_id, t[2]=student_id, t[3]=type
        if t[1].upper() == book_id and t[2] == student_id:
            if t[3] == "1":
                was_issued = True
            elif t[3] == "2":
                was_returned = True

    # If never issued to this student
    if not was_issued:
        print(f"Error! Book '{book[1]}' was never issued to Student '{student_id}'.")
        return

    # If already returned
    if was_returned and was_issued:
        # Count issues vs returns to check current status
        issue_count = sum(
            1 for t in transactions
            if t[1].upper() == book_id and t[2] == student_id and t[3] == "1"
        )
        return_count = sum(
            1 for t in transactions
            if t[1].upper() == book_id and t[2] == student_id and t[3] == "2"
        )
        if return_count >= issue_count:
            print(f"Error! Book '{book[1]}' has already been returned by Student '{student_id}'.")
            return

    # Date
    while True:
        date_str = input("Enter Return Date (DD/MM/YYYY): ").strip()
        if not validate_date(date_str):
            print("Invalid date! Please use DD/MM/YYYY format e.g. 15/04/2026")
            continue
        break

    # Update book availability (increase by 1)
    # Make sure availability never goes above copies
    new_available = int(book[5]) + 1
    if new_available > int(book[4]):
        new_available = int(book[4])

    books[book_index][5] = new_available
    save_books(books)

    # Save transaction (type 2 = returned)
    transactions.append([date_str, book_id, student_id, "2"])
    save_transactions(transactions)

    print(f"\nSuccess! Book '{book[1]}' returned by Student '{student_id}' on {date_str}")
    print(f"Available copies now: {books[book_index][5]}")

# TREND GRAPH
def trend_graph():
    print("\nTrend graph for books issued")
    try:
        import pandas as pd
        import plotly.express as px
    except ImportError:
        print("Required libraries not installed!")
        print("Please run in terminal:")
        print("  pip install pandas")
        print("  pip install plotly")
        return

    transactions = load_transactions()

    if not transactions:
        print("No transactions found. Issue some books first!")
        return

    # Filter only issued transactions (type 1)
    issued = []
    for t in transactions:
        if t[3] == "1":
            issued.append(t)

    if not issued:
        print("No books have been issued yet.")
        return

    # Count how many books were issued per date
    date_counts = {}
    for t in issued:
        date = t[0]  # date is first column
        if date in date_counts:
            date_counts[date] += 1
        else:
            date_counts[date] = 1

    # Convert to a pandas DataFrame (like a table)
    dates = list(date_counts.keys())
    counts = list(date_counts.values())

    df = pd.DataFrame({
        "Date": dates,
        "Books Issued": counts
    })

    # Sort by date so graph shows in order
    df["Date"] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    df = df.sort_values("Date")

    # Draw the graph using Plotly
    fig = px.line(
        df,
        x="Date",
        y="Books Issued",
        title="Books Issued Per Day",
        markers=True,
        labels={"Date": "Date", "Books Issued": "Number of Books Issued"}
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Books Issued",
        plot_bgcolor="white",
        yaxis=dict(tickmode="linear", dtick=1)
    )

    print("Opening graph in your browser...")
    fig.show()


# start
if __name__ == "__main__":
    main_menu()