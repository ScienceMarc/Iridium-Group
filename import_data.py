import csv
import os
import django
import sys

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library_portal.settings')
django.setup()

from libraryapp.models import Book, Author, Borrower

def load_books():
    with open(os.path.join('milestone1', 'book.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            Book.objects.get_or_create(
                isbn=row['Isbn'].strip(),
                title=row['Title'].strip()
            )

def load_authors():
    with open(os.path.join('milestone1', 'authors.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row['Name'].strip()
            if not name:
                print(f"Skipping row with empty name: {row}")
                continue  # Skip rows with empty names
            Author.objects.get_or_create(name=name)

def load_book_authors():
    # Build a mapping from Author_id to author name
    author_id_to_name = {}
    with open(os.path.join('milestone1', 'authors.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            author_id_to_name[row['Author_id'].strip()] = row['Name'].strip()

    with open(os.path.join('milestone1', 'book_authors.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                book = Book.objects.get(isbn=row['Isbn'].strip())
                author_name = author_id_to_name.get(row['Author_id'].strip())
                if not author_name:
                    print(f"Author_id {row['Author_id']} not found in authors.csv")
                    continue
                author = Author.objects.get(name=author_name)
                book.authors.add(author)
            except (Book.DoesNotExist, Author.DoesNotExist) as e:
                print(f"Error linking book and author: {e}")

def load_borrowers():
    with open(os.path.join('milestone1', 'borrower.csv'), newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            print(row)  # Debug: show the row being processed
            ssn = row['Ssn'].replace('-', '').strip()
            Borrower.objects.get_or_create(
                card_no=row['Card_id'].strip(),
                ssn=ssn,
                fname=row['Bname'].strip().split()[0],
                lname=' '.join(row['Bname'].strip().split()[1:]),
                address=row['Address'].strip(),
                phone=row['Phone'].strip()
            )

if __name__ == "__main__":
    print("Loading books...")
    load_books()
    print("Loading authors...")
    load_authors()
    print("Loading book authors...")
    load_book_authors()
    print("Loading borrowers...")
    load_borrowers()
    print("✅ Data successfully imported!")
