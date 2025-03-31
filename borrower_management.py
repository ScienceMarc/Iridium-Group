
# File name: borrower_management.py
# Author: Shiv Bhavsar
# Last Edit: 2025-03-31
# Description: This file is created for the Milestone 2 part of the CS4347 Project.

import mysql.connector
from mysql.connector import Error

def create_borrower(ssn, bname, address, phone):
    connection = None
    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="LIBRARY_SYSTEM"
        )
        cursor = connection.cursor()

        # Check if SSN already exists
        cursor.execute("SELECT * FROM borrower WHERE ssn = %s", (ssn,))
        if cursor.fetchone():
            return "Error: A borrower with this SSN already exists."
        
        # Generate new Card_id
        cursor.execute("SELECT MAX(CAST(SUBSTRING(Card_id, 3) AS UNSIGNED)) FROM BORROWER")
        max_number = cursor.fetchone()[0]
        new_number = max_number + 1 if max_number else 1
        new_card_id = f"ID{new_number:06d}"

        # Insert new borrower
        cursor.execute("""
            INSERT INTO borrower (Card_id, Ssn, Bname, Address, Phone)
            VALUES (%s, %s, %s, %s, %s)
        """, (new_card_id, ssn, bname, address, phone))
        connection.commit()

        return f"Success: Borrow '{bname}' with Card ID {new_card_id} has been added."
    
    except Error as e:
        return f"MySQL Error: {e}"
    
    finally:
        if connection is not None and connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    result = create_borrower(
        ssn="123456781",
        bname="Nick Halden",
        address="123 Library Lane, Plano, TX",
        phone="(469) 123-4567"
    )
    print(result)