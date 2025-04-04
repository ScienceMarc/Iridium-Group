import sqlite3
import csv
import os

conn = sqlite3.connect('library.db')
cursor = conn.cursor()

base_path = 'milestone1'

def load_books():
    with open(os.path.join(base_path, 'book.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("INSERT INTO BOOK (Isbn, Title) VALUES (?, ?)", (row['Isbn'].strip(), row['Title'].strip()))

def load_authors():
    with open(os.path.join(base_path, 'authors.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("INSERT INTO AUTHORS (Author_id, Name) VALUES (?, ?)", (row['Author_id'].strip(), row['Name'].strip()))

def load_book_authors():
    with open(os.path.join(base_path, 'book_authors.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("INSERT OR IGNORE INTO BOOK_AUTHORS (Isbn, Author_id) VALUES (?, ?)", (row['Isbn'].strip(), row['Author_id'].strip()))

def load_borrowers():
    with open(os.path.join(base_path, 'borrower.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute("""
                INSERT INTO BORROWER (Card_id, Bname, Address, Phone, Ssn)
                VALUES (?, ?, ?, ?, ?)
            """, (
                row['Card_id'].strip(),
                row['Bname'].strip(),
                row['Address'].strip(),
                row['Phone'].strip(),
                row['Ssn'].strip()
            ))

if __name__ == "__main__":
    load_books()
    load_authors()
    load_book_authors()
    load_borrowers()
    conn.commit()
    conn.close()
    print("✅ Data successfully loaded into all tables!")
