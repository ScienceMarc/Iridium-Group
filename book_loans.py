import mysql.connector
from datetime import datetime, timedelta

# Connect to the MySQL Database
def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='LIBRARY_SYSTEM'
    )

# Checkout a book
def checkout_book(isbn, card_id):
    conn = connect_db()
    cursor = conn.cursor(buffered=True)

    # Check unpaid fines
    cursor.execute("""
        SELECT COUNT(*)
        FROM FINES F
        JOIN BOOK_LOANS BL ON F.Loan_id = BL.Loan_id
        WHERE BL.Card_id = %s AND F.Paid = FALSE;
    """, (card_id,))
    unpaid_fines = cursor.fetchone()[0]

    if unpaid_fines > 0:
        conn.close()
        return "Borrower has unpaid fines. Cannot checkout."

    # Check active loans (max 3)
    cursor.execute("""
        SELECT COUNT(*)
        FROM BOOK_LOANS
        WHERE Card_id = %s AND Date_in IS NULL;
    """, (card_id,))
    active_loans = cursor.fetchone()[0]

    if active_loans >= 3:
        conn.close()
        return "Borrower already has maximum active loans (3)."

    # Check if book is available
    cursor.execute("""
        SELECT COUNT(*)
        FROM BOOK_LOANS
        WHERE Isbn = %s AND Date_in IS NULL;
    """, (isbn,))
    book_checked_out = cursor.fetchone()[0]

    if book_checked_out > 0:
        conn.close()
        return "Book is already checked out."

    # Checkout the book
    date_out = datetime.today().date()
    date_due = date_out + timedelta(days=14)

    cursor.execute("""
        INSERT INTO BOOK_LOANS (Isbn, Card_id, Date_out, Date_due)
        VALUES (%s, %s, %s, %s);
    """, (isbn, card_id, date_out, date_due))

    conn.commit()
    conn.close()
    return "Checkout successful."

# Check-in a book
def checkin_book(loan_id):
    conn = connect_db()
    cursor = conn.cursor()

    date_in = datetime.today().date()

    cursor.execute("""
        UPDATE BOOK_LOANS
        SET Date_in = %s
        WHERE Loan_id = %s AND Date_in IS NULL;
    """, (date_in, loan_id))

    if cursor.rowcount == 0:
        conn.close()
        return "Invalid Loan ID or book already checked in."

    conn.commit()
    conn.close()
    return "Check-in successful."

# Search active loans by ISBN, Card ID, or Borrower Name
def search_loans(query):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT BL.Loan_id, BL.Isbn, B.Title, BR.Card_id, BR.BName, BL.Date_out, BL.Date_due
        FROM BOOK_LOANS BL
        JOIN BOOK B ON BL.Isbn = B.Isbn
        JOIN BORROWER BR ON BL.Card_id = BR.Card_id
        WHERE (BL.Isbn = %s OR BR.Card_id = %s OR BR.BName LIKE %s)
        AND BL.Date_in IS NULL;
    """, (query, query, f"%{query}%"))

    results = cursor.fetchall()
    conn.close()
    return results

# Update fines (run daily as a cron/script)
def update_fines():
    conn = connect_db()
    cursor = conn.cursor()

    # Insert fines for returned late books
    cursor.execute("""
        INSERT INTO FINES (Loan_id, Fine_amt, Paid)
        SELECT Loan_id, DATEDIFF(Date_in, Date_due) * 0.25, FALSE
        FROM BOOK_LOANS
        WHERE Date_in > Date_due AND Loan_id NOT IN (SELECT Loan_id FROM FINES);
    """)

    # Insert fines for books still out
    cursor.execute("""
        INSERT INTO FINES (Loan_id, Fine_amt, Paid)
        SELECT Loan_id, DATEDIFF(CURDATE(), Date_due) * 0.25, FALSE
        FROM BOOK_LOANS
        WHERE Date_in IS NULL AND Date_due < CURDATE()
        AND Loan_id NOT IN (SELECT Loan_id FROM FINES);
    """)

    # Update existing fines for overdue books
    cursor.execute("""
        UPDATE FINES F
        JOIN BOOK_LOANS BL ON F.Loan_id = BL.Loan_id
        SET F.Fine_amt = DATEDIFF(COALESCE(BL.Date_in, CURDATE()), BL.Date_due) * 0.25
        WHERE F.Paid = FALSE AND BL.Date_due < COALESCE(BL.Date_in, CURDATE());
    """)

    conn.commit()
    conn.close()
    print("Fines updated.")

# Testing the checkout and check-in functionality:
if __name__ == "__main__":
    print(checkout_book("123456789", "C0000001"))
    print(search_loans("C0000001"))  # Search by Card ID
    print(checkin_book(1))  # Provide actual Loan ID for check-in
    update_fines()
