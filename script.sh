#!/usr/bin/env bash

mysql -u root < create_library_data.sql

python import_data.py
python borrower_management.py
python search_books.py
python book_loans.py
python fines.py