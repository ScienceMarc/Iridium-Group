import mysql.connector
from datetime import date
from decimal import Decimal

FINE_RATE = Decimal("0.25")

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LIBRARY_SYSTEM"
    )

def update_fines():
    conn = get_db_connection()
    cursor = conn.cursor()

    today = date.today()

    cursor.execute("SELECT Loan_id, Due_date, Date_in FROM BOOK_LOANS")
    for loan_id, due_date, date_in in cursor.fetchall():
        late_days = 0
        if date_in:
            if date_in > due_date:
                late_days = (date_in - due_date).days
        else:
            if today > due_date:
                late_days = (today - due_date).days

        if late_days > 0:
            fine_amt = FINE_RATE * late_days
            cursor.execute("SELECT Paid FROM FINES WHERE Loan_id = %s", (loan_id,))
            row = cursor.fetchone()

            if row:
                if not row[0]:
                    cursor.execute("UPDATE FINES SET Fine_amt = %s WHERE Loan_id = %s AND Paid = FALSE", (fine_amt, loan_id))
            else:
                cursor.execute("INSERT INTO FINES (Loan_id, Fine_amt, Paid) VALUES (%s, %s, FALSE)", (loan_id, fine_amt))

    conn.commit()
    conn.close()
    print("Fines updated.")

def pay_fines(card_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check unpaid & returned
    cursor.execute("""
        SELECT F.Loan_id FROM FINES F
        JOIN BOOK_LOANS B ON F.Loan_id = B.Loan_id
        WHERE B.Card_id = %s AND F.Paid = FALSE AND B.Date_in IS NOT NULL
    """, (card_id,))
    loan_ids = [row[0] for row in cursor.fetchall()]

    if loan_ids:
        for loan_id in loan_ids:
            cursor.execute("UPDATE FINES SET Paid = TRUE WHERE Loan_id = %s", (loan_id,))
        conn.commit()
        print(f"All fines for card {card_id} have been paid.")
    else:
        print("No unpaid fines available for payment, or books not yet returned.")

    conn.close()

def show_fines(include_paid=False):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT B.Card_id, SUM(F.Fine_amt)
        FROM FINES F
        JOIN BOOK_LOANS B ON F.Loan_id = B.Loan_id
    """
    if not include_paid:
        query += " WHERE F.Paid = FALSE"

    query += " GROUP BY B.Card_id"

    cursor.execute(query)
    results = cursor.fetchall()

    for card_id, total_fine in results:
        print(f"Borrower: {card_id} | Total Fine: ${total_fine:.2f}")

    conn.close()

update_fines()
show_fines()
#pay_fines("") # Put ID instead of empty string
