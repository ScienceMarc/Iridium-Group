import mysql.connector
from datetime import datetime, date
from decimal import Decimal, ROUND_HALF_UP

# Database connection
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="LIBRARY_SYSTEM"
    )

# Update/refresh fines
def update_fines():
    db = get_connection()
    cursor = db.cursor()

    query = """
    SELECT loan_id, due_date, date_in
    FROM book_loans
    WHERE (date_in > due_date)
       OR (date_in IS NULL AND due_date < CURDATE())
    """
    cursor.execute(query)
    overdue_loans = cursor.fetchall()

    for loan_id, due_date, date_in in overdue_loans:
        # Ensure dates are date objects
        if isinstance(due_date, str):
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        if date_in and isinstance(date_in, str):
            date_in = datetime.strptime(date_in, "%Y-%m-%d").date()

        days_overdue = (date_in - due_date).days if date_in else (date.today() - due_date).days
        fine_amt = (Decimal(days_overdue) * Decimal('0.25')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Check for existing fine
        cursor.execute("SELECT paid, fine_amt FROM fines WHERE loan_id = %s", (loan_id,))
        result = cursor.fetchone()

        if result:
            paid, existing_amt = result
            if paid == 0 and existing_amt != fine_amt:
                cursor.execute("UPDATE fines SET fine_amt = %s WHERE loan_id = %s", (fine_amt, loan_id))
        else:
            cursor.execute("INSERT INTO fines (loan_id, fine_amt, paid) VALUES (%s, %s, 0)", (loan_id, fine_amt))

    db.commit()
    print("Fines updated.")
    cursor.close()
    db.close()

# Display fines grouped by card_id
def display_fines(show_paid=False):
    db = get_connection()
    cursor = db.cursor()

    query = """
    SELECT bl.card_id, SUM(f.fine_amt) AS total_fine
    FROM fines f
    JOIN book_loans bl ON f.loan_id = bl.loan_id
    WHERE %s OR f.paid = 0
    GROUP BY bl.card_id
    """
    cursor.execute(query, (show_paid,))
    results = cursor.fetchall()

    if not results:
        print("No fines to display.")
    else:
        print("Card ID\tTotal Fine")
        for card_id, total_fine in results:
            print(f"{card_id}\t${total_fine:.2f}")

    cursor.close()
    db.close()

# Pay all fines for a borrower
def pay_fines(card_id):
    db = get_connection()
    cursor = db.cursor()

    # Check that all loans are returned
    cursor.execute("""
    SELECT f.loan_id
    FROM fines f
    JOIN book_loans bl ON f.loan_id = bl.loan_id
    WHERE bl.card_id = %s AND f.paid = 0 AND bl.date_in IS NULL
    """, (card_id,))
    unreturned = cursor.fetchall()

    if unreturned:
        print("Cannot pay fines: borrower has unreturned books.")
    else:
        cursor.execute("""
        UPDATE fines
        SET paid = 1
        WHERE loan_id IN (
            SELECT loan_id
            FROM book_loans
            WHERE card_id = %s
        ) AND paid = 0
        """, (card_id,))
        db.commit()
        print("Fines paid in full.")

    cursor.close()
    db.close()

# Example interactive menu
if __name__ == "__main__":
    while True:
        print("\n--- Library Fines Manager ---")
        print("1. Update Fines")
        print("2. Display Unpaid Fines")
        print("3. Display All Fines")
        print("4. Pay Fines for Borrower")
        print("5. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            update_fines()
        elif choice == "2":
            display_fines(show_paid=False)
        elif choice == "3":
            display_fines(show_paid=True)
        elif choice == "4":
            card_id = input("Enter card ID: ").strip()
            pay_fines(card_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Try again.")
