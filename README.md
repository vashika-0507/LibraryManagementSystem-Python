# Library Management System: Python

A console application for managing a small library: books, students, and issuing and returning loans. Data is stored in CSV files, and a trend graph shows how many books were issued over time. The CSV files can be imported into the [Java reporting module](https://github.com/vashika-0507/LibraryManagementSystem-Java).

## Features

- Add, edit, search (by ID, title or author) and view books
- Register students
- Issue and return books, with the number of available copies updated automatically
- Trend graph of books issued over time, opened in the browser
- All data saved to CSV files, so it persists between runs

## Business rules

- A book cannot be issued when no copies are available
- A student cannot borrow a second copy of a book they already have
- A book cannot be returned if it was never issued to that student or was already returned
- Book and student IDs must exist before a loan is recorded

## Validation

| Field | Rule |
|---|---|
| Book ID | 2 letters followed by 2 digits (e.g. `AB12`) |
| ISBN | 13 digits with a valid ISBN-13 check digit |
| Title | letters and spaces only, up to 20 characters |
| Price | a number with exactly 2 decimal places |
| Copies | maximum 2 per book |
| Student ID | 8 digits |
| Date | DD/MM/YYYY |

## Data files

| File | Columns |
|---|---|
| `book.csv` | book ID, title, ISBN, author, copies, available, price |
| `student.csv` | student ID, first name |
| `transactions.csv` | date, book ID, student ID, type (`1` = issued, `2` = returned) |

Sample data is included so the program works straight away.

## Technologies

Python 3, `csv` module, pandas, Plotly

## How to run

```bash
pip install pandas plotly
python library.py
```

Choose an option from the menu (1 to 9). Option 8 opens the trend graph.

## Possible improvements

- Split the code into separate modules (books, students, loans)
- Store data in a database such as SQLite instead of CSV files
- Add due dates and late-return fines

## Author

**Vashika Maheswaran**, BSc (Hons) Artificial Intelligence with Data Science, Robert Gordon University (delivered by IIT, Colombo)
[GitHub](https://github.com/vashika-0507) · [LinkedIn](https://www.linkedin.com/in/vashika-maheswaran-71a17738b)
