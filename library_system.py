import mysql.connector
import pandas as pd

def ensure_database_exists(cursor, db_name):
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

def drop_database(cursor, db_name):
    cursor.execute(f"DROP DATABASE IF EXISTS {db_name}")

def create_tables(conn):
    cursor = conn.cursor()
    # Only create tables if they don't already exist
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")

    create_tables_sql = """
    CREATE TABLE IF NOT EXISTS BOOK (
        Isbn CHAR(10) NOT NULL,
        Title VARCHAR(100) NOT NULL,
        CONSTRAINT pk_book PRIMARY KEY (Isbn)
    );

    CREATE TABLE IF NOT EXISTS AUTHORS (
        Author_id INT NOT NULL,
        Name VARCHAR(25) NOT NULL,
        CONSTRAINT pk_authors PRIMARY KEY (Author_id)
    );

    CREATE TABLE IF NOT EXISTS BOOK_AUTHORS (
        Isbn CHAR(10) NOT NULL,
        Author_id INT NOT NULL,
        CONSTRAINT pk_book_authors PRIMARY KEY (Isbn, Author_id),
        CONSTRAINT fk_ba_book FOREIGN KEY (Isbn) REFERENCES BOOK(Isbn),
        CONSTRAINT fk_ba_author FOREIGN KEY (Author_id) REFERENCES AUTHORS(Author_id)
    );

    CREATE TABLE IF NOT EXISTS BORROWER (
        Card_id CHAR(8) NOT NULL,
        Ssn CHAR(9) NOT NULL UNIQUE,
        BName VARCHAR(50) NOT NULL,
        Address VARCHAR(100) NOT NULL,
        Phone VARCHAR(15),
        CONSTRAINT pk_borrower PRIMARY KEY (Card_id)
    );

    CREATE TABLE IF NOT EXISTS BOOK_LOANS (
        Loan_id INT AUTO_INCREMENT PRIMARY KEY,
        Isbn CHAR(10),
        Card_id CHAR(8),
        Date_out DATE,
        Due_date DATE,
        Date_in DATE,
        CONSTRAINT fk_loans_book FOREIGN KEY (Isbn) REFERENCES BOOK(Isbn),
        CONSTRAINT fk_loans_borrower FOREIGN KEY (Card_id) REFERENCES BORROWER(Card_id)
    );

    CREATE TABLE IF NOT EXISTS FINES (
        Loan_id INT,
        Fine_amt DECIMAL(5,2),
        Paid BOOLEAN DEFAULT FALSE,
        CONSTRAINT pk_fines PRIMARY KEY (Loan_id),
        CONSTRAINT fk_fines_loans FOREIGN KEY (Loan_id) REFERENCES BOOK_LOANS(Loan_id)
    );
    """

    for statement in create_tables_sql.strip().split(';'):
        if statement.strip():
            cursor.execute(statement)

def create_borrower(cursor, ssn, bname, address, phone):
    # Check if SSN already exists
    cursor.execute("SELECT * FROM BORROWER WHERE Ssn = %s", (ssn,))
    if cursor.fetchone():
        return "Error: A borrower with this SSN already exists."

    # Generate new Card_id
    cursor.execute("SELECT MAX(CAST(SUBSTRING(Card_id, 3) AS UNSIGNED)) FROM BORROWER")
    max_number = cursor.fetchone()[0]
    new_number = max_number + 1 if max_number else 1
    new_card_id = f"ID{new_number:06d}"

    # Insert new borrower
    cursor.execute("""
        INSERT INTO BORROWER (Card_id, Ssn, BName, Address, Phone)
        VALUES (%s, %s, %s, %s, %s)
    """, (new_card_id, ssn, bname, address, phone))
    return f"Success: Borrower '{bname}' with Card ID {new_card_id} has been added."

if __name__ == "__main__":
    import argparse
    import sys

    parser = argparse.ArgumentParser(description="Library System Management")
    parser.add_argument("--drop", action="store_true", help="Drop the library database")
    parser.add_argument("--create_borrower", type=str, metavar="SSN,Name,Address,Phone", 
        help="Create a new borrower in the format: SSN,Name,Address,Phone (Phone optional)")
    args = parser.parse_args()

    drop_flag = args.drop
    # Parse and unpack borrower info if provided
    borrower_info = None
    if args.create_borrower:
        borrower_info = [field.strip() for field in args.create_borrower.split(",")]
        if len(borrower_info) < 3:
            print("Invalid borrower format. Required: SSN,Name,Address[,Phone]")
            sys.exit(1)
    db_name = "LIBRARY_SYSTEM"

    # Step 1: Connect without specifying database to ensure it exists
    root_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )
    root_cursor = root_conn.cursor()
    if drop_flag:
        drop_database(root_cursor, db_name)
        print(f"Database '{db_name}' has been dropped.")
        root_cursor.close()
        root_conn.close()
        sys.exit()  # Exit after drop to prevent further actions

    # Ensure the database exists before connecting to it
    ensure_database_exists(root_cursor, db_name)
    root_cursor.close()
    root_conn.close()

    # Step 2: Connect to the target database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=db_name
    )
    cursor = conn.cursor()

    create_tables(conn)

    # Add any user interactions here

    # Add a borrower if requested
    # example: --create_borrower "123456789,Nick Halden,123 Library Lane, Plano, TX,(469) 123-4567"
    # example: --create_borrower "123456789,Nick Halden,123 Library Lane, Plano, TX"
    if borrower_info:
        ssn, bname, address = borrower_info[:3]
        phone = borrower_info[3] if len(borrower_info) > 3 else None
        result = create_borrower(
            cursor,
            ssn=ssn,
            bname=bname,
            address=address,
            phone=phone
        )
        print(result)

    conn.commit()
    cursor.close()
    conn.close()
