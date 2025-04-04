# File name: search_books.py
# Author: Arjun Vishal
# Last Edit: 2025-04-03
# Description: Implements 'Book Search and Availability' for Milestone 2 of the CS4347 Project.

import mysql.connector


def get_mysql_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='12345678',
        database='LIBRARY_SYSTEMs',
        port=3306
    )

# Search for books
def search_books_mysql(search_term):
    connect = get_mysql_connection()
    cursor = connect.cursor()

    query = '''
    SELECT b.Isbn, b.Title, GROUP_CONCAT(a.Name SEPARATOR ', '),
    CASE WHEN EXISTS (
        SELECT 1 FROM BOOK_LOANS bl WHERE bl.Isbn = b.Isbn AND bl.Date_in IS NULL
    ) THEN 'OUT' ELSE 'IN' END
    FROM BOOK b
    INNER JOIN BOOK_AUTHORS ba ON ba.Isbn = b.Isbn
    INNER JOIN AUTHORS a ON a.Author_id = ba.Author_id
    GROUP BY b.Isbn, b.Title
    HAVING LOWER(b.Isbn) LIKE %s OR LOWER(b.Title) LIKE %s OR LOWER(GROUP_CONCAT(a.Name SEPARATOR ', ')) LIKE %s
    '''

    term = f"%{search_term.lower()}%"
    cursor.execute(query, (term, term, term))
    results = cursor.fetchall()

    #Prints data in tables
    print(f"{'NO':<3} {'ISBN':<12} {'TITLE':<35} {'AUTHORS':<30} {'STATUS'}")
    print('-' * 90)
    for i, row in enumerate(results, 1):
        print(f"{i:<3} {row[0]:<12} {row[1]:<35} {row[2]:<30} {row[3]}")
   

    cursor.close()
    connect.close()

search_books_mysql("  ")  # type here to search
